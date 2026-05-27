from pathlib import Path

from ccmgr.terminal_holder import holder_name, attach_command, holder_shell_cmd


def test_holder_name_prefixes_and_sanitizes():
    assert holder_name("cc-myproj-1") == "cct-cc-myproj-1"


def test_holder_name_replaces_non_alnum_and_trims():
    assert holder_name("/home/me/proj!") == "cct-home-me-proj"


def test_holder_name_truncates_to_24_chars_after_prefix():
    name = holder_name("a" * 50)
    assert name == "cct-" + "a" * 24


def test_holder_name_empty_falls_back():
    assert holder_name("---") == "cct-x"


def test_attach_command_uses_tmux_prefix_and_quotes():
    assert attach_command("cct-x") == "TMUX= exec tmux attach-session -t cct-x"


def test_holder_shell_cmd_cds_and_execs_shell():
    cmd = holder_shell_cmd(Path("/home/me/proj"), "/bin/zsh")
    assert cmd == "cd /home/me/proj && exec /bin/zsh"


def test_holder_shell_cmd_quotes_paths_with_spaces():
    cmd = holder_shell_cmd(Path("/home/me/my proj"), "/bin/bash")
    assert cmd == "cd '/home/me/my proj' && exec /bin/bash"
