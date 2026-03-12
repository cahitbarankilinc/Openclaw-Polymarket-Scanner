from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ScannerConfig:
    gamma_base: str = 'https://gamma-api.polymarket.com'
    data_base: str = 'https://data-api.polymarket.com'
    db_path: Path = Path('data/scanner.db')
    page_size: int = 50
    leaderboard_limit: int = 50
    leaderboard_offsets: tuple[int, ...] = (0, 50, 100)
    activity_limit: int = 500
    max_workers: int = 8
    enable_event_trade_seeding: bool = False
    seed_event_trade_limit: int = 100
    max_seed_events: int = 20
    minimum_distinct_markets: int = 200
    minimum_positive_pnl: float = 0.0
    minimum_weather_trade_ratio: float = 0.15
    minimum_weather_trade_count: int = 10
    weather_keywords: tuple[str, ...] = (
        'weather',
        'temperature',
        'rain',
        'snow',
        'hurricane',
        'storm',
        'forecast',
        'climate',
    )
    leaderboard_periods: tuple[str, ...] = ('ALL', 'MONTH')
    leaderboard_order_by: str = 'PNL'
    leaderboard_category: str = 'WEATHER'

    def ensure_directories(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
