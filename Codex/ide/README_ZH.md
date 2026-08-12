# 在 VS Code 中使用 Codex IDE Context

English version: [README.md](README.md)

本指南说明如何让 Codex 连接 VS Code 的 IDE context，并在仓库开发时有效利用这些上下文。本文只面向 VS Code。

OpenAI 官方说明指出，Codex VS Code 扩展也兼容多数 VS Code forks；但不同产品的菜单和配置流程并不相同，因此本文不把 VS Code 步骤泛化到其他 IDE。有关受支持的侧栏和编辑器上下文流程，请参见官方 [Codex IDE extension guide](https://developers.openai.com/codex/ide)。

## IDE context 能带来什么

当你将编辑器上下文附加到 Codex composer 后，Codex 可将其作为额外任务上下文。具体可用内容会受扩展版本和配置影响，通常可能包括当前文件、选中代码、光标附近代码和编辑器诊断信息。

它是辅助信息，不取代仓库检查：

- 当任务需要编辑器以外的证据时，Codex 仍会读取相关文件并运行检查。
- 它不表示整个仓库已经被自动读取。
- 它不会自动获得提交、推送、部署、删除文件或修改外部系统的权限。

## 连接 IDE context

1. 在 VS Code 选择 **File > Open Folder...** 并打开仓库目录。请打开目录，而不是只打开一个文件。
2. 若 VS Code 显示 **Restricted Mode**，先检查该目录并确认其来源可信；仅在此之后，才选择 **Manage** 并信任该 workspace。若看不到 banner，可打开命令面板（macOS：`Cmd+Shift+P`）并运行 **Workspaces: Manage Workspace Trust**；随后运行 **Developer: Reload Window**。
3. 打开 Extensions（`Cmd+Shift+X`），找到 Codex 扩展并确认已启用；如有更新，先更新并按提示重载 VS Code。
4. 选择 Codex 图标打开 Codex 侧栏。若图标不可见，打开命令面板并运行 **Codex: Open Codex Sidebar**。
5. 打开一个源码文件，选中与你的任务相关的代码或文本。在 Codex composer 中添加当前文件或选区作为上下文，再发送任务。
6. 用一个小请求验证已附加的上下文：

   ```text
   告诉我当前文件路径，并摘要说明我选中的代码。
   ```

如果返回内容正确反映附加到 composer 的文件或选区，说明该编辑器上下文已随本次请求传入。

## 日常使用方式

打开相关文件，选中最小但足够的代码块，将文件或选区添加到 Codex composer，再告诉 Codex 你的目标和预期结果。例如：

```text
解释这段代码，并指出它的边界条件。
```

```text
诊断当前编辑器错误，说明根因，做最小且安全的修复，并运行相关验证。
```

```text
在不改变公开行为的前提下，让选中逻辑更清晰；补充或更新聚焦的测试。
```

```text
审查这个 API handler 的授权、输入验证和错误处理问题；暂时不要修改代码。
```

跨文件任务请明确说明。在当前会话具有 workspace 读取权限的前提下，Codex 可以以选中代码为起点，再在仓库中查找调用方、类型、配置和测试；IDE context 本身不会授予这项访问权限。

## 排查连接失败

如果无法打开 Codex 侧栏或无法附加编辑器上下文，按以下顺序排查：

1. 确认你是在已打开仓库目录的 VS Code 窗口内、Codex 聊天面板中发送请求。
2. 若处于 Restricted Mode，先检查目录并确认其来源可信，再信任 workspace。可使用 **Manage** 链接，或从命令面板运行 **Workspaces: Manage Workspace Trust**，随后重载窗口。
3. 确认 Codex 扩展已启用，且没有显示 **Reload Required**。
4. 打开实际项目文件、选中几行内容，将文件或选区添加到 composer，并发送一个小型测试请求。
5. 新建一个 Codex 对话后，再次尝试附加文件或选区。
6. 更新 Codex 扩展；若问题仍在，卸载扩展、完全退出 VS Code、重新安装扩展，再打开已信任的 workspace、打开 Codex 侧栏并重试附加上下文。

即使 IDE context 一直无法连接，你仍可在提示中提供仓库相对路径、选中代码或完整诊断信息。在当前会话具有 workspace 读取权限的前提下，Codex 仍能据此读取相关仓库文件并协助完成任务。

## 版本与隐私说明

可用的 IDE context 与 composer 控件会随着 Codex 扩展版本、VS Code 配置和 workspace 策略而变化。请以当前已安装客户端在本次请求中显示的已附加上下文为准。关于 VS Code 的信任行为和 Restricted Mode，请参考官方 [Workspace Trust 文档](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust)。

不要在提示词或公开仓库 issue 中粘贴凭据、访问令牌、私钥、生产数据，或雇主/客户的机密材料。使用本地开发工具时，遵循所在组织的 workspace 和数据处理政策。
