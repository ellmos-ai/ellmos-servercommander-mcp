import subprocess
from pathlib import Path


def _git_check_ignore(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        check=False,
        cwd=Path(__file__).resolve().parents[1],
    )
    return result.returncode == 0


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
