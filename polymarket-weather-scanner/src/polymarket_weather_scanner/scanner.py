from __future__ import annotations

import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .client import PolymarketClient
from .config import ScannerConfig
from .database import ScannerDatabase
from .models import BucketStat, CandidateWallet, WalletScanResult, WalletWinStats


GROUPED_BUCKETS = [
    ('0-15¢', 0, 15),
    ('15-35¢', 15, 35),
    ('35-65¢', 35, 65),
    ('65-85¢', 65, 85),
    ('85-100¢', 85, 101),
]


class WeatherWalletScanner:
    def __init__(self, config: ScannerConfig | None = None) -> None:
        self.config = config or ScannerConfig()
        self.config.ensure_directories()
        self.client = PolymarketClient(self.config.gamma_base, self.config.data_base)
        self.db = ScannerDatabase(self.config.db_path)
        self.db.init()

    def discover_weather_market_terms(self) -> tuple[set[str], set[int]]:
        discovered: set[str] = set(self.config.weather_keywords)
        event_ids: set[int] = set()
        for keyword in self.config.weather_keywords:
            payload = self.client.public_search(keyword, limit_per_type=25, page=1)
            for event in payload.get('events') or []:
                try:
                    event_ids.add(int(event.get('id')))
                except (TypeError, ValueError):
                    pass
                for value in (event.get('title'), event.get('slug'), event.get('category'), event.get('subcategory')):
                    if value:
                        discovered.add(str(value).lower())
                for market in event.get('markets') or []:
                    for value in (market.get('question'), market.get('slug')):
                        if value:
                            discovered.add(str(value).lower())
        return discovered, event_ids

    def seed_candidates(self, weather_event_ids: set[int]) -> dict[str, CandidateWallet]:
        candidates: dict[str, CandidateWallet] = {}
        for period in self.config.leaderboard_periods:
            for offset in self.config.leaderboard_offsets:
                rows = self.client.leaderboard(
                    category=self.config.leaderboard_category,
                    time_period=period,
                    order_by=self.config.leaderboard_order_by,
                    limit=self.config.leaderboard_limit,
                    offset=offset,
                )
                if not rows:
                    continue
                for row in rows:
                    address = str(row.get('proxyWallet') or '').lower()
                    if not address:
                        continue
                    existing = candidates.get(address)
                    candidate = CandidateWallet(
                        address=address,
                        username=row.get('userName'),
                        pnl=float(row.get('pnl') or 0.0),
                        volume=float(row.get('vol') or 0.0),
                        source=f'leaderboard:{period.lower()}',
                        verified_badge=bool(row.get('verifiedBadge')),
                    )
                    if existing is None or (candidate.pnl or 0.0) > (existing.pnl or 0.0):
                        candidates[address] = candidate

        if self.config.enable_event_trade_seeding:
            for event_id in sorted(weather_event_ids)[: self.config.max_seed_events]:
                try:
                    trades = self.client.trades(event_id=event_id, limit=self.config.seed_event_trade_limit)
                except Exception:
                    continue
                for trade in trades:
                    address = str(trade.get('proxyWallet') or '').lower()
                    if not address:
                        continue
                    if address in candidates:
                        continue
                    candidates[address] = CandidateWallet(
                        address=address,
                        username=trade.get('name') or trade.get('pseudonym'),
                        pnl=None,
                        volume=None,
                        source=f'event_trades:{event_id}',
                        verified_badge=None,
                    )

        for address in self.db.list_custom_wallets():
            if address in candidates:
                continue
            candidates[address] = CandidateWallet(
                address=address,
                username=None,
                pnl=None,
                volume=None,
                source='custom_wallet',
                verified_badge=None,
            )
        return candidates

    @staticmethod
    def _matches_weather(activity: dict, weather_terms: set[str]) -> bool:
        haystacks = [
            str(activity.get('title') or '').lower(),
            str(activity.get('slug') or '').lower(),
            str(activity.get('eventSlug') or '').lower(),
            str(activity.get('outcome') or '').lower(),
        ]
        return any(term in hay for hay in haystacks for term in weather_terms if term)

    @staticmethod
    def _price_to_cents(price: float | int | str | None) -> int:
        value = float(price or 0.0)
        cents = int(value * 100)
        return max(0, min(100, cents))

    def calculate_win_stats(self, candidate: CandidateWallet, rows: list[dict] | None = None) -> WalletWinStats:
        rows = rows if rows is not None else self.client.closed_positions_all(candidate.address, max_items=self.config.closed_positions_limit)
        five_cent = [BucketStat(label=f'{start}-{start + 5}¢', start_cents=start, end_cents=start + 5) for start in range(0, 100, 5)]
        grouped = [BucketStat(label=label, start_cents=start, end_cents=end) for (label, start, end) in GROUPED_BUCKETS]
        wins = 0
        losses = 0

        for row in rows:
            cents = self._price_to_cents(row.get('avgPrice'))
            bucket_index = min(cents // 5, len(five_cent) - 1)
            is_win = float(row.get('realizedPnl') or 0.0) > 0.0
            target = five_cent[bucket_index]
            target.total += 1
            if is_win:
                target.wins += 1
                wins += 1
            else:
                target.losses += 1
                losses += 1

            for group in grouped:
                if group.start_cents <= cents < group.end_cents:
                    group.total += 1
                    if is_win:
                        group.wins += 1
                    else:
                        group.losses += 1
                    break

        total = wins + losses
        return WalletWinStats(
            analyzed_closed_positions=total,
            wins=wins,
            losses=losses,
            win_rate=(wins / total) if total else 0.0,
            grouped_buckets=[bucket.to_dict() for bucket in grouped],
            five_cent_buckets=[bucket.to_dict() for bucket in five_cent],
        )

    def evaluate_candidate(self, candidate: CandidateWallet, weather_terms: set[str]) -> WalletScanResult:
        distinct_markets = self.client.total_markets_traded(candidate.address)
        activity = self.client.user_activity(candidate.address, limit=self.config.activity_limit)
        trade_rows = [row for row in activity if row.get('type') == 'TRADE']
        sell_trade_count = sum(1 for row in trade_rows if str(row.get('side') or '').upper() == 'SELL')
        buy_trade_count = sum(1 for row in trade_rows if str(row.get('side') or '').upper() == 'BUY')
        weather_trade_count = sum(1 for row in trade_rows if self._matches_weather(row, weather_terms))
        last_trade_count = len(trade_rows)
        weather_trade_ratio = (weather_trade_count / last_trade_count) if last_trade_count else 0.0
        closed_positions = self.client.closed_positions_all(candidate.address, max_items=self.config.closed_positions_limit)
        pnl_value = float(candidate.pnl) if candidate.pnl is not None else sum(float(row.get('realizedPnl') or 0.0) for row in closed_positions)
        username = candidate.username
        if not username:
            username = next((str(row.get('name') or row.get('pseudonym') or '').strip() for row in trade_rows if (row.get('name') or row.get('pseudonym'))), None) or None
        win_stats = self.calculate_win_stats(candidate, rows=closed_positions)

        qualified = True
        reasons: list[str] = []
        if distinct_markets < self.config.minimum_distinct_markets:
            qualified = False
            reasons.append(f'distinct_markets<{self.config.minimum_distinct_markets}')
        if sell_trade_count > 0:
            qualified = False
            reasons.append('contains_sell_trade')
        if pnl_value is None or pnl_value <= self.config.minimum_positive_pnl:
            qualified = False
            reasons.append('non_positive_pnl')
        if weather_trade_count < self.config.minimum_weather_trade_count:
            qualified = False
            reasons.append(f'weather_trade_count<{self.config.minimum_weather_trade_count}')
        if weather_trade_ratio < self.config.minimum_weather_trade_ratio:
            qualified = False
            reasons.append(f'weather_trade_ratio<{self.config.minimum_weather_trade_ratio:.2f}')
        if not trade_rows:
            qualified = False
            reasons.append('no_trade_rows')

        return WalletScanResult(
            address=candidate.address,
            username=username,
            pnl=pnl_value,
            distinct_markets_traded=distinct_markets,
            last_trade_count=last_trade_count,
            sell_trade_count=sell_trade_count,
            buy_trade_count=buy_trade_count,
            weather_trade_count=weather_trade_count,
            weather_trade_ratio=weather_trade_ratio,
            qualified=qualified,
            qualification_reason='qualified' if qualified else ','.join(reasons),
            source=candidate.source,
            win_stats=win_stats.to_dict(),
        )

    def scan(self) -> list[WalletScanResult]:
        weather_terms, weather_event_ids = self.discover_weather_market_terms()
        candidates = self.seed_candidates(weather_event_ids)
        results: list[WalletScanResult] = []
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = [executor.submit(self.evaluate_candidate, candidate, weather_terms) for candidate in candidates.values()]
            for future in as_completed(futures):
                results.append(future.result())
        scan_id = self.db.create_scan()
        self.db.save_results(scan_id, results)
        return sorted(results, key=lambda item: (item.qualified, item.weather_trade_ratio, item.pnl or 0.0), reverse=True)

    def analyze_wallet(self, address: str, source: str = 'custom_wallet') -> dict:
        weather_terms, _ = self.discover_weather_market_terms()
        candidate = CandidateWallet(address=address.lower(), username=None, pnl=None, volume=None, source=source, verified_badge=None)
        result = self.evaluate_candidate(candidate, weather_terms)
        payload = result.to_dict()
        self.db.add_custom_wallet(address.lower())
        self.db.save_custom_wallet_result(payload)
        return payload

    def latest_results(self, qualified_only: bool = False, limit: int = 100) -> list[dict]:
        return [json.loads(row['payload_json']) for row in self.db.latest_results(qualified_only=qualified_only, limit=limit)]

    def latest_result_by_address(self, address: str) -> dict | None:
        row = self.db.latest_result_by_address(address)
        if row is None:
            return None
        return json.loads(row['payload_json'])

    def export(self, out_path: Path, fmt: str = 'json', qualified_only: bool = True, limit: int = 100) -> Path:
        rows = self.latest_results(qualified_only=qualified_only, limit=limit)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if fmt == 'json':
            out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
        elif fmt == 'csv':
            with out_path.open('w', encoding='utf-8', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
                if rows:
                    writer.writeheader()
                    writer.writerows(rows)
        else:
            raise ValueError(f'unsupported format: {fmt}')
        return out_path
