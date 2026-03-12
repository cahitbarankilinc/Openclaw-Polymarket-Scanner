from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import APP_DIR
from .database import ScannerDatabase
from .scanner import WeatherWalletScanner


WEB_DIR = Path(__file__).with_name('web')


class ScannerWebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, db: ScannerDatabase, web_dir: Path, scanner: WeatherWalletScanner, **kwargs):
        self.db = db
        self.web_dir = web_dir
        self.scanner = scanner
        super().__init__(*args, directory=str(web_dir), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == '/api/results':
            self.handle_results(parsed.query)
            return
        if parsed.path == '/api/summary':
            self.handle_summary()
            return
        if parsed.path == '/api/wallet':
            self.handle_wallet(parsed.query)
            return
        if parsed.path == '/health':
            self.write_json({'ok': True})
            return
        if parsed.path.startswith('/wallet/'):
            self.path = '/wallet.html'
            return super().do_GET()
        super().do_GET()

    def handle_results(self, query_string: str) -> None:
        params = parse_qs(query_string)
        qualified_only = params.get('qualified_only', ['0'])[0] in {'1', 'true', 'yes'}
        limit = int(params.get('limit', ['250'])[0])
        rows = self.db.latest_results(qualified_only=qualified_only, limit=limit)
        items = [dict(row) for row in rows]
        payload = [json.loads(item['payload_json']) for item in items]
        self.write_json(payload)

    def handle_summary(self) -> None:
        rows = [json.loads(dict(row)['payload_json']) for row in self.db.latest_results(qualified_only=False, limit=1000)]
        qualified = [row for row in rows if row['qualified']]
        summary = {
            'total': len(rows),
            'qualified': len(qualified),
            'avg_pnl': average([row['pnl'] for row in rows]),
            'avg_weather_ratio': average([row['weather_trade_ratio'] for row in rows]),
            'avg_win_rate': average([((row.get('win_stats') or {}).get('win_rate')) for row in rows]),
            'top_pnl': max((row['pnl'] or 0.0) for row in rows) if rows else 0.0,
            'top_markets': max((row['distinct_markets_traded'] for row in rows), default=0),
            'sources': sorted({row['source'] or 'unknown' for row in rows}),
        }
        self.write_json(summary)

    def handle_wallet(self, query_string: str) -> None:
        params = parse_qs(query_string)
        address = params.get('address', [''])[0].strip().lower()
        if not address:
            self.write_json({'error': 'address is required'}, status=400)
            return
        row = self.scanner.latest_result_by_address(address)
        if row is None:
            self.write_json({'error': 'wallet not found'}, status=404)
            return
        self.write_json(row)

    def write_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)


def average(values: list[float | None]) -> float:
    nums = [value for value in values if value is not None]
    if not nums:
        return 0.0
    return sum(nums) / len(nums)


def serve(host: str = '127.0.0.1', port: int = 8765) -> None:
    db = ScannerDatabase(APP_DIR / 'data' / 'scanner.db')
    db.init()
    scanner = WeatherWalletScanner()

    def handler(*args, **kwargs):
        return ScannerWebHandler(*args, db=db, web_dir=WEB_DIR, scanner=scanner, **kwargs)

    server = ThreadingHTTPServer((host, port), handler)
    print(f'frontend running at http://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nshutting down')
    finally:
        server.server_close()
