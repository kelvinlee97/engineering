---
description: 通过 agent 团队执行全项目代码安全审计
argument-hint: "[file_path...] [--include *.py,*.js] [--exclude node_modules,dist]"
allowed-tools: Bash, Read, Glob, Write, Grep, Task, Edit, LSP
---

# 全项目安全审计

> **[语言要求]** 所有面向用户的输出（进度提示、摘要、说明、错误信息）必须使用**简体中文**。Agent 提示词中的结构化标签保持中文。JSON 字段名和技术标识符（agent 名称、文件路径等）保持英文不变。

使用 5 个 agent 分 4 个阶段执行全项目安全审计：reconnaissance、quick-scan、deep-scan、verification、remediation。阶段 1-3 自动执行，无需用户交互；用户交互仅在阶段 4 进行。

---

## 阶段 1：侦察

> 进度输出参见 `references/orchestrator-rules.md > 进度输出`

### 1.1 创建审计批次 + 定位插件根目录

```bash
audit_batch_id="project-audit-$(date +%Y%m%d%H%M%S)"
mkdir -p security-scan-output/$audit_batch_id

# 确定性定位插件根目录（通过 plugin.json 锚定）
plugin_root=$(find ~/.codebuddy/plugins/marketplaces -maxdepth 6 -name "plugin.json" \
  -path "*/security-scan/*" 2>/dev/null \
  | xargs grep -l '"name"' 2>/dev/null | head -1 \
  | sed 's|/.codebuddy-plugin/plugin.json$||')
echo "plugin_root=$plugin_root"

# 验证
[ -d "$plugin_root/resource" ] && [ -d "$plugin_root/scripts" ] && echo "OK" || echo "FAIL"
```

> 如果验证 FAIL，回退：`Glob("~/.codebuddy/**/security-scan/resource/default-rules.yaml")` 并推导路径。
> **禁止**全盘 `find $HOME` 搜索或启动 Explore agent 定位插件。

### 1.2 记录规则路径 + 提取契约摘要

将 `$plugin_root/resource/default-rules.yaml` 和 `$plugin_root/resource/anti-hallucination-rules.yaml` 的路径记录到 `stage1-context.json` 的 `defaultRulesPath` 和 `antiHallucinationRulesPath` 字段中。**Agent 按需 Read 相关章节——绝不注入完整内容**。

从 anti-hallucination-rules.yaml 中提取 4 行契约核心，用于 agent 提示词注入。

> Ref: references/anti-hallucination-contract.md

### 1.3 语言检测 + LSP 探活

> Ref: references/lsp-setup.md（与 1.2 并行）

### 1.4 条件规则加载

在 1.2 完成后执行（需要规则路径）。不等待 1.3。

- 检查认证风险信号（Controller/Handler/路由定义、权限检查）
- 如果触发：Read `$plugin_root/resource/logic-audit-rules/authentication-bypass.yaml`
- 检查自定义规则：`$plugin_root/resource/custom/*.yaml`
- 将已加载的规则写入 `stage1-context.json` 的 `auditRules` 字段

> 仅内联执行（Read + Glob）。无需启动 agent。

### 1.4.5 按技术栈加载框架安全知识（在 1.7 reconnaissance 完成后执行）

> Ref: `references/orchestrator-rules.md > 按技术栈加载框架安全知识`

### 1.5 LSP 可用性 + 自动安装

> Ref: references/lsp-setup.md（在 1.3 之后）

### 并行时间线

```
1.1 -> 1.2 -> 1.4
    -> 1.3 -> 1.5
```

### 1.6 启动 reconnaissance agent

初始化完成后，通过 Task 工具后台模式启动：

- **reconnaissance** -- 扫描范围、项目结构、入口点、依赖项

### 1.7 等待 + 收集摘要

等待 reconnaissance 后台任务完成。从 `agents/reconnaissance.json` 中读取关键指标，按 `references/orchestrator-rules.md > 子任务完成摘要` 格式打印摘要。

### 1.8 写入 stage1-context.json

追加探索输出：`fileList`、`projectStructure`、`endpointPermissionMatrix`、`dependencies`。

### 1.9 探索检查点

> Ref: `references/orchestrator-rules.md > 检查点逻辑 > 探索检查点`

---

## 阶段 2：扫描（并行）

### 2.1 并行启动扫描 agent

侦察完成后，通过 Task 工具后台模式**同时并行**启动：

- **quick-scan** -- Grep 广域模式扫描（若未在 1.6 启动）
- **deep-scan** -- LSP 语义数据流追踪

> 重要：quick-scan 和 deep-scan 必须并行执行，互不阻塞。两者独立完成各自的扫描任务。

### 2.2 等待所有阶段 2 的 agent

等待 quick-scan 和 deep-scan 后台任务全部完成。从各自的 JSON 输出文件中提取关键指标，按 `references/orchestrator-rules.md > 子任务完成摘要` 格式打印摘要。

### 2.3 合并扫描结果

> Ref: `references/orchestrator-rules.md > 检查点逻辑 > 扫描合并`
>
> `merge_findings.py merge-scan` 会自动按以下顺序加载 agent 输出：
> - `quick-scan.json`（如果 `pattern-scan-results.json` 不存在则回退加载）
> - `deep-scan.json`（语义分析结果，自动加载）
> - `vulnerability-audit.json`、`logic-defect-audit.json`、`dependency-audit.json`（如存在）
>
> 输出文件名为 `merged-scan.json`（checkpoint 和阶段 3 均支持此名称回退）。

### 2.4 漏洞链检测

合并后，分析 `merged-scan.json` 中的跨文件漏洞链：

- 识别多文件攻击路径（例如：用户输入 -> 未过滤传递 -> SQL 拼接 -> 数据库执行）
- 将同一路径的发现关联为 `vulnerabilityChain` 条目
- 提升严重级别：链中任何节点继承该链的最高严重级别
- 将链数据写入 `merged-scan.json` 的 `chains` 字段，供阶段 3 使用

### 2.4.5 覆盖率评估 + 补漏调度（可选）

> Ref: `references/orchestrator-rules.md > 覆盖率评估与补漏调度`

### 2.5 扫描检查点

> Ref: `references/orchestrator-rules.md > 检查点逻辑 > 扫描检查点`

### 2.6 跨仓库来源关联

> Ref: `references/orchestrator-rules.md > 检查点逻辑 > 跨仓库源关联`

---

## 阶段 3：验证

> `{n}` 来自 merge-scan 标准输出的 `totalFindings`。

内联启发式：如果 `totalFindings <= 20`，则内联执行验证（跳过 agent 启动）。

### 3.1 启动 verification agent

通过 Task 工具后台模式启动。

> verification agent 的输出文件名为 `verification.json`。`merge_findings.py merge-verify` 会优先查找 `finding-validator.json`，若不存在则自动回退加载 `verification.json`。

### 3.2 等待验证完成

### 3.3 合并验证结果

> Ref: `references/orchestrator-rules.md > 检查点逻辑 > 验证合并`

---

## 阶段 4：修复

### 4.1 启动 remediation agent

通过 Task 工具后台模式启动。

### 4.2 等待 + 收集结论

从 `agents/remediation.json` 中读取 `overallVerdict` 和 `qualityScore`（仅读取这两个字段，而非完整文件）。

### 4.3 输出与报告

> Ref: `references/post-audit-workflow.md` for summary template, user interaction
> Ref: `references/output-schemas.md` for JSON output format

项目特有的附加内容：

```
扫描范围：{total_files} 个文件
安全评分：{score}/100
```

### 4.4 执行用户选择

> Ref: `references/post-audit-workflow.md` > User Interaction

---

## Agent 团队概览

```
project command (5 agents + N batch-workers)
  阶段 1 [1/4]: 初始化 + reconnaissance（并行初始化与侦察）
  阶段 2 [2/4]: quick-scan + deep-scan 并行（files<=50: 直接 | >50: batch-workers 并行）
  阶段 3 [3/4]: verification（五阶段验证流水线）
  阶段 4 [4/4]: remediation + 报告 + 用户交互
```

---

## 调度器上下文控制

> Ref: references/orchestrator-rules.md

---

## 大型项目批量策略

### 文件规模阈值

| 规模 | 源文件数 | 策略 |
|-------|-------------|----------|
| 小型 | <= 50 | 不分批，所有 agent 处理完整文件集 |
| 中型 | 51-200 | 按模块/目录分批，每批 <= 50 个文件 |
| 大型 | 201-500 | 按模块分批 + 优先级排序，高风险模块优先 |
| 超大型 | > 500 | 分批 + 优先级 + 增量审计模式 |

### 优先级分类

- **P0（第一批）**：Controllers/Handlers、DAO/Repository、安全配置
- **P1（第二批）**：Service 层、工具类（加密/序列化/网络）
- **P2（第三批）**：Model/DTO、其他辅助代码

### 批量机制

使用 `scripts/batch_files.py` 按行数进行智能分组（大文件 >500 行独立成批，小文件合并，默认 `--max-lines 2000`，`--min-files-per-batch 10` 避免碎片批次）。

并行 batch-worker 拥有独立的上下文窗口：

```
reconnaissance outputs file list
  |
  files > 50? -- no --> normal flow (no batching)
  | yes
  batch_files.py splits by module/priority --> batch-plan.json
  |
  parallel batch-workers (independent context)
    batch-worker-1 --> batch-1-result.json
    batch-worker-2 --> batch-2-result.json
    batch-worker-N --> batch-N-result.json
  |
  merge-batches global dedup --> all-batches-merged.json
  |
  Stage 3-4 (orchestrator)
```

### 批量执行规则

- **阶段 2 分批执行**：每个 batch-worker 在独立的上下文窗口中独立运行扫描
- **阶段 3-4 全局执行**：所有批次在验证、修复和报告之前合并
- **跨批次数据流**：LSP 不受批次边界限制；agent 可跨批次追踪
- **进度**：编排器读取 `batch-{N}-result.json` 输出进度，例如 `[2/4] Deep scan (batch 1/3: Controller layer)...`
- **错误隔离**：单个批次失败不会中止审计；调度器跳过失败的批次

### 增量审计（超大型项目）

当文件数 > 500 时，额外启用增量模式：

- 检查 `security-scan-output/` 中是否有以往的审计记录
- 如果 7 天内存在先前审计，则仅审计变更文件（`git diff`）
- 在 `summary.json` 中标记 `auditMode: "incremental"` 和 `baseAuditBatchId`
- 用户可通过 `--full` 强制执行完整审计
