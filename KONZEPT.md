# ellmos-servercommander-mcp — Konzept

> Server-Operations als MCP: Deploy, Mail, Logs, Health-Checks.
> Aus .UMBRUCH-Tools extrahiert und parametrisiert.

## Tools

| Tool | Quelle | Beschreibung |
|---|---|---|
| `sc_deploy` | .UMBRUCH deploy.py (~221 LoC) | SFTP-Delta-Deploy mit SHA256 (parametrisiert: host, user, remote_path) |
| `sc_deploy_status` | .UMBRUCH deploy.py | Letztes Deployment prüfen (Zeitstempel, geänderte Dateien, Dauer) |
| `sc_mail_list` | .UMBRUCH cli.py (~516 LoC) | IMAP-Postfach auflisten (Ordner, ungelesen, letzte N) |
| `sc_mail_read` | .UMBRUCH cli.py | E-Mail lesen (nach ID oder Suchfilter) |
| `sc_mail_send` | .UMBRUCH cli.py | E-Mail senden (SMTP, mit Anhängen) |
| `sc_mail_search` | .UMBRUCH cli.py | E-Mails durchsuchen (FTS, Datum, Absender) |
| `sc_logs_analyze` | .UMBRUCH traffic_analyzer.py | Server-Logs parsen (Apache/Nginx), Bot-Filterung, Traffic-Stats |
| `sc_health_check` | neu | HTTP-Endpoint(s) prüfen, Status-Codes + Latenz melden |

## Vorarbeiten

### De-Hardcoding (deploy.py)
- Aktuell hardcoded: projektspezifischer Host, SFTP-Account und feste Pfade
- Ziel: host/user/remote_path/local_path als Tool-Argumente ODER Config-Profile
- Config-Profile für wiederkehrende Deploys: `[profiles.umbruch]`, `[profiles.other]`

### Mail-Kern extrahieren (cli.py)
- GUI-Code (gui.py, 2935 LoC) bleibt draußen
- CLI-Kern (~516 LoC) als Basis: IMAP-Verbindung, SMTP-Versand, FTS5-Cache
- Credential-Handling: Config-Datei mit verschlüsseltem Passwort oder Env-Variable

### Kein Hardcoding von Credentials
- Alle Secrets via Config oder Env-Variablen
- Referenz: `$SFTP_PASSWORD`, `$IMAP_PASSWORD` etc.

## Architektur

```
ellmos-servercommander-mcp/
├── src/servercommander/
│   ├── server.py        # MCP-Server Entry Point
│   ├── config.py        # Konfiguration
│   ├── deploy.py        # sc_deploy, sc_deploy_status
│   ├── mail.py          # sc_mail_list/read/send/search
│   ├── logs.py          # sc_logs_analyze
│   └── health.py        # sc_health_check
├── config/
│   └── servercommander.example.toml
├── tests/
└── pyproject.toml
```

## Konfigurationsbeispiel

```toml
[server]
name = "ellmos-servercommander"

[deploy.profiles.example_site]
host = "sftp.example.com"
user = "deploy-user"
remote_path = "/var/www/example"
local_path = "./dist"
protocol = "sftp"

[mail]
imap_host = "imap.example.com"
imap_port = 993
smtp_host = "smtp.example.com"
smtp_port = 587
username = "$MAIL_USER"
password = "$MAIL_PASSWORD"
cache_db = "~/.servercommander/mail_cache.db"

[logs]
default_format = "apache"

[health]
timeout = 5
endpoints = [
    "https://example.com/health",
]
```

## Quellmodule

| Modul | Quellpfad | LoC | Dependencies |
|---|---|---|---|
| deploy.py | `.TOPICS/.UMBRUCH/deploy.py` | ~221 | paramiko (SFTP) |
| cli.py (Mail) | `.TOPICS/.UMBRUCH/cli.py` | ~516 | stdlib (imaplib, smtplib) |
| traffic_analyzer.py | `.TOPICS/.UMBRUCH/traffic_analyzer.py` | ~300 | stdlib |
| health.py | neu | ~50 | stdlib (urllib) |
