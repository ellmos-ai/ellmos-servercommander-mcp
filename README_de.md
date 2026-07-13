# ellmos-servercommander-mcp

<p align="center">
  <img src="assets/servercommander-logo.jpg" alt="ellmos ServerCommander MCP Logo" width="360">
</p>

Alpha-MCP-Server für Server-Operationen: Deployment-Dry-runs, Mail-Status, Access-Log-Analyse und HTTP-Health-Checks.

Englische Standard-README: [README.md](README.md)

*Teil der [ellmos-ai](https://github.com/ellmos-ai)-Familie.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm version](https://img.shields.io/npm/v/ellmos-servercommander-mcp.svg)](https://www.npmjs.com/package/ellmos-servercommander-mcp)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org/)
[![MCP](https://img.shields.io/badge/MCP-stdio-blueviolet.svg)](https://modelcontextprotocol.io/)
[![Status: alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://www.npmjs.com/package/ellmos-servercommander-mcp)

**Auffindbarkeit:** Veröffentlicht auf [npm](https://www.npmjs.com/package/ellmos-servercommander-mcp) als `ellmos-servercommander-mcp`, für MCP-Kataloge in [`server.json`](server.json) beschrieben und für AI-Suche/Indexierung in [`llms.txt`](llms.txt) zusammengefasst.

## Architektur Visualisiert

```mermaid
graph TD
    Client[MCP Host: Claude / Cursor] <-->|stdio / JSON-RPC| NodeWrapper[Node.js Entrypoint]
    NodeWrapper <-->|Spawn subprocess| PyServer[Python MCP Server]
    
    subgraph Tools [ServerCommander Tools]
        PyServer -->|sc_health_check| HTTP[HTTP/HTTPS Endpoint Check]
        PyServer -->|sc_logs_analyze| Logs[Apache/Nginx Access Logs]
        PyServer -->|sc_deploy / sc_deploy_status| Deploy[Dry-Run Manifest & SQLite History]
        PyServer -->|sc_mail_*| Mail[IMAP/SMTP Safe Readiness Diagnostics]
    end
    
    subgraph Storage [Local Storage]
        Deploy -->|Optional persist| SQLite[(SQLite Deploy History)]
        Logs -->|Optional persist| JSONReports[(JSON Log Reports)]
    end
```

## Einstieg

| Ziel | Einstieg |
|---|---|
| ServerCommander in Claude Desktop, Claude Code, Cursor oder einen anderen MCP-Host einbinden | [MCP-Client-Konfiguration](#mcp-client-konfiguration) |
| Einen öffentlichen oder internen HTTP-Endpunkt vor einem Deployment prüfen | `sc_health_check` |
| Apache-/Nginx-Access-Logs nach Fehlern, Bots, Referern und verdächtigen Pfaden prüfen | `sc_logs_analyze` |
| Vor SFTP-/SSH-Ausführung ein trockenes Deployment-Manifest bauen | `sc_deploy` und `sc_deploy_status` |
| Mail-Operationen später vorbereiten, ohne heute versehentlich zu senden | `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search` |

## Status

- Transport: stdio über das Python-MCP-SDK
- Paketstatus: öffentliches Alpha-Paket unter `ellmos-ai`
- Aktiver Kern: MCP-Tool-Liste, MCP-Tool-Dispatch, Config-Lader, HTTP-Health-Checks, erweiterte Access-Log-Analyse mit optional gespeicherten JSON-Reports und optionale lokale Deployment-Dry-run-Historie
- Sichere Alpha-Handler: `sc_deploy` erstellt lokale SHA256-Manifeste, Konfigurationsdiagnosen und opt-in SQLite-History-Einträge im Dry-run, `sc_mail_*` meldet protokollspezifische IMAP-/SMTP-Bereitschaft ohne Mail-Verbindungen
- i18n: lokalisierte MCP-Tool-Beschreibungen, Input-Schema-Feldbeschreibungen und Unknown-Tool-Fehler für `en`, `de`, `es`, `zh`, `ja`, `ru` mit Englisch-Fallback

## Installation

Das npm-Paket enthält einen Node-Wrapper, der den Python-Server startet. Voraussetzung bleibt Python 3.10+ mit installiertem Python-Paket `mcp>=1.0.0`.

### Option 1: Installation per npm

```powershell
npm install -g ellmos-servercommander-mcp@alpha
ellmos-servercommander
```

### Option 2: Installation aus dem Quellcode

```powershell
git clone https://github.com/ellmos-ai/ellmos-servercommander-mcp.git
cd ellmos-servercommander-mcp
$env:PYTHONIOENCODING = "utf-8"
python -m pip install -e ".[dev]"
python -m pytest -q
```

Keine `.venv` in cloud-synchronisierten Ordnern anlegen, wenn der Sync-Client Dateien sperrt. Falls eine isolierte Umgebung gebraucht wird, außerhalb dieses Ordners erstellen.

## Start Aus Dem Quellbaum

```powershell
$env:PYTHONPATH = "src"
python -m servercommander.server
```

## MCP-Client-Konfiguration

### Globale npm-Installation

```json
{
  "mcpServers": {
    "servercommander": {
      "command": "ellmos-servercommander"
    }
  }
}
```

### Quellcode-Checkout

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

`/absolute/path/to/ellmos-servercommander-mcp` durch den eigenen lokalen Checkout-Pfad ersetzen.

## Server-Konfiguration

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

[deploy]
persist_history = false
history_db = "~/.servercommander/deploy_history.db"

[logs]
default_format = "apache" # apache | nginx
persist_reports = false
reports_dir = "~/.servercommander/log_reports"
```

Secrets sollen als Umgebungsvariablen referenziert werden, zum Beispiel `$MAIL_PASSWORD` oder `$SFTP_PASSWORD`.

## Tools

- `sc_health_check`: prüft HTTP-Endpunkte und meldet Status-Code plus Latenz
- `sc_logs_analyze`: analysiert Apache-/Nginx-Access-Logs aus Text oder Datei, inklusive Statusklassen, Bytes, Referern, Fehlerpfaden, verdächtigen Request-Markern und optionaler JSON-Report-Speicherung per `persist_report`
- `sc_deploy`: erstellt einen Deployment-Plan mit lokalem SHA256-Manifest und Profildiagnose, führt aber noch keinen Upload aus; die Bereitschaft prüft Pflichtfelder, manifestierbare lokale Pfade und unterstützte Protokolle vor optionalem `record_history=true`; verschachtelte Symlinks werden ausgewiesen, aber ausgeschlossen, damit ein Manifest nicht unbemerkt außerhalb des gewählten Release-Ordners traversiert
- `sc_deploy_status`: zeigt konfigurierte Deploy-Profile, ausgewählte Profildiagnosen und die jüngste Dry-run-Historie aus der lokalen SQLite-History-Datenbank
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: sichere Alpha-Statusantworten mit aktionsspezifischen IMAP-/SMTP-Bereitschaftsdiagnosen und ohne Mail-Verbindungen

## Suche Und Abgrenzung

ServerCommander ist der ellmos-Operations-MCP-Server für lokale Serververwaltungs-Workflows. Nützliche Suchphrasen:

- MCP server operations tools
- MCP deploy dry-run server
- MCP access log analyzer
- MCP HTTP health check tool
- local-first server management MCP
- Claude Code server operations MCP
- safe SFTP deployment planning MCP

Das Repo ist nicht der GitHub-MCP-Server, kein generischer Shell-Command-MCP-Server, kein Hosting-Control-Panel und noch kein produktiver SFTP-/IMAP-Executor. Die aktuelle Alpha-Oberfläche ist bewusst diagnostisch und Dry-run-first.

## ellmos-MCP-Familie

- [ellmos-filecommander-mcp](https://github.com/ellmos-ai/ellmos-filecommander-mcp): Dateisystemoperationen, Prozesssteuerung, OCR, Archive und Exporte
- [ellmos-codecommander-mcp](https://github.com/ellmos-ai/ellmos-codecommander-mcp): Codeanalyse, JSON-Reparatur, Imports, Diffs, Regex und Formatkonvertierung
- [ellmos-clatcher-mcp](https://github.com/ellmos-ai/ellmos-clatcher-mcp): Reparatur, Konvertierung, Duplikaterkennung, Batch-Operationen und Dokumentwerkzeuge
- [n8n-manager-mcp](https://github.com/ellmos-ai/n8n-manager-mcp): n8n-Workflow-Management über MCP
- [ellmos-controlcenter-mcp](https://github.com/ellmos-ai/ellmos-controlcenter-mcp): lokale MCP-Erkennung, Profile, Bundles und Control-Plane-Checks
- [ellmos-homebase-mcp](https://github.com/ellmos-ai/ellmos-homebase-mcp): BACH-Integrationshub, Memory, Wissensbasis, State, Schwarm- und Auto-Chain-Orchestrierung

## Entwicklung

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q
npm run smoke
npm pack --dry-run
```

Der nächste sinnvolle Schritt ist, explizit konfigurierte Ausführungsadapter für SFTP und IMAP/SMTP zu ergänzen und Dry-run beziehungsweise Status-only als Standard beizubehalten.
