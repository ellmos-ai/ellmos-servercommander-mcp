"""Alpha deploy handlers for ServerCommander.

Real SFTP deployment is intentionally not executed in this alpha layer.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from servercommander.config import ServerCommanderConfig

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".venv", "venv"}


async def sc_deploy(
    config: ServerCommanderConfig,
    profile: str | None = None,
    local_path: str | None = None,
    remote_path: str | None = None,
    dry_run: bool = True,
    record_history: bool | None = None,
) -> dict[str, Any]:
    """Return a deploy plan. Non-dry-run execution is not implemented yet."""
    if not dry_run:
        raise ValueError("sc_deploy execution is not implemented in the alpha server; use dry_run=true")

    profile_config = config.deploy_profile(profile or "") if profile else {}
    plan = {
        "profile": profile,
        "host": profile_config.get("host"),
        "user": profile_config.get("user"),
        "local_path": local_path or profile_config.get("local_path"),
        "remote_path": remote_path or profile_config.get("remote_path"),
        "protocol": profile_config.get("protocol", "sftp"),
        "port": profile_config.get("port", 22),
    }
    missing = [key for key in ("host", "user", "local_path", "remote_path") if not plan.get(key)]
    manifest = _build_manifest(plan["local_path"]) if plan.get("local_path") else None
    diagnostics = _deploy_diagnostics(profile_config, plan, manifest)
    readiness_problems = _readiness_problems(missing, diagnostics)
    ready = not readiness_problems
    history = (
        _record_deploy_plan(config, profile, plan, manifest, diagnostics, ready)
        if _should_record_history(config, record_history)
        else {"persisted": False}
    )

    return {
        "status": "dry_run",
        "ready": ready,
        "missing": missing,
        "readiness_problems": readiness_problems,
        "plan": plan,
        "manifest": manifest,
        "diagnostics": diagnostics,
        "history": history,
    }


async def sc_deploy_status(
    config: ServerCommanderConfig,
    profile: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    """Report configured deploy profile status for the alpha server."""
    profiles = sorted(config.deploy_profiles)
    selected = config.deploy_profile(profile or "") if profile else None
    history = _load_deploy_history(config, profile=profile, limit=limit)
    return {
        "status": "ok" if history else "not_recorded",
        "message": "Deployment execution is still disabled; history contains dry-run plans only.",
        "profiles": profiles,
        "selected_profile": selected,
        "diagnostics": _deploy_diagnostics(selected or {}, selected or {}, None) if profile else None,
        "history": history,
        "history_count": len(history),
        "history_db": str(_history_db_path(config)),
    }


def _build_manifest(local_path: str) -> dict[str, Any]:
    root = Path(local_path).expanduser()
    if not root.exists():
        return {"status": "missing_local_path", "path": str(root), "files": [], "total_bytes": 0}
    if root.is_file():
        return {"status": "ok", "path": str(root), "files": [_file_entry(root, root.parent)], "total_bytes": root.stat().st_size}

    files = []
    total_bytes = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        entry = _file_entry(path, root)
        files.append(entry)
        total_bytes += entry["size"]

    return {
        "status": "ok",
        "path": str(root),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "files": files,
    }


def _file_entry(path: Path, root: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "path": path.relative_to(root).as_posix(),
        "size": path.stat().st_size,
        "sha256": digest.hexdigest(),
    }


def _deploy_diagnostics(profile_config: dict[str, Any], plan: dict[str, Any], manifest: dict[str, Any] | None) -> dict[str, Any]:
    protocol = str(plan.get("protocol") or "sftp").lower()
    auth_methods = []
    if profile_config.get("key_path"):
        auth_methods.append("key_path")
    if profile_config.get("password"):
        auth_methods.append("password")
    if not auth_methods:
        auth_methods.append("agent_or_prompt")
    local_status = manifest.get("status") if manifest else "not_checked"
    return {
        "protocol_supported": protocol == "sftp",
        "protocol": protocol,
        "port": int(plan.get("port") or 22),
        "auth_methods_configured": auth_methods,
        "local_status": local_status,
        "execution_enabled": False,
        "history_supported": True,
        "next_step": "Review the dry-run plan, record history if useful, and enable a future SFTP executor only after credential handling is finalized.",
    }


def _readiness_problems(missing: list[str], diagnostics: dict[str, Any]) -> list[str]:
    problems = list(missing)
    if "local_path" not in missing and diagnostics.get("local_status") != "ok":
        problems.append("local_path_exists")
    if diagnostics.get("protocol_supported") is not True:
        problems.append("unsupported_protocol")
    return problems


def _should_record_history(config: ServerCommanderConfig, record_history: bool | None) -> bool:
    if record_history is not None:
        return bool(record_history)
    deploy_config = config.deploy if isinstance(config.deploy, dict) else {}
    return bool(deploy_config.get("persist_history", False))


def _record_deploy_plan(
    config: ServerCommanderConfig,
    profile: str | None,
    plan: dict[str, Any],
    manifest: dict[str, Any] | None,
    diagnostics: dict[str, Any],
    ready: bool,
) -> dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest_json = json.dumps(manifest or {}, ensure_ascii=False, sort_keys=True)
    manifest_hash = hashlib.sha256(manifest_json.encode("utf-8")).hexdigest()
    path = _history_db_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path, timeout=30.0)
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA busy_timeout=30000")
        _ensure_history_table(connection)
        cursor = connection.execute(
            """
            INSERT INTO deploy_history (
                created_at, profile, ready, local_path, remote_path, host, user,
                manifest_hash, manifest_json, plan_json, diagnostics_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                profile,
                1 if ready else 0,
                plan.get("local_path"),
                plan.get("remote_path"),
                plan.get("host"),
                plan.get("user"),
                manifest_hash,
                manifest_json,
                json.dumps(plan, ensure_ascii=False, sort_keys=True),
                json.dumps(diagnostics, ensure_ascii=False, sort_keys=True),
            ),
        )
        history_id = int(cursor.lastrowid)
        connection.commit()
    finally:
        connection.close()

    return {
        "persisted": True,
        "id": history_id,
        "created_at": created_at,
        "path": str(path),
        "manifest_hash": manifest_hash,
    }


def _load_deploy_history(
    config: ServerCommanderConfig,
    profile: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    path = _history_db_path(config)
    if not path.exists():
        return []
    sql = """
        SELECT id, created_at, profile, ready, local_path, remote_path, host, user, manifest_hash
        FROM deploy_history
    """
    params: list[Any] = []
    if profile:
        sql += " WHERE profile = ?"
        params.append(profile)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(max(1, int(limit)))

    connection = sqlite3.connect(path, timeout=30.0)
    try:
        connection.row_factory = sqlite3.Row
        _ensure_history_table(connection)
        rows = connection.execute(sql, params).fetchall()
    finally:
        connection.close()

    return [{**dict(row), "ready": bool(row["ready"])} for row in rows]


def _ensure_history_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS deploy_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            profile TEXT,
            ready INTEGER NOT NULL,
            local_path TEXT,
            remote_path TEXT,
            host TEXT,
            user TEXT,
            manifest_hash TEXT NOT NULL,
            manifest_json TEXT NOT NULL,
            plan_json TEXT NOT NULL,
            diagnostics_json TEXT NOT NULL
        )
        """
    )


def _history_db_path(config: ServerCommanderConfig) -> Path:
    deploy_config = config.deploy if isinstance(config.deploy, dict) else {}
    configured = deploy_config.get("history_db") or "~/.servercommander/deploy_history.db"
    return Path(str(configured)).expanduser()
