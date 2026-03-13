import tempfile
import unittest
from pathlib import Path

from polymarket_weather_scanner.config import ScannerConfig
from polymarket_weather_scanner.models import CandidateWallet
from polymarket_weather_scanner.scanner import WeatherWalletScanner


class StubScanner(WeatherWalletScanner):
    def __init__(self, root: Path):
        super().__init__(ScannerConfig(db_path=root / 'test-scanner.db'))


class ScannerTests(unittest.TestCase):
    def test_weather_matching_basic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scanner = StubScanner(Path(tmp))
            activity = {
                'title': 'Will it rain in LA by Friday?',
                'slug': 'will-it-rain-in-la',
                'eventSlug': 'weather-la-rain',
                'outcome': 'Yes',
            }
            self.assertTrue(scanner._matches_weather(activity, {'rain', 'weather'}))

    def test_weather_matching_negative(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scanner = StubScanner(Path(tmp))
            activity = {
                'title': 'Will BTC hit 200k?',
                'slug': 'btc-200k',
                'eventSlug': 'crypto-btc',
                'outcome': 'Yes',
            }
            self.assertFalse(scanner._matches_weather(activity, {'rain', 'weather'}))

    def test_export_empty_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scanner = StubScanner(root)
            out = root / 'empty.csv'
            scanner.export(out, fmt='csv', qualified_only=True, limit=1)
            self.assertTrue(out.exists())

    def test_calculate_win_stats_grouped_buckets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scanner = StubScanner(Path(tmp))
            scanner.client.closed_positions_all = lambda user, max_items=500: [
                {'avgPrice': 0.02, 'realizedPnl': 10},
                {'avgPrice': 0.07, 'realizedPnl': 5},
                {'avgPrice': 0.17, 'realizedPnl': -1},
                {'avgPrice': 0.66, 'realizedPnl': 1},
                {'avgPrice': 0.92, 'realizedPnl': 0},
            ]
            stats = scanner.calculate_win_stats(CandidateWallet(address='0xabc'))
            self.assertEqual(stats.analyzed_closed_positions, 5)
            self.assertEqual(stats.wins, 3)
            self.assertEqual(stats.losses, 2)
            self.assertAlmostEqual(stats.win_rate, 0.6)
            grouped = {bucket['label']: bucket for bucket in stats.grouped_buckets}
            self.assertEqual(grouped['0-15¢']['wins'], 2)
            self.assertEqual(grouped['15-35¢']['losses'], 1)
            self.assertEqual(grouped['65-85¢']['wins'], 1)
            self.assertEqual(grouped['85-100¢']['losses'], 1)


if __name__ == '__main__':
    unittest.main()
