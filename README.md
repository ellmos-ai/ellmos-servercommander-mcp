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

**Discoverability:** Published on [npm](https://www.npmjs.com/package/ellmos-servercommander-mcp) as `ellmos-servercommander-mcp` and maintained in the [`ellmos-ai`](https://github.com/ellmos-ai) organization.

## Status

- Transport: stdio via the Python MCP SDK
- Package status: public alpha package under `ellmos-ai`
- Current core: MCP tool listing, MCP tool dispatch, config loading, HTTP health checks, richer access-log analysis
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
```

Secrets should be referenced through environment variables, for example `$MAIL_PASSWORD` or `$SFTP_PASSWORD`.

## Tools

- `sc_health_check`: checks HTTP endpoints and reports status code plus latency
- `sc_logs_analyze`: analyzes Apache/Nginx access logs from inline text or a local file, including status classes, bytes, referers, error paths, and suspicious request markers
- `sc_deploy`: creates a deployment plan with a local SHA256 manifest and profile diagnostics, but does not upload yet
- `sc_deploy_status`: shows configured deploy profiles, selected-profile diagnostics, and the current alpha history status
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: safe alpha status responses with mail configuration diagnostics and no IMAP/SMTP connections

## Development

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q
npm run smoke
npm pack --dry-run
```

Next useful step: add explicitly configured execution adapters for SFTP and IMAP/SMTP, keep dry-run defaults, and extend log analysis with persisted reports.
