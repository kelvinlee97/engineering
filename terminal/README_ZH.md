# 面向全新 Mac 的 Ghostty 终端工作台

English version: [README.md](README.md)

这个模块用于在一台刚初始化的 Mac 上重建可迁移的命令行工作台。Ghostty 是唯一的图形终端；原生 zsh 负责解释命令；Starship 保持提示符简洁；tmux 保存长期会话；其余小工具分别改善导航、搜索和查看体验。

这个仓库是“重建环境的配方”，不是旧电脑的备份。它不会保存凭据、SSH key、云账号配置、Kubernetes 配置、Shell 历史、公司资料或机器专属路径。

> 发布状态：`main` 中的文件目前是发布候选。只有签名标签发布后，下面的 `v1.0.0` 命令才可以使用。当前验证设备是已有环境的 macOS；尚未在全新 MacBook Air 上验收。

## 快速开始

### 推荐：下载、审查、再执行

```zsh
git clone --branch v1.0.0 --depth 1 https://github.com/kelvinlee97/engineering.git
cd engineering/terminal
less install.zsh
./install.zsh
```

### 快速安装

```zsh
bootstrap_dir="$(mktemp -d)" && curl --fail --show-error --location https://raw.githubusercontent.com/kelvinlee97/engineering/c037a2a209f40a1c22711c8ba1f8931c5baeb2b0/terminal/bootstrap.zsh --output "$bootstrap_dir/bootstrap.zsh" && printf '%s  %s\n' e8f01661e79f11ca29667904193dd6e20e99fce7bea0e547e3499d7ea12105e0 "$bootstrap_dir/bootstrap.zsh" | shasum -a 256 --check && /bin/zsh "$bootstrap_dir/bootstrap.zsh"
```

快速命令会执行下载的代码。它把 bootstrap 固定到不可变 commit 并验证 SHA-256；bootstrap 随后还会在解压前验证 `v1.0.0` Release 安装包。先克隆并审查仍然更安全。项目规则要求标签不可移动：修复必须发布 `v1.0.1`，不能重新指向 `v1.0.0`。

安装后打开新 Shell 并运行：

```zsh
~/.local/bin/terminal-doctor
open -a Ghostty
```

## 安装内容

| 工具 | 解决的问题 | 示例 | 边界 |
|---|---|---|---|
| [Ghostty](https://ghostty.org/) | 提供终端文字、标签页、分屏、字体和输入窗口 | 打开本地标签页和分屏 | 不负责解释 Shell 命令 |
| zsh | 执行命令、管道、函数和脚本 | `git status` | 仍需保留可移植的 Shell 基础 |
| [Starship](https://starship.rs/) | 用精简提示符显示必要的仓库状态 | 立即看见 Git dirty state | 默认不显示云账号和集群名称 |
| [tmux](https://github.com/tmux/tmux/wiki) | 保存远程或长期会话 | SSH 断开后重新进入任务 | 普通本地窗口交给 Ghostty |
| [fzf](https://github.com/junegunn/fzf) | 从大量候选项中交互筛选 | 搜索历史命令 | 候选内容通常来自其他工具 |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | 学习常用目录并快速跳转 | `z engineering` | 标准 `cd` 始终保留 |
| [fd](https://github.com/sharkdp/fd) | 用适合开发者的默认规则找文件 | `fd '\.tf$'` | 可移植脚本仍需掌握 `find` |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | 遵守忽略规则搜索仓库内容 | `rg 'image:' --glob '*.yaml'` | 精简服务器仍需掌握 `grep` |
| [eza](https://github.com/eza-community/eza) | 更容易查看目录、权限和 Git 状态 | `ll` | 脚本仍使用标准 `ls` |
| [bat](https://github.com/sharkdp/bat) | 查看 Markdown 原文、代码、行号和 Git 变化 | `preview README.md` | 不负责渲染 Markdown 排版 |
| [Glow](https://github.com/charmbracelet/glow) | 在终端渲染 Markdown 标题、列表、表格、引用和代码块 | `glow README.md` | 需要检查原文时使用 `bat` |
| Git 与 GitHub CLI | 对配置进行版本控制和发布 | `gh auth login` | 登录必须由用户手动授权 |

zsh autosuggestions 和 syntax-highlighting 插件通过 Homebrew 安装。不安装或依赖 Oh My Zsh，从而减少框架耦合并避免第二套提示符主题。

## 分层关系

```text
Ghostty                         窗口、文字渲染、标签页、分屏
└── zsh                         命令解释器
    ├── Starship                精简的仓库状态提示符
    ├── fzf + zoxide            交互检索和目录导航
    ├── fd + ripgrep            文件和内容搜索
    ├── eza + bat + Glow        查看目录、原文和渲染后的 Markdown
    └── tmux                    可持续的远程/长期会话
```

Ghostty 和 tmux 的职责不同。普通本地工作使用 Ghostty 标签页和分屏；只有会话必须承受断网或窗口关闭时才进入 tmux。

## 安装行为

安装器会：

1. 确认 macOS 和 Apple Command Line Tools。
2. 在 Apple Silicon 或 Intel 路径发现 Homebrew；缺失时执行固定到 commit `24173182915f24bdd52a22fd073e421953b2a252` 的官方 Homebrew 安装器。
3. 应用版本控制的 [`Brewfile`](Brewfile)。其中固定的是软件包名称，Homebrew 会解析当前版本；实际测试版本记录在验收证据中，不把 Brewfile 描述为版本锁文件。
4. 将配置复制到 `~/.config/engineering-terminal/`。
5. 替换目标前先备份。
6. 把 Ghostty、tmux、doctor 和 uninstall 入口链接到受管理副本。
7. 只向 `.zshrc` 添加一个有边界的区块，不替换整个文件。
8. 在安装阶段生成 fzf、zoxide 和 Starship 本地初始化文件，Shell 启动时不会访问网络。
9. 验证 zsh 与 Ghostty 配置。

安装器可以重复执行：相同的受管理文件不会反复备份，`.zshrc` 区块也不会重复。

Homebrew 在接管或更新 `/Applications` 中的应用时可能要求当前 macOS 用户输入密码；安装器不会读取或保存密码。执行 bundle 时会禁用 Homebrew 自动清理，避免无关的过期缓存条目让本来成功的安装被判定失败。

### 受管理的 `.zshrc` 区块

```zsh
# BEGIN engineering-terminal
source "$HOME/.config/engineering-terminal/zsh/init.zsh"
# END engineering-terminal
```

安装器不会静默删除已有 Shell 框架。如果旧环境存在 Oh My Zsh，应先检查提示符和插件是否重复，再决定是否移除。

## 配置选择

### Ghostty

提交的配置使用 JetBrainsMono Nerd Font、Catppuccin Mocha、紧凑窗口间距、竖线光标、Shell integration、分屏导航，以及供部分 AI CLI 输入换行的 `Shift+Enter`。左 Option 作为 Alt，右 Option 保留 macOS 字符输入能力。

### Starship

提示符只显示当前目录、Git branch/status、慢命令耗时和退出状态。AWS Profile 与 Kubernetes context 默认不显示，既降低提示符开销，也减少截图或屏幕共享泄露环境名称的风险。

### zsh 工具

公开别名刻意保持明确：

```zsh
ll                 # eza 详细视图和 Git 状态
tree               # eza 目录树
preview README.md  # bat 文本预览
glow README.md     # 渲染 Markdown
glow -p README.md  # 使用分页器渲染 Markdown
```

标准 `ls`、`cat`、`find`、`grep` 不会被覆盖，方便脚本和远程服务器继续使用。

## 验证

自动健康检查：

```zsh
~/.local/bin/terminal-doctor
```

仓库测试：

```zsh
./test/run.zsh
```

Ghostty 人工验收：

- Nerd Font 图标没有空白方框。
- Starship 能显示演示 Git 仓库的 branch 和 dirty state。
- `Ctrl+Shift+D` 打开右分屏，`Ctrl+Shift+-` 打开下分屏。
- `fzf`、`z`、`fd`、`rg`、`ll`、`preview` 和 `glow` 在安全本地仓库可用。
- `tmux new -s demo`、detach 和 `tmux attach -t demo` 可用。

## 截图与验证状态

下图来自已经安装配置的真实 Ghostty，并在安全本地演示仓库中运行。画面展示 Starship Git 状态、`fd` 文件查找、`rg` 内容搜索和 `eza` 目录树；示例域名使用保留的 `.invalid` 后缀。提交前已经检查标题、可见输出、图片像素和文件元数据，确认没有账号 ID、主机名、私人路径、凭据或公司信息。

![Ghostty 在安全演示仓库中运行终端工作台](docs/images/ghostty-terminal-workstation.png)

| 环境 | 状态 |
|---|---|
| 已有 macOS 设备 | 自动检查通过；2026-08-07 已完成真实 Ghostty 截图 |
| 全新 MacBook Air | 尚未验证 |

只有在个人 MacBook Air 上实际运行已发布标签后，文档才会标记 fresh-device verified。

## 安全模型

- 推荐先克隆、审查再运行，不优先推荐快速安装。
- 发布命令固定版本标签，不使用浮动 `main` URL。
- 远程下载使用 HTTPS，并在 HTTP 错误时停止。
- 临时目录删除前验证目录前缀。
- 替换现有文件前创建备份。
- 不复制或生成凭据和私有配置。
- GitHub 登录和个人 Git identity 保持人工操作。
- Critical/High 安全问题或任何凭据命中都会阻断发布。

发布门详见[安全与发布](docs/SECURITY_ZH.md)，恢复方法详见[故障排查](docs/TROUBLESHOOTING_ZH.md)。
已有设备的具体证据和未完成发布门记录在[验证记录](docs/VALIDATION_ZH.md)中。

## 卸载与恢复

```zsh
~/.local/bin/terminal-uninstall
```

卸载只移除受管理链接和 `.zshrc` 区块，刻意保留 Homebrew 软件、`~/.config/engineering-terminal/` 和带时间戳的备份。恢复备份前必须先查看内容。

## 维护者开发通道

`main` 只用于开发和审查。维护者可从干净 clone 测试：

```zsh
git clone https://github.com/kelvinlee97/engineering.git
cd engineering/terminal
./test/run.zsh
```

不得把基于 `main` 的远程执行命令当成稳定安装方式。
