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

CREATE TABLE IF NOT EXISTS custom_wallets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT NOT NULL UNIQUE,
  label TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS custom_wallet_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_custom_wallets_address ON custom_wallets(address);
CREATE INDEX IF NOT EXISTS idx_custom_wallet_results_address ON custom_wallet_results(address);
'''


class ScannerDatabase:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    @staticmethod
    def _row_payload(row: sqlite3.Row) -> dict:
        return json.loads(row['payload_json'])

    @classmethod
    def _row_score(cls, row: sqlite3.Row) -> tuple:
        payload = cls._row_payload(row)
        source = str(payload.get('source') or '')
        return (
            1 if payload.get('qualified') else 0,
            1 if payload.get('pnl') is not None else 0,
            float(payload.get('pnl') or 0.0),
            1 if payload.get('username') else 0,
            1 if source == 'custom_wallet' else 0,
            int(payload.get('distinct_markets_traded') or 0),
            int(payload.get('win_stats', {}).get('analyzed_closed_positions') or 0),
        )

    @classmethod
    def _prefer_row(cls, left: sqlite3.Row | None, right: sqlite3.Row | None) -> sqlite3.Row | None:
        if left is None:
            return right
        if right is None:
            return left
        return left if cls._row_score(left) >= cls._row_score(right) else right

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
            scan_rows = conn.execute(
                f'''
                SELECT sr.*
                FROM scan_results sr
                {where}
                ORDER BY sr.qualified DESC, sr.weather_trade_ratio DESC, sr.pnl DESC
                LIMIT ?
                ''',
                (max(limit * 3, limit),),
            ).fetchall()
            custom_rows = conn.execute(
                '''
                SELECT cwr.*
                FROM custom_wallet_results cwr
                INNER JOIN (
                  SELECT lower(address) AS address, MAX(id) AS max_id
                  FROM custom_wallet_results
                  GROUP BY lower(address)
                ) latest
                  ON lower(cwr.address) = latest.address AND cwr.id = latest.max_id
                ORDER BY cwr.id DESC
                '''
            ).fetchall()

            merged: dict[str, sqlite3.Row] = {}
            for row in scan_rows:
                key = str(row['address']).lower()
                merged[key] = self._prefer_row(merged.get(key), row)
            for row in custom_rows:
                payload = self._row_payload(row)
                if qualified_only and not payload.get('qualified'):
                    continue
                key = str(row['address']).lower()
                merged[key] = self._prefer_row(merged.get(key), row)

            rows = list(merged.values())
            rows.sort(
                key=lambda row: (
                    self._row_payload(row).get('qualified', False),
                    self._row_payload(row).get('weather_trade_ratio', 0.0),
                    self._row_payload(row).get('pnl') or 0.0,
                ),
                reverse=True,
            )
            return rows[:limit]

    def latest_result_by_address(self, address: str) -> sqlite3.Row | None:
        with self.connect() as conn:
            custom = conn.execute(
                '''
                SELECT *
                FROM custom_wallet_results
                WHERE lower(address) = lower(?)
                ORDER BY id DESC
                LIMIT 1
                ''',
                (address,),
            ).fetchone()
            scan = conn.execute(
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
            return self._prefer_row(scan, custom)

    def add_custom_wallet(self, address: str, label: str | None = None) -> None:
        with self.connect() as conn:
            conn.execute(
                'INSERT OR IGNORE INTO custom_wallets(address, label) VALUES(lower(?), ?)',
                (address, label),
            )

    def list_custom_wallets(self) -> list[str]:
        with self.connect() as conn:
            rows = conn.execute('SELECT address FROM custom_wallets ORDER BY id ASC').fetchall()
            return [str(row['address']).lower() for row in rows]

    def save_custom_wallet_result(self, payload: dict) -> None:
        with self.connect() as conn:
            conn.execute(
                'INSERT INTO custom_wallet_results(address, payload_json) VALUES(lower(?), ?)',
                (payload['address'], json.dumps(payload, ensure_ascii=False, sort_keys=True)),
            )

    def update_payload_json(self, row_id: int, payload: dict) -> None:
        with self.connect() as conn:
            conn.execute(
                'UPDATE scan_results SET payload_json = ? WHERE id = ?',
                (json.dumps(payload, ensure_ascii=False, sort_keys=True), row_id),
            )
