# One-command Ghostty environment for macOS

This directory provides a real one-command setup: Ghostty, focused CLI tools, and persistent zsh integration.

## One-command installation

Paste this into macOS Terminal:

```zsh
/bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/kelvinlee97/engineering/main/Ghostty/personal/install.zsh)"
```

The installer includes:

- Ghostty and JetBrainsMono Nerd Font
- ripgrep, fd, zoxide, tmux, and fzf
- eza, bat, Starship, and Glow
- GitHub CLI, jq, and tree
- zsh autosuggestions and syntax highlighting

When it finishes, close Terminal and open a new Ghostty window. These commands are immediately available:

```zsh
rg --version
fd --version
z project-name
tmux
ll
```

Persistent configuration lives at `~/.config/engineering-ghostty-personal/init.zsh`. The installer adds only one bounded block to `.zshrc`, backs up existing Ghostty and zsh configuration, and does not duplicate the block on repeated runs.

From an existing clone, you can also run:

```zsh
./install.zsh
```

## Verification

```zsh
./test/install_test.zsh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
```

Only portable, personally owned settings belong here. Do not add credentials, shell history, company information, machine-specific paths, or confidential data.
