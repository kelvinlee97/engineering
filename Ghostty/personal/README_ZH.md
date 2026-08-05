# 个人 Ghostty 配置

这个目录是个人 Ghostty macOS 配置的版本控制来源。

## 内容

- `config.ghostty` 保存可迁移的终端配置。
- `install.zsh` 将配置安装到 Ghostty 的 macOS Application Support 目录。
- `test/install_test.zsh` 在隔离的临时主目录中验证安装和备份行为。

## 环境要求

- Ghostty 1.3 或更高版本
- JetBrainsMono Nerd Font
- Ghostty 内置的 `Catppuccin Mocha` 主题
- zsh

## 在新 Mac 上安装

进入这个目录后运行：

```zsh
./install.zsh
```

如果目标位置已有配置，安装脚本会先在同一目录建立带时间戳的备份，再安装仓库版本。安装后请完整重启 Ghostty，让仅在新进程中生效的设置得到应用。

## 验证

运行隔离的安装测试：

```zsh
./test/install_test.zsh
```

安装 Ghostty 后，可验证实际配置：

```zsh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
```

## 安全边界

这里只保存个人拥有且可迁移的设置。不要加入凭据、Shell 历史记录、公司信息、机器专属路径或机密数据。从公司电脑迁移个人配置前，应遵守适用的公司政策。
