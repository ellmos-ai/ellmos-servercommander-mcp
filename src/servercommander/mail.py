"""Alpha mail handlers for ServerCommander.

These handlers expose safe configuration/status checks. Real IMAP/SMTP
operations will be added after credential handling is finalized.
"""

from __future__ import annotations

from typing import Any

from servercommander.config import ServerCommanderConfig, resolve_env_value

IMAP_ACTIONS = {"list", "read", "search"}
SMTP_ACTIONS = {"send"}


async def sc_mail_list(config: ServerCommanderConfig, folder: str = "INBOX", limit: int = 10) -> dict[str, Any]:
    return _mail_alpha_response(config, "list", {"folder": folder, "limit": limit})


async def sc_mail_read(config: ServerCommanderConfig, message_id: str | None = None) -> dict[str, Any]:
    return _mail_alpha_response(config, "read", {"message_id": message_id})


async def sc_mail_send(
    config: ServerCommanderConfig,
    to: str,
    subject: str,
    body: str,
) -> dict[str, Any]:
    return _mail_alpha_response(
        config,
        "send",
        {"to": to, "subject": subject, "body_preview": body[:80]},
    )


async def sc_mail_search(config: ServerCommanderConfig, query: str, limit: int = 10) -> dict[str, Any]:
    return _mail_alpha_response(config, "search", {"query": query, "limit": limit})


def _mail_alpha_response(config: ServerCommanderConfig, action: str, request: dict[str, Any]) -> dict[str, Any]:
    mail = config.mail
    checks = {
        "imap_host": _configured(mail, "imap_host"),
        "smtp_host": _configured(mail, "smtp_host"),
        "username": _configured(mail, "username"),
        "password": _configured(mail, "password"),
    }
    configured = all(checks.values())
    missing = [key for key, ok in checks.items() if not ok]
    requirements = _requirements_for_action(action)
    action_missing = [key for key in requirements if not checks[key]]
    return {
        "status": "not_implemented",
        "action": action,
        "configured": configured,
        "missing": missing,
        "checks": checks,
        "action_ready": not action_missing,
        "action_missing": action_missing,
        "diagnostics": _mail_diagnostics(mail, checks, action, requirements, action_missing),
        "capabilities": {
            "list": False,
            "read": False,
            "send": False,
            "search": False,
            "config_diagnostics": True,
        },
        "request": request,
        "message": "IMAP/SMTP execution is not implemented in the alpha server.",
    }


def _configured(mail: dict[str, Any], key: str) -> bool:
    return bool(resolve_env_value(mail.get(key, "")))


def _requirements_for_action(action: str) -> tuple[str, ...]:
    if action in SMTP_ACTIONS:
        return ("smtp_host", "username", "password")
    if action in IMAP_ACTIONS:
        return ("imap_host", "username", "password")
    return ("imap_host", "smtp_host", "username", "password")


def _mail_diagnostics(
    mail: dict[str, Any],
    checks: dict[str, bool],
    action: str,
    requirements: tuple[str, ...],
    action_missing: list[str],
) -> dict[str, Any]:
    imap_missing = [key for key in ("imap_host", "username", "password") if not checks[key]]
    smtp_missing = [key for key in ("smtp_host", "username", "password") if not checks[key]]
    return {
        "action": action,
        "action_requirements": list(requirements),
        "action_missing": action_missing,
        "imap": {
            "ready": not imap_missing,
            "missing": imap_missing,
            "host_configured": checks["imap_host"],
            "port": _port(mail, "imap_port", 993),
            "cache_db_configured": bool(mail.get("cache_db")),
        },
        "smtp": {
            "ready": not smtp_missing,
            "missing": smtp_missing,
            "host_configured": checks["smtp_host"],
            "port": _port(mail, "smtp_port", 587),
        },
        "execution_enabled": False,
        "safe_mode": "status_only",
    }


def _port(mail: dict[str, Any], key: str, default: int) -> int:
    try:
        return int(resolve_env_value(mail.get(key, default)) or default)
    except (TypeError, ValueError):
        return default
