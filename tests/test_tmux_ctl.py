import subprocess

import ccmgr.tmux_ctl as tmux_ctl
from ccmgr.tmux_ctl import build_scroll_options, build_copy_mode_command


def test_build_scroll_options_enables_mouse_and_vi_copy():
    """mouse + vi mode let the user drag-select and navigate copy-mode in the
    claude pane; history-limit gives copy-mode something to scroll back over."""
    cmds = build_scroll_options("claude-myproj", scrollback_lines=8000)

    assert ["set-option", "-t", "claude-myproj", "mouse", "on"] in cmds
    assert ["set-window-option", "-t", "claude-myproj", "mode-keys", "vi"] in cmds
    assert [
        "set-option", "-t", "claude-myproj", "history-limit", "8000"
    ] in cmds


def test_build_scroll_options_targets_the_named_session():
    cmds = build_scroll_options("other-session", scrollback_lines=5000)

    for args in cmds:
        assert "other-session" in args


def test_build_copy_mode_command_freezes_the_named_pane():
    """copy-mode freezes the pane so a drag-selection isn't dragged away by new
    streaming output. -e lets scrolling back to the bottom exit copy-mode."""
    args = build_copy_mode_command("%7")

    assert args == ["copy-mode", "-e", "-t", "%7"]


def test_split_window_v_includes_size_percent(monkeypatch):
    captured = {}

    def fake_check_output(args, **kwargs):
        captured["args"] = args
        return b"%9\n"

    monkeypatch.setattr(tmux_ctl, "in_tmux", lambda: True)
    monkeypatch.setattr(subprocess, "check_output", fake_check_output)

    pane = tmux_ctl.split_window_v("echo hi", target="%3", size_percent=30)

    assert pane == "%9"
    assert captured["args"][:4] == ["tmux", "split-window", "-v", "-P"]
    assert "-l" in captured["args"]
    assert captured["args"][captured["args"].index("-l") + 1] == "30%"
    assert "%3" in captured["args"]
    assert captured["args"][-1] == "echo hi"


def test_split_window_v_omits_size_when_none(monkeypatch):
    captured = {}

    def fake_check_output(args, **kwargs):
        captured["args"] = args
        return b"%1\n"

    monkeypatch.setattr(tmux_ctl, "in_tmux", lambda: True)
    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    tmux_ctl.split_window_v("sh")
    assert "-l" not in captured["args"]
