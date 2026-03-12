from __future__ import annotations

import argparse
from pathlib import Path

from .scanner import WeatherWalletScanner
from .web import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='polymarket_weather_scanner')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('scan', help='run a full scan')

    report = sub.add_parser('report', help='print latest results')
    report.add_argument('--limit', type=int, default=25)
    report.add_argument('--qualified-only', action='store_true')

    export = sub.add_parser('export', help='export latest results')
    export.add_argument('--format', choices=('json', 'csv'), default='json')
    export.add_argument('--out', required=True)
    export.add_argument('--limit', type=int, default=100)
    export.add_argument('--qualified-only', action='store_true', default=True)

    serve_parser = sub.add_parser('serve', help='run local frontend server')
    serve_parser.add_argument('--host', default='127.0.0.1')
    serve_parser.add_argument('--port', type=int, default=8765)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    scanner = WeatherWalletScanner()

    if args.command == 'scan':
        results = scanner.scan()
        qualified = [result for result in results if result.qualified]
        print(f'scan complete: {len(results)} wallets checked, {len(qualified)} qualified')
        for item in qualified[:20]:
            pnl_text = 'n/a' if item.pnl is None else f'{item.pnl:.2f}'
            print(f"{item.address} | pnl={pnl_text} | markets={item.distinct_markets_traded} | weather_ratio={item.weather_trade_ratio:.2%}")
        return 0

    if args.command == 'report':
        rows = scanner.latest_results(qualified_only=args.qualified_only, limit=args.limit)
        for row in rows:
            pnl_text = 'n/a' if row['pnl'] is None else f"{row['pnl']:.2f}"
            print(
                f"{row['address']} | qualified={row['qualified']} | pnl={pnl_text} | "
                f"markets={row['distinct_markets_traded']} | sells={row['sell_trade_count']} | "
                f"weather={row['weather_trade_count']} ({row['weather_trade_ratio']:.2%}) | {row['qualification_reason']}"
            )
        return 0

    if args.command == 'export':
        path = scanner.export(Path(args.out), fmt=args.format, qualified_only=args.qualified_only, limit=args.limit)
        print(f'exported to {path}')
        return 0

    if args.command == 'serve':
        serve(host=args.host, port=args.port)
        return 0

    parser.error('unknown command')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
