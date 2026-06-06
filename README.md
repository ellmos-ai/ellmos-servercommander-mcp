# ellmos-servercommander-mcp

<p align="center">
  <img src="assets/servercommander-logo.jpg" alt="ellmos ServerCommander MCP logo" width="360">
</p>

Alpha MCP server for server operations: deployment dry-runs, mail status, access-log analysis, and HTTP health checks.

German README: [README_de.md](README_de.md)

*Part of the [ellmos-ai](https://github.com/ellmos-ai) family.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm version](https://img.shields.io/npm/v/ellmos-servercommander-mcp.svg)](https://www.npmjs.com/package/ellmos-servercommander-mcp)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org/)
[![MCP](https://img.shields.io/badge/MCP-stdio-blueviolet.svg)](https://modelcontextprotocol.io/)
[![Status: alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://www.npmjs.com/package/ellmos-servercommander-mcp)

**Discoverability:** Published on [npm](https://www.npmjs.com/package/ellmos-servercommander-mcp) as `ellmos-servercommander-mcp`, described for MCP catalogs in [`server.json`](server.json), and summarized for AI search/indexing in [`llms.txt`](llms.txt).

## Start Here

| Goal | Start with |
|---|---|
| Add ServerCommander to Claude Desktop, Claude Code, Cursor, or another MCP host | [MCP Client Configuration](#mcp-client-configuration) |
| Check a public or internal HTTP endpoint before a deploy | `sc_health_check` |
| Inspect Apache/Nginx access logs for errors, bots, referrers, and suspicious paths | `sc_logs_analyze` |
| Build a dry-run deployment manifest before SFTP/SSH execution exists | `sc_deploy` and `sc_deploy_status` |
| Wire mail operations later without accidental sends today | `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search` |

## Status

- Transport: stdio via the Python MCP SDK
- Package status: public alpha package under `ellmos-ai`
- Current core: MCP tool listing, MCP tool dispatch, config loading, HTTP health checks, richer access-log analysis with optional persisted JSON reports
- Safe alpha handlers: `sc_deploy` builds local SHA256 manifests and configuration diagnostics in dry-run mode; `sc_mail_*` reports mail configuration gaps without IMAP/SMTP operations
- i18n: localized MCP tool descriptions, input-schema field descriptions, and unknown-tool errors for `en`, `de`, `es`, `zh`, `ja`, `ru` with English fallback

## Install

The npm package contains a Node wrapper that starts the Python server. You still need Python 3.10+ and the Python package `mcp>=1.0.0`.

### Option 1: Install From npm

```powershell
npm install -g ellmos-servercommander-mcp@alpha
ellmos-servercommander
```

### Option 2: Install From Source

```powershell
git clone https://github.com/ellmos-ai/ellmos-servercommander-mcp.git
cd ellmos-servercommander-mcp
$env:PYTHONIOENCODING = "utf-8"
python -m pip install -e ".[dev]"
python -m pytest -q
```

Avoid creating a `.venv` inside cloud-synced folders if your sync client locks files. If you need an isolated environment, create it outside that folder.

## Start From Source

```powershell
$env:PYTHONPATH = "src"
python -m servercommander.server
```

## MCP Client Configuration

### Global npm Install

```json
{
  "mcpServers": {
    "servercommander": {
      "command": "ellmos-servercommander"
    }
  }
}
```

### Source Checkout

```json
{
  "mcpServers": {
    "servercommander": {
      "command": "python",
      "args": ["-m", "servercommander.server"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/ellmos-servercommander-mcp/src"
      }
    }
  }
}
```

Replace `/absolute/path/to/ellmos-servercommander-mcp` with your local checkout path.

## Server Configuration

Example: [config/servercommander.example.toml](config/servercommander.example.toml)

Default paths:

- `%USERPROFILE%\.servercommander\config.toml`
- `%USERPROFILE%\.config\servercommander\config.toml`
- override with `SERVERCOMMANDER_CONFIG`

Language can be configured with `[server].language`, `SERVERCOMMANDER_LANG`, or `SERVERCOMMANDER_LOCALE`.

```toml
[server]
name = "ellmos-servercommander"
language = "en" # en, de, es, zh, ja, ru

[logs]
default_format = "apache" # apache | nginx
persist_reports = false
reports_dir = "~/.servercommander/log_reports"
```

Secrets should be referenced through environment variables, for example `$MAIL_PASSWORD` or `$SFTP_PASSWORD`.

## Tools

- `sc_health_check`: checks HTTP endpoints and reports status code plus latency
- `sc_logs_analyze`: analyzes Apache/Nginx access logs from inline text or a local file, including status classes, bytes, referers, error paths, suspicious request markers, and optional JSON report persistence via `persist_report`
- `sc_deploy`: creates a deployment plan with a local SHA256 manifest and profile diagnostics, but does not upload yet
- `sc_deploy_status`: shows configured deploy profiles, selected-profile diagnostics, and the current alpha history status
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: safe alpha status responses with mail configuration diagnostics and no IMAP/SMTP connections

## Search And Disambiguation

ServerCommander is the ellmos operations MCP server for local-first server administration workflows. Use this repo when searching for:

- MCP server operations tools
- MCP deploy dry-run server
- MCP access log analyzer
- MCP HTTP health check tool
- local-first server management MCP
- Claude Code server operations MCP
- safe SFTP deployment planning MCP

It is not the GitHub MCP server, not a generic shell-command MCP server, not a hosting provider control panel, and not a production SFTP/IMAP executor yet. The current alpha surface is intentionally diagnostic and dry-run first.

## ellmos MCP Family

- [ellmos-filecommander-mcp](https://github.com/ellmos-ai/ellmos-filecommander-mcp): filesystem operations, process management, OCR, archives, and exports
- [ellmos-codecommander-mcp](https://github.com/ellmos-ai/ellmos-codecommander-mcp): code analysis, JSON repair, imports, diffs, regex, and format conversion
- [ellmos-clatcher-mcp](https://github.com/ellmos-ai/ellmos-clatcher-mcp): repair, conversion, duplicate detection, batch operations, and document utilities
- [n8n-manager-mcp](https://github.com/ellmos-ai/n8n-manager-mcp): n8n workflow management through MCP
- [ellmos-controlcenter-mcp](https://github.com/ellmos-ai/ellmos-controlcenter-mcp): local MCP discovery, profiles, bundles, and control-plane checks

## Development

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q
npm run smoke
npm pack --dry-run
```

Next useful step: add explicitly configured execution adapters for SFTP and IMAP/SMTP while keeping dry-run/status-only defaults.
