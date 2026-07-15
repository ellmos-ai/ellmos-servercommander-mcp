import json
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import pytest

from servercommander.config import ServerCommanderConfig
from servercommander.i18n import normalize_locale
from servercommander.server import ServerCommanderRegistry


@pytest.mark.asyncio
async def test_registry_lists_expected_tools():
    registry = ServerCommanderRegistry(ServerCommanderConfig())

    tool_names = {tool.name for tool in registry.list_tools()}

    assert tool_names == {
        "sc_deploy",
        "sc_deploy_status",
        "sc_mail_list",
        "sc_mail_read",
        "sc_mail_send",
        "sc_mail_search",
        "sc_logs_analyze",
        "sc_health_check",
    }


def test_tool_descriptions_are_localized():
    registry = ServerCommanderRegistry(ServerCommanderConfig(language="de"))

    tools = {tool.name: tool for tool in registry.list_tools()}

    assert tools["sc_health_check"].description.startswith("Prüft HTTP-Endpunkte")


def test_tool_input_schema_descriptions_are_localized():
    registry = ServerCommanderRegistry(ServerCommanderConfig(language="de"))

    tools = {tool.name: tool for tool in registry.list_tools()}
    properties = tools["sc_health_check"].inputSchema["properties"]

    assert properties["endpoints"]["description"] == "Zu prüfende HTTP-Endpunkt-URLs."
    assert properties["timeout"]["description"] == "Request-Timeout in Sekunden."


def test_tool_input_schema_descriptions_gain_english_defaults():
    registry = ServerCommanderRegistry(ServerCommanderConfig())

    tools = {tool.name: tool for tool in registry.list_tools()}
    properties = tools["sc_logs_analyze"].inputSchema["properties"]

    assert properties["log_text"]["description"] == "Inline access-log text."
    assert properties["persist_report"]["description"] == "Persist the analysis summary as a JSON report."


def test_locale_normalization_and_fallback():
    assert normalize_locale("de-DE") == "de"
    assert normalize_locale("ja_JP") == "ja"
    assert normalize_locale("klingon") == "en"


@pytest.mark.asyncio
async def test_logs_analyze_inline_text():
    registry = ServerCommanderRegistry(ServerCommanderConfig())
    log_text = (
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        '"GET /index.html HTTP/1.1" 200 123 "-" "Mozilla/5.0"\n'
        '127.0.0.1 - - [04/Jun/2026:20:00:01 +0200] '
        '"GET /robots.txt HTTP/1.1" 404 12 "-" "ExampleBot/1.0"\n'
    )

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text})

    assert result["parsed_lines"] == 2
    assert result["status_counts"] == {"200": 1, "404": 1}
    assert result["bot_requests"] == 1
    assert result["unique_hosts"] == 1
    assert result["error_rate"] == 0.5
    assert result["top_error_paths"] == [("/robots.txt", 1)]


@pytest.mark.asyncio
async def test_logs_analyze_reports_referers_bytes_and_suspicious_paths():
    registry = ServerCommanderRegistry(ServerCommanderConfig())
    log_text = (
        '10.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        '"GET /.env HTTP/1.1" 404 5 "https://ref.example/" "curl/8"\n'
        '10.0.0.2 - - [04/Jun/2026:20:00:01 +0200] '
        '"POST /login HTTP/1.1" 403 7 "-" "Mozilla/5.0"\n'
    )

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text})

    assert result["unique_hosts"] == 2
    assert result["total_bytes"] == 12
    assert result["suspicious_requests"] == 2
    assert result["top_referers"] == [("https://ref.example/", 1)]


@pytest.mark.asyncio
async def test_logs_analyze_can_persist_json_report(tmp_path):
    registry = ServerCommanderRegistry(ServerCommanderConfig(logs={"reports_dir": str(tmp_path)}))
    log_text = (
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        '"GET /index.html HTTP/1.1" 200 123 "-" "Mozilla/5.0"\n'
    )

    result = await registry.call_tool(
        "sc_logs_analyze",
        {"log_text": log_text, "persist_report": True, "report_name": "../daily report"},
    )

    report = result["report"]
    assert report["persisted"] is True
    assert report["raw_log_text_included"] is False
    assert report["id"].startswith("daily-report-")
    assert ".." not in report["id"]

    report_path = tmp_path / f"{report['id']}.json"
    assert report["path"] == str(report_path)
    saved = json.loads(report_path.read_text(encoding="utf-8"))
    assert saved["analysis"]["parsed_lines"] == 1
    assert saved["analysis"]["source"]["type"] == "inline_text"
    assert log_text not in report_path.read_text(encoding="utf-8")


@pytest.mark.asyncio
async def test_logs_analyze_config_persistence_can_be_overridden(tmp_path):
    registry = ServerCommanderRegistry(
        ServerCommanderConfig(logs={"reports_dir": str(tmp_path), "persist_reports": True})
    )
    log_text = (
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        '"GET /index.html HTTP/1.1" 200 123 "-" "Mozilla/5.0"\n'
    )

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text, "persist_report": False})

    assert result["report"] == {"persisted": False}
    assert list(tmp_path.glob("*.json")) == []


@pytest.mark.asyncio
async def test_registry_rejects_unknown_tool_with_localized_error():
    registry = ServerCommanderRegistry(ServerCommanderConfig(language="de"))

    with pytest.raises(ValueError, match="Unbekanntes ServerCommander-Tool"):
        await registry.call_tool("sc_missing", {})


@pytest.mark.asyncio
async def test_deploy_dry_run_reports_missing_fields():
    registry = ServerCommanderRegistry(ServerCommanderConfig())

    result = await registry.call_tool("sc_deploy", {"profile": "missing"})

    assert result["status"] == "dry_run"
    assert result["ready"] is False
    assert "host" in result["missing"]
    assert result["diagnostics"]["execution_enabled"] is False


@pytest.mark.asyncio
async def test_deploy_dry_run_builds_local_manifest(tmp_path):
    local_path = tmp_path / "site"
    local_path.mkdir()
    (local_path / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
    (local_path / "style.css").write_text("body { color: black; }", encoding="utf-8")
    config = ServerCommanderConfig(
        deploy_profiles={
            "site": {
                "host": "sftp.example.com",
                "user": "deploy",
                "local_path": str(local_path),
                "remote_path": "/var/www/site",
            }
        }
    )
    registry = ServerCommanderRegistry(config)

    result = await registry.call_tool("sc_deploy", {"profile": "site"})

    assert result["ready"] is True
    assert result["history"] == {"persisted": False}
    assert result["manifest"]["file_count"] == 2
    assert result["diagnostics"]["protocol_supported"] is True
    assert result["diagnostics"]["history_supported"] is True
    assert {entry["path"] for entry in result["manifest"]["files"]} == {"index.html", "style.css"}
    assert result["manifest"]["skipped_symlinks"] == 0


@pytest.mark.asyncio
async def test_deploy_manifest_skips_nested_symlinks_outside_release_root(tmp_path):
    local_path = tmp_path / "site"
    local_path.mkdir()
    (local_path / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
    outside_file = tmp_path / "outside-secret.txt"
    outside_file.write_text("not part of this release", encoding="utf-8")
    nested_link = local_path / "outside-link.txt"
    try:
        nested_link.symlink_to(outside_file)
    except OSError as exc:
        pytest.skip(f"File symlinks are unavailable in this environment: {exc}")

    config = ServerCommanderConfig(
        deploy_profiles={
            "site": {
                "host": "sftp.example.com",
                "user": "deploy",
                "local_path": str(local_path),
                "remote_path": "/var/www/site",
            }
        }
    )
    result = await ServerCommanderRegistry(config).call_tool("sc_deploy", {"profile": "site"})

    assert result["ready"] is True
    assert {entry["path"] for entry in result["manifest"]["files"]} == {"index.html"}
    assert result["manifest"]["skipped_symlinks"] == 1


@pytest.mark.asyncio
async def test_deploy_dry_run_rejects_missing_local_path_readiness(tmp_path):
    missing_path = tmp_path / "missing-site"
    config = ServerCommanderConfig(
        deploy_profiles={
            "site": {
                "host": "sftp.example.com",
                "user": "deploy",
                "local_path": str(missing_path),
                "remote_path": "/var/www/site",
            }
        }
    )
    registry = ServerCommanderRegistry(config)

    result = await registry.call_tool("sc_deploy", {"profile": "site"})

    assert result["ready"] is False
    assert result["missing"] == []
    assert result["manifest"]["status"] == "missing_local_path"
    assert result["diagnostics"]["local_status"] == "missing_local_path"
    assert result["readiness_problems"] == ["local_path_exists"]


@pytest.mark.asyncio
async def test_deploy_dry_run_rejects_unsupported_protocol_readiness(tmp_path):
    local_path = tmp_path / "site"
    local_path.mkdir()
    (local_path / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
    config = ServerCommanderConfig(
        deploy_profiles={
            "site": {
                "host": "ftp.example.com",
                "user": "deploy",
                "local_path": str(local_path),
                "remote_path": "/var/www/site",
                "protocol": "ftp",
            }
        }
    )
    registry = ServerCommanderRegistry(config)

    result = await registry.call_tool("sc_deploy", {"profile": "site"})

    assert result["ready"] is False
    assert result["missing"] == []
    assert result["diagnostics"]["protocol_supported"] is False
    assert result["readiness_problems"] == ["unsupported_protocol"]


@pytest.mark.asyncio
async def test_deploy_can_record_and_report_local_history(tmp_path):
    local_path = tmp_path / "site"
    local_path.mkdir()
    (local_path / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
    history_db = tmp_path / "deploy-history.db"
    config = ServerCommanderConfig(
        deploy={"history_db": str(history_db)},
        deploy_profiles={
            "site": {
                "host": "sftp.example.com",
                "user": "deploy",
                "local_path": str(local_path),
                "remote_path": "/var/www/site",
            }
        },
    )
    registry = ServerCommanderRegistry(config)

    deployed = await registry.call_tool("sc_deploy", {"profile": "site", "record_history": True})
    status = await registry.call_tool("sc_deploy_status", {"profile": "site"})

    assert deployed["history"]["persisted"] is True
    assert deployed["history"]["path"] == str(history_db)
    assert history_db.exists()
    assert status["status"] == "ok"
    assert status["history_count"] == 1
    assert status["history"][0]["profile"] == "site"
    assert status["history"][0]["ready"] is True
    assert status["history"][0]["manifest_hash"] == deployed["history"]["manifest_hash"]


@pytest.mark.asyncio
async def test_deploy_history_can_be_enabled_by_config(tmp_path):
    local_path = tmp_path / "site"
    local_path.mkdir()
    (local_path / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
    history_db = tmp_path / "deploy-history.db"
    config = ServerCommanderConfig(
        deploy={"history_db": str(history_db), "persist_history": True},
        deploy_profiles={
            "site": {
                "host": "sftp.example.com",
                "user": "deploy",
                "local_path": str(local_path),
                "remote_path": "/var/www/site",
            }
        },
    )
    registry = ServerCommanderRegistry(config)

    deployed = await registry.call_tool("sc_deploy", {"profile": "site"})

    assert deployed["history"]["persisted"] is True


@pytest.mark.asyncio
async def test_deploy_history_releases_sqlite_files_after_write_and_read(tmp_path):
    scratch = tmp_path / "history-cleanup"
    local_path = scratch / "site"
    local_path.mkdir(parents=True)
    (local_path / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
    history_db = scratch / "deploy-history.db"
    config = ServerCommanderConfig(
        deploy={"history_db": str(history_db)},
        deploy_profiles={
            "site": {
                "host": "sftp.example.com",
                "user": "deploy",
                "local_path": str(local_path),
                "remote_path": "/var/www/site",
            }
        },
    )
    registry = ServerCommanderRegistry(config)

    await registry.call_tool("sc_deploy", {"profile": "site", "record_history": True})
    await registry.call_tool("sc_deploy_status", {"profile": "site"})

    shutil.rmtree(scratch)
    assert not scratch.exists()


@pytest.mark.asyncio
async def test_mail_handlers_report_configuration_gaps_without_executing():
    registry = ServerCommanderRegistry(ServerCommanderConfig(mail={"imap_host": "imap.example.com"}))

    result = await registry.call_tool("sc_mail_list", {"folder": "INBOX"})

    assert result["status"] == "not_implemented"
    assert result["configured"] is False
    assert result["checks"]["imap_host"] is True
    assert "smtp_host" in result["missing"]
    assert result["diagnostics"]["imap"]["ready"] is False
    assert result["diagnostics"]["smtp"]["ready"] is False
    assert result["diagnostics"]["execution_enabled"] is False
    assert result["capabilities"]["config_diagnostics"] is True


@pytest.mark.asyncio
async def test_mail_list_reports_imap_ready_without_smtp(monkeypatch):
    monkeypatch.setenv("MAIL_USER", "reader@example.com")
    monkeypatch.setenv("MAIL_PASSWORD", "secret")
    registry = ServerCommanderRegistry(
        ServerCommanderConfig(
            mail={
                "imap_host": "imap.example.com",
                "imap_port": 993,
                "username": "$MAIL_USER",
                "password": "$MAIL_PASSWORD",
            }
        )
    )

    result = await registry.call_tool("sc_mail_list", {"folder": "INBOX"})

    assert result["configured"] is False
    assert result["action_ready"] is True
    assert result["action_missing"] == []
    assert result["missing"] == ["smtp_host"]
    assert result["diagnostics"]["imap"]["ready"] is True
    assert result["diagnostics"]["imap"]["port"] == 993
    assert result["diagnostics"]["smtp"]["ready"] is False


@pytest.mark.asyncio
async def test_mail_send_requires_smtp_readiness(monkeypatch):
    monkeypatch.setenv("MAIL_USER", "sender@example.com")
    monkeypatch.setenv("MAIL_PASSWORD", "secret")
    registry = ServerCommanderRegistry(
        ServerCommanderConfig(
            mail={
                "imap_host": "imap.example.com",
                "username": "$MAIL_USER",
                "password": "$MAIL_PASSWORD",
            }
        )
    )

    result = await registry.call_tool(
        "sc_mail_send",
        {"to": "a@example.com", "subject": "Hi", "body": "Short message"},
    )

    assert result["action_ready"] is False
    assert result["action_missing"] == ["smtp_host"]
    assert result["diagnostics"]["smtp"]["missing"] == ["smtp_host"]
    assert result["diagnostics"]["smtp"]["port"] == 587
    assert result["diagnostics"]["execution_enabled"] is False


@pytest.mark.asyncio
async def test_health_check_local_http_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, format, *args):
            return

    httpd = HTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    try:
        endpoint = f"http://127.0.0.1:{httpd.server_port}/health"
        registry = ServerCommanderRegistry(ServerCommanderConfig())

        result = await registry.call_tool("sc_health_check", {"endpoints": [endpoint], "timeout": 2})

        assert result["ok"] is True
        assert result["results"][0]["status_code"] == 200
    finally:
        httpd.shutdown()
        thread.join(timeout=2)


@pytest.mark.asyncio
async def test_health_check_reports_invalid_endpoint_without_aborting_batch():
    registry = ServerCommanderRegistry(ServerCommanderConfig())

    result = await registry.call_tool("sc_health_check", {"endpoints": ["not-a-url"]})

    assert result["status"] == "degraded"
    assert result["ok"] is False
    assert result["results"][0]["endpoint"] == "not-a-url"
    assert result["results"][0]["ok"] is False
    assert result["results"][0]["status_code"] is None
    assert result["results"][0]["latency_ms"] >= 0
    assert result["results"][0]["error"] == "unknown url type: 'not-a-url'"
