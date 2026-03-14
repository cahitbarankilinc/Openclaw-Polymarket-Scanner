from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import contextlib

from .config import APP_DIR
from .database import ScannerDatabase
from .scanner import WeatherWalletScanner, normalize_win_stats_payload


WEB_DIR = Path(__file__).with_name('web')


class ScannerWebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, db: ScannerDatabase, web_dir: Path, scanner: WeatherWalletScanner, **kwargs):
        self.db = db
        self.web_dir = web_dir
        self.scanner = scanner
        super().__init__(*args, directory=str(web_dir), **kwargs)

    def end_headers(self) -> None:
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == '/api/results':
            self.handle_results(parsed.query)
            return
        if parsed.path == '/api/summary':
            self.handle_summary()
            return
        if parsed.path == '/api/scan-state':
            self.handle_scan_state()
            return
        if parsed.path == '/health':
            self.write_json({'ok': True})
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == '/api/custom-wallets':
            self.handle_add_wallet()
            return
        self.write_json({'error': 'not found'}, status=404)

    def handle_results(self, query_string: str) -> None:
        params = parse_qs(query_string)
        qualified_only = params.get('qualified_only', ['0'])[0] in {'1', 'true', 'yes'}
        limit = int(params.get('limit', ['250'])[0])
        rows = self.db.latest_results(qualified_only=qualified_only, limit=limit)
        items = [dict(row) for row in rows]
        payload = [json.loads(item['payload_json']) for item in items]
        for row in payload:
            row['win_stats'] = normalize_win_stats_payload(row.get('win_stats'))
        self.write_json(payload)

    def handle_summary(self) -> None:
        rows = [json.loads(dict(row)['payload_json']) for row in self.db.latest_results(qualified_only=False, limit=5000)]
        qualified = [row for row in rows if row['qualified']]
        category_counts: dict[str, int] = {}
        for row in rows:
            category = str(row.get('source_category') or 'unknown').lower()
            category_counts[category] = category_counts.get(category, 0) + 1
        summary = {
            'total': len(rows),
            'qualified': len(qualified),
            'avg_pnl': average([row['pnl'] for row in rows]),
            'avg_win_rate': average([((row.get('win_stats') or {}).get('win_rate')) for row in rows]),
            'top_pnl': max((row['pnl'] or 0.0) for row in rows) if rows else 0.0,
            'sources': sorted({row['source'] or 'unknown' for row in rows}),
            'categories': category_counts,
        }
        self.write_json(summary)

    def handle_scan_state(self) -> None:
        self.write_json(self.scanner.read_scan_state())

    def handle_add_wallet(self) -> None:
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            length = 0
        try:
            raw = self.rfile.read(length) if length else b'{}'
            payload = json.loads(raw.decode('utf-8') or '{}')
        except json.JSONDecodeError:
            self.write_json({'error': 'invalid json'}, status=400)
            return

        address = str(payload.get('address') or '').strip().lower()
        label = str(payload.get('label') or '').strip() or None
        if not address:
            self.write_json({'error': 'address is required'}, status=400)
            return
        if not address.startswith('0x') or len(address) != 42:
            self.write_json({'error': 'invalid wallet address'}, status=400)
            return

        try:
            self.db.add_custom_wallet(address, label)
            result = self.scanner.analyze_wallet(address, source='custom_wallet')
        except Exception as exc:  # noqa: BLE001
            self.write_json({'error': f'wallet analysis failed: {exc}'}, status=500)
            return

        self.write_json(result, status=201)

    def write_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        with contextlib.suppress(BrokenPipeError, ConnectionResetError):
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
