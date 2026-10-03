"""Combined-log escaped header values must not hide traffic statistics."""

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
