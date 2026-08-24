# Security Policy / Sicherheitsrichtlinie

## English

### Execution Safety and Local-First Guarantees

`ellmos-servercommander-mcp` is engineered as a local-first, safe Model Context Protocol (MCP) server for server operations, log diagnostics, health checks, and deployment staging:

1. **Local-First & Dry-Run Architecture**: All deployment staging (`sc_deploy`, `sc_deploy_status`) operates strictly in **dry-run mode** by default, producing deterministic local SHA-256 manifests and optional local SQLite history without performing unauthorized remote modifications or unverified file mutations.
2. **Mail Diagnostic Safety**: Mail tools (`sc_mail_*`) evaluate IMAP/SMTP configuration and readiness without opening unauthenticated network sockets or transmitting live messages unexpectedly.
3. **Log Analysis Isolation**: Access log inspection (`sc_logs_analyze`) reads local or configured web server logs, sanitizes report paths, and writes optional structured JSON reports exclusively to designated local directories.
4. **Secret & Credential Protection**: Real credentials (`.env`, `.npmrc`, `.pypirc`, private keys `id_rsa`, `id_ed25519`, `*.pem`, `*.key`) and token files (`*.token.json`) are strictly git-ignored and excluded via `.npmignore` from npm package distribution.
5. **Unprivileged Execution (Non-Elevation)**: Operates entirely within unprivileged user space and requires no administrative (sudo/root/Administrator) privileges.

### Tool Risk Classification

| Tool | Risk Level | Safety Mechanisms |
|------|------------|-------------------|
| `sc_health_check` | Low | Read-only HTTP/HTTPS status probe with strict timeout and thread-pool isolation |
| `sc_logs_analyze` | Low | Read-only log parsing; sanitized optional JSON report persistence |
| `sc_deploy` | Low / Dry-Run | Builds local SHA-256 manifest and config check; dry-run only |
| `sc_deploy_status` | Low | Reads local deployment status and SQLite dry-run history |
| `sc_mail_list` | Low | Safe local / credential-checked readiness report (reusing verified `mail-connector`) |
| `sc_mail_read` | Low | Safe message structure diagnostic |
| `sc_mail_send` | Low / Safe Mode | Alpha readiness check; no unexpected autonomous dispatch |
| `sc_mail_search` | Low | Safe query diagnostic |

### Supported Versions

| Version | Supported | Notes |
|---|---|---|
| `0.1.0-alpha.x` | :white_check_mark: | Current active release branch |
| `< 0.1.0-alpha.1` | :x: | Legacy preview prototypes |

### Reporting a Vulnerability

We take the security of our tools seriously. If you discover a security issue or unexpected network behavior within `ellmos-servercommander-mcp`, please report it through one of the following channels:

- **GitHub Security Advisories (Preferred)**: [Open a Private Advisory](https://github.com/ellmos-ai/ellmos-servercommander-mcp/security/advisories)
- **Email Security Contacts**:
  - `security@ellmos.ai`
  - `security@open-bricks.org`
  - `lukas@open-bricks.org`
  - `support@lukasgeiger.com`

**Response SLA**: We commit to acknowledging receipt of vulnerability reports within **48 hours** and providing an assessment with target mitigation timelines within **5 business days**.

---

## Deutsch

### Ausführungssicherheit und Local-First Garantien

`ellmos-servercommander-mcp` ist als Local-First-, sicherer Model Context Protocol (MCP) Server für Server-Operationen, Log-Diagnosen, Health-Checks und Deployment-Staging konzipiert:

1. **Local-First & Dry-Run Architektur**: Alle Deployment-Staging-Operationen (`sc_deploy`, `sc_deploy_status`) laufen standardmäßig strikt im **Dry-Run-Modus**, erzeugen deterministische lokale SHA-256-Manifeste sowie optionale SQLite-Historien und führen keine unautorisierten Remote-Veränderungen durch.
2. **Sichere Mail-Diagnostik**: Mail-Werkzeuge (`sc_mail_*`) bewerten IMAP-/SMTP-Konfigurationen und Bereitschaftszustände, ohne unauthentifizierte Netzwerk-Sockets zu öffnen oder eigenmächtig Live-Nachrichten zu versenden.
3. **Isolierte Log-Analyse**: Die Access-Log-Prüfung (`sc_logs_analyze`) liest lokale Webserver-Logs, bereinigt Pfade und schreibt optionale JSON-Reports ausschließlich in definierte lokale Verzeichnisse.
4. **Schutz von Zugangsdaten & Secrets**: Echte Anmeldedaten (`.env`, `.npmrc`, `.pypirc`, Private Keys `id_rsa`, `id_ed25519`, `*.pem`, `*.key`) und Token-Dateien (`*.token.json`) sind strikt ignoriert und über `.npmignore` von npm-Paketen ausgeschlossen.
5. **Rechtefreie Ausführung (Non-Elevation)**: Läuft vollständig im unprivilegierten Benutzerkontext und benötigt keinerlei Administrator- oder Root-Rechte.

### Sicherheitskontakt & 48h SLA

Sicherheitsrelevante Befunde können vertraulich über [GitHub Security Advisories](https://github.com/ellmos-ai/ellmos-servercommander-mcp/security/advisories) oder per E-Mail an `security@ellmos.ai` / `security@open-bricks.org` gemeldet werden. Wir garantieren eine Erstreaktion innerhalb von **48 Stunden**.
