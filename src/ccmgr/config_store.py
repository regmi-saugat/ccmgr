"""Writer for the `[projects]` table in config.toml. Preserves comments via tomlkit."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import tomlkit
from tomlkit import TOMLDocument


def _load_doc(path: Path) -> TOMLDocument:
    if not path.is_file():
        return tomlkit.document()
    return tomlkit.parse(path.read_text())


def _projects_table(doc: TOMLDocument):
    if "projects" not in doc:
        doc["projects"] = tomlkit.table()
    return doc["projects"]


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".ccmgr-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def set_hidden(config_path: Path, real_path: str, hidden: bool) -> None:
    doc = _load_doc(config_path)
    projects = _projects_table(doc)
    arr = projects.get("hidden") or tomlkit.array()
    existing = [str(x) for x in arr]
    if hidden:
        if real_path not in existing:
            existing.append(real_path)
        projects["hide_enabled"] = True
    else:
        existing = [p for p in existing if p != real_path]
    projects["hidden"] = existing
    _atomic_write(config_path, tomlkit.dumps(doc))
