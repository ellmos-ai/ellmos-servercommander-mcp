"""Configuration loader for ServerCommander MCP."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    import tomli as tomllib


DEFAULT_CONFIG_PATHS = [
    Path.home() / ".servercommander" / "config.toml",
    Path.home() / ".config" / "servercommander" / "config.toml",
]


@dataclass
class ServerCommanderConfig:
    server_name: str = "ellmos-servercommander"
    deploy_profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    mail: dict[str, Any] = field(default_factory=dict)
    logs: dict[str, Any] = field(default_factory=dict)
    health: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def deploy_profile(self, name: str) -> dict[str, Any]:
        return self.deploy_profiles.get(name, {})


def load_config(path: str | Path | None = None) -> ServerCommanderConfig:
    """Load TOML config. Missing config is valid for alpha-safe defaults."""
    if path is None:
        env_path = os.environ.get("SERVERCOMMANDER_CONFIG")
        if env_path:
            path = Path(env_path)
        else:
            for candidate in DEFAULT_CONFIG_PATHS:
                if candidate.exists():
                    path = candidate
                    break

    if path is None or not Path(path).exists():
        return ServerCommanderConfig()

    with open(path, "rb") as f:
        raw = tomllib.load(f)

    deploy = raw.get("deploy", {})
    profiles = deploy.get("profiles", {}) if isinstance(deploy, dict) else {}
    server = raw.get("server", {})

    return ServerCommanderConfig(
        server_name=server.get("name", "ellmos-servercommander"),
        deploy_profiles=profiles if isinstance(profiles, dict) else {},
        mail=raw.get("mail", {}),
        logs=raw.get("logs", {}),
        health=raw.get("health", {}),
        raw=raw,
    )


def resolve_env_value(value: Any) -> Any:
    """Resolve config values of the form '$ENV_NAME' without exposing secrets."""
    if isinstance(value, str) and value.startswith("$") and len(value) > 1:
        return os.environ.get(value[1:], "")
    return value
