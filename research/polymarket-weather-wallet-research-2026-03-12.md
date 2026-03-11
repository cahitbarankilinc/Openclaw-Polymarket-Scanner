# Polymarket Weather Wallet Research — 2026-03-12

## Goal
Find Polymarket wallets focused on weather markets, with filters:
- last 500 activities contain no SELL
- minimum 200 predictions
- positive PnL

Then design a program that can keep finding such wallets continuously.

## Important Findings

### 1) Public APIs appear sufficient for a strong first version
Polymarket exposes multiple public data surfaces:
- Gamma API (`https://gamma-api.polymarket.com`) for events, markets, search, profiles, tags
- Data API (`https://data-api.polymarket.com`) for user activity, trades, current/closed positions, value, leaderboard, total traded markets
- Goldsky subgraphs for positions, orders, activity, open interest, PnL

This means the first productionable version likely does **not** need browser scraping for core wallet discovery.
Browser automation should be a fallback / verification layer only.

### 2) WEATHER category exists in the official leaderboard API
Endpoint:
- `GET https://data-api.polymarket.com/v1/leaderboard?category=WEATHER&timePeriod=ALL&orderBy=PNL&limit=...`

This is a very strong seed source for candidate wallets.
It directly returns:
- proxyWallet
- userName
- vol
- pnl
- profileImage
- verifiedBadge

This dramatically reduces search space.

### 3) Activity endpoint exposes side and type
Endpoint:
- `GET /activity?user={address}&limit=500`

Important fields returned:
- `type` (TRADE, SPLIT, MERGE, REDEEM, etc.)
- `side` (BUY / SELL)
- `title`
- `eventSlug`
- `outcome`
- `timestamp`
- `usdcSize`

This should be enough to test the “last 500 activities contain no SELL” rule, as long as we define whether we mean:
- no SELL in all activity rows, or
- no SELL among TRADE rows only

Recommendation: apply the rule only to `type=TRADE` rows.

### 4) There is an endpoint for total markets traded
Endpoint:
- `GET /traded?user={address}`

Returns integer count of markets traded.
This may map more closely to “minimum 200 prediction yapmis” than raw activity count.

Potential interpretations of “200 prediction”:
1. `traded >= 200` (unique markets traded)
2. at least 200 TRADE rows
3. at least 200 BUY trades

Best default interpretation: `traded >= 200`.
If needed, also compute raw trade count as a secondary metric.

### 5) Positive PnL can be sourced multiple ways
Possible sources:
- leaderboard `pnl` (fastest seed metric, category-specific)
- `closed-positions` summed `realizedPnl`
- PnL subgraph for more complete position-level PnL

Recommendation:
- Use leaderboard/category PnL when available for ranking and seeding
- Use closed positions and/or PnL subgraph for verification/audit

### 6) Weather market discovery is possible from public search and market metadata
Useful methods:
- `GET /public-search?q=weather`
- `GET /public-search?q=temperature`
- `GET /public-search?q=rain`
- `GET /public-search?q=snow`
- possibly `hurricane`, `forecast`, city names, etc.

Observed examples include markets like:
- highest temperature in Seoul on a date
- global temperature bracket events
- rain in LA
- snow in NYC
- named storm / hurricane season

So weather-themed market discovery can be built by:
- official WEATHER leaderboard
- query-based weather event discovery
- category/tag inspection from Gamma data

### 7) User’s previous repo is currently mostly a front-end template / mock UI
Repo checked:
- `cahitbarankilinc/polymarket-insights-hub`

Current repo shape suggests:
- React/Vite front-end
- local mock data
- no real Polymarket ingestion backend in the checked version

Conclusion:
- Better to build a fresh data pipeline / scanner module
- UI from the repo can maybe be reused later, but not as the core discovery engine right now

### 8) Community repos confirm common patterns
Useful reference themes found on GitHub:
- official clients: `Polymarket/clob-client`, `Polymarket/py-clob-client`
- open subgraph: `Polymarket/polymarket-subgraph`
- community trackers emphasize pagination, dedupe, CSV export, wallet-first analysis, alerting

This suggests our architecture should prioritize:
- pagination support
- local cache/database
- deterministic scoring/filtering
- audit trail for why a wallet matched

## Proposed Data Strategy

### Candidate generation (cheap -> broad)
1. Pull WEATHER leaderboard pages (ALL time, maybe MONTH too)
2. Pull market/event search results for weather keywords
3. Collect wallets that appear in weather market trades / activity
4. Deduplicate candidate wallets

### Candidate verification (more expensive)
For each candidate wallet:
1. fetch `/activity?user=...&limit=500`
2. count `TRADE` rows and verify no `side=SELL`
3. fetch `/traded?user=...` to verify 200+ predictions/markets
4. fetch leaderboard row or closed positions / PnL source to confirm positive PnL
5. compute “weather focus score” based on fraction of activity in weather markets

### Continuous mode
Run on schedule:
- refresh weather markets
- refresh candidate wallet list
- rescore known wallets
- insert newly matching wallets into results store
- emit audit record / notification when a new wallet qualifies

## Recommended Architecture

### Version 1 (fastest path)
- Python scanner service
- SQLite or Postgres
- pure API approach first
- CLI + CSV/JSON output
- no browser dependency for discovery

Modules:
- `market_discovery.py`
- `wallet_seeds.py`
- `wallet_activity.py`
- `wallet_scoring.py`
- `runner.py`
- `storage.py`

### Version 2
- web UI or dashboard
- browser verification / screenshot collector
- alerting (Telegram)
- historical trend analysis per wallet

## Core Scoring / Filtering Model

Suggested hard filters:
- `leaderboard_pnl > 0` OR `verified_total_realized_pnl > 0`
- `traded >= 200`
- among last 500 TRADE activities: `sell_count == 0`
- weather relevance score >= threshold

Suggested soft metrics:
- weather_trade_ratio
- avg trade size
- recent activity recency
- number of unique weather markets traded
- realized pnl / total volume ratio

## Critical Ambiguities to Resolve Later
1. “prediction” exact definition:
   - unique markets traded?
   - total trades?
   - only BUY trades?
2. SELL rule scope:
   - all activities?
   - only TRADE activities?
3. Positive PnL scope:
   - weather-only pnl?
   - account-wide pnl?
   - realized only or realized+unrealized?
4. Weather scope:
   - only official WEATHER category?
   - include temperature/rain/snow/hurricane/climate markets discovered by keyword?

## Recommended Defaults
- prediction := total markets traded (`/traded`)
- no SELL := among last 500 `TRADE` activities
- pnl := account-level positive pnl from leaderboard or verified realized pnl
- weather scope := official WEATHER category + keyword-derived weather market set

## Why this approach is strong
- starts from official public APIs
- minimizes brittle scraping
- supports repeatable continuous scans
- can explain exactly why each wallet matched
- leaves room for browser fallback when API data is incomplete
