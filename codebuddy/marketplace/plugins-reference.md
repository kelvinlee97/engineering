# CodeBuddy 插件参考文档

## 概述

CodeBuddy 插件系统允许通过标准化的插件机制扩展 AI 助手的功能。插件可以提供自定义命令、代理、技能、规则、钩子和 MCP 服务器等组件。

---

## 一、插件组件参考

插件可以提供以下类型的组件：

### 1. Commands （命令）

**位置**：插件根目录的 `commands/` 目录
**格式**：带有 frontmatter 的 Markdown 文件

**功能**:
- 添加自定义斜杠命令
- 与 CodeBuddy 命令系统无缝集成

**Frontmatter 配置**:
```markdown
---
description：命令描述
allowed-tools: Read,Write,Bash
argument-hint：参数提示
model：使用的模型ID或名称
---

命令的提示词内容
```

**命令文件组织**:
- 支持子目录嵌套组织
- 子目录路径会转换为命令名的一部分，使用冒号分隔
- 例如： `commands/deploy/production.md` → 命令名为 `deploy:production`

### 2. Agents （代理）

**位置**：插件根目录的 `agents/` 目录
**格式**：带有 frontmatter 的 Markdown 文件

**Frontmatter 配置**:
```markdown
---
name：代理名称（可选，默认使用文件名）
description：代理描述
model：使用的模型ID或名称
tools: Read,Write,Bash（可用工具列表，逗号分隔）
color: #FF5733（代理显示颜色，可选）
---

代理的指令内容
```

**特性**:
- 代理可以作为工具被主代理调用
- 支持自定义工具列表
- 自动生成源标签标识来源

### 3. Skills （技能）

**位置**：插件根目录的 `skills/` 目录
**格式**：每个技能一个子目录，包含 `SKILL.md` 文件

**目录结构**:
```
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md （可选）
│   └── scripts/ （可选）
└── code-reviewer/
    └── SKILL.md
```

**SKILL.md Frontmatter 配置**:
```markdown
---
name：技能名称（可选，默认使用目录名）
description：技能描述
allowed-tools: Read,Write,Bash（允许使用的工具列表）
---

技能的指令内容
```

**特性**:
- 技能可以包含辅助文件和脚本
- 技能的 `baseDirectory` 指向技能目录，可访问同目录下的资源文件

### 4. Hooks （钩子）

**位置**：插件根目录的 `hooks/hooks.json`,或在 `plugin.json` 中通过 PluginInfo 扩展字段配置
**格式**: JSON 配置，包含事件匹配器和操作

**配置示例**:
```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CODEBUDDY_PLUGIN_ROOT}/scripts/format-code.sh",
          "timeout": 30000
        }
      ]
    }
  ]
}
```

**可用事件**:
- `PreToolUse`：在工具使用之前触发
- `PostToolUse`：在工具使用之后触发
- `UserPromptSubmit`：用户提交提示时触发
- `Notification`：发送通知时触发
- `Stop`：尝试停止时触发
- `SubagentStop`：子代理尝试停止时触发
- `SessionStart`：会话开始时触发
- `SessionEnd`：会话结束时触发
- `PreCompact`：对话历史压缩之前触发

**钩子类型**:
- `command`：执行 shell 命令或脚本

**Matcher 规则**:
- 支持正则表达式匹配工具名称
- 例如： `"Write|Edit"` 匹配 Write 或 Edit 工具

### 5. Rules （规则）

**位置**：插件根目录的 `rules/` 目录
**格式**：带有 YAML frontmatter 的 Markdown 文件

**功能**:
- 为插件提供项目级指令和行为规则
- 支持始终应用或条件触发两种模式
- 插件启用时自动加载规则到上下文中

**Rules 目录结构**:
```
rules/
├── general.md           # 通用规则
├── frontend/
│   └── react.md         # 前端相关规则
└── backend/
    └── api.md           # 后端相关规则
```

**YAML Frontmatter 配置**:
```markdown
---
alwaysApply: true
---

规则内容（Markdown 格式）
```

**Frontmatter 字段说明**:

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| enabled | boolean | true | 是否加载此规则。设为 false 时规则完全不加载 |
| alwaysApply | boolean | true | 是否始终应用此规则 |
| paths | string/string[] | — | 触发规则的文件路径 glob 模式 |

**规则类型**:

| alwaysApply | paths | 规则类型 | 行为 |
|-------------|-------|----------|------|
| true（默认） | 任意 | ALWAYS | 始终注入到上下文 |
| false | 有值 | 条件触发 | 仅在操作匹配文件时触发 |
| false | 无值 | 不支持 | 规则不会加载 |

**示例**:

始终应用的规则：
```markdown
---
alwaysApply: true
---

## 代码规范
- 使用 2 空格缩进
- 文件末尾保留空行
```

条件触发的规则：
```markdown
---
alwaysApply: false
paths: src/api/**/*.ts
---

## API 开发规则
- 所有 API 端点必须包含输入验证
- 使用标准错误响应格式
```

**特性**:
- 所有 `.md` 文件在 `rules/` 目录下递归发现
- 支持子目录组织规则
- `paths` 字段支持标准 glob 模式（启用 matchBase）
- 所有 frontmatter 字段均为可选，不写 frontmatter 时使用默认值

### 6. MCP Servers (MCP 服务器）

**位置**:
- 插件根目录的 `.mcp.json` 配置文件
- 或在 `plugin.json` 中通过 PluginInfo 扩展字段配置

**配置示例** (.mcp.json):
```json
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CODEBUDDY_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CODEBUDDY_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CODEBUDDY_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CODEBUDDY_PLUGIN_ROOT}"
    }
  }
}
```

**集成行为**:
- 插件启用时自动启动 MCP 服务器
- 服务器作为标准 MCP 工具出现在工具包中
- 服务器功能与现有工具无缝集成

### 7. LSP Servers（LSP 服务器）

> **提示**: 需要使用 LSP 插件? 可从官方市场安装——在 `/plugin` Discover 标签中搜索 "lsp"。本节介绍如何为官方市场未涵盖的语言创建 LSP 插件。

插件可以提供 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) 服务器，为 AI 助手在代码库上工作时提供实时代码智能支持。

LSP 集成提供:

* **即时诊断**: AI 助手在每次编辑后立即看到错误和警告
* **代码导航**: 跳转到定义、查找引用和悬停信息
* **语言感知**: 代码符号的类型信息和文档

**位置**: 插件根目录的 `.lsp.json` 文件，或在 `plugin.json` 中内联配置

**格式**: JSON 配置，将语言服务器名称映射到其配置

**`.lsp.json` 文件格式**:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**在 `plugin.json` 中内联配置**:

```json
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**必需字段**:

| 字段 | 描述 |
| :--- | :--- |
| `command` | 要执行的 LSP 二进制文件（必须在 PATH 中） |
| `extensionToLanguage` | 将文件扩展名映射到语言标识符 |

**可选字段**:

| 字段 | 描述 |
| :--- | :--- |
| `args` | LSP 服务器的命令行参数 |
| `transport` | 通信传输方式: `stdio`（默认）或 `socket` |
| `env` | 启动服务器时设置的环境变量 |
| `initializationOptions` | 在初始化期间传递给服务器的选项 |
| `settings` | 通过 `workspace/didChangeConfiguration` 传递的设置 |
| `workspaceFolder` | 服务器的工作区文件夹路径 |
| `startupTimeout` | 等待服务器启动的最大时间（毫秒） |
| `shutdownTimeout` | 等待优雅关闭的最大时间（毫秒） |
| `restartOnCrash` | 服务器崩溃时是否自动重启 |
| `maxRestarts` | 放弃前的最大重启尝试次数 |
| `loggingConfig` | 调试日志配置（见下文） |

> **警告**: **您必须单独安装语言服务器二进制文件。** LSP 插件配置 CodeBuddy 如何连接到语言服务器，但不包含服务器本身。如果在 `/plugin` Errors 标签中看到 `Executable not found in $PATH` 错误，请为您的语言安装所需的二进制文件。

**可用的 LSP 插件**:

| 插件 | 语言服务器 | 安装命令 |
| :--- | :--- | :--- |
| `pyright-lsp` | Pyright (Python) | `pip install pyright` 或 `npm install -g pyright` |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript` |
| `rust-lsp` | rust-analyzer | [参见 rust-analyzer 安装](https://rust-analyzer.github.io/manual.html#installation) |

先安装语言服务器，然后从市场安装插件。

---

## 二、插件清单架构 （plugin.json)

### 完整架构示例

```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "插件简短描述",
  "author": {
    "name": "作者名称",
    "email": "[email protected]",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "category": "开发工具",
  "features": ["特性1", "特性2"],
  "requirements": {
    "node": ">=16.0.0"
  },
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": [
    {
      "name": "custom-server",
      "command": "node",
      "args": ["./servers/custom.js"],
      "env": {
        "SERVER_PORT": "3000"
      }
    }
  ],
  "lspServers": "./.lsp.json"
}
```

### 必需字段

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| name | string | 唯一标识符（kebab-case，无空格） | "deployment-tools" |
| description | string | 插件用途简述 | "部署自动化工具" |

### 元数据字段

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| version | string | 语义化版本 | "2.1.0" |
| author | object | 作者信息 | `{"name": "开发团队", "email": "[email protected]"}` |
| homepage | string | 文档 URL | "https://docs.example.com" |
| repository | string | 源代码 URL | "https://github.com/user/plugin" |
| license | string | 许可证标识符 | "MIT", "Apache-2.0" |
| keywords | array | 发现标签 | `["deployment", "ci-cd"]` |
| category | string | 插件分类 | "开发工具" |
| features | array | 功能列表 | `["自动部署", "日志分析"]` |

### 组件路径字段（PluginManifest）

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| commands | string / string[] | 额外的命令文件路径数组 | `["./custom/cmd.md"]` |
| agents | string / string[] | 额外 Agent 文件目录路径 | "./custom/agents/" |
| hooks | string / object | 额外 Hook 文件或配置 | "./custom/hooks.json" |
| mcpServers | string / `Record<string,MCPServerConfig>` | MCP服务器配置文件路径或配置对象 | 见下方 MCPServerConfig |
| lspServers | string / object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 配置，用于代码智能（跳转定义、查找引用等） | `"./.lsp.json"` |

### MCPServerConfig 结构

```typescript
{
  "name": "服务器名称",
  "command": "执行命令",
  "args": ["命令参数数组"],
  "env": {
    "环境变量名": "值"
  }
}
```

### 运行时扩展字段（PluginInfo）

插件在运行时会扩展以下字段，支持更灵活的配置方式：

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| agents | string[] | Agent 文件或目录路径 | `["./custom/agents/"]` |
| commands | string[] | Command 文件或目录路径 | `["./custom/commands/"]` |
| skills | string[] | Skill 文件或目录路径 | `["./custom/skills/"]` |
| hooks | `Record<string, any>` \| string | Hook 配置对象或文件路径 | "./hooks/custom.json" |
| mcpServers | `Record<string, McpConfig>` \| string | MCP 配置对象或文件路径 | "./mcp-config.json" |
| lspServers | `Record<string, LspConfig>` \| string | LSP 配置对象或文件路径 | "./.lsp.json" |

**说明**:
- 这些扩展字段用于 marketplace.json 中配置插件的加载方式
- 支持直接配置对象或文件路径字符串
- 加载器会智能合并配置路径和默认目录扫描的结果

### 路径行为规则

**重要**：自定义路径是对默认目录的**补充**，而不是替换。

- 如果 `commands/` 目录存在，它会与自定义命令路径一起加载
- 所有路径必须相对于插件根目录，并以 `./` 开头
- 可以将多个路径指定为数组以提高灵活性
- 路径可以指向单个文件或目录

**路径解析规则**:
- 文件路径： 必须以 `.md` 结尾（对于 commands/agents）或为 `SKILL.md`（对于 skills）
- 目录路径： 会递归扫描目录中的所有符合条件的文件

### 环境变量

**`${CODEBUDDY_PLUGIN_ROOT}`**：包含插件目录的绝对路径。在钩子、MCP 服务器和脚本中使用此变量，以确保无论安装位置如何都能使用正确的路径。

**兼容性**：同时支持 `${CLAUDE_PLUGIN_ROOT}` 变量名以兼容 Claude Code 插件。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CODEBUDDY_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 三、插件目录结构

### 标准插件布局

```
enterprise-plugin/
├── .codebuddy-plugin/       # 元数据目录
│   └── plugin.json          # 必需：插件清单
├── commands/                # 默认命令位置
│   ├── status.md
│   └── logs.md
├── agents/                  # 默认代理位置
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                  # 代理技能
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── rules/                   # 规则文件
│   └── my-rules.md          # 项目级规则
├── hooks/                   # 钩子配置
│   └── hooks.json           # 钩子配置文件
├── .mcp.json               # MCP 服务器定义
├── .lsp.json               # LSP 服务器配置
├── scripts/                # 钩子和实用脚本
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                 # 许可证文件
└── README.md               # 插件说明
```

**重要**:
- `.codebuddy-plugin/` 或 `.claude-plugin/` 目录包含 `plugin.json` 文件
- 所有其他目录（`commands/`、`agents/`、`skills/`、`rules/`、`hooks/`）必须位于插件根目录
- 系统优先识别 `.codebuddy-plugin/`,同时兼容 `.claude-plugin/`

### 文件位置参考

| 组件 | 默认位置 | 用途 |
|------|----------|------|
| Manifest | .codebuddy-plugin/plugin.json | 必需的元数据文件 |
| Commands | commands/ | 斜杠命令 markdown 文件 |
| Agents | agents/ | 子代理 markdown 文件 |
| Skills | skills/ | 带有 SKILL.md 文件的代理技能 |
| Rules | rules/ | 项目级规则 markdown 文件 |
| Hooks | hooks/hooks.json | 钩子配置 |
| MCP servers | .mcp.json | MCP 服务器定义 |
| LSP servers | .lsp.json | 语言服务器配置 |

---

## 四、市场清单架构 （marketplace.json)

### 完整架构示例

```json
{
  "name": "企业插件市场",
  "description": "企业内部插件集合",
  "version": "1.0.0",
  "owner": {
    "name": "企业开发团队",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "deployment-tool",
      "description": "自动化部署工具",
      "version": "1.0.0",
      "source": "plugins/deployment-tool"
    },
    {
      "name": "code-review-bot",
      "description": "代码审查机器人",
      "version": "2.1.0",
      "source": {
        "source": "github",
        "repo": "company/code-review-bot"
      }
    },
    {
      "name": "security-scanner",
      "description": "安全扫描工具",
      "version": "1.5.0",
      "source": {
        "source": "url",
        "url": "https://github.com/company/security-scanner.git"
      }
    }
  ]
}
```

### 必需字段

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| name | string | 市场名称 | "企业插件市场" |
| plugins | array | 插件列表 | 见下方 |

### 元数据字段

| 字段 | 类型 | 描述 | 示例 |
|------|------|------|------|
| description | string | 市场描述 | "企业内部插件集合" |
| version | string | 市场版本 | "1.0.0" |
| owner | object | 所有者信息 | `{"name": "团队", "email": "..."}` |

### 插件条目 （MarketplacePluginEntry)

每个插件条目包含以下字段：

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| name | string | ✓ | 插件唯一标识符 |
| description | string | ✓ | 插件描述 |
| version | string | | 插件版本号 |
| source | string \| PluginSource | ✓ | 插件源配置 |
| strict | boolean | | 严格模式（兼容 superpowers-marketplace） |

### PluginSource 配置

插件源支持三种类型：

#### 1. 本地相对路径（字符串）
```json
{
  "source": "plugins/my-plugin"
}
```

#### 2. 本地路径（对象）
```json
{
  "source": {
    "source": "local",
    "path": "plugins/my-plugin"
  }
}
```

#### 3. GitHub 仓库
```json
{
  "source": {
    "source": "github",
    "repo": "owner/repo-name"
  }
}
```

#### 4. Git URL
```json
{
  "source": {
    "source": "url",
    "url": "https://github.com/owner/repo.git"
  }
}
```

### 市场类型

CodeBuddy 支持四种市场类型：

| 类型 | 说明 | source 字段 |
|------|------|-------------|
| Directory | 本地文件系统目录 | path：本地目录绝对路径 |
| Github | GitHub 仓库 | repo: owner/repo 格式 |
| Git | Git 仓库 | url: Git 仓库 URL |
| URL | HTTP/HTTPS 远端 | url: marketplace.json 的 URL |

---

## 五、插件加载机制

### 加载流程

1. **市场安装**:
   - 从配置的源安装市场
   - 读取 `marketplace.json` 获取插件列表

2. **插件安装**:
   - 根据 `source` 配置选择合适的安装器（Local/Git）
   - 将插件内容安装到目标位置

3. **插件启用**:
   - 读取插件的 `plugin.json` 清单
   - 根据清单配置加载各类组件

4. **组件加载**:
   - 并发加载所有类型的扩展组件
   - 合并配置路径和默认目录扫描的结果
   - 缓存加载的组件以提高性能

### 加载器智能合并

每个扩展加载器都会智能合并两个来源的内容：

1. **配置路径**：在 `plugin.json` 或运行时配置中指定的路径
2. **默认扫描**：默认目录（如 `commands/`、`agents/`）中的文件

**示例**:
```json
{
  "commands": ["./custom/deploy.md"],
  // 实际加载：
  // - ./custom/deploy.md （配置路径）
  // - commands/ 目录中的所有 .md 文件 （默认扫描）
}
```

### 命令名称生成规则

- 文件名： `command.md` → 命令名: `command`
- 子目录： `deploy/prod.md` → 命令名: `deploy:prod`
- 插件前缀： 自动添加插件名作为前缀，如 `plugin-name:command`

### 代理和技能标签

所有从插件加载的代理和技能都会自动添加以下标签：
- 来源标签： `(plugin-name@marketplace-name)`
- 类型标签： `plugin`
- 自定义标签： `custom-agent` 或 `custom-command`

---

## 六、调试和开发工具

### 查看插件加载日志

使用 `--verbose` 参数查看详细的插件加载信息：

```bash
codebuddy --verbose
```

**显示内容**:
- 正在加载哪些插件
- 插件清单中的任何错误
- 命令、代理和技能注册
- MCP 服务器初始化
- Hooks 配置加载

### 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 插件未加载 | 无效的 plugin.json | 验证 JSON 语法，检查必需字段 |
| 命令未出现 | 错误的目录结构 | 确保 commands/ 在插件根目录 |
| 钩子未触发 | 脚本不可执行 | 运行 `chmod +x script.sh` |
| MCP 服务器失败 | 缺少环境变量 | 使用 `${CODEBUDDY_PLUGIN_ROOT}` |
| 路径错误 | 使用了绝对路径 | 所有路径必须是相对路径并以 `./` 开头 |
| 元数据目录未识别 | 使用了错误的目录名 | 使用 `.codebuddy-plugin/` 或 `.claude-plugin/` |
| LSP `Executable not found in $PATH` | 语言服务器未安装 | 安装二进制文件（例如：`npm install -g typescript-language-server typescript`） |

### 插件开发最佳实践

1. **使用相对路径**：所有文件引用使用相对路径，确保跨环境兼容
2. **环境变量**：在脚本中使用 `${CODEBUDDY_PLUGIN_ROOT}` 引用插件目录
3. **错误处理**：为钩子脚本添加适当的错误处理和超时设置
4. **文档完善**：在 README.md 中提供清晰的安装和使用说明
5. **语义化版本**：遵循语义化版本规范管理插件版本
6. **测试覆盖**：在不同环境下测试插件的安装和功能

---

## 七、版本管理参考

### 语义化版本控制

遵循语义化版本控制进行插件发布：

- **主版本号 （MAJOR)**：不兼容的 API 更改
- **次版本号 （MINOR)**：向后兼容的功能添加
- **修订号 （PATCH)**：向后兼容的错误修复

示例： `1.2.0` → `1.2.1` （修复） → `1.3.0` （新功能） → `2.0.0` （破坏性更改）

### 插件更新流程

1. 修改插件代码和资源
2. 更新 `plugin.json` 中的 version 字段
3. 在 CHANGELOG.md 中记录变更
4. 提交到版本控制系统
5. 用户通过 marketplace 更新插件

---

## 八、CLI 命令参考

### 市场管理

```bash
# 添加市场
codebuddy plugin marketplace add <source> [--name <name>]

# 列出市场
codebuddy plugin marketplace list

# 更新市场
codebuddy plugin marketplace update <name>

# 删除市场
codebuddy plugin marketplace remove <name>
```

### 插件管理

```bash
# 安装插件
codebuddy plugin install <plugin-name> <marketplace-name>

# 列出已安装插件
codebuddy plugin list [--marketplace <name>]

# 启用插件
codebuddy plugin enable <plugin-name> <marketplace-name>

# 禁用插件
codebuddy plugin disable <plugin-name> <marketplace-name>

# 卸载插件
codebuddy plugin uninstall <plugin-name> <marketplace-name>

# 更新插件
codebuddy plugin update <plugin-name> <marketplace-name>
```

### 市场源格式

支持以下格式添加市场：

```bash
# 本地目录
codebuddy plugin marketplace add /path/to/marketplace

# GitHub 简写
codebuddy plugin marketplace add owner/repo

# Git URL
codebuddy plugin marketplace add https://github.com/owner/repo.git

# HTTP URL (marketplace.json)
codebuddy plugin marketplace add https://example.com/marketplace.json
```

---

## 九、与 Claude Code 的兼容性

CodeBuddy 插件系统在设计上兼容 Claude Code 插件规范，但存在以下差异：

### 命名差异

| 概念 | Claude Code | CodeBuddy |
|------|-------------|-----------|
| 元数据目录 | `.claude-plugin/` | `.codebuddy-plugin/` （优先） 或 `.claude-plugin/` （兼容） |
| 环境变量 | `${CLAUDE_PLUGIN_ROOT}` | `${CODEBUDDY_PLUGIN_ROOT}` （优先） 或 `${CLAUDE_PLUGIN_ROOT}` （兼容） |

### 扩展功能

CodeBuddy 在 Claude Code 基础上提供了以下扩展：

1. **运行时配置**: PluginInfo 支持运行时扩展字段配置
2. **多元数据目录**：同时支持 `.codebuddy-plugin/` 和 `.claude-plugin/`
3. **灵活的配置**：支持配置对象和文件路径两种配置方式

### 迁移指南

从 Claude Code 迁移到 CodeBuddy：

1. 可选择将 `.claude-plugin/` 重命名为 `.codebuddy-plugin/`
2. 可选择将脚本中的 `${CLAUDE_PLUGIN_ROOT}` 替换为 `${CODEBUDDY_PLUGIN_ROOT}`
3. 如果使用了 `mcpServers` 字段,需要重命名为 `mcpServers`

**注意**：保持原有命名也完全兼容，CodeBuddy 会自动识别。

---

## 相关资源

- **插件开发教程** - 如何创建自定义插件
- **市场创建指南** - 创建和管理插件市场
- **Hooks 深入指南** - 事件处理和自动化
- **MCP 集成文档** - 外部工具集成
- **Settings 配置** - 插件配置选项

---

## 总结

本文档提供了 CodeBuddy 插件系统的完整技术规范，涵盖：

1. 七种插件组件类型（Commands、Agents、Skills、Rules、Hooks、MCP Servers、LSP Servers）
2. 完整的 plugin.json 清单架构和字段说明
3. marketplace.json 市场清单架构
4. 标准目录结构和文件位置
5. 插件加载机制和智能合并规则
6. CLI 命令和调试工具
7. 版本管理最佳实践
8. 与 Claude Code 的兼容性说明

开发者可以使用此参考文档创建功能完整、结构规范的 CodeBuddy 插件。
