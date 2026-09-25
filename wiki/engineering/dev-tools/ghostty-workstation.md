---
type: Configuration
title: Ghostty workstation
description: A manual setup of the Ghostty terminal plus starship, zoxide, eza, bat, fzf, fd, and ripgrep on macOS or Ubuntu 26.04.
tags: [ghostty, terminal, dev-tools]
sources:
  - id: ghostty-workstation
    resource: https://github.com/kelvinlee97/engineering/blob/main/Ghostty/README.md
    title: Ghostty Workstation
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
A manual, installer-free terminal setup: install the tools, add a few shell lines once, and copy one `config.ghostty` file into Ghostty's configuration location. Nothing manages state afterwards.[^ghostty-workstation]

## Tools

`starship`, `tmux`, `fzf`, `fd`, `ripgrep`, `eza`, `bat`, `zoxide`, `git`, and `gh`, via Homebrew on macOS or apt on Ubuntu 26.04 (where `fd` is `fd-find` and `bat` runs as `batcat`).[^ghostty-workstation]

## Shell lines

`starship init` and `zoxide init` for the shell, plus aliases: `ll` and `tree` through `eza`, `preview` through `bat` (or `batcat`), and on Ubuntu `fd='fdfind'`.[^ghostty-workstation]

## Config location

| System | Path |
| --- | --- |
| macOS | `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty` |
| Ubuntu | `${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/config.ghostty` |

Copy with `cp -i`, keep one source of truth, and fold any older `config` file into `config.ghostty` rather than keeping both; macOS can load both the XDG and native locations. Validate with `ghostty +validate-config`.[^ghostty-workstation] Only portable personal settings belong in the repository: no credentials, SSH keys, cloud profiles, or history.[^ghostty-workstation]

## Related

- Source: [Ghostty workstation](../../sources/ghostty-workstation.md)

[^ghostty-workstation]: Ghostty Workstation
