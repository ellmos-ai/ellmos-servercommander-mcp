"""Combined-log escaped header values must not hide traffic statistics."""

import json
from pathlib import Path

import pytest

from servercommander.config import ServerCommanderConfig
from servercommander.server import ServerCommanderRegistry


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("referer", "agent"),
    [
        (r'https://ref.example/\"quoted\"', "ExampleBot/1.0"),
        ("https://ref.example/", r'Client \"quoted\" ExampleBot/1.0'),
        (r"https://ref.example/\\", r"Client \\ ExampleBot/1.0"),
        (r"https://ref.example/\x22quoted\x22", r"Client\tExampleBot/1.0"),
    ],
)
async def test_combined_log_preserves_escaped_headers_and_bot_count(referer, agent):
    registry = ServerCommanderRegistry(ServerCommanderConfig())
    log_text = (
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        f'"GET /index.html HTTP/1.1" 200 123 "{referer}" "{agent}"'
    )

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text})

    assert result["parsed_lines"] == 1
    assert result["unparsed_lines"] == 0
    assert result["top_referers"] == [(referer, 1)]
    assert result["top_agents"] == [(agent, 1)]
    assert result["bot_requests"] == 1
    assert result["status_counts"] == {"200": 1}
    assert result["total_bytes"] == 123


@pytest.mark.asyncio
async def test_common_log_without_headers_still_counts_requests():
    registry = ServerCommanderRegistry(ServerCommanderConfig())
    log_text = '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] "GET /index.html HTTP/1.1" 304 -'

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text})

    assert result["parsed_lines"] == 1
    assert result["status_counts"] == {"304": 1}
    assert result["top_paths"] == [("/index.html", 1)]
    assert result["total_bytes"] == 0
    assert result["top_referers"] == []
    assert result["top_agents"] == []
    assert result["bot_requests"] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("persist_report", [False, True])
async def test_url_secrets_are_removed_before_aggregation_and_persistence(tmp_path, persist_report):
    registry = ServerCommanderRegistry(ServerCommanderConfig(logs={"reports_dir": str(tmp_path)}))
    log_text = "\n".join(
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        f'"GET /checkout?token={token}#fragment-secret HTTP/1.1" 403 12 '
        f'"https://user-secret:password-secret@ref.example/cart?session={token}#ref-secret" "ExampleBot/1.0"'
        for token in ("first-token-secret", "second-token-secret")
    )

    result = await registry.call_tool(
        "sc_logs_analyze", {"log_text": log_text, "persist_report": persist_report}
    )

    assert result["top_paths"] == [("/checkout", 2)]
    assert result["top_error_paths"] == [("/checkout", 2)]
    assert result["top_referers"] == [("https://ref.example/cart", 2)]
    assert result["parsed_lines"] == 2
    assert result["status_counts"] == {"403": 2}
    assert result["total_bytes"] == 24
    assert result["bot_requests"] == 2
    serialized = json.dumps(result)
    if persist_report:
        saved_text = Path(result["report"]["path"]).read_text(encoding="utf-8")
        saved = json.loads(saved_text)
        assert saved["analysis"]["top_paths"] == [["/checkout", 2]]
        serialized += saved_text
    else:
        assert not list(tmp_path.iterdir())
    for secret in (
        "first-token-secret", "second-token-secret", "fragment-secret", "user-secret",
        "password-secret", "ref-secret",
    ):
        assert secret not in serialized


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("target", "referer", "safe_target", "safe_referer"),
    [
        ("https://user:secret@site.example:8443/api?key=hidden", "//user:secret@ref.example:443/a?key=hidden",
         "https://site.example:8443/api", "//ref.example:443/a"),
        ("/api#fragment?query", "https://ref.example/a#fragment?query", "/api", "https://ref.example/a"),
        ("/api%3Fkeep%23keep?token=hidden", "https://ref.example/a%3Fkeep%23keep?token=hidden",
         "/api%3Fkeep%23keep", "https://ref.example/a%3Fkeep%23keep"),
        ("/users/a@b", "https://ref.example/users/a@b", "/users/a@b", "https://ref.example/users/a@b"),
    ],
)
async def test_url_redaction_preserves_path_and_authority_shape(target, referer, safe_target, safe_referer):
    registry = ServerCommanderRegistry(ServerCommanderConfig())
    log_text = (
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        f'"GET {target} HTTP/1.1" 200 12 "{referer}" "Client"'
    )

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text})

    assert result["top_paths"] == [(safe_target, 1)]
    assert result["top_referers"] == [(safe_referer, 1)]


@pytest.mark.asyncio
async def test_query_only_scanner_markers_still_count_without_exposing_query():
    registry = ServerCommanderRegistry(ServerCommanderConfig())
    log_text = (
        '127.0.0.1 - - [04/Jun/2026:20:00:00 +0200] '
        '"GET /download?file=../../.env&token=hidden HTTP/1.1" 400 12'
    )

    result = await registry.call_tool("sc_logs_analyze", {"log_text": log_text})

    assert result["suspicious_requests"] == 1
    assert result["top_paths"] == [("/download", 1)]
    assert result["top_error_paths"] == [("/download", 1)]
