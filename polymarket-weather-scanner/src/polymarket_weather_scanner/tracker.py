from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .client import PolymarketClient
from .config import APP_DIR, ScannerConfig


DEFAULT_CITY_SOURCES: dict[str, str] = {
    'Toronto': 'https://www.wunderground.com/history/daily/ca/mississauga/CYYZ',
    'Atlanta': 'https://www.wunderground.com/history/daily/us/ga/atlanta/KATL',
    'Chicago': 'https://www.wunderground.com/history/daily/us/il/chicago/KORD',
    'Lucknow': 'https://www.wunderground.com/history/daily/in/lucknow/VILK',
    'Ankara': 'https://www.wunderground.com/history/daily/tr/%C3%A7ubuk/LTAC',
    'Shanghai': 'https://www.wunderground.com/history/daily/cn/shanghai/ZSPD',
    'Seoul': 'https://www.wunderground.com/history/daily/kr/incheon/RKSI',
    'London': 'https://www.wunderground.com/history/daily/gb/london/EGLC',
    'Singapore': 'https://www.wunderground.com/history/daily/sg/singapore/WSSS',
    'Dallas': 'https://www.wunderground.com/history/daily/us/tx/dallas/KDAL',
    'Wellington': 'https://www.wunderground.com/history/daily/nz/wellington/NZWN',
    'NYC': 'https://www.wunderground.com/history/daily/us/ny/new-york-city/KLGA',
    'Paris': 'https://www.wunderground.com/history/daily/fr/paris/LFPG',
    'Munich': 'https://www.wunderground.com/history/daily/de/munich/EDDM',
    'Seattle': 'https://www.wunderground.com/history/daily/us/wa/seatac/KSEA',
    'Tel Aviv': 'https://www.wunderground.com/history/daily/il/tel-aviv/LLBG',
    'Tokyo': 'https://www.wunderground.com/history/daily/jp/tokyo/RJTT',
    'Sao Paulo': 'https://www.wunderground.com/history/daily/br/guarulhos/SBGR',
    'Miami': 'https://www.wunderground.com/history/daily/us/fl/miami/KMIA',
    'Buenos Aires': 'https://www.wunderground.com/history/daily/ar/ezeiza/SAEZ',
}


@dataclass(frozen=True)
class TrackingCity:
    name: str
    source_url: str

    @property
    def slug(self) -> str:
        return slugify(self.name)


@dataclass
class EventMarketSnapshot:
    event_id: str
    event_slug: str
    event_title: str
    city: str
    city_slug: str
    target_date: str
    source_url_expected: str
    source_url_actual: str | None
    source_url_matches_expected: bool
    fetched_at_utc: str
    fetched_at_source_local: str | None
    event_end_utc: str | None
    market_count: int
    markets: list[dict[str, Any]]


@dataclass
class EventForecastSnapshot:
    event_id: str
    event_slug: str
    event_title: str
    city: str
    city_slug: str
    target_date: str
    source_url_expected: str
    source_url_actual: str | None
    source_forecast_page: str
    source_forecast_api_url: str
    fetched_at_utc: str
    fetched_at_source_local: str | None
    hourly_count: int
    hours: list[dict[str, Any]]


class WeatherSourceClient:
    def __init__(self, user_agent: str = 'polymarket-weather-scanner/0.1') -> None:
        self.user_agent = user_agent
        self._forecast_api_cache: dict[str, str] = {}

    def _get_text(self, url: str, timeout: int = 30) -> str:
        request = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode('utf-8', 'ignore')

    def _get_json(self, url: str, timeout: int = 30) -> Any:
        request = urllib.request.Request(url, headers={'User-Agent': self.user_agent, 'Accept': 'application/json'})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)

    @staticmethod
    def history_to_forecast_url(source_url: str) -> str:
        return source_url.replace('/history/daily/', '/forecast/')

    def discover_forecast_api_url(self, source_url: str) -> str:
        cached = self._forecast_api_cache.get(source_url)
        if cached:
            return cached
        forecast_page = self.history_to_forecast_url(source_url)
        html = self._get_text(forecast_page)
        matches = re.findall(r'https://api\.weather\.com/v3/wx/forecast/hourly/15day[^"\']+', html)
        if not matches:
            raise RuntimeError(f'forecast api url not found for {source_url}')
        self._forecast_api_cache[source_url] = matches[0]
        return matches[0]

    def fetch_hourly_forecast_for_date(self, source_url: str, target_date: str) -> tuple[str, list[dict[str, Any]], str | None]:
        forecast_page = self.history_to_forecast_url(source_url)
        api_url = self.discover_forecast_api_url(source_url)
        payload = self._get_json(api_url)

        valid_times = list(payload.get('validTimeLocal') or [])
        hours: list[dict[str, Any]] = []
        first_offset: str | None = None
        for idx, local_time in enumerate(valid_times):
            if not str(local_time).startswith(target_date):
                continue
            if first_offset is None:
                first_offset = extract_offset(str(local_time))
            item = {
                'valid_time_local': local_time,
                'valid_time_utc': safe_index(payload.get('validTimeUtc'), idx),
                'temperature_c': f_to_c(safe_index(payload.get('temperature'), idx)),
                'temperature_f': safe_index(payload.get('temperature'), idx),
                'feels_like_c': f_to_c(safe_index(payload.get('temperatureFeelsLike'), idx)),
                'feels_like_f': safe_index(payload.get('temperatureFeelsLike'), idx),
                'dewpoint_c': f_to_c(safe_index(payload.get('temperatureDewPoint'), idx)),
                'dewpoint_f': safe_index(payload.get('temperatureDewPoint'), idx),
                'precip_chance': safe_index(payload.get('precipChance'), idx),
                'precip_type': safe_index(payload.get('precipType'), idx),
                'qpf_in': safe_index(payload.get('qpf'), idx),
                'qpf_mm': in_to_mm(safe_index(payload.get('qpf'), idx)),
                'humidity': safe_index(payload.get('relativeHumidity'), idx),
                'cloud_cover': safe_index(payload.get('cloudCover'), idx),
                'wind_speed_mph': safe_index(payload.get('windSpeed'), idx),
                'wind_speed_kph': mph_to_kph(safe_index(payload.get('windSpeed'), idx)),
                'wind_gust_mph': safe_index(payload.get('windGust'), idx),
                'wind_gust_kph': mph_to_kph(safe_index(payload.get('windGust'), idx)),
                'wind_direction_cardinal': safe_index(payload.get('windDirectionCardinal'), idx),
                'wx_phrase_long': safe_index(payload.get('wxPhraseLong'), idx),
                'wx_phrase_short': safe_index(payload.get('wxPhraseShort'), idx),
                'icon_code': safe_index(payload.get('iconCode'), idx),
                'day_or_night': safe_index(payload.get('dayOrNight'), idx),
            }
            hours.append(item)
        return forecast_page, hours, first_offset


class PolymarketEventTracker:
    def __init__(self, config: ScannerConfig | None = None, root_dir: Path | None = None) -> None:
        self.config = config or ScannerConfig()
        self.client = PolymarketClient(self.config.gamma_base, self.config.data_base)
        self.weather = WeatherSourceClient(user_agent=self.client.user_agent)
        self.root_dir = root_dir or (APP_DIR / 'data' / 'tracker')
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.cities = [TrackingCity(name=name, source_url=url) for name, url in DEFAULT_CITY_SOURCES.items()]

    def run_forever(
        self,
        *,
        market_interval_seconds: int = 60,
        forecast_interval_seconds: int = 300,
        max_cycles: int | None = None,
        city_names: list[str] | None = None,
    ) -> None:
        cycle = 0
        selected = self._selected_cities(city_names)
        while True:
            cycle += 1
            started = time.time()
            summary = self.run_cycle(forecast_interval_seconds=forecast_interval_seconds, city_names=[city.name for city in selected])
            print(
                f"cycle={cycle} cities={summary['cities']} open_events={summary['open_events']} "
                f"market_snapshots={summary['market_snapshots']} forecast_snapshots={summary['forecast_snapshots']}"
            )
            if max_cycles is not None and cycle >= max_cycles:
                return
            elapsed = time.time() - started
            time.sleep(max(1, market_interval_seconds - int(elapsed)))

    def run_cycle(self, *, forecast_interval_seconds: int = 300, city_names: list[str] | None = None) -> dict[str, Any]:
        selected = self._selected_cities(city_names)
        open_events = self.discover_all_open_events(selected)
        market_snapshots = 0
        forecast_snapshots = 0
        state = {
            'generated_at_utc': utc_now_iso(),
            'cities': [],
        }
        for city in selected:
            city_events = open_events.get(city.name, [])
            city_state = {
                'city': city.name,
                'city_slug': city.slug,
                'source_url_expected': city.source_url,
                'open_events': [],
            }
            for event in city_events:
                snapshot = self.capture_market_snapshot(city, event)
                self._append_jsonl(self._event_dir(city, event['target_date']) / 'market_prices.jsonl', asdict(snapshot))
                self._write_json(self._event_dir(city, event['target_date']) / 'event_meta.json', event)
                market_snapshots += 1

                should_fetch_forecast = self._should_fetch_forecast(city, event['target_date'], forecast_interval_seconds)
                if should_fetch_forecast:
                    forecast_snapshot = self.capture_forecast_snapshot(city, event)
                    self._append_jsonl(self._event_dir(city, event['target_date']) / 'forecast_hourly.jsonl', asdict(forecast_snapshot))
                    forecast_snapshots += 1

                city_state['open_events'].append({
                    'event_id': event['event_id'],
                    'event_slug': event['event_slug'],
                    'event_title': event['event_title'],
                    'target_date': event['target_date'],
                    'event_end_utc': event.get('event_end_utc'),
                    'source_url_actual': event.get('source_url_actual'),
                    'source_url_matches_expected': event.get('source_url_matches_expected'),
                })
            self._write_json(self._city_dir(city) / 'open_events.json', city_state)
            state['cities'].append(city_state)
        self._write_json(self.root_dir / 'state.json', state)
        return {
            'generated_at_utc': state['generated_at_utc'],
            'cities': len(selected),
            'open_events': sum(len(city['open_events']) for city in state['cities']),
            'market_snapshots': market_snapshots,
            'forecast_snapshots': forecast_snapshots,
        }

    def discover_all_open_events(self, cities: list[TrackingCity]) -> dict[str, list[dict[str, Any]]]:
        out: dict[str, list[dict[str, Any]]] = {}
        for city in cities:
            out[city.name] = self.discover_open_events_for_city(city)
        return out

    def discover_open_events_for_city(self, city: TrackingCity) -> list[dict[str, Any]]:
        payload = self.client.public_search(f'Highest temperature in {city.name}', limit_per_type=25, page=1)
        candidates = []
        for event in payload.get('events') or []:
            title = str(event.get('title') or '')
            if 'highest temperature' not in title.lower():
                continue
            if city.name.lower() not in title.lower():
                continue
            if not event.get('active') or event.get('closed'):
                continue
            candidates.append(event)

        events: list[dict[str, Any]] = []
        for event in candidates:
            detail = self.client.gamma_get(f"/events/{event['id']}")
            markets = [market for market in (detail.get('markets') or []) if market.get('active') and not market.get('closed')]
            if not markets:
                continue
            target_date = str(detail.get('endDate') or '')[:10]
            actual_source = detail.get('resolutionSource')
            events.append({
                'event_id': str(detail.get('id')),
                'event_slug': detail.get('slug') or '',
                'event_title': detail.get('title') or '',
                'target_date': target_date,
                'event_end_utc': detail.get('endDate'),
                'source_url_expected': city.source_url,
                'source_url_actual': actual_source,
                'source_url_matches_expected': normalize_url(actual_source) == normalize_url(city.source_url),
                'markets': markets,
            })
        events.sort(key=lambda item: item['target_date'])
        unique: dict[str, dict[str, Any]] = {}
        for event in events:
            unique[event['target_date']] = event
        return list(unique.values())

    def capture_market_snapshot(self, city: TrackingCity, event: dict[str, Any]) -> EventMarketSnapshot:
        fetched_at = utc_now_iso()
        source_local = local_now_from_offset(first_market_offset(event.get('markets') or []))
        rows: list[dict[str, Any]] = []
        for market in event.get('markets') or []:
            outcome_prices = parse_json_list(market.get('outcomePrices'))
            outcomes = parse_json_list(market.get('outcomes'))
            clob_ids = parse_json_list(market.get('clobTokenIds'))
            yes_prob = to_float(safe_index(outcome_prices, 0))
            no_prob = to_float(safe_index(outcome_prices, 1))
            yes_sell = to_float(market.get('bestBid'))
            yes_buy = to_float(market.get('bestAsk'))
            yes_last = to_float(market.get('lastTradePrice'))
            no_sell = complement_price(yes_buy)
            no_buy = complement_price(yes_sell)
            no_last = complement_price(yes_last)
            row = {
                'market_id': str(market.get('id') or ''),
                'condition_id': market.get('conditionId'),
                'question': market.get('question'),
                'group_item_title': market.get('groupItemTitle'),
                'outcomes': outcomes,
                'yes_token_id': safe_index(clob_ids, 0),
                'no_token_id': safe_index(clob_ids, 1),
                'yes_probability': yes_prob,
                'no_probability': no_prob,
                'yes_probability_cents': to_cents(yes_prob),
                'no_probability_cents': to_cents(no_prob),
                'yes_best_bid_sell_price': yes_sell,
                'yes_best_bid_sell_cents': to_cents(yes_sell),
                'yes_best_ask_buy_price': yes_buy,
                'yes_best_ask_buy_cents': to_cents(yes_buy),
                'yes_last_trade_price': yes_last,
                'yes_last_trade_cents': to_cents(yes_last),
                'no_best_bid_sell_price': no_sell,
                'no_best_bid_sell_cents': to_cents(no_sell),
                'no_best_ask_buy_price': no_buy,
                'no_best_ask_buy_cents': to_cents(no_buy),
                'no_last_trade_price': no_last,
                'no_last_trade_cents': to_cents(no_last),
                'spread': to_float(market.get('spread')),
                'spread_cents': to_cents(market.get('spread')),
                'market_slug': market.get('slug'),
                'market_active': bool(market.get('active')),
                'market_closed': bool(market.get('closed')),
                'outcome_price_semantics': {
                    'yes_best_bid': 'best price to SELL YES',
                    'yes_best_ask': 'best price to BUY YES',
                    'no_best_bid': 'best price to SELL NO (derived as 1 - YES best_ask)',
                    'no_best_ask': 'best price to BUY NO (derived as 1 - YES best_bid)',
                },
            }
            rows.append(row)
        return EventMarketSnapshot(
            event_id=event['event_id'],
            event_slug=event['event_slug'],
            event_title=event['event_title'],
            city=city.name,
            city_slug=city.slug,
            target_date=event['target_date'],
            source_url_expected=city.source_url,
            source_url_actual=event.get('source_url_actual'),
            source_url_matches_expected=bool(event.get('source_url_matches_expected')),
            fetched_at_utc=fetched_at,
            fetched_at_source_local=source_local,
            event_end_utc=event.get('event_end_utc'),
            market_count=len(rows),
            markets=rows,
        )

    def capture_forecast_snapshot(self, city: TrackingCity, event: dict[str, Any]) -> EventForecastSnapshot:
        fetched_at = utc_now_iso()
        source_url = str(event.get('source_url_actual') or city.source_url)
        forecast_page, hours, offset = self.weather.fetch_hourly_forecast_for_date(source_url, event['target_date'])
        return EventForecastSnapshot(
            event_id=event['event_id'],
            event_slug=event['event_slug'],
            event_title=event['event_title'],
            city=city.name,
            city_slug=city.slug,
            target_date=event['target_date'],
            source_url_expected=city.source_url,
            source_url_actual=event.get('source_url_actual'),
            source_forecast_page=forecast_page,
            source_forecast_api_url=self.weather.discover_forecast_api_url(source_url),
            fetched_at_utc=fetched_at,
            fetched_at_source_local=local_now_from_offset(offset),
            hourly_count=len(hours),
            hours=hours,
        )

    def _should_fetch_forecast(self, city: TrackingCity, target_date: str, forecast_interval_seconds: int) -> bool:
        path = self._event_dir(city, target_date) / 'forecast_hourly.jsonl'
        if not path.exists():
            return True
        age = time.time() - path.stat().st_mtime
        return age >= forecast_interval_seconds

    def _selected_cities(self, city_names: list[str] | None) -> list[TrackingCity]:
        if not city_names:
            return list(self.cities)
        wanted = {name.strip().lower() for name in city_names if name.strip()}
        return [city for city in self.cities if city.name.lower() in wanted]

    def _city_dir(self, city: TrackingCity) -> Path:
        path = self.root_dir / 'cities' / city.slug
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _event_dir(self, city: TrackingCity, target_date: str) -> Path:
        path = self._city_dir(city) / 'events' / target_date
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=False) + '\n')

    @staticmethod
    def _write_json(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def safe_index(values: Any, index: int) -> Any:
    if not isinstance(values, list) or index >= len(values):
        return None
    return values[index]


def parse_json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            loaded = json.loads(value)
            return loaded if isinstance(loaded, list) else []
        except json.JSONDecodeError:
            return []
    return []


def to_float(value: Any) -> float | None:
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_cents(value: Any) -> int | None:
    num = to_float(value)
    if num is None:
        return None
    return int(round(num * 100))


def complement_price(value: Any) -> float | None:
    num = to_float(value)
    if num is None:
        return None
    return round(1.0 - num, 6)


def f_to_c(value: Any) -> float | None:
    num = to_float(value)
    if num is None:
        return None
    return round((num - 32) * 5 / 9, 2)


def mph_to_kph(value: Any) -> float | None:
    num = to_float(value)
    if num is None:
        return None
    return round(num * 1.60934, 2)


def in_to_mm(value: Any) -> float | None:
    num = to_float(value)
    if num is None:
        return None
    return round(num * 25.4, 3)


def slugify(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def normalize_url(value: str | None) -> str:
    return urllib.parse.unquote((value or '').strip())


def extract_offset(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r'([+-]\d{4})$', value)
    return match.group(1) if match else None


def local_now_from_offset(offset: str | None) -> str | None:
    if not offset:
        return None
    sign = 1 if offset[0] == '+' else -1
    hours = int(offset[1:3])
    minutes = int(offset[3:5])
    delta = timedelta(hours=hours, minutes=minutes) * sign
    tz = timezone(delta)
    return datetime.now(UTC).astimezone(tz).replace(microsecond=0).isoformat()


def first_market_offset(markets: list[dict[str, Any]]) -> str | None:
    del markets
    return None
