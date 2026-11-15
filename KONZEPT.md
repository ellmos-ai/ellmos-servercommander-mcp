# ellmos-servercommander-mcp — Konzept

> Server-Operations als MCP: Deploy, Mail, Logs, Health-Checks.
> Aus .UMBRUCH-Tools extrahiert und parametrisiert.

## Tools

Die Zielspalte beschreibt die ursprüngliche Produktidee, keine bereits
freigegebene Ausführung. Der Alpha-Stand wurde am 01.11.2026 gegen die
registrierten Handler geprüft; Details stehen in [README.md](README.md),
[README_de.md](README_de.md) und [llms.txt](llms.txt).

| Tool | Ziel / historische Quelle | Implementierter Alpha-Stand |
|---|---|---|
| `sc_deploy` | SFTP-Delta-Deploy mit SHA-256; .UMBRUCH deploy.py | Lokaler Dry-Run-Plan mit Manifest und Profildiagnose; optionale SQLite-Plan-Historie. `dry_run=false` wird abgewiesen, kein SFTP-Transfer. |
| `sc_deploy_status` | Letztes Deployment prüfen; .UMBRUCH deploy.py | Konfigurierte Profile und lokale Dry-Run-Historie lesen; kein Beleg eines ausgeführten Remote-Deployments. |
| `sc_mail_list` | Postfach und Nachrichten auflisten; .UMBRUCH cli.py | Standardmäßig nur Konfigurationsdiagnose. Mit `execution_enabled=true`, passenden Credentials und verfügbarem `mail-connector`: read-only IMAP-Reachability (Verbindung und Ordnerliste), keine Nachrichtenliste. Bei fehlendem Connector Rückfall auf Diagnose. |
| `sc_mail_read` | Nachricht lesen; .UMBRUCH cli.py | Diagnose; bei aktiviertem Ausführungsmodus Hinweis `delegated_to=mail-connector`. Kein eigener Nachrichtenabruf und kein automatischer Connector-Aufruf für Read/Search. |
| `sc_mail_send` | SMTP-Versand mit Anhängen; .UMBRUCH cli.py | SMTP-Konfigurationsdiagnose; kein Mailversand, auch nicht durch `execution_enabled=true`. |
| `sc_mail_search` | Nachrichten durchsuchen; .UMBRUCH cli.py | Diagnose; bei aktiviertem Ausführungsmodus Delegationshinweis auf `mail-connector`, keine eigene Suche. |
| `sc_logs_analyze` | Access-Log-Analyse; .UMBRUCH traffic_analyzer.py | Lokales Apache-/Nginx-Parsing, Bot-/Traffic-Statistik und optionale JSON-Berichte. URL-Redaktion ist keine allgemeine Anonymisierung. |
| `sc_health_check` | HTTP-Endpunkte prüfen; neu | HTTP-/HTTPS-Probes mit Status, Headern und Latenz; Netzwerkzugriff auf angeforderte Ziele. |

## Historische Extraktionsplanung

Die folgenden Notizen beschreiben die ursprünglichen Quellmodule und Ziele.
Sie sind kein aktueller Implementierungsnachweis. Aktuell werden Deployment-
Profile konfiguriert; der Mail-Zugriff folgt der oben beschriebenen
`mail-connector`-Grenze. Das aktuelle Konfigurationsschema zeigt
[config/servercommander.example.toml](config/servercommander.example.toml).

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

## Historisches Konfigurationsbeispiel

Dieses frühe Zielbeispiel aktiviert weder SFTP noch SMTP und belegt keinen
FTS-Cache oder verschlüsselten Credential-Store. Für die Alpha-Konfiguration
das verlinkte aktuelle Beispiel verwenden; Mail-Ausführung bleibt standardmäßig
deaktiviert.

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
persist_reports = false
reports_dir = "~/.servercommander/log_reports"

[health]
timeout = 5
endpoints = [
    "https://example.com/health",
]
```

## Aufgabenvertrag und Review-Register (01.11.2026)

Das Konzept enthält Zielbeschreibungen; maßgeblicher Alpha-Ist-Stand sind die
vorhandenen Handler und ihre Tests. Die folgenden Aufgaben ändern diesen Stand
nicht und autorisieren keine Netzwerkaktion, Mail, Veröffentlichung oder
Produktivbereitstellung. Version bleibt gemäß CONTRIBUTING.md eingefroren.

### SC-TW-01 — Grenze zwischen Konzept und Alpha dokumentieren

**Erledigt am 01.11.2026 (Task 2235):** Acht Toolzeilen gegen deploy.py,
mail.py, Registry und README EN/DE / llms.txt abgeglichen. Historische
Extraktionsplanung und frühes Config-Beispiel gekennzeichnet; aktuelles
Template verlinkt. Prüfung: `tests/test_tools.py` 26 passed, 1 skipped;
acht Tabellenzeilen, interne Links, UTF-8 und `git diff --check` bestanden.
Nur KONZEPT.md und der Unreleased-Changelog geändert; kein Runtime-Wechsel.

- **Ergebnis:** Kennzeichne in der Tooltabelle Ziel und implementierten Status
  getrennt. Beschreibe Deploy als Dry-Run, Mail standardmäßig als Diagnose,
  den opt-in IMAP-Reachability-Test und die Delegation an `mail-connector`.
- **Quelle:** KONZEPT.md Tooltabelle; README.md Abschnitt 12;
  `src/servercommander/deploy.py` weist `dry_run=false` zurück;
  `src/servercommander/mail.py` liefert Diagnose-/Delegationsantworten;
  `tests/test_tools.py` prüft diese Grenzen.
- **Einstufung:** `effort=easy`, `scope=local`, Priorität normal, weil die
  ungetrennte Zielbeschreibung Erwartungen an bereits verfügbare Funktionen weckt.
- **Abnahme:** Acht Tools mit eindeutigem Status; keine behauptete SFTP- oder
  SMTP-Ausführung. README EN/DE und llms.txt widersprechen der Tabelle nicht.
- **Prüfweg:** Tabelle gegen registrierte Handler und vorhandene Tests lesen;
  relative Links, UTF-8 und Dokumentations-Diff prüfen.
- **Abhängigkeiten:** Keine Credentials erforderlich; kein Live-Server-Test.

### SC-TW-02 — Schutzversprechen auf belegte Grenzen präzisieren

- **Ergebnis:** Gleiche pauschale Zero-Egress-/Secret-Leak-Aussagen in
  CONTRIBUTING.md, README EN/DE und llms.txt mit den konkreten Kontrollen ab.
- **Quelle:** README.md Abschnitt 12 und CHANGELOG.md vom 07.10.2026 grenzen
  URL-Redaktion auf Request-/Referer-URLs ein; Pfade, User-Agent, Quelldateinamen
  und bestehende Reports sind nicht allgemein anonymisiert. HTTP-Health-Checks
  und opt-in IMAP-Reachability sind ausdrücklich netzwerkfähig.
- **Einstufung:** `effort=medium`, `scope=local`, Priorität normal wegen
  widersprüchlicher Dokumentation der bestehenden Schutzgrenzen.
- **Abnahme:** EN/DE-Dokumentation unterscheidet lokale Verarbeitung, Telemetrie,
  angeforderte Netzwerkprüfungen und begrenzte URL-Redaktion. Keine allgemeine
  Anonymisierung oder Netzwerksandbox behauptet; Laufzeitverhalten unverändert.
- **Prüfweg:** Claims-Matrix mit Dokumentstelle, Kontrolle und Restgrenze;
  vorhandene URL-Redaktions-Regressionen sowie Dokumentationskonsistenz prüfen.
- **Abhängigkeiten:** Keine neuen Sicherheits- oder Rechtszusagen erfinden;
  keine Mail-/Deployment-Ausführung aktivieren.

### SC-TW-03 — Freigabevertrag für echte Deploy-/Mail-Ausführung entscheiden

- **Ergebnis:** Entscheide vor einer Implementierung, ob und mit welchem
  Freigabe-, Credential-, Ziel- und Rückrollvertrag echte SFTP-Deployments und
  SMTP-Versand unterstützt werden sollen; vorhandene `mail-connector`-Hoheit
  und getrennte Adaptergrenzen berücksichtigen.
- **Quelle:** Konzeptziele `sc_deploy` / `sc_mail_send`; Alpha-Grenzen in
  deploy.py, mail.py und README.md. [Ableitung: Soll/Ist-Lücke]
- **Einstufung:** `effort=special`, `scope=local`, Priorität niedrig, weil der
  sichere Diagnosebetrieb bereits möglich ist und eine Produktentscheidung fehlt.
- **Abnahme:** Explizite dokumentierte Entscheidung einschließlich Nicht-Zielen,
  zulässiger Testziele, Freigabe-/Rollback-Kriterien und Adapterzuständigkeit.
- **Prüfweg:** Entscheidungsreview gegen Alpha-Sicherheitsgrenzen; kein Live-
  Deployment oder Mailversand als Teil dieser Entscheidungsaufgabe.
- **Blocker:** Nutzerentscheidung und gesonderte Autorisierung externer Aktionen.

Review 01.11.2026, TASKWRITER: vorhandenes Konzept, Contribution-Regeln,
Changelog, README, Security, Paketmetadaten und gezielte Handler-/Teststellen
inventarisiert. Drei Punkte formalisiert, keine Aufgaben ausgeführt.
TASKPLAN-Readback: SC-TW-01 → 2235 (easy/local), SC-TW-02 → 2236
(medium/local), SC-TW-03 → 2237 (special/local).

## Historische Quellmodultabelle

| Modul | Herkunft | LoC | Dependencies |
|---|---|---|---|
| deploy.py | interne Extraktionsnotiz | ~221 | paramiko (SFTP) |
| cli.py (Mail) | interne Extraktionsnotiz | ~516 | stdlib (imaplib, smtplib) |
| traffic_analyzer.py | interne Extraktionsnotiz | ~300 | stdlib |
| health.py | neu | ~50 | stdlib (urllib) |
