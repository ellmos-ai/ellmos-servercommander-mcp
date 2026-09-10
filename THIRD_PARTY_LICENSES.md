# Third-Party Licenses / Drittanbieter-Lizenzen

This document lists the third-party open-source software libraries, packages, and components utilized by **ellmos-servercommander-mcp**, along with their respective license types and copyright notices.

Dieses Dokument führt die von **ellmos-servercommander-mcp** verwendeten quelloffenen Bibliotheken, Pakete und Komponenten von Drittanbietern inklusive Lizenztyp und Urheberrechtshinweisen auf.

---

## Direct Runtime Dependencies / Direkte Laufzeit-Abhängigkeiten

### 1. `mcp` (Python SDK)
- **Purpose:** Official Model Context Protocol (MCP) Python SDK for stdio / JSON-RPC server and client interfaces.
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

### 2. `update-notifier` (Node.js Wrapper)
- **Purpose:** CLI update notifications for interactive terminal sessions.
- **License:** BSD 2-Clause License
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

## Optional Runtime Dependencies / Optionale Laufzeit-Abhängigkeiten

### 3. `paramiko` (`[sftp]` Extra)
- **Purpose:** SSHv2 protocol and SFTP client library for secure deployment execution.
- **License:** GNU Lesser General Public License v2.1 or later (LGPL-2.1-or-later)
- **Copyright:** (c) 2003-2026 Jeff Forcier, Robey Pointer, and Paramiko contributors
- **Repository:** https://github.com/paramiko/paramiko
- **SPDX Identifier:** `LGPL-2.1-or-later`

---

## Build, Test & Tooling Dependencies / Entwicklungs- & Testwerkzeuge

### 4. `hatchling`
- **Purpose:** Modern PEP 517 build backend for wheel and source distribution packaging.
- **License:** MIT License
- **Copyright:** (c) 2022-present Ofek Lev <oss@ofek.dev>
- **Repository:** https://github.com/pypa/hatch
- **SPDX Identifier:** `MIT`

### 5. `pytest`
- **Purpose:** Python testing framework for unit, integration, and security regression tests.
- **License:** MIT License
- **Copyright:** (c) 2004-2026 Holger Krekel and pytest-dev team
- **Repository:** https://github.com/pytest-dev/pytest
- **SPDX Identifier:** `MIT`

### 6. `pytest-asyncio`
- **Purpose:** Pytest extension for asynchronous test execution.
- **License:** Apache License 2.0
- **Copyright:** (c) 2015-2026 Tin Tvrtković and contributors
- **Repository:** https://github.com/pytest-dev/pytest-asyncio
- **SPDX Identifier:** `Apache-2.0`

### 7. `ruff`
- **Purpose:** Fast Python linter, code formatter, and import sorter.
- **License:** MIT License / Apache License 2.0
- **Copyright:** (c) 2023-2026 Astral Software Inc.
- **Repository:** https://github.com/astral-sh/ruff
- **SPDX Identifier:** `MIT OR Apache-2.0`
