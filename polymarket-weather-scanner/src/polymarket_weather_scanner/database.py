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
                merged[str(row['address']).lower()] = row
            for row in custom_rows:
                payload = json.loads(row['payload_json'])
                if qualified_only and not payload.get('qualified'):
                    continue
                merged[str(row['address']).lower()] = row

            rows = list(merged.values())
            rows.sort(
                key=lambda row: (
                    json.loads(row['payload_json']).get('qualified', False),
                    json.loads(row['payload_json']).get('weather_trade_ratio', 0.0),
                    json.loads(row['payload_json']).get('pnl') or 0.0,
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
            if custom is not None:
                return custom
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
