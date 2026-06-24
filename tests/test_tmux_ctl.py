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
