import pytest

from ccmgr.config_store import set_hidden


def _read(cfg):
    return cfg.read_text()


def test_set_hidden_true_creates_file_and_auto_enables(tmp_path):
    cfg = tmp_path / "config.toml"
    assert not cfg.exists()
    set_hidden(cfg, "/home/me/a", True)
    text = _read(cfg)
    assert "[projects]" in text
    assert "hide_enabled = true" in text
    assert "/home/me/a" in text


def test_set_hidden_true_appends_and_keeps_enabled(tmp_path):
    cfg = tmp_path / "config.toml"
    set_hidden(cfg, "/home/me/a", True)
    set_hidden(cfg, "/home/me/b", True)
    text = _read(cfg)
    assert "/home/me/a" in text and "/home/me/b" in text
    assert text.count("hide_enabled = true") == 1


def test_set_hidden_true_idempotent(tmp_path):
    cfg = tmp_path / "config.toml"
    set_hidden(cfg, "/home/me/a", True)
    set_hidden(cfg, "/home/me/a", True)
    text = _read(cfg)
    assert text.count("/home/me/a") == 1


def test_set_hidden_false_removes_entry_and_leaves_flag(tmp_path):
    cfg = tmp_path / "config.toml"
    set_hidden(cfg, "/home/me/a", True)
    set_hidden(cfg, "/home/me/b", True)
    set_hidden(cfg, "/home/me/a", False)
    text = _read(cfg)
    assert "/home/me/a" not in text
    assert "/home/me/b" in text
    assert "hide_enabled = true" in text


def test_set_hidden_false_missing_entry_is_noop(tmp_path):
    cfg = tmp_path / "config.toml"
    cfg.write_text("[claude]\nbinary = 'claude'\n")
    set_hidden(cfg, "/home/me/nope", False)
    text = _read(cfg)
    assert "[claude]" in text


def test_set_hidden_preserves_comments_and_unrelated_keys(tmp_path):
    cfg = tmp_path / "config.toml"
    cfg.write_text(
        "# top comment\n"
        "[claude]\n"
        "binary = 'claude'  # inline\n"
        "\n"
        "[live]\n"
        "poll_interval_ms = 1000\n"
    )
    set_hidden(cfg, "/home/me/a", True)
    text = _read(cfg)
    assert "# top comment" in text
    assert "[claude]" in text
    assert "binary = 'claude'" in text
    assert "# inline" in text
    assert "[live]" in text
    assert "poll_interval_ms = 1000" in text
    assert "[projects]" in text
    assert "/home/me/a" in text


def test_set_hidden_malformed_file_raises_and_preserves_file(tmp_path):
    cfg = tmp_path / "config.toml"
    original = "this is = = not valid toml\n"
    cfg.write_text(original)
    with pytest.raises(Exception):
        set_hidden(cfg, "/home/me/a", True)
    assert cfg.read_text() == original


def test_set_hidden_reads_disk_state_not_cache(tmp_path):
    cfg = tmp_path / "config.toml"
    set_hidden(cfg, "/home/me/a", True)
    # External mutation between calls — second call must NOT clobber it.
    text = cfg.read_text().replace('"/home/me/a"', '"/home/me/a", "/home/me/external"')
    cfg.write_text(text)
    set_hidden(cfg, "/home/me/b", True)
    final = cfg.read_text()
    assert "/home/me/a" in final
    assert "/home/me/external" in final
    assert "/home/me/b" in final
