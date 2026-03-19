import json
import tempfile
import unittest
from pathlib import Path

from polymarket_weather_scanner.config import ScannerConfig
from polymarket_weather_scanner.tracker import PolymarketEventTracker, TrackingCity


class TrackerCacheTests(unittest.TestCase):
    def test_discovery_cache_is_reused_when_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tracker = PolymarketEventTracker(ScannerConfig(), root_dir=root / 'tracker')
            tracker.cities = [TrackingCity(name='Munich', source_url='https://www.wunderground.com/history/daily/de/munich/EDDM')]

            calls = {'count': 0}

            def fake_discover(cities):
                calls['count'] += 1
                return {
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
                            'markets': [],
                        }
                    ]
                }

            tracker.discover_all_open_events = fake_discover
            first = tracker._load_or_refresh_open_events(tracker.cities, 1800)
            second = tracker._load_or_refresh_open_events(tracker.cities, 1800)

            self.assertEqual(calls['count'], 1)
            self.assertEqual(first['Munich'][0]['event_id'], '1')
            self.assertEqual(second['Munich'][0]['event_id'], '1')
            cache_path = root / 'tracker' / 'open_events_cache.json'
            self.assertTrue(cache_path.exists())
            payload = json.loads(cache_path.read_text(encoding='utf-8'))
            self.assertIn('Munich', payload['cities'])


if __name__ == '__main__':
    unittest.main()
