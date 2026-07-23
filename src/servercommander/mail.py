"""Alpha mail handlers for ServerCommander.

Two layers:

* **Readiness (default).** Every handler reports whether IMAP/SMTP are
  configured without opening any connection. This stays the behavior while
  ``[mail].execution_enabled`` is unset/false.
* **Live IMAP reachability (opt-in).** When ``[mail].execution_enabled = true``
  and IMAP credentials are present, ``sc_mail_list`` performs a real, read-only
  reachability probe (connect + list folders) by **reusing the canonical
  ``mail-connector`` module's** ``ImapConnector`` -- ServerCommander does not
  reimplement an IMAP client. Message-level read/search stay the domain of
  ``mail-connector`` (sync + cache); ServerCommander only offers the server-ops
  reachability check. SMTP sending is intentionally not executed in the alpha.

The ``mail-connector`` package is imported with a locate-and-import-with-
fallback seam (mirroring homebase ``engines.py``): a missing/broken module
degrades to readiness, it never crashes the server.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Any

from servercommander.config import ServerCommanderConfig, resolve_env_value

IMAP_ACTIONS = {"list", "read", "search"}
SMTP_ACTIONS = {"send"}

# Where the canonical mail-connector module lives. Overridable via env so other
# systems / tests can point elsewhere; defaults follow this ecosystem's
# .MODULES/.CONNECTORS layout. Only a convenience default -- never required.
_MAIL_CONNECTOR_CANDIDATES = (
    "~/OneDrive/.TOPICS/.AI/.MODULES/.CONNECTORS/mail-connector",
    "~/.TOPICS/.AI/.MODULES/.CONNECTORS/mail-connector",
)


def _load_imap_connector_class() -> Any | None:
    """Return the canonical ``mail_connector.imap_client.ImapConnector`` class,
    or ``None`` if the module cannot be located/imported.

    Never raises: a missing canonical module degrades to readiness. Tests
    monkeypatch this to inject a fake connector without touching the network.
    """
    candidates: list[str] = []
    env_override = os.environ.get("SERVERCOMMANDER_MAIL_CONNECTOR_PATH")
    if env_override:
        candidates.append(env_override)
    candidates.extend(_MAIL_CONNECTOR_CANDIDATES)

    for candidate in candidates:
        path = Path(candidate).expanduser()
        if not path.exists():
            continue
        search = str(path)
        inserted = search not in sys.path
        if inserted:
            sys.path.insert(0, search)
        try:
            module = importlib.import_module("mail_connector.imap_client")
            connector = getattr(module, "ImapConnector", None)
            if connector is not None:
                return connector
        except Exception:
            # Any import failure must degrade to readiness, not crash.
            continue
        finally:
            if inserted:
                try:
                    sys.path.remove(search)
                except ValueError:
                    pass
    return None


def _execution_enabled(mail: dict[str, Any]) -> bool:
    return bool(mail.get("execution_enabled", False))


def _build_account(mail: dict[str, Any]) -> dict[str, Any]:
    """Assemble the account dict shape ``ImapConnector`` expects.

    ServerCommander already resolves ``$ENV`` references, so the password is
    passed via the connector's ``account['password']`` fallback -- no keyring or
    mail-connector env convention is required.
    """
    host = resolve_env_value(mail.get("imap_host", ""))
    return {
        "id": str(host or "servercommander-imap"),
        "host": host,
        "port": _port(mail, "imap_port", 993),
        "username": resolve_env_value(mail.get("username", "")),
        "password": resolve_env_value(mail.get("password", "")),
        "timeout_seconds": _port(mail, "imap_timeout", 30),
    }


async def sc_mail_list(config: ServerCommanderConfig, folder: str = "INBOX", limit: int = 10) -> dict[str, Any]:
    mail = config.mail
    checks = _mail_checks(mail)
    imap_ready = not [key for key in ("imap_host", "username", "password") if not checks[key]]

    if _execution_enabled(mail) and imap_ready:
        probe = _imap_probe(mail, folder)
        if probe is not None:
            return probe

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


def _imap_probe(mail: dict[str, Any], folder: str) -> dict[str, Any] | None:
    """Live, read-only IMAP reachability check via the canonical mail-connector.

    Returns a result dict, or ``None`` to fall back to readiness when the
    canonical connector cannot be loaded (never reimplements IMAP here).
    """
    connector_cls = _load_imap_connector_class()
    if connector_cls is None:
        return None

    account = _build_account(mail)
    base = {
        "action": "list",
        "probe": "live",
        "execution_enabled": True,
        "reused_module": "mail-connector",
        "folder": folder,
    }
    try:
        with connector_cls(account) as conn:
            folders = list(conn.list_folders())
    except Exception as exc:  # noqa: BLE001 - report, do not crash the server
        return {
            **base,
            "status": "error",
            "reachable": False,
            "error": f"{type(exc).__name__}: {exc}",
            "message": "IMAP reachability probe failed; check host/credentials.",
        }

    return {
        **base,
        "status": "ok",
        "reachable": True,
        "folder_exists": folder in folders,
        "folder_count": len(folders),
        "folders": folders,
        "capabilities": {"imap_reachability": True},
        "message": (
            "Live read-only IMAP reachability via mail-connector. Message-level "
            "read/search remain the mail-connector module's domain."
        ),
    }


def _mail_checks(mail: dict[str, Any]) -> dict[str, bool]:
    return {
        "imap_host": _configured(mail, "imap_host"),
        "smtp_host": _configured(mail, "smtp_host"),
        "username": _configured(mail, "username"),
        "password": _configured(mail, "password"),
    }


def _mail_alpha_response(config: ServerCommanderConfig, action: str, request: dict[str, Any]) -> dict[str, Any]:
    mail = config.mail
    checks = _mail_checks(mail)
    configured = all(checks.values())
    missing = [key for key, ok in checks.items() if not ok]
    requirements = _requirements_for_action(action)
    action_missing = [key for key in requirements if not checks[key]]
    execution_enabled = _execution_enabled(mail)
    delegated = execution_enabled and action in {"read", "search"}
    response = {
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
            "imap_reachability": execution_enabled and action == "list",
        },
        "request": request,
        "message": "IMAP/SMTP execution is not implemented in the alpha server.",
    }
    if delegated:
        # read/search are message-level operations owned by mail-connector; we
        # explicitly delegate rather than build a second mail client.
        response["delegated_to"] = "mail-connector"
        response["message"] = (
            "Message-level read/search are provided by the mail-connector module "
            "(sync + cache). ServerCommander offers IMAP reachability via sc_mail_list."
        )
    return response


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
        "execution_enabled": _execution_enabled(mail),
        "safe_mode": "reachability_only" if _execution_enabled(mail) else "status_only",
    }


def _port(mail: dict[str, Any], key: str, default: int) -> int:
    try:
        return int(resolve_env_value(mail.get(key, default)) or default)
    except (TypeError, ValueError):
        return default
