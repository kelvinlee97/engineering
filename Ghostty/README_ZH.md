# Ghostty 工作台

English version: [README.md](README.md)

这是一个面向 Ghostty 和常用终端工具的简洁手动配置方案。

支持的系统：

- macOS：使用系统自带 zsh 和 Homebrew
- Ubuntu 26.04：使用系统自带 bash 和 apt

本方案没有安装器，也没有自定义配置管理目录。安装需要的工具，在 Shell 配置中添加一次初始化命令，然后把 [`config.ghostty`](config.ghostty) 复制到 Ghostty 的默认配置位置即可。

克隆仓库后，请先在本目录执行下面的命令，再执行后续配置命令：

```bash
cd engineering/Ghostty
```

## 安装工具

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

## 配置 Shell

在 macOS 的 `~/.zshrc` 中添加一次：

```zsh
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"
alias ll='eza --long --all --git --group-directories-first'
alias tree='eza --tree --group-directories-first'
alias preview='bat --paging=always'
```

在 Ubuntu 的 `~/.bashrc` 中添加一次：

```bash
eval "$(starship init bash)"
eval "$(zoxide init bash)"
alias ll='eza --long --all --git --group-directories-first'
alias tree='eza --tree --group-directories-first'
alias preview='batcat --paging=always'
alias fd='fdfind'
```

修改 Shell 配置后，打开新的终端。基础用法直接运行 `fzf` 即可，不额外配置 Shell 集成。

## 配置 Ghostty

使用 `cp -i`，已有配置在覆盖前会要求确认。

### macOS

```zsh
mkdir -p ~/Library/Application\ Support/com.mitchellh.ghostty
cp -i config.ghostty ~/Library/Application\ Support/com.mitchellh.ghostty/config.ghostty
```

### Ubuntu 26.04

```bash
ghostty_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty"
mkdir -p "$ghostty_dir"
cp -i config.ghostty "$ghostty_dir/config.ghostty"
```

如果已经存在 Ghostty 配置，请只保留一个配置来源并手动合并。Ghostty 仍然识别旧的 `config` 文件名，但新配置应使用 `config.ghostty`。

在 Ubuntu 上，如果旧的 `config` 文件和 `config.ghostty` 位于同一目录，请先比较两个文件，把需要的设置迁移到 `config.ghostty`，然后移除旧的 `config`。不要同时保留两个生效文件：

```bash
ghostty_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty"
if [ -f "$ghostty_dir/config" ]; then
    diff -u "$ghostty_dir/config" "$ghostty_dir/config.ghostty" || true
fi
```

在 macOS 上要同时检查两个旧的 `config` 文件，因为 macOS 可能同时读取 XDG 配置位置和原生配置位置：

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

如果 `ghostty` 命令可用，可以验证复制后的配置。

macOS：

```zsh
ghostty +validate-config --config-file="$HOME/Library/Application Support/com.mitchellh.ghostty/config.ghostty"
```

Ubuntu：

```bash
ghostty +validate-config --config-file="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/config.ghostty"
```

## 移除配置

从 `~/.zshrc` 或 `~/.bashrc` 中删除本方案添加的行。只有在复制的 Ghostty 配置不包含个人设置时，才删除该文件。已安装的软件包不会自动移除。

本目录只保存可迁移的个人设置。不要加入凭据、SSH key、云账号配置、Shell 历史、公司资料或机器专属密钥。
