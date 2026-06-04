# ellmos-servercommander-mcp

Alpha-MCP-Server für Server-Operationen: Deployment-Planung, Mail-Status, Log-Analyse und HTTP-Health-Checks.

## Status

- Transport: stdio über das Python-MCP-SDK
- Paketstatus: Alpha-Paket, GitHub-Repo unter `ellmos-ai` vorgesehen
- Aktiver Kern: MCP-Tool-Liste, MCP-Tool-Dispatch, Config-Lader, `sc_logs_analyze`, `sc_health_check`
- Sichere Alpha-Handler: `sc_deploy` erstellt lokale SHA256-Manifeste im Dry-run, `sc_mail_*` führt noch keine IMAP/SMTP-Aktionen aus

## Installation für lokale Tests

```powershell
cd "C:\Users\User\OneDrive\.TOPICS\.AI\.MCP\ellmos-servercommander-mcp"
$env:PYTHONIOENCODING = "utf-8"
python -m pip install -e ".[dev]"
python -m pytest -q
```

Keine `.venv` im OneDrive-Ordner anlegen. Falls eine isolierte Umgebung gebraucht wird, außerhalb von OneDrive erstellen.

## npm Alpha

Das npm-Paket enthält einen Node-Wrapper, der den Python-Server startet. Voraussetzung bleibt Python 3.10+ mit installiertem Python-Paket `mcp>=1.0.0`.

```powershell
npm install -g ellmos-servercommander-mcp@alpha
ellmos-servercommander
```

## Start

```powershell
ellmos-servercommander
```

Oder direkt aus dem Quellbaum:

```powershell
$env:PYTHONPATH = "src"
python -m servercommander.server
```

## Konfiguration

Beispiel: [config/servercommander.example.toml](config/servercommander.example.toml)

Standardpfade:

- `%USERPROFILE%\.servercommander\config.toml`
- `%USERPROFILE%\.config\servercommander\config.toml`
- Override per `SERVERCOMMANDER_CONFIG`

Secrets sollen als Umgebungsvariablen referenziert werden, zum Beispiel `$MAIL_PASSWORD` oder `$SFTP_PASSWORD`.

## Tools

- `sc_health_check`: prüft HTTP-Endpunkte und meldet Status-Code plus Latenz
- `sc_logs_analyze`: analysiert Apache-/Nginx-Access-Logs aus Text oder Datei
- `sc_deploy`: erstellt im Alpha-Modus einen Deployment-Plan mit lokalem SHA256-Manifest, führt aber noch keinen Upload aus
- `sc_deploy_status`: zeigt konfigurierte Deploy-Profile und den noch fehlenden History-Status
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: liefern aktuell sichere Alpha-Statusantworten ohne IMAP/SMTP-Verbindung

## Entwicklung

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m pytest -q
```

Der nächste sinnvolle Schritt ist die Extraktion der echten SFTP-, IMAP/SMTP- und erweiterten Traffic-Module aus `.UMBRUCH` in credential-freie Adapter mit lokalen Tests.
