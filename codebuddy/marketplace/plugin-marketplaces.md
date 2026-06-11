# 插件市场 （Plugin Marketplaces)

插件市场（Plugin Marketplace）是一个插件目录文件，用于分发和管理 CodeBuddy 扩展。它是一个 JSON 格式的配置文件，列出了可用的插件及其来源信息。

## 核心功能

- **集中发现**：在一个地方浏览来自多个来源的插件
- **版本管理**：自动跟踪和更新插件版本
- **自动更新**：支持启用自动更新，定期同步市场内容
- **团队分发**：在组织内共享必需的插件
- **灵活来源**：支持 Git 仓库、GitHub 仓库、本地路径和 HTTP URL

## 使用插件市场

### 前置要求

- 已安装并运行 CodeBuddy
- 基本了解 JSON 文件格式
- 创建 marketplace 需要：Git 仓库或本地开发环境

### 添加插件市场

#### 1. 添加 GitHub 市场

```bash
/plugin marketplace add owner/repo
```

要求仓库包含 `.codebuddy-plugin/marketplace.json` 文件。

#### 2. 添加 Git 仓库市场

```bash
# HTTPS 格式
/plugin marketplace add https://gitlab.com/company/plugins.git

# SSH 格式 （git@)
/plugin marketplace add git@gitlab.com:company/plugins.git

# .git 后缀格式
/plugin marketplace add https://example.com/repo.git
```

#### 3. 添加本地市场（用于开发）

```bash
# 添加包含 .codebuddy-plugin/marketplace.json 的本地目录
/plugin marketplace add ./my-marketplace

# 直接添加 marketplace.json 文件路径
/plugin marketplace add ./path/to/marketplace.json
```

#### 4. 添加 HTTP 市场

```bash
# 通过 URL 添加远程 marketplace.json
/plugin marketplace add https://url.of/marketplace.json
```

### 从市场安装插件

```bash
# 从已知的 marketplace 安装
/plugin install plugin-name@marketplace-name

# 交互式浏览可用插件
/plugin
```

### 验证市场安装

1. **列出市场**：运行 `/plugin marketplace list` 确认已添加
2. **浏览插件**：使用 `/plugin` 查看 marketplace 中的可用插件
3. **测试安装**：尝试安装一个插件以验证 marketplace 正常工作

## 团队配置

### 自动安装团队市场

在 `.codebuddy/settings.json` 中配置：

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/codebuddy-plugins"
      }
    },
    "project-specific": {
      "source": {
        "source": "git",
        "url": "https://git.company.com/project-plugins.git"
      }
    }
  },
  "enabledPlugins": {
    "plugin-a@team-tools": true,
    "plugin-b@team-tools": true
  }
}
```

当团队成员启动 CodeBuddy 时，系统会自动安装这些 marketplace 和 `enabledPlugins` 字段中指定的插件。

### 自动安装流程

1. **启动检测**：CodeBuddy 启动时会自动检测配置文件
2. **市场安装**：自动安装 `extraKnownMarketplaces` 中未安装的市场
3. **插件安装**：自动安装 `enabledPlugins` 中已启用但未安装的插件
4. **后台执行**：安装过程在后台异步执行，不阻塞启动流程
5. **日志记录**：安装过程会记录详细日志，可通过 `--debug` 查看

## 创建自己的市场

### 创建前置要求

- Git 仓库（GitHub、GitLab 或其他 git 托管服务）
- 了解 JSON 文件格式
- 一个或多个要分发的插件

### 创建市场文件

在仓库根目录创建 `.codebuddy-plugin/marketplace.json`：

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0"
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

### 市场配置结构 （Marketplace Schema)

#### 必需字段

| 字段 | 类型 | 描述 |
|------|------|------|
| name | string | 市场标识符（kebab-case，无空格）|
| owner | object | 市场维护者信息 |
| plugins | array | 可用插件列表 |

#### 可选元数据字段

| 字段 | 类型 | 描述 |
|------|------|------|
| description | string | 市场简要描述 |
| version | string | 市场版本 |

### 插件条目配置

#### 必需字段

| 字段 | 类型 | 描述 |
|------|------|------|
| name | string | 插件标识符（kebab-case，无空格）|
| source | string/object | 插件获取来源 |
| description | string | 插件简要描述 |

#### 可选元数据字段

| 字段 | 类型 | 描述 |
|------|------|------|
| version | string | 插件版本 |
| author | object | 插件作者信息 |
| homepage | string | 插件主页或文档 URL |
| repository | string | 源代码仓库 URL |
| license | string | SPDX 许可证标识符（如 MIT、Apache-2.0）|
| keywords | array | 用于插件发现和分类的标签 |
| category | string | 插件分类 |
| strict | boolean | 要求插件文件夹中有 plugin.json（默认：true）|

#### 组件配置字段

| 字段 | 类型 | 描述 |
|------|------|------|
| commands | string/array | 命令文件或目录的自定义路径 |
| agents | string/array | Agent 文件的自定义路径 |
| skills | string/array | Skill 文件的自定义路径 |
| rules | string/array | Rules 文件或目录的自定义路径 |
| hooks | string/object | 自定义 hooks 配置或 hooks 文件路径 |
| mcpServers | string/object | MCP 服务器配置或 MCP 配置路径 |

**关于 strict 字段**：

- `strict: true`(默认):插件必须包含 `plugin.json` 清单文件，marketplace 字段补充这些值
- `strict: false`:`plugin.json` 是可选的。如果缺失，marketplace 条目作为完整的插件清单

### 插件来源类型

#### 1. 相对路径（Local）

用于同一仓库中的插件：

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "My local plugin"
}
```

#### 2. GitHub 仓库

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  },
  "description": "Plugin from GitHub"
}
```

#### 3. Git URL

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  },
  "description": "Plugin from Git URL"
}
```

### 高级插件条目示例

```json
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "[email protected]"
  },
  "homepage": "https://docs.company.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": [
    "./agents/security-reviewer.md",
    "./agents/compliance-checker.md"
  ],
  "skills": [
    "./skills/deployment.md",
    "./skills/monitoring.md"
  ],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "${CODEBUDDY_PLUGIN_ROOT}/scripts/validate.sh"
        }]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CODEBUDDY_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CODEBUDDY_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

**注意**：`${CODEBUDDY_PLUGIN_ROOT}` 是一个环境变量，解析为插件的安装目录。

## 托管和分发市场

### 1. 在 GitHub 上托管（推荐）

**步骤**：

1. 创建仓库：为 marketplace 设置新仓库
2. 添加 marketplace 文件：创建 `.codebuddy-plugin/marketplace.json` 并定义插件
3. 与团队共享：团队成员使用 `/plugin marketplace add owner/repo` 添加

**优势**：内置版本控制、问题跟踪和团队协作功能

### 2. 在其他 Git 服务上托管

任何 git 托管服务都可以用于 marketplace 分发。例如使用 GitLab：

```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### 3. 使用 HTTP URL 托管

可以将 marketplace.json 文件托管在任何 HTTP(S) 服务器上：

```bash
/plugin marketplace add https://example.com/path/to/marketplace.json
```

### 4. 使用本地市场进行开发

在分发前本地测试 marketplace：

```bash
# 添加本地 marketplace 进行测试
/plugin marketplace add ./my-local-marketplace

# 测试插件安装
/plugin install test-plugin@my-local-marketplace
```

## 市场管理操作

### 列出已知的市场

```bash
/plugin marketplace list
```

显示所有配置的 marketplace 及其来源和状态。

### 更新市场元数据

```bash
/plugin marketplace update marketplace-name
```

从 marketplace 来源刷新插件列表和元数据。

### 移除市场

```bash
/plugin marketplace remove marketplace-name
```

从配置中移除 marketplace。

**⚠️ 警告**：移除 marketplace 将卸载从中安装的所有插件。

### 管理自动更新

可以为市场启用自动更新功能，CodeBuddy 会在启动时自动检查并更新已启用的市场。

**启用方式**：

1. 运行 `/plugin` 命令进入插件管理界面
2. 选择「Marketplaces」查看市场列表
3. 选择需要配置的市场
4. 选择「Enable auto-update」或「Disable auto-update」切换状态

**自动更新机制**：

- 启动时延迟 5 秒后执行，不影响主流程
- 仅更新距上次更新超过 24 小时的市场
- 多个市场间隔 2 秒依次更新，避免资源竞争
- 更新失败不影响其他市场，错误记录到日志

## 实现原理

### 市场类型

CodeBuddy 支持以下几种市场类型：

1. **Directory（本地目录）**：从本地文件系统加载插件
2. **GitHub**：从 GitHub 仓库克隆和更新插件
3. **Git**：从任意 Git 仓库克隆和更新插件
4. **URL（HTTP）**：从 HTTP(S) URL 下载 marketplace.json

### 市场工厂模式

通过 `MarketplaceFactory` 根据配置创建不同类型的市场实例：

```typescript
// 根据源类型创建对应的市场实例
switch (sourceType) {
    case MarketplaceType.Directory:
        marketplace = new DirectoryMarketplace();
        break;
    case MarketplaceType.Github:
    case MarketplaceType.Git:
        marketplace = new GithubMarketplace();
        break;
    case MarketplaceType.URL:
        marketplace = new HttpMarketplace();
        break;
    default:
        marketplace = new BaseMarketplace();
        break;
}
```

### 安装流程

1. **解析源**：根据输入字符串判断市场类型（本地路径、GitHub 仓库、Git URL、HTTP URL）
2. **下载/克隆**：根据市场类型下载或克隆市场内容
3. **读取清单**：解析 `.codebuddy-plugin/marketplace.json` 文件
4. **保存配置**：将市场信息保存到本地存储
5. **更新缓存**：刷新插件缓存和市场列表

### 插件安装器

CodeBuddy 使用插件安装器（PluginInstaller）来处理不同类型的插件源：

- **本地安装器**：处理相对路径插件
- **Git 安装器**：处理 GitHub 和 Git URL 插件

每个安装器实现以下方法：

- `support(source)`：判断是否支持该插件源
- `isInstalled(plugin, targetDir)`：检查插件是否已安装
- `install(plugin, targetDir)`：安装插件
- `update(plugin, installedPath)`：更新插件

## 故障排除

### 常见问题

#### 1. 市场无法加载

**症状**：无法添加 marketplace 或看不到其中的插件

**解决方案**：

- 验证 marketplace URL 可访问
- 检查指定路径是否存在 `.codebuddy-plugin/marketplace.json`
- 确保 JSON 语法有效
- 对于私有仓库，确认您有访问权限

#### 2. 插件安装失败

**症状**：Marketplace 显示但插件安装失败

**解决方案**：

- 验证插件源 URL 可访问
- 检查插件目录是否包含必需文件
- 对于 GitHub 源，确保仓库是公开的或您有访问权限
- 通过克隆/下载手动测试插件源

#### 3. Git 操作失败

**症状**：克隆或拉取仓库时出错

**解决方案**：

- 确保已安装 Git 并可在命令行使用
- 检查网络连接和代理设置
- 验证 Git 凭据配置正确
- 使用 `--debug` 标志查看详细日志

### 调试技巧

1. **启用调试日志**：

```bash
codebuddy --debug
```

2. **手动验证市场文件**：

```bash
# 检查 marketplace.json 格式
cat .codebuddy-plugin/marketplace.json | jq
```

3. **测试 Git 克隆**：

```bash
# 手动测试 Git 克隆是否成功
git clone https://github.com/owner/repo.git /tmp/test-clone
```

## 下一步

### 对于市场用户

- 发现社区 marketplaces：在 GitHub 上搜索 CodeBuddy 插件集合
- 贡献反馈：向 marketplace 维护者报告问题和建议改进
- 分享有用的 marketplaces：帮助团队发现有价值的插件集合

### 对于市场创建者

- 构建插件集合：围绕特定用例创建主题 marketplace
- 建立版本控制：实施清晰的版本控制和更新策略
- 社区参与：收集反馈并维护活跃的 marketplace 社区
- 文档：提供清晰的 README 文件解释 marketplace 内容

### 对于组织

- 私有 marketplaces：为专有工具设置内部 marketplace
- 治理策略：建立插件审批和安全审查指南
- 培训资源：帮助团队有效发现和采用有用的插件

## 相关资源

- [插件系统](./plugins.md) - 插件系统总览
- [技能系统](./skills.md) - 创建和使用技能
- [斜杠命令](./slash-commands.md) - 创建自定义命令
- [Hooks](./hooks.md) - 创建事件钩子
- [设置](./settings.md) - 插件配置选项
