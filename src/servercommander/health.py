"""HTTP health checks for ServerCommander."""

from __future__ import annotations

import asyncio
import os
import shutil
import socket
import subprocess
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from servercommander.config import ServerCommanderConfig


def _configured_list(value: Any) -> list[str]:
    """Return a conservative list of non-empty string settings."""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


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


async def sc_host_diagnostics(
    config: ServerCommanderConfig,
    storage_paths: list[str] | None = None,
    ping_hosts: list[str] | None = None,
    dns_hosts: list[str] | None = None,
    timeout: float | None = None,
) -> dict[str, Any]:
    """Run explicitly configured local storage, ping, and DNS diagnostics.

    This deliberately has no built-in network targets.  A caller must provide
    hosts directly or configure them under ``[health]`` before a probe leaves
    the machine.  That keeps the portable BACH delta useful without retaining
    its personal FritzBox, NAS, or database assumptions.
    """
    health_config = config.health
    selected_paths = _configured_list(storage_paths if storage_paths is not None else health_config.get("storage_paths"))
    selected_ping_hosts = _configured_list(ping_hosts if ping_hosts is not None else health_config.get("ping_hosts"))
    selected_dns_hosts = _configured_list(dns_hosts if dns_hosts is not None else health_config.get("dns_hosts"))
    check_timeout = float(timeout if timeout is not None else health_config.get("timeout", 5))
    check_timeout = max(0.1, min(check_timeout, 60.0))

    storage_results = await asyncio.gather(
        *[asyncio.to_thread(_check_storage_path, path) for path in selected_paths]
    )
    ping_results = await asyncio.gather(
        *[asyncio.to_thread(_check_ping_host, host, check_timeout) for host in selected_ping_hosts]
    )
    dns_results = await asyncio.gather(
        *[asyncio.to_thread(_check_dns_host, host) for host in selected_dns_hosts]
    )
    results = list(storage_results) + list(ping_results) + list(dns_results)

    if not results:
        return {
            "status": "not_configured",
            "ok": False,
            "timeout": check_timeout,
            "results": [],
            "hint": "Configure [health] storage_paths, ping_hosts, or dns_hosts, or pass them explicitly.",
        }

    return {
        "status": "ok" if all(result["ok"] for result in results) else "degraded",
        "ok": all(result["ok"] for result in results),
        "timeout": check_timeout,
        "results": results,
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


def _check_storage_path(path: str) -> dict[str, Any]:
    try:
        usage = shutil.disk_usage(path)
        return {
            "kind": "storage",
            "target": path,
            "ok": True,
            "free_bytes": usage.free,
            "total_bytes": usage.total,
            "used_percent": round((usage.used / usage.total) * 100, 2),
            "error": None,
        }
    except OSError as exc:
        return {"kind": "storage", "target": path, "ok": False, "error": str(exc)}


def _check_ping_host(host: str, timeout: float) -> dict[str, Any]:
    timeout_ms = max(1, int(timeout * 1000))
    command = ["ping", "-n", "1", "-w", str(timeout_ms), host] if os.name == "nt" else [
        "ping", "-c", "1", "-W", str(max(1, int(timeout))), host
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            timeout=timeout + 1,
            check=False,
        )
        return {
            "kind": "ping",
            "target": host,
            "ok": completed.returncode == 0,
            "error": None if completed.returncode == 0 else "ping failed",
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"kind": "ping", "target": host, "ok": False, "error": str(exc)}


def _check_dns_host(host: str) -> dict[str, Any]:
    try:
        addresses = sorted({entry[4][0] for entry in socket.getaddrinfo(host, None)})
        return {"kind": "dns", "target": host, "ok": bool(addresses), "addresses": addresses, "error": None}
    except socket.gaierror as exc:
        return {"kind": "dns", "target": host, "ok": False, "addresses": [], "error": str(exc)}
