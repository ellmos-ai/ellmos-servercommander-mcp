from servercommander.config import load_config


def test_load_config_defaults_when_missing():
    config = load_config("missing-servercommander.toml")

    assert config.server_name == "ellmos-servercommander"
    assert config.language == "en"
    assert config.deploy_profiles == {}
    assert config.health == {}


def test_load_config_with_profiles(tmp_path):
    config_path = tmp_path / "servercommander.toml"
    config_path.write_text(
        """
[server]
name = "ellmos-servercommander"
language = "de"

[deploy]
history_db = "./deploy-history.db"
persist_history = true

[deploy.profiles.example]
host = "sftp.example.com"
user = "deploy"
local_path = "./dist"
remote_path = "/var/www/example"

[health]
timeout = 2
endpoints = ["http://127.0.0.1/health"]
""".strip(),
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.deploy_profile("example")["host"] == "sftp.example.com"
    assert config.deploy["history_db"] == "./deploy-history.db"
    assert config.deploy["persist_history"] is True
    assert config.language == "de"
    assert config.health["timeout"] == 2


def test_env_language_overrides_config(tmp_path, monkeypatch):
    config_path = tmp_path / "servercommander.toml"
    config_path.write_text('[server]\nlanguage = "de"\n', encoding="utf-8")
    monkeypatch.setenv("SERVERCOMMANDER_LANG", "ru-RU")

    config = load_config(config_path)

    assert config.language == "ru-RU"
