# Third-Party Licenses / Drittanbieter-Lizenzen

This document lists the third-party open-source software libraries, packages, and components utilized by **ellmos-servercommander-mcp**, along with their respective license types, copyright notices, and local-first governance guarantees.

Dieses Dokument führt die von **ellmos-servercommander-mcp** verwendeten quelloffenen Bibliotheken, Pakete und Komponenten von Drittanbietern inklusive Lizenztyp, Urheberrechtshinweisen und Local-First-Sicherheitsgarantien auf.

Stand: 2026-09-11

---

## License Overview & Compliance Guarantees

- **Primary Repository License:** MIT License (c) 2026 Lukas Geiger / ellmos-ai
- **License Permissiveness:** 100% Permissive Open Source (MIT, BSD-2-Clause, Apache-2.0, PSFL-2.0) and LGPL-2.1 dynamic library linking.
- **Copyleft Stance:** No strong viral copyleft (GPL / AGPL) dependencies in core runtime or distribution packages.
- **Local-First & Zero-Egress:** All operations execute locally in diagnostic or dry-run mode. Zero telemetry, zero unverified outbound network requests.
- **Non-Elevation / RunAsInvoker:** Server operations operate entirely within standard unprivileged user space; zero administrative or root/sudo elevation required.

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

## Verification & Audit Summary

| Component | Category | License Type | SPDX ID | Permissive / Safe |
|---|---|---|---|:---:|
| `mcp` | Direct Runtime | MIT License | `MIT` | Yes |
| Python stdlib | Direct Runtime | Python Software Foundation | `PSF-2.0` | Yes |
| `update-notifier` | CLI Wrapper | BSD 2-Clause | `BSD-2-Clause` | Yes |
| `paramiko` | Optional Extra | GNU LGPL v2.1 | `LGPL-2.1-or-later` | Yes (Dynamic link) |
| `pytest` | Dev / Test | MIT License | `MIT` | Yes |
| `pytest-asyncio` | Dev / Test | Apache 2.0 | `Apache-2.0` | Yes |
| `ruff` | Dev / Lint | MIT OR Apache-2.0 | `MIT OR Apache-2.0` | Yes |
| `hatchling` | Build System | MIT License | `MIT` | Yes |

All packaged distribution artifacts are fully compliant with open-source licensing standards, free of unverified binary blobs, and completely transparent for enterprise and individual adoption.
