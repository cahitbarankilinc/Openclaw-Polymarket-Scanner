from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import WalletScanResult


SCHEMA = '''
CREATE TABLE IF NOT EXISTS scans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scan_started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scan_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scan_id INTEGER NOT NULL,
  address TEXT NOT NULL,
  username TEXT,
  pnl REAL,
  distinct_markets_traded INTEGER NOT NULL,
  last_trade_count INTEGER NOT NULL,
  sell_trade_count INTEGER NOT NULL,
  buy_trade_count INTEGER NOT NULL,
  weather_trade_count INTEGER NOT NULL,
  weather_trade_ratio REAL NOT NULL,
  qualified INTEGER NOT NULL,
  qualification_reason TEXT NOT NULL,
  source TEXT,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(scan_id) REFERENCES scans(id)
);

CREATE INDEX IF NOT EXISTS idx_scan_results_scan_id ON scan_results(scan_id);
CREATE INDEX IF NOT EXISTS idx_scan_results_address ON scan_results(address);
CREATE INDEX IF NOT EXISTS idx_scan_results_qualified ON scan_results(qualified);
'''


class ScannerDatabase:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def create_scan(self) -> int:
        with self.connect() as conn:
            cursor = conn.execute('INSERT INTO scans DEFAULT VALUES')
            return int(cursor.lastrowid)

    def save_results(self, scan_id: int, results: Iterable[WalletScanResult]) -> None:
        with self.connect() as conn:
            conn.executemany(
                '''
                INSERT INTO scan_results (
                  scan_id, address, username, pnl, distinct_markets_traded,
                  last_trade_count, sell_trade_count, buy_trade_count,
                  weather_trade_count, weather_trade_ratio, qualified,
                  qualification_reason, source, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                [
                    (
                        scan_id,
                        result.address,
                        result.username,
                        result.pnl,
                        result.distinct_markets_traded,
                        result.last_trade_count,
                        result.sell_trade_count,
                        result.buy_trade_count,
                        result.weather_trade_count,
                        result.weather_trade_ratio,
                        1 if result.qualified else 0,
                        result.qualification_reason,
                        result.source,
                        json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True),
                    )
                    for result in results
                ],
            )

    def latest_results(self, qualified_only: bool = False, limit: int = 100) -> list[sqlite3.Row]:
        with self.connect() as conn:
            where = 'WHERE sr.scan_id = (SELECT MAX(id) FROM scans)'
            if qualified_only:
                where += ' AND sr.qualified = 1'
            rows = conn.execute(
                f'''
                SELECT sr.*
                FROM scan_results sr
                {where}
                ORDER BY sr.qualified DESC, sr.weather_trade_ratio DESC, sr.pnl DESC
                LIMIT ?
                ''',
                (limit,),
            ).fetchall()
            return rows

    def latest_result_by_address(self, address: str) -> sqlite3.Row | None:
        with self.connect() as conn:
            return conn.execute(
                '''
                SELECT sr.*
                FROM scan_results sr
                WHERE sr.scan_id = (SELECT MAX(id) FROM scans)
                  AND lower(sr.address) = lower(?)
                ORDER BY sr.id DESC
                LIMIT 1
                ''',
                (address,),
            ).fetchone()

    def update_payload_json(self, row_id: int, payload: dict) -> None:
        with self.connect() as conn:
            conn.execute(
                'UPDATE scan_results SET payload_json = ? WHERE id = ?',
                (json.dumps(payload, ensure_ascii=False, sort_keys=True), row_id),
            )
