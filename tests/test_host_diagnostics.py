import subprocess

import pytest

from servercommander.config import ServerCommanderConfig
from servercommander.server import ServerCommanderRegistry


@pytest.mark.asyncio
async def test_host_diagnostics_requires_explicit_configuration():
    result = await ServerCommanderRegistry(ServerCommanderConfig()).call_tool("sc_host_diagnostics", {})

    assert result["status"] == "not_configured"
    assert result["ok"] is False
    assert result["results"] == []


@pytest.mark.asyncio
async def test_host_diagnostics_checks_configured_storage_path(tmp_path):
    registry = ServerCommanderRegistry(
        ServerCommanderConfig(health={"storage_paths": [str(tmp_path)]})
    )

    result = await registry.call_tool("sc_host_diagnostics", {})

    assert result["status"] == "ok"
    assert result["results"] == [
        {
            "kind": "storage",
            "target": str(tmp_path),
            "ok": True,
            "free_bytes": result["results"][0]["free_bytes"],
            "total_bytes": result["results"][0]["total_bytes"],
            "used_percent": result["results"][0]["used_percent"],
            "error": None,
        }
    ]


@pytest.mark.asyncio
async def test_host_diagnostics_reports_missing_storage_path(tmp_path):
    missing = tmp_path / "missing"
    result = await ServerCommanderRegistry(
        ServerCommanderConfig(health={"storage_paths": [str(missing)]})
    ).call_tool("sc_host_diagnostics", {})

    assert result["status"] == "degraded"
    assert result["results"][0]["kind"] == "storage"
    assert result["results"][0]["ok"] is False


@pytest.mark.asyncio
async def test_host_diagnostics_probes_explicit_hosts(monkeypatch):
    import servercommander.health as health

    monkeypatch.setattr(
        health.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(args=[], returncode=0),
    )
    monkeypatch.setattr(
        health.socket,
        "getaddrinfo",
        lambda *_args, **_kwargs: [(None, None, None, None, ("127.0.0.1", 0))],
    )

    result = await ServerCommanderRegistry(ServerCommanderConfig()).call_tool(
        "sc_host_diagnostics",
        {"ping_hosts": ["router.test"], "dns_hosts": ["resolver.test"], "timeout": 2},
    )

    assert result["status"] == "ok"
    assert [(item["kind"], item["target"]) for item in result["results"]] == [
        ("ping", "router.test"),
        ("dns", "resolver.test"),
    ]
