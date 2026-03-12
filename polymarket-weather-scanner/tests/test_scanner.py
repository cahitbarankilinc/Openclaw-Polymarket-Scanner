import tempfile
import unittest
from pathlib import Path

from polymarket_weather_scanner.config import ScannerConfig
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


if __name__ == '__main__':
    unittest.main()
