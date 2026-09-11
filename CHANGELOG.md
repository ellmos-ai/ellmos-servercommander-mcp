# Changelog

All notable changes to this project will be documented in this file.

## 0.1.0-alpha.19 - 2026-09-11

### Discoverability, Visual Design, Bilingual Parity & Governance (Pfad B)
- **10 Governance & Runtime Invariants**: Codified strict execution boundaries (`INV-LOCAL-01` to `INV-SLA-10`) spanning 100% Local-First / Zero-Egress, Fail-Safe Deployment Staging (`dry_run=True`), Sanitized Access-Log Analysis, Non-Blocking Resilient Health Probes, Dry-Run Mail Readiness, Non-Elevation (RunAsInvoker), Process & Working Directory Isolation (`PYTHONSAFEPATH=1`), Native 6-Language i18n Engine, Cloud-Sync Conflict Defense, and Bilingual 48h Security SLA.
- **Third-Party License Audit (`THIRD_PARTY_LICENSES.md`)**: Published exhaustive audit covering direct runtime dependencies (`mcp`, Python stdlib), CLI launcher wrapper (`update-notifier`), optional extras (`paramiko`), and developer tooling (`pytest`, `pytest-asyncio`, `ruff`, `hatchling`), certifying 100% permissive open-source licensing and zero copyleft contamination in default distributions.
- **Discoverability & Marketing Log (`MARKETING-LOG.txt`)**: Established structured marketing ledger defining 4 target personas (Autonomous Agent Engineers, DevOps/SREs, System Administrators, Solo Developers), 5-way competitive matrix against raw bash/SSH and heavy web panels, high-intent discovery search queries (EN/DE), and sibling ecosystem synergies.
- **15-Point Bilingual Navigation Parity**: Restructured `README.md` and `README_de.md` to feature 15 standardized navigation anchors with 100% bilingual parity, including dedicated sections for Third-Party Licenses & Transparency and Marketing & Target Personas.
- **PEP 621 Extended URLs**: Expanded `pyproject.toml` with explicit `[project.urls]` entries pointing to `Third-Party Licenses`, `Marketing Log`, and `LLM Ready` endpoints.
- **AI / LLM Search Index (`llms.txt`)**: Synchronized machine-readable context with version `0.1.0-alpha.19`, current verification timestamp `2026-09-11`, 15-point navigation references, and all 10 governance invariants.
- **Automated Contract Tests**: Expanded `tests/test_repository_hygiene.py` with contract tests verifying third-party license audit compliance, marketing log presence, 10-invariant documentation parity, PEP 621 extended URLs, and 15-anchor quick navigation.

## 0.1.0-alpha.18 - 2026-09-10

### Security & Hardening
- Hardened the npm-to-Python launcher against current-directory package hijacking by binding Python to the trusted package root, enabling safe-path mode where supported (`PYTHONSAFEPATH=1`), and replacing inherited `PYTHONPATH` entries.
- Added regression test `tests/test_launcher_security.py` verifying isolation against rogue working directory packages.

### Technical Hygiene & Lifecycle Governance (Pfad A)
- **CI Matrix Hardening & Bytecode Gate**: Added explicit pre-test bytecode compilation check (`python -m compileall -q src tests`) and standardized pytest invocation (`python -m pytest -ra -v`) to `.github/workflows/ci.yml` ensuring syntax and AST integrity across Linux, Windows, and macOS environments.
- **Automated Lifecycle Governance**: Added `.github/workflows/stale.yml` according to the centrally managed GitHub Actions ecosystem standard (daily 01:30 UTC cron, 30 days inactive, 7 days close, high-priority label exemptions).
- **Multi-Host Sync & Lock Defense**: Hardened `.gitignore` against multi-host file conflicts (`*-conflict-*`, `*.sync-conflict-*`, `*-ASUS-GEI.*`, `*-WORKSTATION-LG.*`, `*-WORKSTATION.*`, `* (copy)*`, `*.sync-temp-*`, `*.tmp`, `*.bak`, `*.swp`), multi-agent locks (`LOCK`, `LOCK.*`, `*.lock`, `LOCK*.txt`, `LOCK.permissions.json`, `uv.lock`), and coverage/packaging caches (`.coverage.*`, `wheelhouse/`, `.wheel-smoke/`), with explicit exemption for `package-lock.json`.
- **PEP 621 & Pytest Configuration**: Configured pytest `testpaths = ["tests"]` and standardized `addopts = "-ra -v"` in `pyproject.toml`.
- **Contract Test Suite Expansion**: Added automated contract tests in `tests/test_repository_hygiene.py` covering gitignore conflict/lock defense, CI bytecode gate, stale workflow compliance, pytest configuration integrity, changelog parity, and end-to-end Python bytecode compilation (suite expanded to 50 passed, 1 skipped | 100% green).
- **Metadata & LLM Context Synchronization**: Synchronized package version to `0.1.0-alpha.18` (Python `0.1.0a18`) across `package.json`, `server.json`, `glama.json`, `pyproject.toml`, and `__version__`, and refreshed `llms.txt` verification timestamp to `2026-09-10`.

## 0.1.0-alpha.17 - 2026-08-24

### Discoverability, Dual Mermaid Diagrams & Multi-OS CI Matrix
- **Dual Mermaid Visualizations**: Integrated 5-tier architecture flowchart (`flowchart TD`) and end-to-end server operations & diagnostics sequence diagram (`sequenceDiagram`) across bilingual README architecture (`README.md` & `README_de.md`).
- **Quick Navigation & Key Capabilities Table**: Added structured 13-anchor jump navigation and bilingual Key Capabilities & Safety Invariants matrix with concrete technical guarantees (100% Local-First / Dry-Run, Non-Elevation, SHA-256 integrity, 6-language i18n).
- **Expanded Sibling Ecosystem Matrix**: Documented full 9-server MCP family and 8 sibling AI infrastructure tools across `ellmos-ai` and `open-bricks`.
- **Multi-OS GitHub Actions CI**: Implemented `.github/workflows/ci.yml` covering `ubuntu-latest`, `windows-latest`, and `macos-latest` across Python 3.10-3.13 and Node.js 18-22 with concurrency cancellation (`cancel-in-progress: true`), Ruff linting gate, and Pytest execution.
- **Bilingual Security Policy**: Hardened `SECURITY.md` with explicit 48-hour response SLA, GitHub Security Advisories link, official security contacts (`security@ellmos.ai`, `security@open-bricks.org`, `lukas@open-bricks.org`, `support@lukasgeiger.com`), and Local-First / Zero-Egress guarantees.
- **PEP 621 Metadata**: Expanded `pyproject.toml` with standard Trove classifiers, DevOps/MCP keywords, and complete `[project.urls]` taxonomy.
- **Automated Contract Tests**: Extended repository hygiene test suite in `tests/test_repository_hygiene.py` to 15 contract tests covering CI matrix integrity, bilingual README parity, Mermaid syntax, Sibling matrix, and PEP 621 compliance (45 passed, 1 skipped including the launcher security regression).
- **LLM Context**: Synchronized `llms.txt` verification timestamp to `2026-08-24`.


### Maintenance & Discoverability
- Synchronized Registry Triad manifests (`server.json`, `glama.json`, `smithery.yaml`) and AI/LLM indexing in `llms.txt` with timestamp `2026-08-16`.
- Enhanced `README.md` and `README_de.md` with test status badges (`37 passed`), ecosystem badges, npx client configuration examples, and cross-linking to sibling developer tools (`sqlite-transit-sync`, `workflowhooker`, `system-explorer`, `companion-for-agy`).
- Extended automated repository hygiene and discoverability test suite in `tests/test_repository_hygiene.py` covering registry parity, manifest consistency, and bilingual README parity (37 passed, 1 skipped).
- Verified npm package manifest (22 files, 0 secrets) and strict zero-configuration leak policy.

## 0.1.0-alpha.17 - 2026-08-14

### Maintenance
- Synchronized `llms.txt` Last-checked verification timestamp (`2026-08-14`) and updated related MCP server family references.
- Added `[tool.ruff]` linting configuration in `pyproject.toml` (target py310, line-length 120, ruff check 100% clean).
- Re-verified complete test suite (34 passed, 1 skipped in pytest), node smoke CLI, and repository hygiene tests.
- Validated npm package manifest (20 files, 0 secrets) and strict exclusion of local configuration.

## 0.1.0-alpha.17 - 2026-08-02

### Maintenance
- Aligned MCP catalog metadata (`server.json`, `glama.json`), Python package version (`pyproject.toml`, `__version__`), and `llms.txt` timestamp (`2026-08-02`) with npm version `0.1.0-alpha.17`.
- Enhanced Discoverability & SEO in `README.md` and `README_de.md` with GFM callout boxes for `llms.txt` & MCP catalog manifests (`server.json`, `glama.json`) and added `open-bricks` umbrella badges.

## 0.1.0-alpha.15 - 2026-07-29

### Maintenance
- Certified `llms.txt` Last-checked timestamp (`2026-07-29`), re-verified unit test suite (34 passed, 1 skipped) and smoke CLI, and verified MCP catalog discoverability metadata (`server.json`, `glama.json`, `package.json`).
- Updated ecosystem overview and checked i18n localization parity across `README.md` and `README_de.md`.
- Removed the unverified legacy `smithery.yaml`; current Smithery publication for local stdio servers requires a validated MCPB bundle.

## 0.1.0-alpha.14 - 2026-07-24

### Fixed
- Correct FileCommander (46) and CodeCommander (22) tool counts in the ecosystem family table; counts now verified against the live MCP `tools/list` surface.
- Align `pyproject.toml` and `servercommander.__version__` with the npm package version (were stuck at 0.1.0a12).

## 0.1.0-alpha.13 - 2026-07-24

### Changed
- Unified the ellmos-ai ecosystem section in README.md and README_de.md: full 9-server MCP family table with refreshed tool counts, AI infrastructure, and desktop software links.
- Added `glama.json` for the Glama MCP directory listing.
- Synced `server.json` version metadata.

## 0.1.0-alpha.12 - 2026-07-23

### Added
- Opt-in live IMAP reachability for `sc_mail_list`. With `[mail].execution_enabled = true` and IMAP credentials present, `sc_mail_list` performs a real, read-only reachability probe (connect + list folders) by **reusing the canonical `mail-connector` module's** `ImapConnector` instead of reimplementing an IMAP client. The module is located with a locate-and-import-with-fallback seam (env override `SERVERCOMMANDER_MAIL_CONNECTOR_PATH`, then default `.MODULES/.CONNECTORS/mail-connector`); a missing/broken module degrades to readiness and never crashes the server. Default stays `execution_enabled = false` (readiness-only, no connections). Message-level read/search remain the `mail-connector` module's domain (they report a `delegated_to` note when execution is enabled); SMTP send and `sc_deploy` stay non-executing until validated against a real server.

### Fixed
- `sc_mail_list` readiness responses no longer advertise the `imap_reachability` capability when the canonical `mail-connector` module cannot be loaded; the fallback now carries a `probe_unavailable` reason (review finding, Fable cross-model review 2026-07-23).
- `sc_health_check` reports malformed endpoint URLs as failed checks instead of aborting the complete health-check batch.
- `sc_deploy` dry-run readiness now also fails when the configured local path cannot be manifested or when the selected protocol is unsupported, and reports the exact `readiness_problems` without changing the existing `missing` field semantics.
- `sc_deploy` manifests now exclude nested symbolic links and expose their count as `skipped_symlinks`, preventing dry-run hashing from silently traversing beyond the selected release directory.

### Maintenance
- Certified `llms.txt` Last-checked timestamp (`2026-07-22`), expanded search phrases (`resilient HTTP health check MCP`, `SQLite deploy history MCP`), and updated discoverability metadata.

## 0.1.0-alpha.11 - 2026-07-03

### Fixed
- Close SQLite deploy-history connections explicitly so Windows can clean up history database files after writes and reads.
- Ignore SQLite WAL/SHM/journal sidecar files created by local deploy-history databases.

### Security
- Harden npm packaging so only the example ServerCommander config is included, while local config, registry credentials, token files, recovery-code files, and private key material stay out of release artifacts.

## 0.1.0-alpha.10 - 2026-06-18

### Added
- `sc_deploy` can now persist dry-run deployment plans to a local SQLite history database via `record_history=true` or `[deploy].persist_history=true`.
- `sc_deploy_status` now reports recent dry-run deployment history, including manifest hashes, readiness, profile, host, local path, and remote path.

### Changed
- `sc_deploy` remains dry-run-only by default; history recording is opt-in unless explicitly enabled in configuration.

## 0.1.0-alpha.9 - 2026-06-17

### Changed
- Add a TTY-guarded `update-notifier` check for interactive CLI starts while keeping MCP stdio output unchanged.

### Fixed
- Align `package.json`, lockfile, `pyproject.toml`, Python `__version__`, and `server.json` metadata after the update-notifier release.

## 0.1.0-alpha.7 - 2026-06-13

### Fixed
- `sc_health_check`: `urlopen()` runs in worker threads via `asyncio.to_thread` + `asyncio.gather`, so concurrent health checks no longer block the MCP event loop.
- npm package file selection now includes only Python source files from `src/`, preventing local `__pycache__` bytecode from entering the tarball.
- Corrected the unreleased changelog entry for log-report persistence to use the implemented `persist_report`, `[logs].persist_reports`, and `[logs].reports_dir` names.

### Added
- `sc_mail_*`: action-specific readiness diagnostics now distinguish IMAP needs for list/read/search from SMTP needs for send, while keeping mail execution disabled in alpha.
- `sc_logs_analyze`: optional persistence of log-analysis JSON reports to a configurable output directory; enabled via `persist_report` per call or `[logs].persist_reports` in `servercommander.toml`.
- Example config keys `[logs].persist_reports` and `[logs].reports_dir` added to `config/servercommander.example.toml`.
- `server.json` with MCP Registry metadata for `io.github.ellmos-ai/ellmos-servercommander-mcp`.
- `llms.txt` with canonical project context, search phrases, disambiguation, current tools, and sibling ellmos MCP servers.
- MIT `LICENSE` text so GitHub and package consumers can detect the repository license directly.

### Changed
- README and README_de: start tables, search/disambiguation context, and ellmos MCP family links.
- Expanded npm and Python package keywords for server operations, MCP hosts, access-log analysis, deployment dry-runs, and health checks.
- Included `server.json`, `llms.txt`, and `LICENSE` in the npm package file list.
