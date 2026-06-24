"""Pure project visibility filter for the hide/show feature."""
from __future__ import annotations

from pathlib import Path
from collections.abc import Iterable

from ccmgr.models import Project


def _canon(p: str | Path) -> str:
    try:
        return str(Path(p).expanduser().resolve())
    except OSError:
        return str(Path(p).expanduser())


def visible_projects(
    projects: Iterable[Project],
    hidden: frozenset[str],
    enabled: bool,
) -> list[Project]:
    if not enabled:
        return list(projects)
    hidden_canon = {_canon(h) for h in hidden}
    return [p for p in projects if _canon(p.real_path) not in hidden_canon]
