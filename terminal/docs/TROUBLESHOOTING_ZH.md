# 故障排查

## 缺少 Apple Command Line Tools

完成 macOS 安装提示后重新运行 `./install.zsh`。脚本会退出，不会带着不完整工具链继续执行。

## Homebrew 完成但找不到 `brew`

打开新的系统 Terminal，执行 Homebrew 输出的 Shell 环境说明，然后重跑安装器。脚本会同时检查 `/opt/homebrew` 与 `/usr/local`，不会预设 CPU 架构。

## 已存在 Oh My Zsh

安装器会保留它，并把受管理区块添加到 `.zshrc` 末尾。如果出现两套提示符或重复建议，先检查带时间戳的 `.zshrc` 备份；确认配置属于个人而非公司管理后，再人工移除旧主题和插件初始化。

## Ghostty 没有加载预期配置

运行：

```zsh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
readlink ~/.config/ghostty/config
```

验证后完整退出并重新打开 Ghostty。

## 图标显示方框

确认已经安装 `font-jetbrains-mono-nerd-font`，然后完整重启 Ghostty。字体渲染仍需人工观察，不能只依赖 `terminal-doctor`。

## 恢复旧文件

运行 `terminal-uninstall`，检查原目标旁边的 `.backup-*` 文件，只恢复真正需要的文件。Homebrew 软件会被刻意保留。
