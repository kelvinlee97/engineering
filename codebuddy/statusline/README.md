# CodeBuddy Statusline

CodeBuddy Code 的 statusline 脚本，简约无彩色显示。

## 功能

显示以下信息：
- 当前目录
- Git 分支
- Model ID
- 推理努力度 (reasoning effort)
- 上下文使用进度条

## 效果示例

```
~/Documents/projects/automation-ocr | main | hy3-preview-ioa | xhigh | [==>-------] 19.4%
```

- `|` 表示分隔符（实际显示：``）
- `[==>-------]` 表示上下文进度条（实际显示：`█░░░░░░░░░`）
- `19.4%` 是当前上下文使用百分比

## 安装

```bash
# 方案1：复制到 CodeBuddy Code 配置目录
cp statusline-command.sh ~/.codebuddy/statusline-command.sh

# 方案2：直接指向脚本（推荐）
# 修改 ~/.codebuddy/settings.json:
# "statusLine": {
#   "type": "command",
#   "command": "bash /path/to/engineering/codebuddy/statusline/statusline-command.sh"
# }
```
