"""HTTP health checks for ServerCommander."""

from __future__ import annotations

import asyncio
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from servercommander.config import ServerCommanderConfig


async def sc_health_check(
    config: ServerCommanderConfig,
    endpoints: list[str] | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    """Check HTTP endpoints and report status codes plus latency."""
    configured_endpoints = config.health.get("endpoints", [])
    selected_endpoints = endpoints if endpoints is not None else configured_endpoints
    check_timeout = float(timeout if timeout is not None else config.health.get("timeout", 5))

    if not selected_endpoints:
        return {
            "status": "no_endpoints",
            "ok": False,
            "timeout": check_timeout,
            "results": [],
        }

    results = await asyncio.gather(
        *[asyncio.to_thread(_check_one, endpoint, check_timeout) for endpoint in selected_endpoints]
    )
    return {
        "status": "ok" if all(result["ok"] for result in results) else "degraded",
        "ok": all(result["ok"] for result in results),
        "timeout": check_timeout,
        "results": list(results),
    }


def _check_one(endpoint: str, timeout: float) -> dict[str, Any]:
    started = time.perf_counter()

    try:
        request = Request(endpoint, method="GET", headers={"User-Agent": "ellmos-servercommander/0.1"})
        with urlopen(request, timeout=timeout) as response:
            status_code = int(response.status)
            ok = 200 <= status_code < 400
            error = None
    except HTTPError as exc:
        status_code = int(exc.code)
        ok = False
        error = str(exc)
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        status_code = None
        ok = False
        error = str(exc)

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "endpoint": endpoint,
        "ok": ok,
        "status_code": status_code,
        "latency_ms": elapsed_ms,
        "error": error,
    }
