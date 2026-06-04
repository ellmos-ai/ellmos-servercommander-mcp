"""Alpha mail handlers for ServerCommander.

These handlers expose safe configuration/status checks. Real IMAP/SMTP
operations will be added after credential handling is finalized.
"""

from __future__ import annotations

from typing import Any

from servercommander.config import ServerCommanderConfig, resolve_env_value


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
    username = resolve_env_value(mail.get("username", ""))
    password = resolve_env_value(mail.get("password", ""))
    configured = bool(mail.get("imap_host") and mail.get("smtp_host") and username and password)
    return {
        "status": "not_implemented",
        "action": action,
        "configured": configured,
        "request": request,
        "message": "IMAP/SMTP execution is not implemented in the alpha server.",
    }
