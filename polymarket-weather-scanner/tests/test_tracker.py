import json
import tempfile
import unittest
from pathlib import Path

from polymarket_weather_scanner.config import ScannerConfig
from polymarket_weather_scanner.tracker import (
    EventForecastSnapshot,
    PolymarketEventTracker,
    TrackingCity,
    WeatherSourceClient,
    f_to_c,
    normalize_url,
    slugify,
)


class TrackerTests(unittest.TestCase):
    def test_history_url_converts_to_forecast_url(self) -> None:
        self.assertEqual(
            WeatherSourceClient.history_to_forecast_url('https://www.wunderground.com/history/daily/ca/mississauga/CYYZ'),
            'https://www.wunderground.com/forecast/ca/mississauga/CYYZ',
        )

    def test_helper_normalization(self) -> None:
        self.assertEqual(slugify('Tel Aviv'), 'tel-aviv')
        self.assertEqual(normalize_url('https://x/tr/%C3%A7ubuk/LTAC'), 'https://x/tr/çubuk/LTAC')
        self.assertAlmostEqual(f_to_c(32), 0.0)

    def test_run_cycle_writes_market_and_forecast_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tracker = PolymarketEventTracker(ScannerConfig(), root_dir=root / 'tracker')
            tracker.cities = [TrackingCity(name='Munich', source_url='https://www.wunderground.com/history/daily/de/munich/EDDM')]
            tracker.discover_all_open_events = lambda cities: {
                'Munich': [
                    {
                        'event_id': '1',
                        'event_slug': 'munich-2026-03-20',
                        'event_title': 'Highest temperature in Munich on March 20?',
                        'target_date': '2026-03-20',
                        'event_end_utc': '2026-03-20T12:00:00Z',
                        'source_url_expected': 'https://www.wunderground.com/history/daily/de/munich/EDDM',
                        'source_url_actual': 'https://www.wunderground.com/history/daily/de/munich/EDDM',
                        'source_url_matches_expected': True,
                        'markets': [
                            {
                                'id': 'm1',
                                'conditionId': 'cond1',
                                'question': 'Will the highest temperature in Munich be 8°C on March 20?',
                                'groupItemTitle': '8°C',
                                'outcomes': json.dumps(['Yes', 'No']),
                                'outcomePrices': json.dumps(['0.42', '0.58']),
                                'clobTokenIds': json.dumps(['yes1', 'no1']),
                                'bestBid': 0.41,
                                'bestAsk': 0.43,
                                'lastTradePrice': 0.42,
                                'spread': 0.02,
                                'slug': 'munich-8c',
                                'active': True,
                                'closed': False,
                            }
                        ],
                    }
                ]
            }
            tracker.capture_forecast_snapshot = lambda city, event: EventForecastSnapshot(
                event_id=event['event_id'],
                event_slug=event['event_slug'],
                event_title=event['event_title'],
                city=city.name,
                city_slug=city.slug,
                target_date=event['target_date'],
                source_url_expected=city.source_url,
                source_url_actual=event['source_url_actual'],
                source_forecast_page='https://www.wunderground.com/forecast/de/munich/EDDM',
                source_forecast_api_url='https://api.weather.com/v3/wx/forecast/hourly/15day?...',
                fetched_at_utc='2026-03-19T10:00:00Z',
                fetched_at_source_local='2026-03-19T11:00:00+01:00',
                hourly_count=2,
                hours=[
                    {'valid_time_local': '2026-03-20T00:00:00+0100', 'temperature_c': 3.0},
                    {'valid_time_local': '2026-03-20T01:00:00+0100', 'temperature_c': 2.0},
                ],
            )

            summary = tracker.run_cycle(forecast_interval_seconds=300, discovery_interval_seconds=1800)
            self.assertEqual(summary['cities'], 1)
            self.assertEqual(summary['open_events'], 1)
            self.assertEqual(summary['market_snapshots'], 1)
            self.assertEqual(summary['forecast_snapshots'], 1)

            event_dir = root / 'tracker' / 'cities' / 'munich' / 'events' / '2026-03-20'
            self.assertTrue((event_dir / 'market_prices.jsonl').exists())
            self.assertTrue((event_dir / 'forecast_hourly.jsonl').exists())
            self.assertTrue((event_dir / 'event_meta.json').exists())

            market_line = (event_dir / 'market_prices.jsonl').read_text(encoding='utf-8').splitlines()[-1]
            market_obj = json.loads(market_line)
            first_market = market_obj['markets'][0]
            self.assertEqual(first_market['yes_best_bid_sell_cents'], 41)
            self.assertEqual(first_market['yes_best_ask_buy_cents'], 43)
            self.assertEqual(first_market['no_best_bid_sell_cents'], 57)
            self.assertEqual(first_market['no_best_ask_buy_cents'], 59)


if __name__ == '__main__':
    unittest.main()
