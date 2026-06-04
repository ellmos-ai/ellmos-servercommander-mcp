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


@pytest.mark.asyncio
async def test_deploy_dry_run_reports_missing_fields():
    registry = ServerCommanderRegistry(ServerCommanderConfig())

    result = await registry.call_tool("sc_deploy", {"profile": "missing"})

    assert result["status"] == "dry_run"
    assert result["ready"] is False
    assert "host" in result["missing"]


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
    assert result["manifest"]["file_count"] == 2
    assert {entry["path"] for entry in result["manifest"]["files"]} == {"index.html", "style.css"}


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
