# Third-Party Licenses / Drittanbieter-Lizenzen (Level 1 SBOM)

> **Project:** `ellmos-ai/ellmos-servercommander-mcp`<br>
> Stand: 2026-09-29<br>
> **Plain-Text Companion:** [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt)<br>
> **Repository License:** [MIT License](LICENSE)<br>
> **Repository Attribution Notice:** [NOTICE](NOTICE)<br>
> **Architecture & Privacy:** 100% Local-First, Zero-Egress by default, Unprivileged User-Mode (`RunAsInvoker`)

---

## Executive Summary & Compliance Assurance

**ellmos-servercommander-mcp** is engineered under strict architectural and governance invariants: **100% Local-First, Zero-Egress by default, and unprivileged user-mode execution (`RunAsInvoker`)**. All server diagnostics, Apache/Nginx access log analysis, SHA-256 deployment tree hashing, and health probe verifications execute within local process boundaries without requiring elevated administrative privileges.

All direct, optional, and development dependencies utilized across `ellmos-servercommander-mcp` are distributed under strictly **permissive open-source licenses** (MIT, BSD-2-Clause, Apache-2.0, PSFL) or dynamically linked optional modules (LGPL-2.1). There are **zero viral copyleft (GPL / AGPL) dependencies in core runtime or distribution packages**, ensuring maximum safety and portability for enterprise adoption, AI agent tool dispatching, and automated CI/CD environments.

### Invariant Cross-Reference Matrix

| Invariant ID | Security & Operational Mandate | Technical Enforcement Mechanism | License & Isolation Scope |
|:---|:---|:---|:---|
| `INV-LOCAL-01` | **100% Local-First & Zero-Egress** | Diagnosen and dry-runs run locally; zero unverified outbound telemetry | [PSFL-2.0](https://docs.python.org/3/license.html) |
| `INV-DRY-02` | **Fail-Safe Deployment Staging** | Default `dry_run=True`; SHA-256 tree hashing & profile checks before remote sync | [MIT](LICENSE) |
| `INV-LOG-03` | **Sanitized Access-Log Analysis** | Read-only regex token parsing; bot/error detection without secret leaks | [PSFL-2.0](https://docs.python.org/3/license.html) |
| `INV-PROBE-04` | **Non-Blocking Resilient Health Probes** | Dedicated worker thread HTTP GET; resilient timeout & batch error handling | [PSFL-2.0](https://docs.python.org/3/license.html) |
| `INV-MAIL-05` | **Dry-Run Mail Configuration Status** | Readiness checks report gaps without sending emails; protocol verification only | [PSFL-2.0](https://docs.python.org/3/license.html) |
| `INV-PRIV-06` | **Non-Elevation (`RunAsInvoker`)** | Unprivileged user-mode execution; zero sudo/root/UAC requirements | [MIT](LICENSE) |
| `INV-SEC-07` | **Safe Process & CWD Isolation** | `PYTHONSAFEPATH=1`; hardened launcher against rogue working directory packages | [BSD-2-Clause](https://opensource.org/licenses/BSD-2-Clause) |
| `INV-I18N-08` | **Native Multi-Language i18n Engine** | 6 locales (en, de, es, zh, ja, ru) with automated English fallback | [MIT](LICENSE) |
| `INV-SYNC-09` | **Cloud-Sync Conflict & Lock Defense** | `.gitignore` hardened against sync conflicts (`*-conflict-*`) & multi-agent locks (`LOCK*`) | [MIT](LICENSE) |
| `INV-SLA-10` | **Bilingual Security SLA (48h/5d/30d)** | 48h initial response, 5-day triage assessment, and 30-day remediation SLA via security@ellmos.ai & security@open-bricks.org | [SECURITY.md](SECURITY.md) |

---

## Zero-Copyleft Isolation Guarantee & RunAsInvoker Certification

1. **Zero-Copyleft Guarantee:** No core component of `ellmos-servercommander-mcp` links against, vendors, or invokes any code under GPLv2, GPLv3, AGPLv3, SSPL, or CC-BY-SA licenses. Core runtime dependencies are strictly permissive (MIT, BSD-2-Clause, PSFL-2.0).
2. **Dynamic Linking of Optional Extras:** The optional `[sftp]` extension relies on `paramiko` (LGPL-2.1-or-later). In accordance with LGPL compliance, `paramiko` is dynamically imported at runtime only when explicitly installed; core functionality operates completely without it.
3. **Unprivileged Execution (`RunAsInvoker`):** `ellmos-servercommander-mcp` requires no administrative privileges, no daemon background services, and no root credentials. It operates entirely in unprivileged user space.
4. **Zero-Egress Perimeter:** By default, no network traffic is emitted by `ellmos-servercommander-mcp`. Health checks (`sc_health_check`) execute outbound HTTP GET requests strictly to user-supplied URLs on explicit invocation.

---

## Direct Runtime Dependencies / Direkte Laufzeit-Abhängigkeiten

### 1. `mcp` (Python SDK)
- **Purpose:** Official Model Context Protocol Python SDK for FastMCP stdio server and JSON-RPC protocol handling.
- **License:** MIT License
- **Copyright:** (c) 2024-2026 Anthropic, PBC
- **Repository:** https://github.com/modelcontextprotocol/python-sdk
- **SPDX Identifier:** `MIT`

```text
MIT License

Copyright (c) 2024 Anthropic, PBC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### 2. Python Standard Library
- **Purpose:** Built-in standard library components (`asyncio`, `pathlib`, `json`, `hashlib`, `urllib`, `sqlite3`, `re`, `logging`, `dataclasses`).
- **License:** Python Software Foundation License Version 2 (PSFL-2.0)
- **Copyright:** (c) 2001-2026 Python Software Foundation
- **Repository:** https://github.com/python/cpython
- **SPDX Identifier:** `PSF-2.0`

---

## Node.js CLI & Launcher Dependencies

### 3. `update-notifier`
- **Purpose:** Non-intrusive update notification checks for the global npm CLI launcher wrapper (`bin/ellmos-servercommander.js`).
- **License:** BSD 2-Clause "Simplified" License
- **Copyright:** (c) Sindre Sorhus <sindresorhus@gmail.com> (https://sindresorhus.com)
- **Repository:** https://github.com/yeoman/update-notifier
- **SPDX Identifier:** `BSD-2-Clause`

```text
BSD 2-Clause License

Copyright (c) Sindre Sorhus <sindresorhus@gmail.com> (https://sindresorhus.com)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

## Optional Dependencies / Optionale Erweiterungen

### 4. `paramiko` (optional `[sftp]` extra)
- **Purpose:** Optional SSHv2 protocol and SFTP client library for future direct deployment synchronization.
- **License:** GNU Lesser General Public License Version 2.1 (LGPL-2.1-or-later)
- **Copyright:** (c) 2003-2026 Robey Pointer and Paramiko Contributors
- **Repository:** https://github.com/paramiko/paramiko
- **SPDX Identifier:** `LGPL-2.1-or-later`
- **Dynamic Linking Compliance:** Dynamically imported at runtime only when the optional `[sftp]` extra is explicitly installed; core functionality operates completely without Paramiko.

---

## Development & Build Tooling / Entwicklungs- und Build-Werkzeuge

### 5. `pytest`
- **Purpose:** Testing framework for automated contract, unit, and integration tests.
- **License:** MIT License
- **Copyright:** (c) 2004-2026 Holger Krekel and pytest-dev contributors
- **Repository:** https://github.com/pytest-dev/pytest
- **SPDX Identifier:** `MIT`

---

### 6. `pytest-asyncio`
- **Purpose:** Pytest support for asyncio coroutines and asynchronous tool testing.
- **License:** Apache License 2.0
- **Copyright:** (c) 2012-2026 pytest-dev team
- **Repository:** https://github.com/pytest-dev/pytest-asyncio
- **SPDX Identifier:** `Apache-2.0`

---

### 7. `ruff`
- **Purpose:** Extremely fast Python linter and code formatter.
- **License:** MIT License / Apache License 2.0
- **Copyright:** (c) Astral Software Inc.
- **Repository:** https://github.com/astral-sh/ruff
- **SPDX Identifier:** `MIT OR Apache-2.0`

---

### 8. `hatchling`
- **Purpose:** Standards-compliant modern PEP 517 build backend.
- **License:** MIT License
- **Copyright:** (c) Ofek Lev
- **Repository:** https://github.com/pypa/hatch
- **SPDX Identifier:** `MIT`

---

## Verification & Audit Summary (Level 1 SBOM)

| Component | Category | License Type | SPDX ID | Permissive / Safe | RunAsInvoker Safe |
|---|---|---|---|:---:|:---:|
| `mcp` | Direct Runtime | MIT License | `MIT` | Yes | Yes |
| Python stdlib | Direct Runtime | Python Software Foundation | `PSF-2.0` | Yes | Yes |
| `update-notifier` | CLI Wrapper | BSD 2-Clause | `BSD-2-Clause` | Yes | Yes |
| `paramiko` | Optional Extra | GNU LGPL v2.1 | `LGPL-2.1-or-later` | Yes (Dynamic link) | Yes |
| `pytest` | Dev / Test | MIT License | `MIT` | Yes | Yes |
| `pytest-asyncio` | Dev / Test | Apache 2.0 | `Apache-2.0` | Yes | Yes |
| `ruff` | Dev / Lint | MIT OR Apache-2.0 | `MIT OR Apache-2.0` | Yes | Yes |
| `hatchling` | Build System | MIT License | `MIT` | Yes | Yes |

All packaged distribution artifacts are fully compliant with open-source licensing standards, free of unverified binary blobs, and completely transparent for enterprise and individual adoption.
