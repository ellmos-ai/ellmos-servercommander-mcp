import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _git_check_ignore(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        check=False,
        cwd=REPO_ROOT,
    )
    return result.returncode == 0


def _npmignore_patterns() -> set[str]:
    return {
        line.strip()
        for line in (REPO_ROOT / ".npmignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_local_secret_and_credential_files_are_ignored():
    ignored = [
        ".env",
        ".env.production",
        ".npmrc",
        ".pypirc",
        "secrets.json",
        "credentials.json",
        "token.json",
        "tokens.json",
        "deploy.token.json",
        "npm_recovery_codes.txt",
        "deploy-history.db-wal",
        "deploy-history.db-shm",
        "deploy-history.sqlite-wal",
        "deploy-history.sqlite-shm",
        "deploy-history.sqlite3-wal",
        "deploy-history.sqlite3-shm",
        "id_rsa",
        "id_ed25519",
        "private.pem",
        "client.key",
    ]

    for path in ignored:
        assert _git_check_ignore(path), path


def test_public_examples_and_package_metadata_remain_trackable():
    trackable = [
        ".env.example",
        "package.json",
        "package-lock.json",
        "server.json",
        "config/servercommander.example.toml",
    ]

    for path in trackable:
        assert not _git_check_ignore(path), path


def test_npm_package_excludes_local_config_and_secret_artifacts():
    required_patterns = {
        "servercommander.toml",
        "config/servercommander.toml",
        "config/*.local.toml",
        "config/*.secret.toml",
        ".npmrc",
        ".pypirc",
        "token.json",
        "tokens.json",
        "*.token.json",
        "*recovery*codes*.txt",
        "*.pem",
        "*.key",
        "*.p12",
        "*.pfx",
        "*.kdbx",
        "id_rsa",
        "id_ed25519",
        "id_ecdsa",
        "id_dsa",
    }

    assert required_patterns <= _npmignore_patterns()


def test_npm_package_manifest_only_includes_example_config():
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    files = set(package["files"])

    assert "config/" not in files
    assert "config/servercommander.example.toml" in files


def test_package_json_version_matches_python_and_server_metadata():
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    npm_version = package["version"]

    server_json = json.loads((REPO_ROOT / "server.json").read_text(encoding="utf-8"))
    assert server_json["version"] == npm_version
    assert server_json["packages"][0]["version"] == npm_version

    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pyproject_match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', pyproject_text)
    assert pyproject_match, "pyproject.toml must declare a [project] version"

    init_text = (REPO_ROOT / "src" / "servercommander" / "__init__.py").read_text(encoding="utf-8")
    init_match = re.search(r'__version__\s*=\s*"([^"]+)"', init_text)
    assert init_match, "src/servercommander/__init__.py must declare __version__"

    npm_python_version = npm_version.replace("-alpha.", "a")
    assert pyproject_match.group(1) == npm_python_version
    assert init_match.group(1) == npm_python_version


def test_glama_and_smithery_manifests_exist_and_match():
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    npm_version = package["version"]

    glama_json = json.loads((REPO_ROOT / "glama.json").read_text(encoding="utf-8"))
    assert glama_json["version"] == npm_version
    assert glama_json["name"] == "ellmos-servercommander-mcp"

    smithery_yaml = (REPO_ROOT / "smithery.yaml").read_text(encoding="utf-8")
    assert "startCommand:" in smithery_yaml
    assert "ellmos-servercommander-mcp" in smithery_yaml


def test_llms_txt_contains_required_discoverability_sections():
    llms_text = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")
    assert "Last-checked: 2026-09-10" in llms_text
    assert "sc_health_check" in llms_text
    assert "sc_logs_analyze" in llms_text
    assert "sc_deploy" in llms_text
    assert "sc_deploy_status" in llms_text
    assert "sc_mail_list" in llms_text
    assert "server.json" in llms_text
    assert "glama.json" in llms_text
    assert "smithery.yaml" in llms_text
    assert "SECURITY.md" in llms_text
    assert "5-Tier System" in llms_text


def test_readme_and_readme_de_have_badge_and_ecosystem_parity():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    for keyword in [
        "pytest-50%20passed",
        "smithery.yaml",
        "sqlite-transit-sync",
        "workflowhooker",
        "system-explorer",
        "companion-for-agy",
        "open-bricks",
        "ellmos--ai",
        "SECURITY.md",
    ]:
        assert keyword in readme_en, f"'{keyword}' missing in README.md"
        assert keyword in readme_de, f"'{keyword}' missing in README_de.md"


def test_readme_and_readme_de_quick_navigation_and_jump_links():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "## Quick Navigation" in readme_en
    assert "## Schnellnavigation" in readme_de

    en_links = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", readme_en)
    de_links = re.findall(r"\[([^\]]+)\]\(#([^\)]+)\)", readme_de)

    assert len(en_links) >= 10, f"Expected >= 10 quick nav links in EN, got {len(en_links)}"
    assert len(de_links) >= 10, f"Expected >= 10 quick nav links in DE, got {len(de_links)}"


def test_readme_and_readme_de_dual_mermaid_diagrams():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    for doc, name in [(readme_en, "README.md"), (readme_de, "README_de.md")]:
        assert "flowchart TD" in doc, f"Flowchart missing in {name}"
        assert "sequenceDiagram" in doc, f"Sequence diagram missing in {name}"
        assert "sc_health_check" in doc, f"sc_health_check missing in {name}"
        assert "sc_logs_analyze" in doc, f"sc_logs_analyze missing in {name}"
        assert "sc_deploy" in doc, f"sc_deploy missing in {name}"


def test_key_capabilities_and_safety_invariants_table_parity():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "## Key Capabilities & Safety Invariants" in readme_en
    assert "## Kernfähigkeiten & Sicherheitsinvarianten" in readme_de

    for key in [
        "Local-First",
        "Non-Elevation",
        "SHA-256",
        "i18n",
    ]:
        assert key in readme_en, f"'{key}' missing in README.md capabilities table"
        assert key in readme_de, f"'{key}' missing in README_de.md capabilities table"


def test_sibling_ecosystem_matrix_parity():
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    siblings = [
        "FileCommander",
        "CodeCommander",
        "Clatcher",
        "n8n Manager",
        "ControlCenter",
        "Homebase",
        "ServerCommander",
        "Blender Use",
        "Open Compute",
        "BACH",
        "ProFiler",
        "DevCenter",
    ]

    for sibling in siblings:
        assert sibling in readme_en, f"Sibling '{sibling}' missing in README.md"
        assert sibling in readme_de, f"Sibling '{sibling}' missing in README_de.md"


def test_security_policy_bilingual_sla_and_contacts():
    security_md = REPO_ROOT / "SECURITY.md"
    assert security_md.exists(), "SECURITY.md must exist in repository root"
    assert not _git_check_ignore("SECURITY.md"), "SECURITY.md must remain trackable"

    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    files = set(package["files"])
    assert "SECURITY.md" in files, "SECURITY.md must be included in package.json files list"

    content = security_md.read_text(encoding="utf-8")
    assert "Security Policy / Sicherheitsrichtlinie" in content
    assert "Execution Safety and Local-First Guarantees" in content
    assert "Ausführungssicherheit und Local-First Garantien" in content
    assert "security@ellmos.ai" in content
    assert "security@open-bricks.org" in content
    assert "48 hours" in content or "48 Stunden" in content
    assert "github.com/ellmos-ai/ellmos-servercommander-mcp/security/advisories" in content


def test_third_party_licenses_inventory_and_pep639():
    licenses_md = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert licenses_md.exists(), "THIRD_PARTY_LICENSES.md must exist in repository root"
    assert not _git_check_ignore("THIRD_PARTY_LICENSES.md"), "THIRD_PARTY_LICENSES.md must remain trackable"

    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    files = set(package["files"])
    assert "THIRD_PARTY_LICENSES.md" in files, "THIRD_PARTY_LICENSES.md must be included in package.json files list"

    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]' in pyproject_text

    content = licenses_md.read_text(encoding="utf-8")
    assert "Third-Party Licenses / Drittanbieter-Lizenzen" in content
    assert "mcp" in content
    assert "update-notifier" in content
    assert "paramiko" in content
    assert "pytest" in content
    assert "ruff" in content


def test_pyproject_pep621_classifiers_and_urls():
    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "classifiers = [" in pyproject_text
    assert "Development Status :: 4 - Beta" in pyproject_text
    assert "Operating System :: OS Independent" in pyproject_text
    assert "Topic :: System :: Systems Administration" in pyproject_text

    assert "[project.urls]" in pyproject_text
    assert "Homepage = " in pyproject_text
    assert "Documentation = " in pyproject_text
    assert "Repository = " in pyproject_text
    assert "Bug Tracker" in pyproject_text
    assert "Changelog = " in pyproject_text
    assert "Security = " in pyproject_text
    assert "Parent Organization" in pyproject_text
    assert "Umbrella Ecosystem" in pyproject_text


def test_ci_workflow_multi_os_matrix_and_concurrency():
    ci_path = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    assert ci_path.exists(), ".github/workflows/ci.yml must exist"

    content = ci_path.read_text(encoding="utf-8")
    assert "cancel-in-progress: true" in content
    assert "ubuntu-latest" in content
    assert "windows-latest" in content
    assert "macos-latest" in content
    assert "actions/checkout@v4" in content
    assert "actions/setup-python@v5" in content
    assert "actions/setup-node@v4" in content
    assert "ruff check ." in content
    assert "python -m compileall -q src tests" in content
    assert "python -m pytest" in content


def test_gitignore_conflict_and_lock_hygiene():
    ignored_conflicts_and_locks = [
        "file-conflict-20260910.txt",
        "nested/path/sample.sync-conflict-2026.json",
        "sync-temp-001.tmp",
        "doc.md-WORKSTATION-LG",
        "README.md-ASUS-GEI.md",
        "config-LAPTOP.toml",
        "patch.orig",
        "patch.rej",
        "backup.bak",
        "editor.swp",
        "file.txt~",
        "LOCK",
        "LOCK.user",
        "LOCK.until.2026",
        "LOCK-CACHE.md",
        "LOCK.permissions.json",
        "LOCK.txt",
        "wheelhouse/package.whl",
        ".wheel-smoke/status.json",
    ]

    for item in ignored_conflicts_and_locks:
        assert _git_check_ignore(item), f"'{item}' must be ignored by .gitignore"

    assert not _git_check_ignore("package-lock.json"), "package-lock.json must NOT be ignored"


def test_stale_workflow_present_and_configured():
    stale_path = REPO_ROOT / ".github" / "workflows" / "stale.yml"
    assert stale_path.exists(), ".github/workflows/stale.yml must exist"

    content = stale_path.read_text(encoding="utf-8")
    assert "name: 'Stale Issues & PRs'" in content
    assert "cron: '30 1 * * *'" in content
    assert "actions/stale@v9" in content
    assert "days-before-stale: 30" in content
    assert "days-before-close: 7" in content
    assert "stale-issue-label: 'stale'" in content


def test_pytest_configuration_integrity():
    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.pytest.ini_options]" in pyproject_text
    assert 'pythonpath = ["src"]' in pyproject_text
    assert 'testpaths = ["tests"]' in pyproject_text
    assert "addopts = " in pyproject_text


def test_python_bytecode_compilation_clean():
    import compileall

    src_dir = REPO_ROOT / "src"
    tests_dir = REPO_ROOT / "tests"

    assert compileall.compile_dir(str(src_dir), quiet=1, force=True)
    assert compileall.compile_dir(str(tests_dir), quiet=1, force=True)


def test_pyproject_dependencies_and_build_system():
    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires = ["hatchling"]' in pyproject_text
    assert 'build-backend = "hatchling.build"' in pyproject_text
    assert "dependencies = [" in pyproject_text
    assert '"mcp>=1.0.0"' in pyproject_text
    assert "[project.optional-dependencies]" in pyproject_text
    assert "sftp = " in pyproject_text
    assert "dev = " in pyproject_text
    assert "[tool.hatch.build.targets.wheel]" in pyproject_text
    assert 'packages = ["src/servercommander"]' in pyproject_text
