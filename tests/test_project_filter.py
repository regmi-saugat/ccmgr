from pathlib import Path

from ccmgr.models import Project
from ccmgr.project_filter import visible_projects


def _proj(path: str) -> Project:
    p = Path(path)
    return Project(real_path=p, encoded_name=path.replace("/", "-"),
                   claude_dir=Path("/tmp/x"), session_count=0, last_activity_ts=0.0)


def test_returns_all_when_disabled():
    projects = [_proj("/a"), _proj("/b")]
    out = visible_projects(projects, frozenset({"/a"}), enabled=False)
    assert out == projects


def test_filters_when_enabled():
    projects = [_proj("/a"), _proj("/b")]
    out = visible_projects(projects, frozenset({"/a"}), enabled=True)
    assert [str(p.real_path) for p in out] == ["/b"]


def test_canonicalizes_both_sides(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)
    projects = [_proj(str(link))]
    out = visible_projects(projects, frozenset({str(real)}), enabled=True)
    assert out == []


def test_trailing_slash_does_not_break_match():
    projects = [_proj("/a")]
    out = visible_projects(projects, frozenset({"/a/"}), enabled=True)
    assert out == []
