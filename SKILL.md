---
name: ellmos-servercommander-mcp
version: 0.1.0-alpha.21
type: tool-skill
visibility: public
description: >
  Local-first Model Context Protocol (MCP) server for safe server operations:
  HTTP/HTTPS health checks, Apache/Nginx access-log analysis, SHA-256 dry-run
  deployment manifest planning, and IMAP/SMTP readiness diagnostics.
tags:
  - mcp
  - mcp-server
  - server-operations
  - health-check
  - log-analysis
  - dry-run
  - deployment
  - mail-diagnostics
  - local-first
  - zero-egress
---

# ellmos-servercommander-mcp — Product Skill

Local-first MCP server (`stdio` transport via FastMCP + Node.js CLI wrapper) for safe server diagnostics and dry-run deployment staging.

## Prerequisites

- **Node.js**: `>= 18` (for `npx` / global `ellmos-servercommander` wrapper)
- **Python**: `>= 3.10`
- **Core dependency**: `mcp>=1.0.0,<2.0.0`
- **Optional SFTP extra**: `paramiko>=3.0` (only when `[sftp]` extra is explicitly installed)

## Installation

### Option 1: npm / npx (Global or Ephemeral)

```bash
npm install -g ellmos-servercommander-mcp@alpha
# or invoke directly without global install:
npx -y ellmos-servercommander-mcp@alpha --version
```

### Option 2: Isolated Python Source Install

```bash
git clone https://github.com/ellmos-ai/ellmos-servercommander-mcp.git
cd ellmos-servercommander-mcp
python -m venv .venv
# Linux/macOS: .venv/bin/pip install -e ".[dev]"
# Windows:     .venv\Scripts\pip.exe install -e ".[dev]"
```

## Verification Commands

```bash
node bin/ellmos-servercommander.js --version
python -c "import servercommander; print(servercommander.__file__)"
python -m pytest -q
```

## Minimal MCP Client Configuration

```json
{
  "mcpServers": {
    "servercommander": {
      "command": "npx",
      "args": ["-y", "ellmos-servercommander-mcp@alpha"]
    }
  }
}
```

## Available MCP Tools (8 Tools)

| Tool | Purpose | Default Safety Boundary |
|---|---|---|
| `sc_health_check` | Non-blocking HTTP/HTTPS endpoint probe (`status_code`, `latency_ms`) | Explicit URLs only; malformed URLs isolated per item |
| `sc_logs_analyze` | Apache/Nginx access-log parser (status classes, bytes, referrers, bot markers, optional JSON report) | Read-only; strips query, fragment & URL authority userinfo before aggregation |
| `sc_deploy` | Local recursive SHA-256 deployment manifest & profile readiness check | `dry_run=true` enforced in alpha; skips nested symlinks |
| `sc_deploy_status` | Shows configured deployment profiles and recent dry-run history from SQLite | Read-only status inspection |
| `sc_mail_list` | IMAP readiness check or opt-in read-only folder listing via `mail-connector` | `execution_enabled=false` by default |
| `sc_mail_read` | Alpha mail readiness / delegation status for reading messages | Does not open unconfigured sockets |
| `sc_mail_send` | Alpha mail readiness check for SMTP settings | Does not send emails in alpha |
| `sc_mail_search` | Alpha mail readiness / delegation status for searching messages | Does not open unconfigured sockets |

## Safety & Governance Boundaries

1. **Local-First & Zero-Egress (`INV-LOCAL-01`)**: No background telemetry; outbound HTTP only when `sc_health_check` is explicitly invoked.
2. **Dry-Run Staging (`INV-DRY-02`)**: `sc_deploy` builds local SHA-256 manifests and never mutates remote targets in alpha.
3. **Unprivileged Execution (`INV-PRIV-06`)**: Runs strictly as `RunAsInvoker` without root/sudo/Admin privileges.
4. **Process Isolation (`INV-SEC-07`)**: Node wrapper sets `PYTHONSAFEPATH=1` and pins package root to prevent CWD import hijacking.
5. **Multilingual i18n (`INV-I18N-08`)**: Supports `en`, `de`, `es`, `zh`, `ja`, `ru` with automatic English fallback.

## Configuration Resolution Order

1. `SERVERCOMMANDER_CONFIG_PATH` environment variable
2. `./servercommander.toml`
3. `./config/servercommander.toml`
4. `~/.config/servercommander/servercommander.toml`

Reference template: `config/servercommander.example.toml`.

## When NOT to Use

- Do not use this server for arbitrary remote shell execution, interactive SSH sessions, or unverified production SMTP/SFTP writes.
- Do not use it as a GitHub API or local filesystem MCP server (use dedicated ecosystem tools for those domains).
