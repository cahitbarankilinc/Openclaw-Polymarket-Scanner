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
            scanner.client.positions = lambda user, limit=500, offset=0, sort_by=None, sort_direction=None: []
            stats = scanner.calculate_win_stats(CandidateWallet(address='0xabc'))
            self.assertEqual(stats.analyzed_positions, 5)
            self.assertEqual(stats.analyzed_closed_positions, 5)
            self.assertEqual(stats.analyzed_open_loss_positions, 0)
            self.assertEqual(stats.wins, 3)
            self.assertEqual(stats.losses, 2)
            self.assertAlmostEqual(stats.win_rate, 0.6)
            grouped = {bucket['label']: bucket for bucket in stats.grouped_buckets}
            self.assertEqual(grouped['0-15¢']['wins'], 2)
            self.assertEqual(grouped['15-35¢']['losses'], 1)
            self.assertEqual(grouped['65-85¢']['wins'], 1)
            self.assertEqual(grouped['85-100¢']['losses'], 1)

    def test_calculate_win_stats_outcome_filter_is_case_insensitive_exact_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scanner = StubScanner(Path(tmp))
            scanner.client.closed_positions_all = lambda user, max_items=500: [
                {'avgPrice': 0.10, 'realizedPnl': 8, 'outcome': 'Yes'},
                {'avgPrice': 0.20, 'realizedPnl': -2, 'outcome': 'YES'},
                {'avgPrice': 0.30, 'realizedPnl': 5, 'outcome': 'No'},
                {'avgPrice': 0.40, 'realizedPnl': 4, 'outcome': 'Yes '},
                {'avgPrice': 0.50, 'realizedPnl': 7, 'outcome': 'Yes sir'},
            ]
            scanner.client.positions = lambda user, limit=500, offset=0, sort_by=None, sort_direction=None: []
            stats = scanner.calculate_win_stats(CandidateWallet(address='0xabc'))
            yes_stats = stats.outcome_stats['yes']
            no_stats = stats.outcome_stats['no']

            self.assertEqual(yes_stats['analyzed_positions'], 3)
            self.assertEqual(yes_stats['analyzed_closed_positions'], 3)
            self.assertEqual(yes_stats['analyzed_open_loss_positions'], 0)
            self.assertEqual(yes_stats['wins'], 2)
            self.assertEqual(yes_stats['losses'], 1)
            self.assertAlmostEqual(yes_stats['win_rate'], 2 / 3)
            self.assertEqual(no_stats['analyzed_positions'], 1)
            self.assertEqual(no_stats['analyzed_closed_positions'], 1)
            self.assertIn('yes sir', stats.outcome_stats)
            self.assertEqual(stats.outcome_stats['yes sir']['analyzed_closed_positions'], 1)


    def test_calculate_win_stats_includes_only_target_open_position_losses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scanner = StubScanner(Path(tmp))
            closed_rows = [
                {'avgPrice': 0.10, 'realizedPnl': 3, 'outcome': 'Yes'},
                {'avgPrice': 0.72, 'realizedPnl': -1, 'outcome': 'No'},
            ]
            open_rows = [
                {'avgPrice': 0.12, 'percentPnl': -95, 'outcome': 'Yes'},
                {'avgPrice': 0.18, 'percentPnl': -99.5, 'outcome': 'Yes'},
                {'avgPrice': 0.88, 'percentPnl': -101, 'outcome': 'No'},
                {'avgPrice': 0.52, 'percentPnl': -94.99, 'outcome': 'No'},
                {'avgPrice': 0.43, 'percentPnl': -101.01, 'outcome': 'Maybe'},
            ]
            stats = scanner.calculate_win_stats(CandidateWallet(address='0xabc'), rows=closed_rows, open_rows=open_rows)

            self.assertEqual(stats.analyzed_positions, 5)
            self.assertEqual(stats.analyzed_closed_positions, 2)
            self.assertEqual(stats.analyzed_open_loss_positions, 3)
            self.assertEqual(stats.wins, 1)
            self.assertEqual(stats.losses, 4)
            self.assertAlmostEqual(stats.win_rate, 0.2)

            grouped = {bucket['label']: bucket for bucket in stats.grouped_buckets}
            self.assertEqual(grouped['0-15¢']['total'], 2)
            self.assertEqual(grouped['0-15¢']['wins'], 1)
            self.assertEqual(grouped['0-15¢']['losses'], 1)
            self.assertEqual(grouped['15-35¢']['total'], 1)
            self.assertEqual(grouped['15-35¢']['losses'], 1)
            self.assertEqual(grouped['65-85¢']['total'], 1)
            self.assertEqual(grouped['65-85¢']['losses'], 1)
            self.assertEqual(grouped['85-100¢']['total'], 1)
            self.assertEqual(grouped['85-100¢']['losses'], 1)

            yes_stats = stats.outcome_stats['yes']
            self.assertEqual(yes_stats['analyzed_positions'], 3)
            self.assertEqual(yes_stats['analyzed_closed_positions'], 1)
            self.assertEqual(yes_stats['analyzed_open_loss_positions'], 2)
            self.assertEqual(yes_stats['wins'], 1)
            self.assertEqual(yes_stats['losses'], 2)

            no_stats = stats.outcome_stats['no']
            self.assertEqual(no_stats['analyzed_positions'], 2)
            self.assertEqual(no_stats['analyzed_closed_positions'], 1)
            self.assertEqual(no_stats['analyzed_open_loss_positions'], 1)
            self.assertEqual(no_stats['wins'], 0)
            self.assertEqual(no_stats['losses'], 2)


if __name__ == '__main__':
    unittest.main()
