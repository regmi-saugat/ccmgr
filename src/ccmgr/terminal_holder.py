"""Pure helpers for the collapsible terminal feature.

The terminal's shell lives in a detached tmux session ("holder") so its state
survives while the terminal is hidden. These functions build the holder's name
and the commands around it. All stateful wiring lives in the App; all tmux calls
go through tmux_ctl.
"""
from __future__ import annotations

import shlex
from pathlib import Path


def holder_name(key: str) -> str:
    """Stable detached-session name for a terminal bound to `key`.

    Mirrors App._claude_session_name's `cc-<...>` convention with a `cct-` prefix.
    """
    safe = "".join(c if c.isalnum() else "-" for c in key).strip("-") or "x"
    return f"cct-{safe[:24]}"


def attach_command(holder: str) -> str:
    """Command that displays a detached holder session in a visible pane.

    The `TMUX=` prefix clears the env var so the nested attach works; tmux
    otherwise refuses to attach from within another tmux session.
    """
    return f"TMUX= exec tmux attach-session -t {shlex.quote(holder)}"


def holder_shell_cmd(cwd: Path, shell: str) -> str:
    """Command the holder session runs: a shell cd'd into `cwd`."""
    return f"cd {shlex.quote(str(cwd))} && exec {shlex.quote(shell)}"
