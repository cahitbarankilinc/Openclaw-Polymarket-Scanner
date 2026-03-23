from __future__ import annotations

import json
import re
import urllib.request

from .base import FetchResult

USER_AGENT = 'OpenClaw forecast snapshot tracker'


def history_to_forecast_url(source_url: str) -> str:
    return source_url.replace('/history/daily/', '/forecast/')


def f_to_c(temp_f: float | int | None) -> float | None:
    if temp_f is None:
        return None
    return round((float(temp_f) - 32) * 5 / 9, 3)


def fetch_wunderground(source_url: str) -> FetchResult:
    forecast_page = history_to_forecast_url(source_url)
    req = urllib.request.Request(forecast_page, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode('utf-8', 'ignore')
    matches = re.findall(r'https://api\.weather\.com/v3/wx/forecast/hourly/15day[^"\']+', html)
    if not matches:
        raise RuntimeError(f'forecast api url not found for {source_url}')
    api_url = matches[0].replace('&amp;', '&')
    api_req = urllib.request.Request(api_url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    with urllib.request.urlopen(api_req, timeout=30) as api_resp:
        payload = json.loads(api_resp.read().decode('utf-8'))
    times = list(payload.get('validTimeLocal') or [])
    temps_f = list(payload.get('temperature') or [])
    temps_c = [f_to_c(x) for x in temps_f]
    return FetchResult(
        source_id='wunderground',
        status_code=200,
        payload={'forecast_page': forecast_page, 'forecast_api_url': api_url, 'hourly': payload},
        times=times,
        temperatures_c=temps_c,
    )
