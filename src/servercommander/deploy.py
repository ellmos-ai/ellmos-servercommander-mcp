"""Alpha deploy handlers for ServerCommander.

Real SFTP deployment is intentionally not executed in this alpha layer.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from servercommander.config import ServerCommanderConfig

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".venv", "venv"}


async def sc_deploy(
    config: ServerCommanderConfig,
    profile: str | None = None,
    local_path: str | None = None,
    remote_path: str | None = None,
    dry_run: bool = True,
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

    return {
        "status": "dry_run",
        "ready": not missing,
        "missing": missing,
        "plan": plan,
        "manifest": manifest,
        "diagnostics": _deploy_diagnostics(profile_config, plan, manifest),
    }


async def sc_deploy_status(
    config: ServerCommanderConfig,
    profile: str | None = None,
) -> dict[str, Any]:
    """Report configured deploy profile status for the alpha server."""
    profiles = sorted(config.deploy_profiles)
    selected = config.deploy_profile(profile or "") if profile else None
    return {
        "status": "not_recorded",
        "message": "Deployment history storage is not implemented yet.",
        "profiles": profiles,
        "selected_profile": selected,
        "diagnostics": _deploy_diagnostics(selected or {}, selected or {}, None) if profile else None,
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
        "next_step": "Review the dry-run plan and enable a future SFTP executor only after credential handling is finalized.",
    }
