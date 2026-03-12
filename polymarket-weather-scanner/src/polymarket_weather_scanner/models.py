from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class CandidateWallet:
    address: str
    username: str | None = None
    pnl: float | None = None
    volume: float | None = None
    source: str | None = None
    verified_badge: bool | None = None


@dataclass
class BucketStat:
    label: str
    start_cents: int
    end_cents: int
    total: int = 0
    wins: int = 0
    losses: int = 0

    @property
    def win_rate(self) -> float:
        return (self.wins / self.total) if self.total else 0.0

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data['win_rate'] = self.win_rate
        return data


@dataclass
class WalletWinStats:
    analyzed_closed_positions: int
    wins: int
    losses: int
    win_rate: float
    grouped_buckets: list[dict[str, Any]] = field(default_factory=list)
    five_cent_buckets: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WalletScanResult:
    address: str
    username: str | None
    pnl: float | None
    distinct_markets_traded: int
    last_trade_count: int
    sell_trade_count: int
    buy_trade_count: int
    weather_trade_count: int
    weather_trade_ratio: float
    qualified: bool
    qualification_reason: str
    source: str | None
    win_stats: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
