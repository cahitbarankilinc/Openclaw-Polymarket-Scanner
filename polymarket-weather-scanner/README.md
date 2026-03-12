# Polymarket Weather Scanner

API-first scanner for discovering Polymarket wallets that:

- have traded at least 200 distinct markets
- have **no SELL** in their last 500 `TRADE` activities
- have **positive account-wide PnL**
- are meaningfully active in weather-themed markets

## Why this exists

This project is built for continuous discovery of weather-focused wallets without depending on brittle browser scraping for the core signal pipeline.

## Data sources

- Gamma API: market discovery, public search, profiles
- Data API: leaderboard, activity, traded market count, closed positions
- Optional browser/manual verification later

## Default logic

A wallet qualifies when all of these are true:

1. `distinct_markets_traded >= 200`
2. Among the last 500 `TRADE` activities, `SELL` count is 0
3. Account-wide PnL is positive
4. Weather relevance score is above threshold

## Weather relevance

Weather market discovery combines:

- official WEATHER leaderboard seeds
- keyword search over weather-related terms
- matching against discovered weather market/event slugs
- optional event-trade seeding layer (disabled by default in v1 for speed/stability)

Current keyword set:

- weather
- temperature
- rain
- snow
- hurricane
- storm
- forecast
- climate

## Project layout

- `src/polymarket_weather_scanner/` — scanner package
- `tests/` — automated tests
- `data/` — generated SQLite DB and exports

## Quick start

```bash
cd polymarket-weather-scanner
PYTHONPATH=src python3 -m polymarket_weather_scanner scan
PYTHONPATH=src python3 -m polymarket_weather_scanner report --limit 25
```

## Commands

### Run a full scan

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner scan
```

### Show top matches

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner report --limit 20
```

### Export latest qualifying wallets to JSON

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner export --format json --out data/latest-wallets.json
```

### Export latest qualifying wallets to CSV

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner export --format csv --out data/latest-wallets.csv
```

### Open local frontend

```bash
PYTHONPATH=src python3 -m polymarket_weather_scanner serve --host 127.0.0.1 --port 8765
```

Then open:

```text
http://127.0.0.1:8765
```

The frontend reads the latest scan results from `data/scanner.db` and gives you:

- summary cards
- search/filter/sort controls
- a browsable results table
- lightweight JSON API endpoints at `/api/results` and `/api/summary`

## Notes

- Uses only Python stdlib right now
- Keeps an audit-friendly local SQLite database
- Designed to be scheduled later (cron/heartbeat/etc.)
