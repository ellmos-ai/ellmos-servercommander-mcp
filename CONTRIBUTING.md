# Contributing to ellmos-servercommander-mcp / Mitwirken an ellmos-servercommander-mcp

[English](#english) | [Deutsch](#deutsch)

---

<a id="english"></a>
## English

Thank you for your interest in contributing to **ellmos-servercommander-mcp** (`ellmos-ai/ellmos-servercommander-mcp`), the authoritative Model Context Protocol (MCP) server for local-first, dry-run-first server operations, diagnostics, deployment staging, log analysis, and resilient health checks.

### 1. Architectural Principles & 10 Governance Invariants

All contributions must strictly adhere to our core architectural invariants:

1. **100% Local-First & Zero-Egress (`INV-LOCAL-01`)**: All server diagnostics, Apache/Nginx access log parsing, and deployment manifest hashing run strictly locally within process boundaries. Zero unverified outbound network telemetry.
2. **Fail-Safe Deployment Staging (`INV-DRY-02`)**: Deployment operations default to `dry_run=True`. Recursive SHA-256 tree hashing and profile readiness checks must complete before any remote file transfer or target mutations occur.
3. **Sanitized Access-Log Analysis (`INV-LOG-03`)**: Read-only log parsing using strict regular expression extraction. Error spikes, bot scanners, and suspicious path traversals are analyzed without leaking credentials, query secrets, or sensitive session tokens.
4. **Non-Blocking Resilient Health Probes (`INV-PROBE-04`)**: Endpoint health checks execute within dedicated worker threads with strict timeouts and resilient batch handling without aborting test batches.
5. **Dry-Run Mail Configuration Status (`INV-MAIL-05`)**: Mail handlers report configuration readiness and connectivity gaps without transmitting emails or mutating mailboxes by default.
6. **Non-Elevation User Mode (`INV-PRIV-06`)**: Pure `RunAsInvoker` user mode execution. The server and its CLI launchers require zero administrative elevation, zero sudo/root permissions, and zero system daemon registrations.
7. **Safe Process & Working Directory Isolation (`INV-SEC-07`)**: Safe subprocess isolation enforced by `PYTHONSAFEPATH=1`. Hardened against rogue Python packages or DLLs in caller working directories.
8. **Native Multi-Language i18n Engine (`INV-I18N-08`)**: Full 6-language internationalization support (English, German, Spanish, Chinese, Japanese, Russian) across all tool declarations, schema descriptions, and diagnostic outputs with automated English fallback.
9. **Cloud-Sync Conflict & Multi-Agent Lock Defense (`INV-SYNC-09`)**: Hardened `.gitignore` and `.npmignore` preventing sync conflicts (`*-conflict-*`, `*.sync-conflict-*`), multi-host collision tokens, and multi-agent locks (`LOCK*`, `LOCK.user.*`, `LOCK.until.*`, `LOCK.condition.*`).
10. **Bilingual Security SLA (`INV-SLA-10`)**: Binding 48-hour initial response SLA, 5-business-day triage assessment, and 30-day remediation commitment for all reported vulnerabilities via `security@ellmos.ai` and `security@open-bricks.org`.

### 2. Plan D Local Development Workflow

In accordance with our cross-system architecture (Plan D), the local git repository at `C:\_Local_DEV\repos\ellmos-servercommander-mcp` serves as the authoritative **Source of Truth**. Development, testing, and commits must take place exclusively in the canonical local clone.

```bash
# Clone the canonical repository
git clone https://github.com/ellmos-ai/ellmos-servercommander-mcp.git C:\_Local_DEV\repos\ellmos-servercommander-mcp
cd C:\_Local_DEV\repos\ellmos-servercommander-mcp

# Run automated test suite
pytest -ra -v

# Run static linting
ruff check .

# Verify Python bytecode compilation
python -m compileall -q src tests .
```

### 3. Version Freeze Discipline (`T-20260920-167562623`)

`ellmos-servercommander-mcp` operates under strict version-freeze discipline. Version `0.1.0-alpha.21` (Python `0.1.0a21`) in `pyproject.toml`, `package.json`, and documentation badges must not be incremented without explicit release authorization. All technical hygiene, documentation updates, and workflow additions are documented under `## [Unreleased]` in `CHANGELOG.md`.

### 4. Quality Gates

Before submitting a pull request, verify that all local quality gates pass:
1. `pytest`: 100% green test execution across all contract and unit suites.
2. `ruff check .`: Zero lint errors.
3. `python -m compileall -q src tests .`: Zero bytecode compilation errors.
4. `git diff --check`: Zero whitespace anomalies.
5. `git diff -G"version = "`: Zero unauthorized version bumps.

### 5. Statutory Notice (§ 521 BGB) & Liability Disclaimer

This software is provided free of charge as open-source software under the MIT License. In accordance with statutory German law (§ 521 BGB - Gefälligkeitsrecht), liability for defects in quality and title is strictly limited to intentional misconduct (*Vorsatz*) and gross negligence (*grobe Fahrlässigkeit*).

---

<a id="deutsch"></a>
## Deutsch

Vielen Dank für dein Interesse an einer Mitwirkung bei **ellmos-servercommander-mcp** (`ellmos-ai/ellmos-servercommander-mcp`), dem maßgeblichen Model Context Protocol (MCP) Server für lokale Server-Operationen, Diagnosen, Deployment-Staging im Dry-Run-Modus, Log-Analyse und robuste HTTP-Health-Checks.

### 1. Architektur-Prinzipien & 10 Governance-Invarianten

Alle Beiträge müssen unsere verbindlichen Kern-Invarianten strikt einhalten:

1. **100% Local-First & Zero-Egress (`INV-LOCAL-01`)**: Alle Server-Diagnosen, Apache/Nginx-Log-Analysen und Deployment-Manifest-Hashes laufen ausschließlich lokal innerhalb der Prozessgrenzen. Null unautorisierte ausgehende Telemetrie.
2. **Ausfallsicheres Deployment-Staging (`INV-DRY-02`)**: Deployment-Operationen nutzen standardmäßig `dry_run=True`. Rekursive SHA-256-Hashbäume und Profilprüfungen müssen abgeschlossen sein, bevor Remote-Übertragungen oder Dateiänderungen stattfinden.
3. **Bereinigte Access-Log-Analyse (`INV-LOG-03`)**: Schreibgeschütztes Log-Parsing über strikte reguläre Ausdrücke. Fehlerspitzen, Bot-Scanner und verdächtige Pfadtraversierungen werden erkannt, ohne Anmeldedaten, Query-Parameter oder Tokens preiszugeben.
4. **Nicht-blockierende robuste Health-Probes (`INV-PROBE-04`)**: HTTP-Endpunktprüfungen laufen in dedizierten Worker-Threads mit strikten Timeouts und robuster Stapelfehlerbehandlung ohne Testabbrüche.
5. **Dry-Run Mail-Konfigurationsstatus (`INV-MAIL-05`)**: Mail-Handler melden Konfigurationsbereitschaft und Protokolllücken, ohne standardmäßig E-Mails zu versenden oder Postfächer zu verändern.
6. **Rechtefreier Benutzermodus (`INV-PRIV-06`)**: Reiner `RunAsInvoker`-Benutzermodus. Der Server und seine Starter erfordern keinerlei administrative Rechte, kein sudo/root und keine Daemon-Registrierung.
7. **Sichere Prozess- und Arbeitsverzeichnis-Isolation (`INV-SEC-07`)**: Sichere Subprozess-Isolation über `PYTHONSAFEPATH=1`. Schutz vor bösartigen Python-Paketen oder DLLs im Aufrufer-Arbeitsverzeichnis.
8. **Native 6-Sprachen i18n-Engine (`INV-I18N-08`)**: Vollständige Lokalisierung in 6 Sprachen (Englisch, Deutsch, Spanisch, Chinesisch, Japanisch, Russisch) für alle Tools, Parameterschemata und Diagnosen mit automatischem englischen Fallback.
9. **Cloud-Sync Konflikt- & Lock-Schutz (`INV-SYNC-09`)**: Gehärtete `.gitignore` und `.npmignore` gegen Synchronisationskonflikte (`*-conflict-*`, `*.sync-conflict-*`), Multi-Host-Konfliktdateien und Multi-Agenten-Locks (`LOCK*`, `LOCK.user.*`, `LOCK.until.*`, `LOCK.condition.*`).
10. **Zweisprachige Sicherheits-SLA (`INV-SLA-10`)**: Verbindliche 48-Stunden-Erstantwortgarantie, 5-Werktage-Triage-Zusage und 30-Tage-Behebungszusage für Sicherheitsmeldungen über `security@ellmos.ai` und `security@open-bricks.org`.

### 2. Plan D Lokaler Entwicklungsworkflow

Gemäß unserer systemweiten Architektur (Plan D) bildet das lokale Repository unter `C:\_Local_DEV\repos\ellmos-servercommander-mcp` die alleinige maßgebliche **Source of Truth**. Entwicklung, Tests und Commits finden ausschließlich im kanonischen lokalen Klon statt.

```bash
# Kanonischen Klon verwenden
git clone https://github.com/ellmos-ai/ellmos-servercommander-mcp.git C:\_Local_DEV\repos\ellmos-servercommander-mcp
cd C:\_Local_DEV\repos\ellmos-servercommander-mcp

# Testsuite ausführen
pytest -ra -v

# Linter ausführen
ruff check .

# Python-Bytecode kompilieren
python -m compileall -q src tests .
```

### 3. Version Freeze Disziplin (`T-20260920-167562623`)

`ellmos-servercommander-mcp` unterliegt einer strikten Version-Freeze-Disziplin. Die Version `0.1.0-alpha.21` (Python `0.1.0a21`) in `pyproject.toml`, `package.json` und Dokumentations-Badges darf ohne ausdrückliche Freigabe nicht erhöht werden. Alle technischen Hygiene-Arbeiten und Workflow-Erweiterungen werden unter `## [Unreleased]` in `CHANGELOG.md` dokumentiert.

### 4. Quality Gates

Vor dem Einreichen eines Pull Requests müssen alle lokalen Prüfstufen fehlerfrei durchlaufen:
1. `pytest`: 100% grüne Testergebnisse über alle Vertrags- und Modultests.
2. `ruff check .`: Null Linter-Fehler.
3. `python -m compileall -q src tests .`: Null Bytecode-Kompilierungsfehler.
4. `git diff --check`: Null Whitespace-Fehler.
5. `git diff -G"version = "`: Null unautorisierte Versionsänderungen.

### 5. Gesetzlicher Hinweis (§ 521 BGB) & Haftungsausschluss

Diese Software wird unentgeltlich als Open-Source-Software unter der MIT-Lizenz bereitgestellt. Gemäß den gesetzlichen Bestimmungen des deutschen Rechts (§ 521 BGB - Gefälligkeitsrecht) ist die Haftung für Sach- und Rechtsmängel auf Vorsatz und grobe Fahrlässigkeit beschränkt.
