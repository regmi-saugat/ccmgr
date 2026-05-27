"""Name/command builders for the detached tmux session that holds a hidden terminal."""
from __future__ import annotations

import shlex
from pathlib import Path


def holder_name(key: str) -> str:
    """Stable `cct-<sanitized>` session name for the terminal bound to `key`."""
    safe = "".join(c if (c.isalnum() and c.isascii()) else "-" for c in key).strip("-")
    return f"cct-{safe[:24].strip('-') or 'x'}"


def attach_command(holder: str) -> str:
    # TMUX= lets the nested attach work; tmux refuses to attach from within tmux otherwise.
    return f"TMUX= exec tmux attach-session -t {shlex.quote(holder)}"


def holder_shell_cmd(cwd: Path, shell: str) -> str:
    return f"cd {shlex.quote(str(cwd))} && exec {shlex.quote(shell)}"
