# Security-Scan 代码安全审计插件

基于 Agent Teams 架构的代码安全审计插件，通过 5 个专业 agent 协同执行深度安全分析。核心采用**完整语义分析**（非简单模式匹配），支持 LSP 跨文件数据流追踪、多态穿透、业务逻辑缺陷检测、跨仓库源码关联分析，以及自动修复和 HTML 报告导出。

---

## 价值与优势

| 维度 | 说明 |
|------|------|
| **完整语义分析** | 基于 LLM + LSP 追踪跨文件数据流、穿透多态和接口，识别传统 SAST 难以发现的复杂漏洞模式 |
| **多 Agent 协同** | 5 个专业 agent 分 4 阶段流水线执行，兼顾广度（模式扫描）和深度（语义分析） |
| **阶段 2 并行扫描** | quick-scan 和 deep-scan 在阶段 2 并行执行，互不阻塞，缩短扫描时间 |
| **五阶段交叉验证** | 反幻觉校验 + 攻击路径验证 + 红队挑战 + 可验证性论证 + 置信度评估，消除误报 |
| **跨仓库源码关联** | 追踪到第三方无源码模块时引导用户可选关联外部源码，避免因依赖边界导致漏报 |
| **编码阶段发现** | 在 IDE 中实时审计，比上线后修复成本低 10-100 倍 |
| **大项目适配** | 自动按模块分批、优先级排序、增量审计，适应不同规模项目（batch-worker 并行调度） |
| **置信度量化** | 0-100 分三维度评分：攻击链可达性（40分）+ 防御措施（30分）+ 数据源可控性（30分） |
| **一键修复** | 高置信度漏洞自动生成修复代码，经用户确认后应用 |
| **中文友好** | 全中文进度提示，每阶段完成后输出精简摘要 |
| **可扩展** | 支持自定义 Source/Sink/Sanitizer 规则，可新增 agent 扩展检测能力 |

---

## 架构概览

### 4 阶段流水线

```
阶段 1              阶段 2（并行）                     阶段 3                  阶段 4
探索              威胁发现（扫描）                  验证                   修复与报告
───────────  ──────────────────────────────  ────────────────────  ────────────────────
reconnaissance   quick-scan ─┐ 并行          verification          remediation
├ 项目结构探索     ├ Grep 密钥/凭证检测  │       ├ 反幻觉校验             ├ 修复代码生成
├ 入口点枚举       ├ CVE/高危组件初筛    │       ├ 攻击路径验证           ├ HTML 报告生成
├ 端点-权限矩阵    ├ 配置基线扫描        │       ├ 红队挑战               └ 用户交互选择
├ 攻击面映射       ├ 危险 Sink 定位      │       ├ 可验证性论证
└ 依赖解析         └ 防护指标收集        │       └ 置信度评分
                  deep-scan ──────────┘
                  ├ LSP Source→Sink 数据流追踪
                  ├ 鉴权覆盖度审计
                  ├ IDOR/越权检测
                  ├ 业务逻辑缺陷检测
                  └ 漏洞链推理
             ──→                        ──→                  ──→
```

### 5+1 个 Agent

| # | Agent | 角色 | 阶段 | 关键能力 |
|---|-------|------|:----:|---------|
| 1 | reconnaissance | 侦察兵 — 项目结构探索、入口点枚举、端点-权限矩阵构建、攻击面映射、依赖解析 | 1 | LSP documentSymbol/workspaceSymbol + 依赖文件解析 |
| 2 | quick-scan | 快速扫描 — 基于 Grep 的模式匹配、已知 CVE 检测、配置基线扫描 | 2 | Grep 正则 + 版本号比对（无 LSP 依赖） |
| 3 | deep-scan | 深度扫描 — 基于 LSP 的语义数据流追踪、授权覆盖审计、业务逻辑缺陷检测 | 2 | LSP incomingCalls/outgoingCalls/goToDefinition/goToImplementation/findReferences |
| 4 | verification | 验证师 — 反幻觉验证 + 攻击路径验证 + 红队挑战 + 可验证性论证 + 置信度评分 | 3 | Glob/Read 事实校验 + LSP 路径验证 |
| 5 | remediation | 修复师 — 修复代码生成 + HTML 审计报告输出 | 4 | 修复代码生成 + generate_report.py |
| +1 | batch-worker | 批次执行器 — 大型项目分批并行执行阶段 2 扫描和阶段 3 验证 | 2-3 | 由编排器并行调度，独立上下文窗口 |

---

## 操作指引

### 命令一览

| 命令 | 说明 | 适用场景 |
|------|------|---------|
| `/security-scan:project` | 全项目安全审计 | 新项目接入、定期安全审查、安全评估 |
| `/security-scan:diff` | Git 变更文件审计 | MR 审查、提交前检查、增量审计 |

### 使用示例

```bash
# 全项目审计
/security-scan:project

# 指定文件范围审计
/security-scan:project src/main/java --include *.java,*.kt --exclude *Test.java

# 审计工作区全部变更
/security-scan:diff

# 审计指定 commit
/security-scan:diff --commit abc123

# 仅审计已暂存变更
/security-scan:diff --mode staged

# 超大型项目强制全量审计
/security-scan:project --full
```

### 输出产物

审计完成后，结果保存在 `security-scan-output/{batch-id}/` 目录：

```
security-scan-output/{batch-id}/
├── agents/                          # 各 agent 详细输出
│   ├── reconnaissance.json
│   ├── quick-scan.json
│   ├── deep-scan.json
│   ├── verification.json
│   └── remediation.json
├── stage1-context.json              # 项目结构与依赖上下文
├── pattern-scan-results.json        # 模式扫描结果
├── finding-{risk-type-slug}.json    # 最终审计结果（按风险类型命名）
├── summary.json                     # 审计摘要（含执行指标、安全评分、跨仓库依赖提示）
└── security-scan-report.html        # HTML 交互式报告
```

### 自定义规则

在 `resource/custom/` 目录下配置业务自定义规则：

```
resource/custom/
├── sources.yaml            # 业务数据源（如自定义参数获取方法）
├── sinks.yaml              # 业务危险函数（如自定义 SQL 执行方法）
├── sanitizers.yaml         # 业务安全函数（如自定义编码/过滤方法）
└── ignore-patterns.yaml    # 忽略规则（如测试代码路径）
```

详细配置说明见 `resource/README-CONFIG-GUIDE.md`。

---

## 检测能力

### 置信度评分体系

置信度（0-100）衡量漏洞判定的可信程度，基于三个独立维度累加计算：

| 维度 | 满分 | 评估内容 |
|------|:----:|---------|
| 攻击链可达性 | 40 | Source 到 Sink 的完整性、LSP 追踪确认程度、入口可达性 |
| 防御措施 | 30 | 目标路径上安全防御的有效性（无防御得高分，有效防御得低分） |
| 数据源可控性 | 30 | 攻击者对输入数据的控制程度（直接用户输入得高分） |

**高置信度门控（≥90）**：需同时满足 7 项条件（验证通过、攻击链完整、防御搜索记录完备等），任一未通过上限 89。

| 等级 | 分值范围 | 操作 |
|------|---------|------|
| 高 | >= 90 | 可自动修复 |
| 中 | 60-89 | 需人工审核 |
| 低 | < 60 | 仅供参考 |

### 支持的风险类型

| 类型 | 示例 | 参考置信度 |
|-----|------|:------:|
| SQL 注入 | 字符串拼接、MyBatis ${}、动态表名列名 | 95 |
| 命令注入 | shell 拼接、shell=True、Runtime.exec | 95 |
| 路径遍历 | 文件路径未校验、../ 绕过 | 90 |
| 硬编码凭证 | 密码、API 密钥、私钥 | 90 |
| 反序列化 | ObjectInputStream、pickle、Fastjson | 90 |
| XXE | XML 外部实体注入、DocumentBuilder | 90 |
| XSS | innerHTML、v-html、未转义输出 | 85 |
| SSRF | 服务端请求伪造、云元数据访问 | 85 |
| 弱加密 | MD5/SHA1 密码哈希、不安全随机数 | 85 |
| 高危组件 | Log4j、Fastjson、Spring4Shell 等 CVE | 85 |
| CORS 配置 | Access-Control-Allow-Origin: * | 80 |
| 敏感信息泄露 | 日志打印密码、异常堆栈暴露 | 75 |
| 越权漏洞 | 缺失权限校验、资源归属未验证、鉴权机制缺陷 | 70 |
| 业务逻辑漏洞 | 支付金额篡改、并发竞争 | 40 |

> 参考置信度为通用场景下的基准值，实际分析时会基于代码上下文动态调整。

### 审计架构

| 审计类型 | Agent | 方法 | 核心能力 |
|---------|-------|------|---------|
| **模式匹配** | quick-scan | Grep 正则 + 配置文件解析 | 快速广度扫描：密钥、CVE、配置风险、Sink 定位、防护指标 |
| **语义数据流追踪** | deep-scan | LSP 数据流追踪 | 跨文件 Source→Sink 追踪、多态穿透、跨仓库源码关联 |
| **授权覆盖审计** | deep-scan | LSP 端点枚举 + 鉴权验证 | 逐端点验证鉴权覆盖度、IDOR 检测 |
| **业务逻辑缺陷检测** | deep-scan | 类人推理 + 状态机分析 | 竞态条件、支付逻辑、流程绕过、漏洞链推理 |
| **配置风险审计** | quick-scan | 依赖数据分析 + 基线对比 | 第三方依赖 CVE 深度分析、可利用性评估 |

quick-scan 和 deep-scan 在阶段 2 **并行执行**，各自独立产出 findings，在阶段 3 合并后由 verification agent 五阶段流水线交叉验证消除误报。

### 支持的代码语言

| 语言 | LSP Server | 自动检测标志 |
|------|-----------|-------------|
| Java / Kotlin | jdtls | pom.xml, build.gradle |
| JavaScript / TypeScript | typescript-language-server | package.json, tsconfig.json |
| Go | gopls | go.mod |
| Python | pylsp | requirements.txt, pyproject.toml |
| Rust | rust-analyzer | Cargo.toml |
| C# | omnisharp | *.sln, *.csproj |
| Swift | sourcekit-lsp | Package.swift |

> LSP 提供精确的语义分析能力（调用链追踪、符号定位、类型推断）。当 LSP 不可用时，所有 agent 自动降级为 Grep + Read 模式，审计仍然有效但精度降低。

---

## 插件结构

```
security-scan/
├── .codebuddy-plugin/plugin.json    # 插件配置（名称、版本、功能声明、入口）
├── agents/                          # 5+1 个 agent 定义
│   ├── reconnaissance.md            # 侦察兵：项目结构探索、入口点枚举、攻击面映射、依赖解析
│   ├── quick-scan.md                # 快速扫描：Grep 模式匹配、CVE 检测、配置基线扫描
│   ├── deep-scan.md                 # 深度扫描：LSP 语义数据流追踪、授权覆盖、业务逻辑缺陷
│   ├── verification.md              # 验证师：反幻觉 + 路径验证 + 红队挑战 + 置信度评分
│   ├── remediation.md               # 修复师：修复代码生成 + HTML 报告
│   └── batch-worker.md              # 批次执行器：大项目分批并行调度
├── commands/                        # 命令定义
│   ├── project.md                   # /security-scan:project — 全项目安全审计
│   └── diff.md                      # /security-scan:diff — Git 变更文件审计
├── resource/                        # 安全规则与配置
│   ├── default-rules.yaml           # 核心审计逻辑索引 + 模式参考库
│   ├── risk-type-taxonomy.yaml      # 标准风险类型分类表（slug + 中文名称映射）
│   ├── rule-details/                # 参考数据文件（2 个）
│   │   ├── ssrf.yaml                # SSRF 绕过技术参考数据
│   │   └── auth-basic.yaml          # 鉴权/越权基础检测模式
│   ├── anti-hallucination-rules.yaml # 反幻觉规则与 Agent 合约条款
│   ├── logic-audit-rules/           # 业务逻辑缺陷审计规则
│   │   └── authentication-bypass.yaml # 鉴权风险置信度评估与模式引用
│   └── custom/                      # 用户自定义规则
│       ├── sources.yaml
│       ├── sinks.yaml
│       ├── sanitizers.yaml
│       └── ignore-patterns.yaml
├── scripts/                         # Python 脚本
│   ├── generate_report.py           # HTML 报告生成
│   ├── batch_files.py               # 文件批处理
│   ├── merge_findings.py            # Findings 合并去重
│   └── checkpoint_verify.py         # 检查点验证
├── references/                      # 参考文档
│   ├── agent-prompt-template.md     # Agent Prompt 模板
│   ├── anti-hallucination-contract.md # 反幻觉合约
│   ├── context-budget-contract.md   # 资源预算合约（上下文 + Turn + 收尾）
│   ├── incremental-write-contract.md # 增量写入合约
│   ├── lsp-setup.md                 # LSP 配置指南
│   ├── orchestrator-rules.md        # 编排器规则（含检查点、覆盖率、框架知识）
│   ├── output-schemas.md            # 输出 Schema 定义
│   └── post-audit-workflow.md       # 审计后工作流（摘要、交互、修复、报告）
├── ARCHITECTURE.md                  # 架构文档
├── CONTRIBUTING.md                  # 贡献指南
└── README.md                        # 本文件
```

详细架构说明见 [ARCHITECTURE.md](./ARCHITECTURE.md)，贡献指南见 [CONTRIBUTING.md](./CONTRIBUTING.md)。
