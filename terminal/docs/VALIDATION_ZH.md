# 验证记录

日期：2026-08-08
状态：已有设备验证通过；正式安全扫描、签名设置、人工 diff 审查和全新设备验收完成前禁止发布

## 环境

- macOS 26.5.2 (25F84)，Apple Silicon `arm64`
- Ghostty 1.3.1
- Starship 1.26.0
- tmux 3.7b
- fzf 0.74.2
- fd 10.4.2
- ripgrep 15.2.0
- eza 0.23.5
- bat 0.26.1
- Glow 2.1.2
- zoxide 0.10.0
- Git 2.55.0
- GitHub CLI 2.97.0

## 已通过证据

- 在路径含空格的隔离 HOME 中安装
- 保留已有 `.zshrc` 和 Ghostty 备份
- 第二次运行保持幂等
- 卸载受管理链接和有边界的 zsh 区块
- 在修改前拒绝损坏的受管理标记
- 在创建目标前拒绝无效的 zsh 源配置
- Ghostty、Starship、tmux 和 zsh 源配置验证
- 25 项 `terminal-doctor` 检查
- fd、ripgrep、eza、bat、Glow、fzf、zoxide 和 tmux 真实场景
- 工作树和精确格式的完整 Git 历史凭据扫描
- 真实 Ghostty 截图的可见内容与元数据审查

历史宽松扫描只命中不可用的教学占位符，例如 `ghp_your_new_github_token`、`sk-your-openai-key-here`，以及正文为 `...` 的私钥区块。精确凭据格式验证没有保留任何命中。

## 尚未完成的发布门

- 正式仓库安全扫描停在预检阶段，尚未完成。
- 本地和远程都不存在 `v1.0.0`。
- 尚未配置 Git 签名身份，因此当前无法创建签名标签。
- ShellCheck 0.11.0 不支持 zsh 并返回 SC1071；当前证据来自 zsh 解析、行为测试和人工审查。
- 尚未在全新的个人 MacBook Air 上运行已发布标签。
- push、创建标签和 GitHub Release 必须经过人工确认。
