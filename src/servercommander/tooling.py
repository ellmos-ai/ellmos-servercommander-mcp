"""Small MCP tool-definition helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

import mcp.types as types


@dataclass
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Awaitable[dict[str, Any]]]

    def as_mcp_tool(self) -> types.Tool:
        return types.Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.input_schema,
        )
