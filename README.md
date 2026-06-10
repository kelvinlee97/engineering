# Engineering

记录自己所学技能的工程实践。

## 目录结构

```
.codebuddy/
  statusline/
    statusline-command.sh  # CodeBuddy Code statusline 脚本
```

## Statusline 脚本

CodeBuddy Code 的 statusline 脚本，显示以下信息：
- 当前目录
- Git 分支
- Model ID
- 推理努力度 (reasoning effort)
- 上下文使用进度条

**特点**：简约无彩色显示，使用 Unicode 分隔符。

**安装**：
```bash
# 复制到 CodeBuddy Code 配置目录
cp .codebuddy/statusline/statusline-command.sh ~/.codebuddy/statusline-command.sh

# 确保 settings.json 里配置了 statusLine command
# "statusLine": {
#   "type": "command",
#   "command": "bash /Users/kelvinlee/.codebuddy/statusline-command.sh"
# }
```
