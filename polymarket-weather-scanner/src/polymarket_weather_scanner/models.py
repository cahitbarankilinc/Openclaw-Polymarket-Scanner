from __future__ import annotations

from dataclasses import dataclass, asdict
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
