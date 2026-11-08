"""The pytest base temp is anchored at the repo and never lands in OneDrive (T-20261107-245040014).

On 2026-11-01 a run of this suite with the working directory inside OneDrive wrote ``.pytest_tmp`` into the control
tree: ``--basetemp=.pytest_tmp`` in pyproject.toml is relative, and pytest resolves it against the current working
directory. ``tests/conftest.py`` now anchors a relative base temp at the rootdir and refuses a base temp that sits
inside OneDrive.
"""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

_conftest_path = Path(__file__).with_name("conftest.py")
_spec = importlib.util.spec_from_file_location("_basetemp_guard_conftest", _conftest_path)
_conftest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_conftest)


@pytest.fixture(autouse=True)
def _no_onedrive_environment(monkeypatch):
    """The developer machine's own OneDrive variables must not decide these cases."""
    for name in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial"):
        monkeypatch.delenv(name, raising=False)


def _configure(root: Path, basetemp: str | None) -> SimpleNamespace:
    config = SimpleNamespace(rootpath=root, option=SimpleNamespace(basetemp=basetemp))
    _conftest.pytest_configure(config)
    return config


def test_relative_basetemp_is_anchored_at_the_rootdir_not_the_working_directory(tmp_path, monkeypatch):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    repo = tmp_path / "repo"

    config = _configure(repo, ".pytest_tmp")

    assert Path(config.option.basetemp) == (repo / ".pytest_tmp").resolve()
    assert not Path(config.option.basetemp).is_relative_to(elsewhere.resolve())


def test_absolute_basetemp_outside_onedrive_is_kept(tmp_path):
    target = tmp_path / "scratch" / "base"

    config = _configure(tmp_path / "repo", str(target))

    assert Path(config.option.basetemp) == target.resolve()


def test_missing_basetemp_is_left_alone(tmp_path):
    assert _configure(tmp_path, None).option.basetemp is None


def test_refuses_a_rootdir_inside_onedrive(tmp_path):
    repo = tmp_path / "OneDrive" / ".TOPICS" / "repo"

    with pytest.raises(pytest.UsageError, match="OneDrive"):
        _configure(repo, ".pytest_tmp")


def test_refuses_an_absolute_basetemp_inside_onedrive(tmp_path):
    inside = tmp_path / "OneDrive" / ".TOPICS" / ".AI" / ".pytest_tmp"

    with pytest.raises(pytest.UsageError, match="OneDrive"):
        _configure(tmp_path / "repo", str(inside))


def test_refuses_a_business_account_folder(tmp_path):
    inside = tmp_path / "OneDrive - Firma" / "scratch"

    with pytest.raises(pytest.UsageError, match="OneDrive"):
        _configure(tmp_path / "repo", str(inside))


def test_refuses_a_basetemp_below_the_onedrive_environment_root(tmp_path, monkeypatch):
    root = tmp_path / "sync-root"  # carries no OneDrive in its name; only the variable says so
    monkeypatch.setenv("OneDrive", str(root))

    with pytest.raises(pytest.UsageError, match="OneDrive"):
        _configure(tmp_path / "repo", str(root / "scratch" / ".pytest_tmp"))


def test_a_folder_that_merely_starts_with_onedrive_is_not_refused(tmp_path):
    target = tmp_path / "onedrive-tools" / "scratch"

    config = _configure(tmp_path / "repo", str(target))

    assert Path(config.option.basetemp) == target.resolve()


def test_refuses_macos_cloudstorage_onedrive_personal(tmp_path):
    inside = tmp_path / "Library" / "CloudStorage" / "OneDrive-Personal" / "scratch"

    with pytest.raises(pytest.UsageError, match="OneDrive"):
        _configure(tmp_path / "repo", str(inside))


def test_refuses_macos_cloudstorage_onedrive_business_and_shared(tmp_path):
    for folder_name in ("OneDrive-AcmeCorp", "OneDrive-SharedLibraries-Org"):
        inside = tmp_path / "CloudStorage" / folder_name / "scratch"
        with pytest.raises(pytest.UsageError, match="OneDrive"):
            _configure(tmp_path / "repo", str(inside))


def test_onedrive_prefix_outside_cloudstorage_is_not_refused(tmp_path):
    for folder_name in ("OneDrive-Tools", "OneDriveBackup"):
        target = tmp_path / "projects" / folder_name / "scratch"
        config = _configure(tmp_path / "repo", str(target))
        assert Path(config.option.basetemp) == target.resolve()

