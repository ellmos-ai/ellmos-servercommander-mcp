"""Apache/Nginx access-log analysis for ServerCommander."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
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
    persist_report: bool | None = None,
    report_name: str | None = None,
) -> dict[str, Any]:
    """Analyze access logs from inline text or a local file path."""
    text = _load_log_text(log_text, log_path)
    lines = [line for line in text.splitlines() if line.strip()]
    logs_config = config.logs if isinstance(config.logs, dict) else {}
    format_hint = format or logs_config.get("default_format")

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

    result: dict[str, Any] = {
        "status": "ok",
        "total_lines": len(lines),
        "parsed_lines": parsed_lines,
        "unparsed_lines": len(lines) - parsed_lines,
        "format": format_hint,
        "source": _source_metadata(log_text, log_path, len(lines)),
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

    if _should_persist_report(logs_config, persist_report):
        result["report"] = _persist_report(logs_config, result, text, report_name)
    else:
        result["report"] = {"persisted": False}

    return result


def _load_log_text(log_text: str | None, log_path: str | None) -> str:
    if log_text is not None:
        return log_text
    if log_path is not None:
        return Path(log_path).expanduser().read_text(encoding="utf-8", errors="replace")
    raise ValueError("Provide either log_text or log_path")


def _source_metadata(log_text: str | None, log_path: str | None, line_count: int) -> dict[str, Any]:
    if log_text is not None:
        return {"type": "inline_text", "line_count": line_count}
    return {"type": "file", "path": str(Path(str(log_path)).expanduser()), "line_count": line_count}


def _should_persist_report(logs_config: dict[str, Any], persist_report: bool | None) -> bool:
    if persist_report is not None:
        return bool(persist_report)
    return bool(logs_config.get("persist_reports", False))


def _persist_report(
    logs_config: dict[str, Any],
    analysis: dict[str, Any],
    source_text: str,
    report_name: str | None,
) -> dict[str, Any]:
    created_at = datetime.now(timezone.utc)
    digest = hashlib.sha256(source_text.encode("utf-8", errors="replace")).hexdigest()[:12]
    timestamp = created_at.strftime("%Y%m%dT%H%M%S%fZ")
    default_stem = "access-log"
    stem = _safe_report_stem(report_name, default_stem)
    report_id = f"{stem}-{timestamp}-{digest}"
    reports_dir = _reports_dir(logs_config)
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{report_id}.json"

    record = {
        "report_id": report_id,
        "created_at": created_at.isoformat(),
        "analysis": {key: value for key, value in analysis.items() if key != "report"},
    }
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return {
        "persisted": True,
        "id": report_id,
        "path": str(path),
        "format": "json",
        "raw_log_text_included": False,
    }


def _reports_dir(logs_config: dict[str, Any]) -> Path:
    configured = logs_config.get("reports_dir") or "~/.servercommander/log_reports"
    return Path(str(configured)).expanduser()


def _safe_report_stem(report_name: str | None, default_stem: str) -> str:
    raw = Path(str(report_name)).stem if report_name else default_stem
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", raw).strip("._-")
    return (safe[:80] or default_stem)
