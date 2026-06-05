# ellmos-servercommander-mcp

<p align="center">
  <img src="assets/servercommander-logo.jpg" alt="ellmos ServerCommander MCP logo" width="360">
</p>

Alpha MCP server for server operations: deployment dry-runs, mail status, access-log analysis, and HTTP health checks.

German README: [README_de.md](README_de.md)

## Status

- Transport: stdio via the Python MCP SDK
- Package status: public alpha package under `ellmos-ai`
- Current core: MCP tool listing, MCP tool dispatch, config loading, `sc_logs_analyze`, `sc_health_check`
- Safe alpha handlers: `sc_deploy` builds local SHA256 manifests in dry-run mode; `sc_mail_*` does not perform IMAP/SMTP operations yet
- i18n: localized MCP tool descriptions, input-schema field descriptions, and unknown-tool errors for `en`, `de`, `es`, `zh`, `ja`, `ru` with English fallback

## Install

The npm package contains a Node wrapper that starts the Python server. You still need Python 3.10+ and the Python package `mcp>=1.0.0`.

```powershell
npm install -g ellmos-servercommander-mcp@alpha
ellmos-servercommander
```

For local development:

```powershell
cd "C:\Users\User\OneDrive\.TOPICS\.AI\.MCP\ellmos-servercommander-mcp"
$env:PYTHONIOENCODING = "utf-8"
python -m pip install -e ".[dev]"
python -m pytest -q
```

Do not create a `.venv` inside a OneDrive-synced folder. If you need an isolated environment, create it outside OneDrive.

## Start From Source

```powershell
$env:PYTHONPATH = "src"
python -m servercommander.server
```

## Configuration

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
- `sc_logs_analyze`: analyzes Apache/Nginx access logs from inline text or a local file
- `sc_deploy`: creates a deployment plan with a local SHA256 manifest, but does not upload yet
- `sc_deploy_status`: shows configured deploy profiles and the current alpha history status
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: safe alpha status responses without IMAP/SMTP connections

## Development

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q
npm run smoke
npm pack --dry-run
```

Next useful step: extract real SFTP, IMAP/SMTP, and extended traffic-analysis modules from `.UMBRUCH` into credential-free adapters with local tests.
