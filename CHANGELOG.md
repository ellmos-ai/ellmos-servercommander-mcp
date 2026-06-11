# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- `sc_logs_analyze`: `urlopen()` now runs in a thread via `asyncio.to_thread` + `asyncio.gather`, so concurrent health checks no longer block the MCP event loop.

### Added
- `sc_logs_analyze`: optional persistence of log-analysis JSON reports to a configurable output directory; enabled via `report_output_dir` in `servercommander.toml`.
- Example config key `report_output_dir` added to `config/servercommander.example.toml`.
- `server.json` with MCP Registry metadata for `io.github.ellmos-ai/ellmos-servercommander-mcp`.
- `llms.txt` with canonical project context, search phrases, disambiguation, current tools, and sibling ellmos MCP servers.
- MIT `LICENSE` text so GitHub and package consumers can detect the repository license directly.

### Changed
- README and README_de: start tables, search/disambiguation context, and ellmos MCP family links.
- Expanded npm and Python package keywords for server operations, MCP hosts, access-log analysis, deployment dry-runs, and health checks.
- Included `server.json`, `llms.txt`, and `LICENSE` in the npm package file list.
