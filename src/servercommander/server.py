"""ServerCommander MCP Server - Entry Point."""

from __future__ import annotations

import asyncio
from functools import partial
import logging
import sys
from typing import Any

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from servercommander.config import ServerCommanderConfig, load_config
from servercommander.deploy import sc_deploy, sc_deploy_status
from servercommander.health import sc_health_check
from servercommander.i18n import I18n
from servercommander.logs import sc_logs_analyze
from servercommander.mail import sc_mail_list, sc_mail_read, sc_mail_search, sc_mail_send
from servercommander.tooling import ToolDefinition

app = Server("ellmos-servercommander")
logger = logging.getLogger("servercommander")
_registry: "ServerCommanderRegistry | None" = None


class ServerCommanderRegistry:
    """Owns ServerCommander tool definitions and dispatch."""

    def __init__(self, config: ServerCommanderConfig):
        self.config = config
        self._tools = build_tools(config)
        self._handlers = {tool.name: tool.handler for tool in self._tools}
        self.i18n = I18n(config.language)

    def list_tools(self) -> list[types.Tool]:
        return [
            types.Tool(
                name=tool.name,
                description=self.i18n.t(f"tool.{tool.name}", tool.description),
                inputSchema=self.i18n.localize_schema(tool.input_schema),
            )
            for tool in self._tools
        ]

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        handler = self._handlers.get(name)
        if handler is None:
            message = self.i18n.t("error.unknown_tool", "Unknown ServerCommander tool: {name}").format(name=name)
            raise ValueError(message)
        return await handler(**(arguments or {}))


def get_registry() -> ServerCommanderRegistry:
    global _registry
    if _registry is None:
        _registry = ServerCommanderRegistry(load_config())
    return _registry


def object_schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    return schema


def build_tools(config: ServerCommanderConfig) -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="sc_deploy",
            description="Build a safe deployment plan. Alpha only: execution requires dry_run=true.",
            input_schema=object_schema(
                {
                    "profile": {"type": "string"},
                    "local_path": {"type": "string"},
                    "remote_path": {"type": "string"},
                    "dry_run": {"type": "boolean", "default": True},
                }
            ),
            handler=partial(sc_deploy, config),
        ),
        ToolDefinition(
            name="sc_deploy_status",
            description="Show configured deployment profiles and alpha deployment-history status.",
            input_schema=object_schema({"profile": {"type": "string"}}),
            handler=partial(sc_deploy_status, config),
        ),
        ToolDefinition(
            name="sc_mail_list",
            description="Alpha mail status endpoint for listing an IMAP folder.",
            input_schema=object_schema(
                {
                    "folder": {"type": "string", "default": "INBOX"},
                    "limit": {"type": "integer", "default": 10},
                }
            ),
            handler=partial(sc_mail_list, config),
        ),
        ToolDefinition(
            name="sc_mail_read",
            description="Alpha mail status endpoint for reading a message.",
            input_schema=object_schema({"message_id": {"type": "string"}}),
            handler=partial(sc_mail_read, config),
        ),
        ToolDefinition(
            name="sc_mail_send",
            description="Alpha mail status endpoint for sending mail; does not send yet.",
            input_schema=object_schema(
                {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                ["to", "subject", "body"],
            ),
            handler=partial(sc_mail_send, config),
        ),
        ToolDefinition(
            name="sc_mail_search",
            description="Alpha mail status endpoint for searching mail.",
            input_schema=object_schema(
                {"query": {"type": "string"}, "limit": {"type": "integer", "default": 10}},
                ["query"],
            ),
            handler=partial(sc_mail_search, config),
        ),
        ToolDefinition(
            name="sc_logs_analyze",
            description="Analyze Apache/Nginx access logs from inline text or a local file path.",
            input_schema=object_schema(
                {
                    "log_text": {"type": "string"},
                    "log_path": {"type": "string"},
                    "top_paths": {"type": "integer", "default": 10},
                    "format": {"type": "string", "enum": ["apache", "nginx"]},
                    "persist_report": {"type": "boolean", "default": False},
                    "report_name": {"type": "string"},
                }
            ),
            handler=partial(sc_logs_analyze, config),
        ),
        ToolDefinition(
            name="sc_health_check",
            description="Check HTTP endpoints and return status codes plus latency.",
            input_schema=object_schema(
                {
                    "endpoints": {"type": "array", "items": {"type": "string"}},
                    "timeout": {"type": "number", "default": 5},
                }
            ),
            handler=partial(sc_health_check, config),
        ),
    ]


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return get_registry().list_tools()


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return await get_registry().call_tool(name, arguments)


async def serve() -> None:
    logger.info("ServerCommander starting...")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    asyncio.run(serve())


if __name__ == "__main__":
    main()
