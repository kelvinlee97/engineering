# LSP 配置（共享片段）

> 引用方：commands/project.md、commands/diff.md

## 语言检测

通过 Glob 检查 `{pom.xml,build.gradle*,package.json,tsconfig.json,go.mod,requirements.txt,pyproject.toml,setup.py,Cargo.toml,*.sln,*.csproj,Package.swift,CMakeLists.txt,composer.json}`。

回退策略：`**/*.{c,cpp,h,hpp}` 和 `**/*.lua`（取匹配数较多的一个）。

| 标记文件 | 语言 |
|---|---|
| `pom.xml`, `build.gradle*` | Java/Kotlin |
| `package.json`, `tsconfig.json` | JavaScript/TypeScript |
| `go.mod` | Go |
| `requirements.txt`, `pyproject.toml`, `setup.py` | Python |
| `Cargo.toml` | Rust |
| `*.sln`, `*.csproj` | C# |
| `Package.swift` | Swift |
| `CMakeLists.txt` | C/C++ |
| `composer.json` | PHP |

## LSP 插件映射

| 语言 | 插件名称 | 二进制文件 | 安装命令 |
|---|---|---|---|
| Java/Kotlin | `jdtls-lsp` | `jdtls` | `brew install jdtls` |
| JS/TS | `typescript-lsp` | `typescript-language-server` | `npm i -g typescript-language-server typescript` |
| Go | `gopls-lsp` | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| Python | `pyright-lsp` | `pyright-langserver` | `pip install pyright` |
| Rust | `rust-analyzer-lsp` | `rust-analyzer` | `rustup component add rust-analyzer` |
| C# | `csharp-lsp` | `csharp-ls` | `dotnet tool install --global csharp-ls` |
| Swift | `swift-lsp` | `sourcekit-lsp` | Xcode 内置 |
| C/C++ | `clangd-lsp` | `clangd` | `brew install llvm` |
| PHP | `php-lsp` | `intelephense` | `npm i -g intelephense` |
| Lua | `lua-lsp` | `lua-language-server` | `brew install lua-language-server` |

## LSP 预热

检测到语言后，立即对任意源文件调用 `LSP documentSymbol` 以触发语言服务器初始化。

## LSP 可用性检查

如果预热失败，执行**并行**检查：

1. `which {lspBinary} 2>/dev/null || echo "NOT_FOUND"`
2. `codebuddy plugin list 2>/dev/null | grep {lspPluginName} || echo "NOT_FOUND"`

### 决策矩阵

| 插件 | 二进制文件 | 操作 |
|---|---|---|
| 缺失 | 缺失 | 安装两者（最常见） |
| 缺失 | 存在 | 仅安装插件 |
| 存在 | 缺失 | 仅安装二进制文件 |
| 存在 | 存在 | 可能需要重启 |

### 用户交互

当 LSP 预热失败时，向用户展示诊断结果和安装引导：

**输出格式**：

```
检测到项目语言为 {language}，但对应的 LSP 插件未就绪。

诊断结果：
  - 插件 {lspPluginName}：{已安装 | 未安装}
  - 二进制 {lspBinary}：{已安装 | 未安装}

LSP 提供精确的语义分析能力（调用链追踪、符号定位、类型推断），
启用 LSP 可显著提升漏洞检测的准确率和深度。

请选择：
1️⃣ 自动安装（推荐）—— 执行以下命令安装所需组件：
   {installCommand}
2️⃣ 跳过 —— 以降级模式继续（仅使用 Grep + Read，精度降低）
```

**安装流程**：

1. 用户选择"自动安装"后，执行对应的安装命令（参见上方 LSP 插件映射表）
2. 安装完成后重试 `LSP documentSymbol`
3. 如果仍然失败，提供进一步引导：

```
LSP 安装完成但预热仍失败。可能原因：
  - 语言服务器需要重新加载窗口才能生效
  - 项目缺少必要的构建配置（如 Java 项目需要 pom.xml / build.gradle）

请选择：
1重新加载窗口后重试
2跳过 LSP，以降级模式继续
```

> 这是阶段 1 初始化中**唯一**的用户交互点。LSP 可用 = 无需交互。

### 后续检查

- 将 `lspStatus` 写入所有 agent 提示词
- 记录到 `summary.json` > `executionMetrics.lspStatus`

## LSP 降级规则

当 `lspStatus: "unavailable"` 时：
- 所有 agent 回退到 `Grep + Read` 手动追踪
- 所有发现必须设置 `traceMethod: "Grep+Read"`
- 未验证比例增加，整体置信度降低
- Agent 提示词包含：`"LSP 不可用。使用 Grep + Read 进行追踪。相应设置 traceMethod。"`
