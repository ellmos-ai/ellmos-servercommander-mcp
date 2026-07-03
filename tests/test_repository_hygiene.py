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
