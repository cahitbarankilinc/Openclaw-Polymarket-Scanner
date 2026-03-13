from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ScannerConfig:
    gamma_base: str = 'https://gamma-api.polymarket.com'
    data_base: str = 'https://data-api.polymarket.com'
    db_path: Path = Path('data/scanner.db')
    scan_state_path: Path = Path('data/scan-state.json')
    page_size: int = 50
    leaderboard_limit: int = 50
    leaderboard_offsets: tuple[int, ...] = tuple(range(0, 501, 50))
    leaderboard_categories: tuple[str, ...] = (
        'WEATHER',
        'POLITICS',
        'SPORTS',
        'CRYPTO',
        'FINANCE',
        'CULTURE',
        'MENTIONS',
        'ECONOMICS',
        'TECH',
    )
    activity_limit: int = 500
    closed_positions_limit: int = 500
    max_workers: int = 8
    stage1_workers: int = 16
    stage2_leaderboard_per_category: int = 100
    stage2_weather_deep_limit: int = 250
    enable_event_trade_seeding: bool = True
    seed_event_trade_limit: int = 100
    max_seed_events: int = 50
    minimum_distinct_markets: int = 200
    minimum_positive_pnl: float = 0.0
    minimum_weather_trade_ratio: float = 0.15
    minimum_weather_trade_count: int = 10
    enforce_weather_filters: bool = False
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

    def ensure_directories(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
