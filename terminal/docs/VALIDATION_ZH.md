# 验证记录

日期：2026-08-09
状态：已有设备验证通过；本地发布门已通过；外部发布、签名标签和全新设备验收仍待完成

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
- 最终 25 个文件的 release diff 审查通过，未命中精确凭据格式
- Release 安装包由提交 `ef2e246` 生成；SHA-256 为 `54759443266da35a51fe4aecc273acd0cd21bf81517859fbab18058c0ef32edd`
- Bootstrap 固定到提交 `c037a2a209f40a1c22711c8ba1f8931c5baeb2b0`；bootstrap SHA-256 为 `e8f01661e79f11ca29667904193dd6e20e99fce7bea0e547e3499d7ea12105e0`
- Homebrew 安装器固定到提交 `24173182915f24bdd52a22fd073e421953b2a252`，并执行 SHA-256 校验

历史宽松扫描只命中不可用的教学占位符，例如 `ghp_your_new_github_token`、`sk-your-openai-key-here`，以及正文为 `...` 的私钥区块。精确凭据格式验证没有保留任何命中。

## 尚未完成的发布门

- 本地和远程都不存在 `v1.0.0`。
- 尚未配置 Git 签名身份，因此当前无法创建签名标签。确认 GitHub SSH signing key 需要 `admin:ssh_signing_key` scope，而当前 CLI 没有该权限。
- ShellCheck 0.11.0 不支持 zsh；当前证据来自 `zsh -n`、行为测试和人工审查。
- 尚未在全新的个人 MacBook Air 上运行已发布标签。
- push、创建标签和 GitHub Release 必须经过人工确认。
