# Ghostty Workstation

Chinese version: [README_ZH.md](README_ZH.md)

A small macOS terminal setup for a new Mac. Ghostty is the terminal, zsh is the shell, and the installer adds a focused set of command-line tools.

## Install

```zsh
git clone https://github.com/kelvinlee97/engineering.git
cd engineering/Ghostty/workstation
./install.zsh
```

The installer installs Homebrew when needed, then applies [`Brewfile`](Brewfile). Already-installed Homebrew tools are kept and skipped by Homebrew. It also installs Ghostty, JetBrainsMono Nerd Font, Starship, tmux, fzf, zoxide, fd, ripgrep, eza, bat, Glow, GitHub CLI, and shell integrations.

Configuration is placed under `~/.config/engineering-terminal/`. The installer links Ghostty and tmux configuration, adds one source block to `~/.zshrc`, and makes `terminal-doctor` and `terminal-uninstall` available in `~/.local/bin/`.

Run the installer again to refresh the managed configuration. It is intended for a new Mac and does not create backups before replacing managed targets.

## First commands

Open a new Ghostty window, then try:

```zsh
rg --version
fd --version
z project-name
tmux
ll
~/.local/bin/terminal-doctor
```

## Uninstall

```zsh
~/.local/bin/terminal-uninstall
```

This removes the managed links and `.zshrc` source block. It leaves Homebrew packages and `~/.config/engineering-terminal/` in place.

Only portable personal settings belong in this repository. Do not add credentials, SSH keys, cloud profiles, shell history, employer data, or machine-specific secrets.
