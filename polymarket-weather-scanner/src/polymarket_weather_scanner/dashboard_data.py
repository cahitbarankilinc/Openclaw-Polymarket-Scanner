from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import re

from .config import APP_DIR

INTERVAL_SECONDS = {
    '1m': 60,
    '5m': 300,
    '15m': 900,
    '30m': 1800,
    '1h': 3600,
}


@dataclass
class TrackerDashboardStore:
    root_dir: Path = APP_DIR / 'data' / 'tracker'

    def list_cities(self) -> list[dict[str, Any]]:
        cities_dir = self.root_dir / 'cities'
        if not cities_dir.exists():
            return []
        rows = []
        for city_dir in sorted([p for p in cities_dir.iterdir() if p.is_dir()]):
            meta_path = city_dir / 'open_events.json'
            payload = self._read_json(meta_path) if meta_path.exists() else {}
            rows.append({
                'city': payload.get('city') or deslugify(city_dir.name),
                'city_slug': city_dir.name,
                'open_events': payload.get('open_events') or [],
                'source_url_expected': payload.get('source_url_expected'),
            })
        return rows

    def list_dates_for_city(self, city_slug: str) -> list[dict[str, Any]]:
        city_dir = self.root_dir / 'cities' / city_slug
        events: list[dict[str, Any]] = []
        meta_path = city_dir / 'open_events.json'
        if meta_path.exists():
            payload = self._read_json(meta_path)
            events.extend(payload.get('open_events') or [])
        history_path = city_dir / 'history_events.json'
        if history_path.exists():
            payload = self._read_json(history_path)
            events.extend(payload.get('historical_events') or [])
        dedup: dict[str, dict[str, Any]] = {}
        for item in events:
            target_date = item.get('target_date') or ''
            if target_date:
                dedup[target_date] = item
        rows = list(dedup.values())
        rows.sort(key=lambda item: item.get('target_date') or '')
        return rows

    def build_series(self, city_slug: str, target_date: str, interval: str = '5m') -> dict[str, Any]:
        interval_seconds = INTERVAL_SECONDS.get(interval, 300)
        event_dir = self.root_dir / 'cities' / city_slug / 'events' / target_date
        meta = self._read_json(event_dir / 'event_meta.json') if (event_dir / 'event_meta.json').exists() else {}
        market_snapshots = self._read_jsonl(event_dir / 'market_prices.jsonl')
        forecast_snapshots = self._read_jsonl(event_dir / 'forecast_hourly.jsonl')

        historical_series_path = event_dir / 'historical_series.json'
        if not market_snapshots and historical_series_path.exists():
            historical = self._read_json(historical_series_path)
            historical_market_series = self._aggregate_prebuilt_market_series(historical.get('market_series') or [], interval_seconds)
            markers = self._color_closed_event_markers(list(historical.get('forecast_markers') or []), historical_market_series)
            return {
                'city_slug': city_slug,
                'city': historical.get('city') or deslugify(city_slug),
                'target_date': historical.get('target_date') or target_date,
                'interval': interval,
                'event_id': historical.get('event_id'),
                'event_title': historical.get('event_title'),
                'source_url_expected': historical.get('source_url_expected'),
                'source_url_actual': historical.get('source_url_actual'),
                'source_url_matches_expected': historical.get('source_url_matches_expected'),
                'market_series': historical_market_series,
                'forecast_markers': markers,
                'snapshot_count': max((len(row.get('points') or []) for row in historical_market_series), default=0),
                'forecast_snapshot_count': historical.get('forecast_snapshot_count') or 0,
                'historical_mode': True,
            }

        market_series = self._aggregate_market_snapshots(market_snapshots, interval_seconds)
        markers = self._color_closed_event_markers(self._build_forecast_markers(forecast_snapshots), market_series)
        return {
            'city_slug': city_slug,
            'city': meta.get('event_title', '').split(' in ')[1].split(' on ')[0] if meta.get('event_title') else deslugify(city_slug),
            'target_date': target_date,
            'interval': interval,
            'event_id': meta.get('event_id'),
            'event_title': meta.get('event_title'),
            'source_url_expected': meta.get('source_url_expected'),
            'source_url_actual': meta.get('source_url_actual'),
            'source_url_matches_expected': meta.get('source_url_matches_expected'),
            'market_series': market_series,
            'forecast_markers': markers,
            'snapshot_count': len(market_snapshots),
            'forecast_snapshot_count': len(forecast_snapshots),
            'historical_mode': False,
        }

    def _aggregate_market_snapshots(self, snapshots: list[dict[str, Any]], interval_seconds: int) -> list[dict[str, Any]]:
        grouped_by_market: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
        labels: dict[str, str] = {}
        for snap in snapshots:
            fetched_at = parse_utc(snap.get('fetched_at_utc'))
            if fetched_at is None:
                continue
            bucket_ts = floor_timestamp(int(fetched_at.timestamp()), interval_seconds)
            for market in snap.get('markets') or []:
                key = str(market.get('market_id') or market.get('group_item_title') or '')
                labels[key] = market.get('group_item_title') or key
                grouped_by_market[key][bucket_ts] = {
                    'ts': iso_utc_from_ts(bucket_ts),
                    'actual_ts': snap.get('fetched_at_utc'),
                    'group_item_title': market.get('group_item_title'),
                    'yes_probability_cents': market.get('yes_probability_cents'),
                    'no_probability_cents': market.get('no_probability_cents'),
                    'yes_best_bid_sell_cents': market.get('yes_best_bid_sell_cents'),
                    'yes_best_ask_buy_cents': market.get('yes_best_ask_buy_cents'),
                    'no_best_bid_sell_cents': market.get('no_best_bid_sell_cents'),
                    'no_best_ask_buy_cents': market.get('no_best_ask_buy_cents'),
                    'yes_last_trade_cents': market.get('yes_last_trade_cents'),
                    'no_last_trade_cents': market.get('no_last_trade_cents'),
                }
        rows = []
        for key, bucket_map in sorted(grouped_by_market.items(), key=lambda item: sort_bucket_label(labels.get(item[0], item[0]))):
            points = [bucket_map[ts] for ts in sorted(bucket_map)]
            rows.append({'market_id': key, 'label': labels.get(key, key), 'points': points})
        return rows

    def _build_forecast_markers(self, snapshots: list[dict[str, Any]]) -> list[dict[str, Any]]:
        markers: list[dict[str, Any]] = []
        previous_signature: tuple[float | None, float | None] | None = None
        for snap in snapshots:
            hours = snap.get('hours') or []
            temps = [to_float(item.get('temperature_c')) for item in hours]
            temps = [value for value in temps if value is not None]
            if not temps:
                continue
            top = sorted(temps, reverse=True)
            day_max = round(top[0], 2)
            top5_avg = round(sum(top[:5]) / min(len(top), 5), 2)
            signature = (top5_avg, day_max)
            if previous_signature is None:
                markers.append({
                    'ts': snap.get('fetched_at_utc'),
                    'fetched_at_source_local': snap.get('fetched_at_source_local'),
                    'top5_avg_c': top5_avg,
                    'day_max_c': day_max,
                    'marker_kind': 'baseline',
                })
                previous_signature = signature
                continue
            if signature != previous_signature:
                markers.append({
                    'ts': snap.get('fetched_at_utc'),
                    'fetched_at_source_local': snap.get('fetched_at_source_local'),
                    'top5_avg_c': top5_avg,
                    'day_max_c': day_max,
                    'marker_kind': 'change',
                })
                previous_signature = signature
        return markers

    def _aggregate_prebuilt_market_series(self, series_rows: list[dict[str, Any]], interval_seconds: int) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for row in series_rows:
            bucket_map: dict[int, dict[str, Any]] = {}
            for point in row.get('points') or []:
                parsed = parse_utc(point.get('ts'))
                if parsed is None:
                    continue
                bucket_ts = floor_timestamp(int(parsed.timestamp()), interval_seconds)
                normalized = dict(point)
                normalized['ts'] = iso_utc_from_ts(bucket_ts)
                bucket_map[bucket_ts] = normalized
            points = [bucket_map[ts] for ts in sorted(bucket_map)]
            out.append({
                'market_id': row.get('market_id'),
                'label': row.get('label'),
                'history_source': row.get('history_source'),
                'points': points,
            })
        out.sort(key=lambda item: sort_bucket_label(item.get('label') or item.get('market_id') or ''))
        return out

    def _color_closed_event_markers(self, markers: list[dict[str, Any]], market_series: list[dict[str, Any]]) -> list[dict[str, Any]]:
        resolved = self._find_resolved_market(market_series)
        if resolved is None:
            return markers
        out: list[dict[str, Any]] = []
        for marker in markers:
            rounded_day_max = round_half_up(to_float(marker.get('observed_temp_c')))
            if rounded_day_max is None:
                rounded_day_max = round_half_up(to_float(marker.get('day_max_c')))
            colored = dict(marker)
            if rounded_day_max is not None and bucket_label_matches_temperature(resolved.get('label') or '', rounded_day_max):
                colored['marker_color'] = 'green'
            out.append(colored)
        return out

    def _find_resolved_market(self, market_series: list[dict[str, Any]], threshold_cents: int = 99) -> dict[str, Any] | None:
        winner: dict[str, Any] | None = None
        for row in market_series:
            points = row.get('points') or []
            if not points:
                continue
            point = points[-1]
            yes_probability_cents = to_int(point.get('yes_probability_cents'))
            if yes_probability_cents is None or yes_probability_cents < threshold_cents:
                continue
            candidate = {
                'market_id': row.get('market_id'),
                'label': row.get('label'),
                'yes_probability_cents': yes_probability_cents,
                'ts': point.get('ts'),
                'actual_ts': point.get('actual_ts'),
            }
            if winner is None or yes_probability_cents > winner['yes_probability_cents']:
                winner = candidate
        return winner

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding='utf-8'))

    @staticmethod
    def _read_jsonl(path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        rows = []
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
        return rows


def floor_timestamp(ts: int, interval_seconds: int) -> int:
    return ts - (ts % interval_seconds)


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)
    except ValueError:
        return None


def iso_utc_from_ts(ts: int) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def to_float(value: Any) -> float | None:
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: Any) -> int | None:
    if value is None or value == '':
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def round_half_up(value: float | None) -> int | None:
    if value is None:
        return None
    if value >= 0:
        return int(value + 0.5)
    return int(value - 0.5)


def bucket_label_matches_temperature(label: str, rounded_temp_c: int) -> bool:
    match = re.search(r'-?\d+', label)
    if not match:
        return False
    bucket_value = int(match.group(0))
    lowered = label.lower()
    if 'or higher' in lowered or 'or above' in lowered:
        return rounded_temp_c >= bucket_value
    if 'or below' in lowered:
        return rounded_temp_c <= bucket_value
    return rounded_temp_c == bucket_value


def sort_bucket_label(label: str) -> tuple[int, str]:
    if 'or below' in label:
        head = label.split('°', 1)[0].strip()
        try:
            return (int(head), label)
        except ValueError:
            return (-9999, label)
    if 'or higher' in label or 'or above' in label:
        head = label.split('°', 1)[0].strip()
        try:
            return (int(head) + 1000, label)
        except ValueError:
            return (9999, label)
    head = label.split('°', 1)[0].strip()
    try:
        return (int(head), label)
    except ValueError:
        return (0, label)


def deslugify(value: str) -> str:
    return value.replace('-', ' ').title()
