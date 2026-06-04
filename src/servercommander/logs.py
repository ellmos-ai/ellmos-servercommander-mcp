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
    agent_counts: Counter[str] = Counter()
    bot_requests = 0
    parsed_lines = 0

    for line in lines:
        match = LOG_PATTERN.search(line)
        if not match:
            continue
        parsed_lines += 1
        status = match.group("status")
        status_counts[status] += 1
        status_classes[f"{status[0]}xx"] += 1
        method_counts[match.group("method")] += 1
        path_counts[match.group("path")] += 1
        agent = match.group("agent") or ""
        if agent:
            agent_counts[agent] += 1
        if any(marker in agent.lower() for marker in BOT_MARKERS):
            bot_requests += 1

    return {
        "status": "ok",
        "total_lines": len(lines),
        "parsed_lines": parsed_lines,
        "unparsed_lines": len(lines) - parsed_lines,
        "status_counts": dict(status_counts),
        "status_classes": dict(status_classes),
        "method_counts": dict(method_counts),
        "top_paths": path_counts.most_common(int(top_paths)),
        "top_agents": agent_counts.most_common(10),
        "bot_requests": bot_requests,
    }


def _load_log_text(log_text: str | None, log_path: str | None) -> str:
    if log_text is not None:
        return log_text
    if log_path is not None:
        return Path(log_path).expanduser().read_text(encoding="utf-8", errors="replace")
    raise ValueError("Provide either log_text or log_path")
