# Security Policy

## Execution Safety and Local-First Guarantees

`ellmos-servercommander-mcp` is designed as a local-first, safe MCP stdio server for server operations, log diagnostics, health checks, and deployment staging:

1. **Local-First & Dry-Run Architecture**: All deployment staging (`sc_deploy`, `sc_deploy_status`) operates strictly in **dry-run mode**, producing local SHA-256 manifests and optional local SQLite history without performing unauthorized remote modifications.
2. **Mail Diagnostic Safety**: Mail tools (`sc_mail_*`) evaluate IMAP/SMTP configuration and readiness without opening unauthenticated network sockets or transmitting live messages unexpectedly.
3. **Log Analysis Isolation**: Access log inspection (`sc_logs_analyze`) reads local or configured web server logs, sanitizes report paths, and writes optional structured JSON reports exclusively to designated local directories.
4. **Secret & Credential Protection**: Real credentials (`.env`, `.npmrc`, `.pypirc`, private keys `id_rsa`, `id_ed25519`, `*.pem`, `*.key`) and token files (`*.token.json`) are strictly git-ignored and excluded via `.npmignore` from npm package distribution.

## Tool Risk Classification

| Tool | Risk Level | Safety Mechanisms |
|------|------------|-------------------|
| `sc_health_check` | Low | Read-only HTTP/HTTPS status probe with strict timeout |
| `sc_logs_analyze` | Low | Read-only log parsing; sanitized optional JSON report persistence |
| `sc_deploy` | Low / Dry-Run | Builds local manifest and config check; dry-run only |
| `sc_deploy_status` | Low | Reads local deployment status and SQLite dry-run history |
| `sc_mail_list` | Low | Safe local / credential-checked readiness report |
| `sc_mail_read` | Low | Safe message structure diagnostic |
| `sc_mail_send` | Low / Safe Mode | Alpha readiness check; no unexpected autonomous dispatch |
| `sc_mail_search` | Low | Safe query diagnostic |

## Supported Versions

| Version | Supported | Notes |
|---|---|---|
| `0.1.0-alpha.x` | :white_check_mark: | Current active release branch |
| `< 0.1.0-alpha.1` | :x: | Legacy preview prototypes |

## Reporting a Vulnerability

If you discover a security issue or unexpected network behavior within `ellmos-servercommander-mcp`, please report it privately via GitHub Security Advisories or contact the maintainers.
