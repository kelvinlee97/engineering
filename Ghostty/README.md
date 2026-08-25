# Ghostty Workstation

Chinese version: [README_ZH.md](README_ZH.md)

A small, manual setup for Ghostty and a focused set of terminal tools.

Supported systems:

- macOS with the built-in zsh and Homebrew
- Ubuntu 26.04 with the built-in bash and apt

There is no installer or managed configuration directory. Install the tools you want, add the shell lines once, and copy [`config.ghostty`](config.ghostty) to Ghostty's default configuration location.

Run the commands below from this directory after cloning the repository:

```bash
cd engineering/Ghostty
```

## Install tools

### macOS

```zsh
brew install starship tmux fzf fd ripgrep eza bat zoxide git gh
brew install --cask ghostty
```

### Ubuntu 26.04

```bash
sudo apt update
sudo apt install ghostty starship tmux fzf fd-find ripgrep eza bat zoxide git gh
```

## Configure the shell

Add these lines once to `~/.zshrc` on macOS:

```zsh
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"
alias ll='eza --long --all --git --group-directories-first'
alias tree='eza --tree --group-directories-first'
alias preview='bat --paging=always'
```

Add these lines once to `~/.bashrc` on Ubuntu:

```bash
eval "$(starship init bash)"
eval "$(zoxide init bash)"
alias ll='eza --long --all --git --group-directories-first'
alias tree='eza --tree --group-directories-first'
alias preview='batcat --paging=always'
alias fd='fdfind'
```

Open a new terminal after editing the shell file. `fzf` works directly as the `fzf` command; no extra shell configuration is required for the basic workflow.

## Configure Ghostty

Use `cp -i` so an existing configuration is not overwritten without confirmation.

### macOS

```zsh
ghostty_dir="$HOME/Library/Application Support/com.mitchellh.ghostty"
mkdir -p "$ghostty_dir"
cp -i config.ghostty "$ghostty_dir/config.ghostty"
```

### Ubuntu 26.04

```bash
ghostty_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty"
mkdir -p "$ghostty_dir"
cp -i config.ghostty "$ghostty_dir/config.ghostty"
```

If another Ghostty configuration already exists, keep one source of truth and merge the settings manually. Ghostty also recognizes the older `config` filename, but new configurations should use `config.ghostty`.

On Ubuntu, if the old `config` file exists beside `config.ghostty`, compare them first, move the settings you want into `config.ghostty`, then remove the old `config`. Do not keep both files active:

```bash
ghostty_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty"
if [ -f "$ghostty_dir/config" ]; then
    diff -u "$ghostty_dir/config" "$ghostty_dir/config.ghostty" || true
fi
```

On macOS, check both older `config` files because macOS can load both the XDG and native configuration locations:

```zsh
legacy_xdg_config="$HOME/.config/ghostty/config"
legacy_native_config="$HOME/Library/Application Support/com.mitchellh.ghostty/config"
native_config="$HOME/Library/Application Support/com.mitchellh.ghostty/config.ghostty"
if [ -f "$legacy_xdg_config" ]; then
    diff -u "$legacy_xdg_config" "$native_config" || true
fi
if [ -f "$legacy_native_config" ]; then
    diff -u "$legacy_native_config" "$native_config" || true
fi
```

To validate the copied file when the `ghostty` command is available:

macOS:

```zsh
ghostty +validate-config --config-file="$HOME/Library/Application Support/com.mitchellh.ghostty/config.ghostty"
```

Ubuntu:

```bash
ghostty +validate-config --config-file="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/config.ghostty"
```

## Remove the setup

Remove the lines added to `~/.zshrc` or `~/.bashrc`. Remove the copied Ghostty configuration only if it contains no personal settings. Installed packages are not removed automatically.

Only portable personal settings belong in this directory. Do not add credentials, SSH keys, cloud profiles, shell history, employer data, or machine-specific secrets.
