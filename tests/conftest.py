"""Pytest guard for the base temp directory.

``--basetemp=.pytest_tmp`` in pyproject.toml is relative, and pytest resolves a relative base temp against the
*current working directory*. A run started with a working directory inside OneDrive therefore dropped ``.pytest_tmp``
into the sync tree (2026-11-01, T-20261107-245040014). The hook below anchors a relative base temp at the rootdir (the
repository) and refuses a base temp that ends up inside OneDrive, so a sync tree is never used as scratch space.
"""

import os
from pathlib import Path

import pytest

_ONEDRIVE_ENV = ("OneDrive", "OneDriveConsumer", "OneDriveCommercial")


def _in_onedrive(path: Path) -> bool:
    """True for a path inside a OneDrive folder.

    Matches a folder named ``OneDrive`` or ``OneDrive - <account>`` and anything below the roots the OneDrive client
    exports as environment variables. Deliberately not a prefix match: ``onedrive-tools`` is an ordinary folder.
    """
    if any(part.casefold() == "onedrive" or part.casefold().startswith("onedrive - ") for part in path.parts):
        return True
    roots = (Path(value).resolve() for name in _ONEDRIVE_ENV if (value := os.environ.get(name)))
    return any(path.is_relative_to(root) for root in roots)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    given = getattr(config.option, "basetemp", None)
    if not given:
        return
    base = Path(given)
    if not base.is_absolute():
        base = Path(config.rootpath) / base
    base = base.resolve()
    if _in_onedrive(base):
        raise pytest.UsageError(
            f"The pytest base temp {base} lies inside OneDrive. Test runs must not write into a sync tree: "
            "run the tests in the canonical clone (C:\\_Local_DEV\\repos\\<repo>) or pass "
            "--basetemp <absolute path outside OneDrive>."
        )
    config.option.basetemp = str(base)
