---
description: 通过 agent 团队执行 Git diff 增量安全审计
argument-hint: [--commit <hash>] [--mode staged|unstaged|all]
allowed-tools: Bash, Read, Glob, Write, Grep, Task, Edit, LSP
---

# Git Diff 增量安全审计

> **[语言要求]** 所有面向用户的输出（进度提示、摘要、说明、错误信息）必须使用**简体中文**。Agent 提示词中的结构化标签保持中文。JSON 字段名和技术标识符（agent 名称、文件路径等）保持英文不变。

通过 agent 团队审计 git 变更。阶段 1-3 自动执行；用户交互仅在阶段 4 进行。

## 阶段 1：侦察

> 进度输出参见 `references/orchestrator-rules.md > 进度输出`

### 1.1 创建审计批次 + 定位插件根目录

```bash
audit_batch_id="diff-audit-$(date +%Y%m%d%H%M%S)"
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

### 1.2 获取 git diff 文件 + 分类

```bash
git diff <hash>^ <hash> --name-only --diff-filter=ACMR  # specific commit
git diff HEAD --name-only --diff-filter=ACMR              # --mode all (default)
git diff --cached --name-only --diff-filter=ACMR           # --mode staged
git diff --name-only --diff-filter=ACMR                    # --mode unstaged
git diff HEAD^ HEAD --name-only --diff-filter=ACMR         # fallback: clean tree
```

对变更文件进行分类：
- **依赖文件**（供应链审计）：`pom.xml`、`package.json`、`go.mod`、`requirements.txt` 等
- **配置文件**（配置基线）：`application.yml`、`.env`、`settings.py`、`config.json` 等
- **代码文件**（漏洞审计）：`.java`、`.kt`、`.py`、`.go`、`.js`、`.ts`、`.tsx`、`.php`、`.rb`、`.cs`、`.cpp`、`.c`、`.rs`、`.swift`、`.vue`
- **运维文件**（凭据扫描）：`Dockerfile`、`docker-compose.yml`、`.env`（非示例文件）

### 1.3 记录规则路径 + 提取契约（与 1.2 并行）

记录路径用于按需读取：
1. `$plugin_root/resource/default-rules.yaml` -- agent 按需 Read 相关章节
2. `$plugin_root/resource/anti-hallucination-rules.yaml` -- 反幻觉规则 + 契约

将路径写入 `stage1-context.json`。提取契约核心（4 句话）用于 agent 提示词注入。

### 1.4 条件规则加载（在 1.3 之后）

内联加载条件规则（`logic-audit-rules/authentication-bypass.yaml`、`custom/*.yaml`）。输出到 `agents/knowledge-retrieval.json` 以保持兼容性。

### 1.4.5 按技术栈加载框架安全知识（在 1.8 reconnaissance 完成后执行）

> Ref: `references/orchestrator-rules.md > 按技术栈加载框架安全知识`

### 1.5 语言检测 + LSP 探活（与 1.2、1.3 并行）

> Ref: `references/lsp-setup.md`

### 1.6 LSP 可用性（Ref: `references/lsp-setup.md`）

阶段 1 中唯一的用户交互步骤（自动安装提示）。

### 1.7 启动 agent（按条件）

通过 Task 后台模式启动：
- **reconnaissance** -- 仅在 `hasCodeChanges = true` 时启动

### 1.8 等待 reconnaissance 后台任务完成，从 `agents/reconnaissance.json` 提取摘要数据。

### 1.9 写入 stage1-context.json + 探索检查点（Ref: `references/orchestrator-rules.md > 检查点逻辑`）

### 并行时间线

```
1.1 -> 1.2
    -> 1.3 -> 1.4
    -> 1.5 -> 1.6
-> 1.7 -> 1.8 -> 1.9
```

## 阶段 2：扫描

> 进度输出参见 `references/orchestrator-rules.md > 进度输出`

### 2.1 并行启动 quick-scan 和 deep-scan

通过 Task 后台模式**同时并行**启动：
- **quick-scan** -- Grep 广域模式扫描
- **deep-scan** -- 仅在 `hasCodeChanges = true` 时启动

> 重要：quick-scan 和 deep-scan 必须并行执行，互不阻塞。

### 2.2 等待全部完成

等待 quick-scan 和 deep-scan 后台任务全部完成。从各自的 JSON 输出文件中提取关键指标，按 `references/orchestrator-rules.md > 子任务完成摘要` 格式打印摘要。

### 2.3 合并扫描结果（Ref: `references/orchestrator-rules.md > 检查点逻辑`）

```bash
python3 $plugin_root/scripts/merge_findings.py merge-scan \
  --batch-dir security-scan-output/{batch}
```

仅解析标准输出 JSON（`totalFindings`、`bySeverity`、`deduplicatedCount`、`discardedCount`）。不要将 `merged-scan.json` Read 到上下文中。

### 2.4 扫描检查点（Ref: `references/orchestrator-rules.md > 检查点逻辑`）

```bash
python3 $plugin_root/scripts/checkpoint_verify.py verify-scan \
  --batch-dir security-scan-output/{batch}
```

### 2.5 跨仓库检查（Ref: `references/orchestrator-rules.md > 检查点逻辑`）

检查 `crossRepoDependencies` 是否需要用户交互。

## 阶段 3：验证

> `{n}` 来自 merge-scan 标准输出的 `totalFindings`。

### 3.1 启动 verification

通过 Task 后台模式启动 **verification**。整合：反幻觉检查、攻击路径验证、置信度评分。

### 3.2 等待验证完成，然后合并验证结果

```bash
python3 $plugin_root/scripts/merge_findings.py merge-verify \
  --batch-dir security-scan-output/{batch}
```

仅解析标准输出 JSON（`finalFindings`、`bySeverity`、`removedByAntiHallucination`、`findingFiles`）。不要将 `finding-*.json` Read 到上下文中。

## 阶段 4：修复

> 进度输出参见 `references/orchestrator-rules.md > 进度输出`

### 4.1 生成修复方案

通过 Task 后台模式启动 **remediation**。等待完成。

### 4.2 输出报告

从 `agents/remediation.json` 读取审计质量结论和评分。
> Ref: `references/post-audit-workflow.md` > Audit Summary Template
> Ref: `references/output-schemas.md` > JSON output format

Diff 特有内容：
- 范围：`Changed files: {n}`
- 无安全评分
- 批次前缀：`diff-audit-`

### 4.3 执行用户选择
> Ref: `references/post-audit-workflow.md` > User Interaction

## Agent 团队概览

```
diff command (up to 5 agents)
  阶段 1: 初始化 + reconnaissance（按条件）
  阶段 2: quick-scan + deep-scan 并行（按条件）
  阶段 3: verification
  阶段 4: remediation + 报告 + 用户交互
```

## 调度器上下文控制

> Ref: `references/orchestrator-rules.md`

## 注意事项

- 必须在 git 仓库中运行
- 依赖文件变更会触发 quick-scan CVE 检测（D2）
- 配置基线仅在配置文件变更时触发
- 所有 agent 使用 Task 后台模式
- 模式扫描与语义分析并发执行
- 规则按需 Read，不批量注入到提示词中
