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

**Auffindbarkeit:** Veröffentlicht auf [npm](https://www.npmjs.com/package/ellmos-servercommander-mcp) als `ellmos-servercommander-mcp` und gepflegt in der Organisation [`ellmos-ai`](https://github.com/ellmos-ai).

## Status

- Transport: stdio über das Python-MCP-SDK
- Paketstatus: öffentliches Alpha-Paket unter `ellmos-ai`
- Aktiver Kern: MCP-Tool-Liste, MCP-Tool-Dispatch, Config-Lader, HTTP-Health-Checks, erweiterte Access-Log-Analyse
- Sichere Alpha-Handler: `sc_deploy` erstellt lokale SHA256-Manifeste und Konfigurationsdiagnosen im Dry-run, `sc_mail_*` meldet Mail-Konfigurationslücken ohne IMAP/SMTP-Aktionen
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
```

Secrets sollen als Umgebungsvariablen referenziert werden, zum Beispiel `$MAIL_PASSWORD` oder `$SFTP_PASSWORD`.

## Tools

- `sc_health_check`: prüft HTTP-Endpunkte und meldet Status-Code plus Latenz
- `sc_logs_analyze`: analysiert Apache-/Nginx-Access-Logs aus Text oder Datei, inklusive Statusklassen, Bytes, Referern, Fehlerpfaden und verdächtigen Request-Markern
- `sc_deploy`: erstellt einen Deployment-Plan mit lokalem SHA256-Manifest und Profildiagnose, führt aber noch keinen Upload aus
- `sc_deploy_status`: zeigt konfigurierte Deploy-Profile, ausgewählte Profildiagnosen und den aktuellen Alpha-History-Status
- `sc_mail_list`, `sc_mail_read`, `sc_mail_send`, `sc_mail_search`: sichere Alpha-Statusantworten mit Mail-Konfigurationsdiagnosen und ohne IMAP/SMTP-Verbindung

## Entwicklung

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"
python -m pytest -q
npm run smoke
npm pack --dry-run
```

Der nächste sinnvolle Schritt ist, explizit konfigurierte Ausführungsadapter für SFTP und IMAP/SMTP zu ergänzen, Dry-run als Standard beizubehalten und Log-Analysen um persistierte Reports zu erweitern.
