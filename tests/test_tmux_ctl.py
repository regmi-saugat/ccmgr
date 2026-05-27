import subprocess

import ccmgr.tmux_ctl as tmux_ctl


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
