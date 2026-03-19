import json
import tempfile
import unittest
from pathlib import Path

from polymarket_weather_scanner.dashboard_data import TrackerDashboardStore


class DashboardDataTests(unittest.TestCase):
    def test_build_series_aggregates_market_points_and_forecast_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'tracker'
            event_dir = root / 'cities' / 'munich' / 'events' / '2026-03-20'
            event_dir.mkdir(parents=True, exist_ok=True)
            (root / 'cities' / 'munich' / 'open_events.json').write_text(json.dumps({
                'city': 'Munich',
                'city_slug': 'munich',
                'source_url_expected': 'src',
                'open_events': [{'target_date': '2026-03-20', 'event_id': '1'}],
            }), encoding='utf-8')
            (event_dir / 'event_meta.json').write_text(json.dumps({
                'event_id': '1',
                'event_title': 'Highest temperature in Munich on March 20?',
                'source_url_expected': 'src',
                'source_url_actual': 'src',
                'source_url_matches_expected': True,
            }), encoding='utf-8')
            market_lines = [
                {
                    'fetched_at_utc': '2026-03-19T10:01:00Z',
                    'markets': [
                        {'market_id': 'a', 'group_item_title': '5°C', 'yes_probability_cents': 22, 'no_probability_cents': 78, 'yes_best_bid_sell_cents': 20, 'yes_best_ask_buy_cents': 24, 'no_best_bid_sell_cents': 76, 'no_best_ask_buy_cents': 80, 'yes_last_trade_cents': 23, 'no_last_trade_cents': 77}
                    ],
                },
                {
                    'fetched_at_utc': '2026-03-19T10:04:00Z',
                    'markets': [
                        {'market_id': 'a', 'group_item_title': '5°C', 'yes_probability_cents': 25, 'no_probability_cents': 75, 'yes_best_bid_sell_cents': 24, 'yes_best_ask_buy_cents': 26, 'no_best_bid_sell_cents': 74, 'no_best_ask_buy_cents': 76, 'yes_last_trade_cents': 25, 'no_last_trade_cents': 75}
                    ],
                },
                {
                    'fetched_at_utc': '2026-03-19T10:06:00Z',
                    'markets': [
                        {'market_id': 'a', 'group_item_title': '5°C', 'yes_probability_cents': 27, 'no_probability_cents': 73, 'yes_best_bid_sell_cents': 26, 'yes_best_ask_buy_cents': 28, 'no_best_bid_sell_cents': 72, 'no_best_ask_buy_cents': 74, 'yes_last_trade_cents': 27, 'no_last_trade_cents': 73}
                    ],
                },
            ]
            (event_dir / 'market_prices.jsonl').write_text('\n'.join(json.dumps(item) for item in market_lines) + '\n', encoding='utf-8')
            forecast_lines = [
                {'fetched_at_utc': '2026-03-19T10:00:00Z', 'fetched_at_source_local': '2026-03-19T11:00:00+01:00', 'hours': [{'temperature_c': 6}, {'temperature_c': 7}, {'temperature_c': 8}, {'temperature_c': 9}, {'temperature_c': 10}]},
                {'fetched_at_utc': '2026-03-19T10:05:00Z', 'fetched_at_source_local': '2026-03-19T11:05:00+01:00', 'hours': [{'temperature_c': 6}, {'temperature_c': 7}, {'temperature_c': 8}, {'temperature_c': 9}, {'temperature_c': 10}]},
                {'fetched_at_utc': '2026-03-19T10:10:00Z', 'fetched_at_source_local': '2026-03-19T11:10:00+01:00', 'hours': [{'temperature_c': 7}, {'temperature_c': 8}, {'temperature_c': 9}, {'temperature_c': 10}, {'temperature_c': 11}]},
            ]
            (event_dir / 'forecast_hourly.jsonl').write_text('\n'.join(json.dumps(item) for item in forecast_lines) + '\n', encoding='utf-8')

            store = TrackerDashboardStore(root)
            payload = store.build_series('munich', '2026-03-20', '5m')
            self.assertEqual(payload['snapshot_count'], 3)
            self.assertEqual(payload['forecast_snapshot_count'], 3)
            self.assertEqual(len(payload['market_series']), 1)
            self.assertEqual(len(payload['market_series'][0]['points']), 2)
            self.assertEqual(payload['market_series'][0]['points'][0]['yes_probability_cents'], 25)
            self.assertEqual(payload['market_series'][0]['points'][1]['yes_probability_cents'], 27)
            self.assertEqual(len(payload['forecast_markers']), 1)
            self.assertEqual(payload['forecast_markers'][0]['day_max_c'], 11)
            self.assertEqual(payload['forecast_markers'][0]['top5_avg_c'], 9.0)


if __name__ == '__main__':
    unittest.main()
