from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from typing import Any


class PolymarketClient:
    def __init__(self, gamma_base: str, data_base: str, user_agent: str = 'polymarket-weather-scanner/0.1') -> None:
        self.gamma_base = gamma_base.rstrip('/')
        self.data_base = data_base.rstrip('/')
        self.user_agent = user_agent

    def _get_json(self, url: str, retries: int = 3, timeout: int = 30) -> Any:
        last_error: Exception | None = None
        for attempt in range(1, retries + 1):
            try:
                request = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    return json.load(response)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt == retries:
                    raise
                time.sleep(0.5 * attempt)
        raise RuntimeError(f'failed to fetch {url}: {last_error}')

    def gamma_get(self, path: str, **params: Any) -> Any:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        url = f'{self.gamma_base}{path}'
        if query:
            url = f'{url}?{query}'
        return self._get_json(url)

    def data_get(self, path: str, **params: Any) -> Any:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        url = f'{self.data_base}{path}'
        if query:
            url = f'{url}?{query}'
        return self._get_json(url)

    def leaderboard(self, category: str, time_period: str, order_by: str, limit: int, offset: int) -> list[dict[str, Any]]:
        return self.data_get('/v1/leaderboard', category=category, timePeriod=time_period, orderBy=order_by, limit=limit, offset=offset)

    def user_activity(self, user: str, limit: int, offset: int = 0, activity_type: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {'user': user, 'limit': limit, 'offset': offset}
        if activity_type:
            params['type'] = activity_type
        return self.data_get('/activity', **params)

    def total_markets_traded(self, user: str) -> int:
        payload = self.data_get('/traded', user=user)
        return int(payload.get('traded', 0))

    def closed_positions(self, user: str, limit: int = 50, offset: int = 0, sort_by: str = 'TIMESTAMP') -> list[dict[str, Any]]:
        return self.data_get('/closed-positions', user=user, limit=limit, offset=offset, sortBy=sort_by, sortDirection='DESC')

    def closed_positions_all(self, user: str, max_items: int = 500, page_size: int = 50, sort_by: str = 'TIMESTAMP') -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        offset = 0
        while len(rows) < max_items:
            batch = self.closed_positions(user=user, limit=min(page_size, max_items - len(rows)), offset=offset, sort_by=sort_by)
            if not batch:
                break
            rows.extend(batch)
            if len(batch) < min(page_size, max_items - (len(rows) - len(batch))):
                break
            offset += len(batch)
        return rows

    def public_search(self, query: str, limit_per_type: int = 25, page: int = 1) -> dict[str, Any]:
        return self.gamma_get('/public-search', q=query, limit_per_type=limit_per_type, page=page, search_profiles='false', search_tags='false', optimized='true')

    def trades(self, *, user: str | None = None, event_id: int | None = None, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        params: dict[str, Any] = {'limit': limit, 'offset': offset}
        if user:
            params['user'] = user
        if event_id is not None:
            params['eventId'] = event_id
        return self.data_get('/trades', **params)

    def positions(
        self,
        user: str,
        limit: int = 500,
        offset: int = 0,
        sort_by: str | None = None,
        sort_direction: str | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {'user': user, 'limit': limit, 'offset': offset}
        if sort_by:
            params['sortBy'] = sort_by
        if sort_direction:
            params['sortDirection'] = sort_direction
        return self.data_get('/positions', **params)
