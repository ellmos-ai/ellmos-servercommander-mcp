"""Apache/Nginx access-log analysis for ServerCommander."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from servercommander.config import ServerCommanderConfig


LOG_PATTERN = re.compile(
    r'(?P<host>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<path>\S+)(?:\s+HTTP/[0-9.]+)?"\s+'
    r'(?P<status>\d{3})\s+(?P<size>\S+)'
    r'(?:\s+"(?P<referer>[^"]*)"\s+"(?P<agent>[^"]*)")?'
)

BOT_MARKERS = ("bot", "crawler", "spider", "slurp", "bingpreview")
SUSPICIOUS_MARKERS = ("../", "%2e%2e", "/wp-admin", "/.env", "/phpmyadmin", "/admin", "/login")


async def sc_logs_analyze(
    config: ServerCommanderConfig,
    log_text: str | None = None,
    log_path: str | None = None,
    top_paths: int = 10,
    format: str | None = None,
) -> dict[str, Any]:
    """Analyze access logs from inline text or a local file path."""
    _ = config, format
    text = _load_log_text(log_text, log_path)
    lines = [line for line in text.splitlines() if line.strip()]

    status_counts: Counter[str] = Counter()
    status_classes: Counter[str] = Counter()
    method_counts: Counter[str] = Counter()
    path_counts: Counter[str] = Counter()
    error_path_counts: Counter[str] = Counter()
    agent_counts: Counter[str] = Counter()
    referer_counts: Counter[str] = Counter()
    hosts: set[str] = set()
    total_bytes = 0
    bot_requests = 0
    suspicious_requests = 0
    parsed_lines = 0

    for line in lines:
        match = LOG_PATTERN.search(line)
        if not match:
            continue
        parsed_lines += 1
        hosts.add(match.group("host"))
        status = match.group("status")
        status_counts[status] += 1
        status_classes[f"{status[0]}xx"] += 1
        method_counts[match.group("method")] += 1
        path = match.group("path")
        path_counts[path] += 1
        if int(status) >= 400:
            error_path_counts[path] += 1
        size = match.group("size")
        if size.isdigit():
            total_bytes += int(size)
        referer = match.group("referer") or ""
        if referer and referer != "-":
            referer_counts[referer] += 1
        agent = match.group("agent") or ""
        if agent:
            agent_counts[agent] += 1
        if any(marker in agent.lower() for marker in BOT_MARKERS):
            bot_requests += 1
        if any(marker in path.lower() for marker in SUSPICIOUS_MARKERS):
            suspicious_requests += 1

    error_count = sum(count for status, count in status_counts.items() if int(status) >= 400)
    error_rate = round(error_count / parsed_lines, 4) if parsed_lines else 0.0

    return {
        "status": "ok",
        "total_lines": len(lines),
        "parsed_lines": parsed_lines,
        "unparsed_lines": len(lines) - parsed_lines,
        "unique_hosts": len(hosts),
        "total_bytes": total_bytes,
        "error_rate": error_rate,
        "status_counts": dict(status_counts),
        "status_classes": dict(status_classes),
        "method_counts": dict(method_counts),
        "top_paths": path_counts.most_common(int(top_paths)),
        "top_error_paths": error_path_counts.most_common(int(top_paths)),
        "top_referers": referer_counts.most_common(10),
        "top_agents": agent_counts.most_common(10),
        "bot_requests": bot_requests,
        "suspicious_requests": suspicious_requests,
    }


def _load_log_text(log_text: str | None, log_path: str | None) -> str:
    if log_text is not None:
        return log_text
    if log_path is not None:
        return Path(log_path).expanduser().read_text(encoding="utf-8", errors="replace")
    raise ValueError("Provide either log_text or log_path")
