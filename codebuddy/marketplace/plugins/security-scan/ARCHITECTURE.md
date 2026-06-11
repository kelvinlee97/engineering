# Security-Scan 插件架构文档

## 插件结构

```
security-scan/
├── .codebuddy-plugin/
│   └── plugin.json                    # 插件配置（名称、版本、功能声明、入口）
├── agents/                            # 5+1 个 agent 定义文件
│   ├── reconnaissance.md              # 侦察兵：项目结构探索、入口点枚举、攻击面映射、依赖解析
│   ├── quick-scan.md                  # 快速扫描：Grep 模式匹配、CVE 检测、配置基线扫描
│   ├── deep-scan.md                   # 深度扫描：LSP 语义数据流追踪、授权覆盖、业务逻辑缺陷
│   ├── verification.md                # 验证师：反幻觉 + 路径验证 + 红队挑战 + 置信度评分
│   ├── remediation.md                 # 修复师：修复代码生成 + HTML 报告
│   └── batch-worker.md                # 批次执行器：大项目分批并行调度
├── commands/                          # 命令定义
│   ├── project.md                     # /security-scan:project — 全项目安全审计
│   └── diff.md                        # /security-scan:diff — Git 变更文件审计
├── resource/                          # 安全规则与配置
│   ├── default-rules.yaml             # 核心审计逻辑索引 + 模式参考库
│   ├── risk-type-taxonomy.yaml        # 标准风险类型分类表（slug + 中文名称映射）
│   ├── rule-details/                  # 参考数据文件
│   │   ├── ssrf.yaml                  # SSRF 绕过技术参考数据
│   │   └── auth-basic.yaml            # 鉴权/越权基础检测模式
│   ├── anti-hallucination-rules.yaml  # 反幻觉规则与 Agent 合约条款
│   ├── logic-audit-rules/             # 业务逻辑缺陷审计规则
│   │   └── authentication-bypass.yaml # 鉴权风险置信度评估与模式引用
│   ├── custom/                        # 用户自定义规则
│   │   ├── ignore-patterns.yaml       # 忽略模式配置
│   │   ├── sanitizers.yaml            # 净化函数配置
│   │   ├── sinks.yaml                 # 自定义 Sink 配置
│   │   └── sources.yaml               # 自定义 Source 配置
│   └── README-CONFIG-GUIDE.md         # 规则配置指南
├── scripts/                           # Python 脚本
│   ├── generate_report.py             # HTML 报告生成
│   ├── get_git_diff_files.py          # Git 变更文件获取
│   ├── merge_findings.py              # Findings 合并去重
│   ├── checkpoint_verify.py           # 检查点验证
│   ├── batch_files.py                 # 文件批处理
│   ├── context_budget.py              # 上下文预算追踪（估算剩余 token 容量）
│   └── extract_context.py             # 批量代码上下文提取（减少 Read 调用）
├── references/                        # 参考文档
│   ├── agent-prompt-template.md       # Agent Prompt 模板
│   ├── anti-hallucination-contract.md # 反幻觉合约
│   ├── context-budget-contract.md     # 资源预算合约（上下文预算 + Turn 预算 + 收尾协议）
│   ├── incremental-write-contract.md  # 增量写入合约（所有 Agent 强制遵守）
│   ├── lsp-setup.md                   # LSP 配置指南
│   ├── orchestrator-rules.md          # 编排器规则（含检查点逻辑、覆盖率评估、框架知识加载）
│   ├── output-schemas.md              # 输出合约（JSON 格式、Agent 输出字段、输出目录结构）
│   └── post-audit-workflow.md         # 审计后工作流（摘要、用户交互、修复、报告）
├── ARCHITECTURE.md                    # 本文件
├── CONTRIBUTING.md                    # 贡献指南
└── README.md                          # 插件说明
```

---

## 流水线概览

插件采用 4 阶段流水线架构，由 `project` 和 `diff` 命令共享核心扫描逻辑：

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
                  ├ LSP Source→Sink 追踪
                  ├ 鉴权覆盖度审计
                  ├ IDOR/越权检测
                  ├ 业务逻辑缺陷检测
                  └ 漏洞链推理
             ──→                        ──→                  ──→
```

**关键设计**：
- 阶段 1 完成后，quick-scan 和 deep-scan 在阶段 2 **并行启动**，互不阻塞
- 审计核心是完整的语义分析（LSP 跨文件数据流追踪、多态穿透、业务逻辑理解），而非简单模式匹配
- 阶段 2→3 过渡时，若存在跨仓库依赖断点，引导用户可选关联外部源码分析
- 阶段 3 的 verification 综合验证（反幻觉校验 + 路径验证 + 红队挑战 + 置信度评估）消除误报
- 每个阶段和子任务完成后输出中文进度提示和精简摘要

---

## Agent 目录

| # | Agent | 角色 | 阶段 | 关键能力 |
|---|-------|------|:----:|---------|
| 1 | reconnaissance | 侦察兵 — 项目结构探索、入口点枚举、端点-权限矩阵、攻击面映射 | 1 | LSP documentSymbol/workspaceSymbol + 依赖文件解析 |
| 2 | quick-scan | 快速扫描 — Grep 模式匹配、CVE 检测、配置基线 | 2 | Grep 正则 + 版本号比对（无 LSP 依赖） |
| 3 | deep-scan | 深度扫描 — LSP 语义数据流追踪、授权覆盖、业务逻辑缺陷 | 2 | LSP 全套操作 |
| 4 | verification | 验证师 — 五阶段流水线验证 + 置信度评分 | 3 | Glob/Read 事实校验 + LSP 路径验证 |
| 5 | remediation | 修复师 — 修复代码生成 + HTML 报告 | 4 | Edit + generate_report.py |
| +1 | batch-worker | 批次执行器 — 大项目分批并行调度 | 2-3 | 独立上下文窗口 |

---

## 数据流

```
阶段 1                         阶段 2                         阶段 3                    阶段 4
──────                         ──────                         ──────                    ──────
reconnaissance.json ──→ stage1-context.json ──→ quick-scan.json ──┐
                                              deep-scan.json ─────┤
                                                                  ├→ [merge] merged-scan.json
                              pattern-scan-results.json ──────────┤      │
                              (sinkLocations, defenseIndicators)  │      ↓
                                                                  └→ verification.json
                                                                        │
                                                                        ↓
                                                              [merge] finding-*.json
                                                                    summary.json
                                                                        │
                                                                        ↓
                                                                  remediation.json
```

**核心中间文件**：
- `stage1-context.json` — 阶段 1 上下文汇总（文件列表、项目结构、入口点矩阵、依赖、规则）
- `pattern-scan-results.json` — 模式扫描结果（sinkLocations、defenseIndicators、cveFindings）
- `merged-scan.json` — 阶段 2 合并去重后的发现
- `agents/{agent-name}.json` — 各 agent 详细输出
- `finding-{risk-type-slug}.json` — 最终审计结果（按风险类型命名）
- `summary.json` — 审计摘要（含执行指标、质量评分）

---

## 置信度评分体系

置信度（0-100）由三个独立维度累加计算：

| 维度 | 满分 | 评估内容 |
|------|:----:|---------|
| 攻击链可达性 | 40 | Source→Sink 完整性、LSP 追踪确认、入口可达性 |
| 防御措施 | 30 | 防御有效性（无防御=高分，有效防御=低分） |
| 数据源可控性 | 30 | 攻击者对输入数据的控制程度 |

**高置信度门控（≥90）**需同时满足 7 项条件（验证通过、链路完整、防御搜索记录等），任一未通过则上限 89。

| 等级 | 范围 | 操作 |
|------|------|------|
| 高 | >= 90 | 可自动修复 |
| 中 | 60-89 | 需人工审核 |
| 低 | < 60 | 仅供参考 |

详细评分逻辑参见 `agents/verification.md > Phase E`。

---

## 文件交叉引用

| 定义层 | 文件 | 作用 |
|--------|------|------|
| Agent 定义 | `agents/{name}.md` | agent 的角色、工具、具体任务指令 |
| 输出合约 | `references/output-schemas.md` | JSON 输出格式、Agent 输出字段、输出目录结构 |
| 审计后工作流 | `references/post-audit-workflow.md` | 摘要模板、用户交互、修复/报告流程 |
| 编排流程 | `references/orchestrator-rules.md` | agent 间调度规则、进度输出 |
| 命令配置 | `commands/project.md` 或 `commands/diff.md` | 各阶段的命令特定逻辑 |
| 风险类型分类 | `resource/risk-type-taxonomy.yaml` | 标准风险类型 slug 与中文名称映射 |
| 安全规则 | `resource/rule-details/*.yaml` | 参考数据文件（绕过技术、检测模式） |
| 反幻觉合约 | `resource/anti-hallucination-rules.yaml` | agent 必须遵守的反幻觉条款 |
| 上下文预算 | `references/context-budget-contract.md` | Read 规范、工具调用计数器、预算检查 |

---

## 上下文控制机制

为防止上下文膨胀、数据丢失和不可预见的上下文耗尽，插件实施三层防御：

### 第一层：Read 约束（减少上下文输入）

- **禁止全文件 Read**：所有 agent 的 Read 调用必须使用 `offset` + `limit` 参数，按需读取
- **同文件去重**：同一文件在单次任务中最多 Read 3 次
- **大文件警戒**：超过 500 行的文件必须先用 LSP documentSymbol 定位后精确读取
- **批量上下文提取**：`scripts/extract_context.py` 支持一次性从 findings 中提取所有代码上下文，替代逐个 Read
- **LSP 结果复用**：同一方法的 LSP 调用结果在本次审计中有效，不重复调用

### 第二层：增量写入（防止数据丢失）

- **统一合约**：`references/incremental-write-contract.md` 定义所有 agent 必须遵守的增量写入规则
- **写入触发条件**：完成一个 finding、完成一个 Phase、累积超过 2000 tokens 未写入、连续 10 次工具调用未写入
- **恢复协议**：每个 agent 启动时检查已有输出文件，支持从 `lastCheckpoint` 断点恢复
- **紧急写入**：当上下文即将耗尽时，立即写入所有数据并设置 `status: "partial"`

### 第三层：预算感知（预测上下文容量）

- **预算追踪器**：`scripts/context_budget.py` 基于文件读取量、工具调用次数和 findings 进度估算已消耗 tokens
- **自动建议**：根据使用百分比返回 `continue`、`flush_and_continue`、`flush_and_stop`、`emergency_flush` 四级建议
- **工具调用计数器**：每个 agent 维护内部计数器，在 30/50/70/90/100 次工具调用时触发对应行动
- **定期检查**：每完成 3 个 findings 或每 20 次工具调用后调用一次预算评估

---

## 关键设计决策

### 为什么用 Markdown 定义合约

agent 定义和 skill 均使用 Markdown 格式。LLM 可直接读取并理解 Markdown 内容，无需额外的解析层。这使得合约对人类开发者和 LLM 都是可读的，降低了维护成本。

### 为什么用文件做 Agent 间通信

agent 间通过 JSON 文件（如 `stage1-context.json`、`pattern-scan-results.json`）传递数据，而非直接在 prompt 中嵌入全量数据。这样做的好处：
- **节省 token**：各 agent 按需 Read 所需字段，避免上下文膨胀
- **可追溯**：中间产物持久化到磁盘，便于调试和审计回溯
- **解耦**：agent 间通过 `findingId` 引用而非嵌套完整数据，降低耦合度

### 为什么阶段 2 并行执行 quick-scan 和 deep-scan

- quick-scan（Grep 模式匹配）和 deep-scan（LSP 语义分析）是独立的扫描方式，互不依赖
- 并行执行缩短了总扫描时间
- deep-scan 可可选使用 quick-scan 的 `sinkLocations` 作为增强输入，但不阻塞等待
- 两者的结果在合并阶段统一去重

### 为什么用 LSP 进行审计

LSP（Language Server Protocol）提供精确的代码语义能力（调用链追踪、符号定位、类型推断），是纯 Grep 模式匹配无法替代的。具体优势：
- `incomingCalls`/`outgoingCalls`：精确追踪攻击链的 Source→Sink 路径
- `goToDefinition`/`goToImplementation`：穿透接口和多态，验证防护措施有效性
- `findReferences`：确认防护函数在所有路径上都被调用

当 LSP 不可用时，所有 agent 自动降级为 Grep + Read 模式，审计仍然有效但精度降低。
