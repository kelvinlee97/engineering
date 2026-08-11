# Ghostty 工作台

English version: [README.md](README.md)

这是一个面向新 Mac 的简洁 macOS 终端环境。Ghostty 负责终端窗口，zsh 负责 Shell，安装器提供一组实用的命令行工具。

## 安装

```zsh
git clone https://github.com/kelvinlee97/engineering.git
cd engineering/Ghostty/workstation
./install.zsh
```

安装器缺少 Homebrew 时会安装，然后应用 [`Brewfile`](Brewfile)。已经安装的 Homebrew 软件会保留并跳过。安装内容包括 Ghostty、JetBrainsMono Nerd Font、Starship、tmux、fzf、zoxide、fd、ripgrep、eza、bat、Glow、GitHub CLI 和 Shell 集成。

配置会写入 `~/.config/engineering-terminal/`。安装器会链接 Ghostty 和 tmux 配置，向 `.zshrc` 添加一个 source 区块，并在 `~/.local/bin/` 提供 `terminal-doctor` 和 `terminal-uninstall`。

再次运行安装器会刷新受管理配置。本安装器面向新 Mac，替换受管理目标前不会创建备份。

## 第一次使用

打开新的 Ghostty 窗口，然后运行：

```zsh
rg --version
fd --version
z project-name
tmux
ll
~/.local/bin/terminal-doctor
```

## 卸载

```zsh
~/.local/bin/terminal-uninstall
```

卸载会移除受管理链接和 `.zshrc` source 区块，保留 Homebrew 软件和 `~/.config/engineering-terminal/`。

仓库只保存可迁移的个人设置。不要加入凭据、SSH key、云账号配置、Shell 历史、公司资料或机器专属密钥。
