# Changelog

All notable changes to **ccmgr** will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.4] - 2026-05-19

### Changed

- Lowered minimum supported Python from 3.12 to 3.10. On Python 3.10 (which lacks stdlib `tomllib`), `tomli` is installed automatically as a conditional dependency.

## [0.1.3] - 2026-05-18

### Added

- Initial public release of ccmgr — a tmux-backed terminal UI to navigate, resume, and start [Claude Code](https://claude.com/claude-code) sessions across projects.
- Projects and Sessions panes that read from `~/.claude/projects/*`.
- Per-session detached tmux sessions (`cc-<short_id>`) so in-progress claude work survives switching panes.
- Key bindings for navigation, focus switching, filtering (`/`), session details popup (`i`), help (`?`), and quit (`q` / `Ctrl-C`).
- `ccmgr --version` flag.

[Unreleased]: https://github.com/regmi-saugat/ccmgr/compare/v0.1.4...HEAD
[0.1.4]: https://github.com/regmi-saugat/ccmgr/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/regmi-saugat/ccmgr/releases/tag/v0.1.3
