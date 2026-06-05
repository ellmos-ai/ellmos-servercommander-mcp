# ellmos-servercommander-mcp

<p align="center">
  <img src="assets/servercommander-logo.jpg" alt="ellmos ServerCommander MCP Logo" width="360">
</p>

Alpha-MCP-Server für Server-Operationen: Deployment-Dry-runs, Mail-Status, Access-Log-Analyse und HTTP-Health-Checks.

Englische Standard-README: [README.md](README.md)

## Status

- Transport: stdio über das Python-MCP-SDK
- Paketstatus: öffentliches Alpha-Paket unter `ellmos-ai`
- Aktiver Kern: MCP-Tool-Liste, MCP-Tool-Dispatch, Config-Lader, `sc_logs_analyze`, `sc_health_check`
- Sichere Alpha-Handler: `sc_deploy` erstellt lokale SHA256-Manifeste im Dry-run, `sc_mail_*` führt noch keine IMAP/SMTP-Aktionen aus
- i18n: lokalisierte MCP-Tool-Beschreibungen, Input-Schema-Feldbeschreibungen und Unknown-Tool-Fehler für `en`, `de`, `es`, `zh`, `ja`, `ru` mit Englisch-Fallback

## Installation

Das npm-Paket enthält einen Node-Wrapper, der den Python-Server startet. Voraussetzung bleibt Python 3.10+ mit installiertem Python-Paket `mcp>=1.0.0`.

```powershell
npm install -g ellmos-servercommander-mcp@alpha
ellmos-servercommander
```

Für lokale Entwicklung:

```powershell
cd "C:\Users\User\OneDrive\.TOPICS\.AI\.MCP\ellmos-servercommander-mcp"
$env:PYTHONIOENCODING = "utf-8"
python -m pip install -e ".[dev]"
python -m pytest -q
```

Keine `.venv` im OneDrive-Ordner anlegen. Falls eine isolierte Umgebung gebraucht wird, außerhalb von OneDrive erstellen.

## Start Aus Dem Quellbaum

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

Die Sprache kann über `[server].language`, `SERVERCOMMANDER_LANG` oder `SERVERCOMMANDER_LOCALE` gesetzt werden.

```toml
[server]
name = "ellmos-servercommander"
language = "de" # en, de, es, zh, ja, ru
```

Secrets sollen als Umgebungsvariablen referenziert werden, zum Beispiel `$MAIL_PASSWORD` oder `$SFTP_PASSWORD`.

## Tools

- `sc_health_check`: prüft HTTP-Endpunkte und meldet Status-Code plus Latenz
- `sc_logs_analyze`: analysiert Apache-/Nginx-Access-Logs aus Text oder Datei
- `sc_deploy`: erstellt einen Deployment-Plan mit lokalem SHA256-Manifest, führt aber noch keinen Upload aus
- `sc_deploy_status`: zeigt konfigurierte Deploy-Profile und den aktuellen Alpha-History-Status
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: sichere Alpha-Statusantworten ohne IMAP/SMTP-Verbindung

## Entwicklung

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q
npm run smoke
npm pack --dry-run
```

Der nächste sinnvolle Schritt ist die Extraktion der echten SFTP-, IMAP/SMTP- und erweiterten Traffic-Module aus `.UMBRUCH` in credential-freie Adapter mit lokalen Tests.
