# macOS 一键 Ghostty 终端环境

这个目录提供真正的一键安装：自动安装 Ghostty、常用 CLI 工具，并永久启用 zoxide、fzf、Starship 和 zsh 插件。

## 一键安装

在 macOS Terminal 中粘贴：

```zsh
/bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/kelvinlee97/engineering/main/Ghostty/personal/install.zsh)"
```

脚本会安装：

- Ghostty 与 JetBrainsMono Nerd Font
- ripgrep、fd、zoxide、tmux、fzf
- eza、bat、Starship、Glow
- GitHub CLI、jq、tree
- zsh autosuggestions 与 syntax highlighting

完成后关闭 Terminal，打开一个新的 Ghostty 窗口。以下命令可以直接使用：

```zsh
rg --version
fd --version
z project-name
tmux
ll
```

永久配置保存在 `~/.config/engineering-ghostty-personal/init.zsh`。安装器只向 `.zshrc` 增加一个带起止标记的加载区块；已有 Ghostty 配置和 `.zshrc` 会先备份，重复运行不会重复追加。

如果已经克隆仓库，也可以在本目录运行：

```zsh
./install.zsh
```

这个目录只保存可迁移的个人设置，不应加入凭据、Shell 历史、公司信息、机器专属路径或机密数据。
