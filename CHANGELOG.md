# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Fixed
- `sc_deploy` dry-run readiness now also fails when the configured local path cannot be manifested or when the selected protocol is unsupported, and reports the exact `readiness_problems` without changing the existing `missing` field semantics.
- `sc_deploy` manifests now exclude nested symbolic links and expose their count as `skipped_symlinks`, preventing dry-run hashing from silently traversing beyond the selected release directory.

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
