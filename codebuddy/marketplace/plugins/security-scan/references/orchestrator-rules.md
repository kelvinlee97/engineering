# 编排器规则（共享片段）

> 引用方：commands/project.md、commands/diff.md

## 核心原则

编排器是调度器，而非执行器。每个 agent 通过 Task 工具（后台模式）运行，拥有独立的上下文窗口。

## 上下文传递预算

编排器在整个生命周期中，**不得将任何 agent 的完整输出读入上下文**。所有跨阶段数据通过 `merge_findings.py` / `checkpoint_verify.py` 的 stdout JSON 摘要传递。

| 来源 | 传递到编排器的内容 | 上限 |
|------|-------------------|------|
| reconnaissance.json | 关键指标（entryPoints/endpoints/dependencies 数量） | ≤200 字 |
| quick-scan.json | `merge_findings.py` stdout（totalFindings、bySeverity） | ≤300 字 |
| deep-scan.json | `merge_findings.py` stdout（totalFindings、bySeverity） | ≤300 字 |
| verification.json | `merge_findings.py merge-verify` stdout（finalFindings、removedByAntiHallucination） | ≤300 字 |
| remediation.json | 仅 `overallVerdict` + `qualityScore` | ≤100 字 |
| batch-N-result.json | `status`、`totalFindings`、`bySeverity` | ≤200 字/批次 |

## 禁止操作

- 不要为安全分析而 Read 项目源文件
- 不要为合并而 Read `agents/*.json`（委托给 `merge_findings.py`）
- 不要在 agent 提示词中嵌入完整源代码

## 允许操作

- Read 标记配置文件（`Dockerfile`、`package.json`、`go.mod`、`pom.xml`）
- Read `stage1-context.json` 的摘要字段
- Glob 检查文件存在性
- 调用 `merge_findings.py`/`checkpoint_verify.py`，解析 stdout JSON
- Read `agents/remediation.json` 的 `overallVerdict` 和 `qualityScore`
- Read `summary.json`
- 调用 `generate_report.py`

## 进度输出

### 阶段级进度
- `[1/4] 侦查阶段：正在探索项目结构...`
- `[2/4] 扫描阶段：正在执行深度安全扫描...`
- `[3/4] 验证阶段：发现 {n} 个潜在风险，正在交叉验证并评估置信度...`
- `[4/4] 修复阶段：正在生成高质量修复方案...`

### 子任务完成摘要
- `  ✓ reconnaissance 完成：识别 {n} 个入口点，{m} 个端点，{k} 个依赖`
- `  ✓ quick-scan 完成：发现 {n} 个模式匹配风险，{m} 个危险 Sink`
- `  ✓ deep-scan 完成：发现 {n} 个语义分析风险，追踪 {m} 条攻击链`
- `  ✓ 合并去重完成：{before} 个发现 → 去重后 {after} 个`
- `  ✓ verification 完成：{verified} 个已验证，{removed} 个误报移除，{downgraded} 个降级`
- `  ✓ remediation 完成：{eligible} 个漏洞可自动修复，审计质量评分 {score}`

### 阶段完成摘要
- `── 侦查阶段完成：{n} 个文件，{m} 个入口点，LSP {status} ──`
- `── 扫描阶段完成：quick-scan {n1} 个 + deep-scan {n2} 个 → 合并去重后 {total} 个风险 ──`
- `── 验证阶段完成：{verified} 个已验证，{high_conf} 个高置信度（≥90），{removed} 个误报移除 ──`
- `── 修复阶段完成：{eligible} 个可自动修复，报告已生成 ──`

## 并行调度规则

阶段 2 中 quick-scan 和 deep-scan **必须并行启动**，互不阻塞。编排器在两者都完成后再执行合并。

## Agent 生命周期

1. Task 工具后台模式启动 agent
2. Task 返回 → 读取 `agents/{name}.json` 提取摘要
3. 调用合并/检查点脚本（仅解析 stdout）
4. 将文件路径引用传递给下一阶段 agent

## 通信机制

Agent 间**没有**消息传递 API。唯一通信方式是**文件读写**：agent 写 JSON → 编排器读 JSON。禁止编造不存在的通信机制。

---

## 检查点逻辑

### 探索检查点（阶段 1 → 阶段 2）

```bash
python3 $plugin_root/scripts/checkpoint_verify.py verify-explore \
  --batch-dir security-scan-output/{batch}
```

仅解析 stdout JSON（`status`、`passRate`、`failedItems`）。
- `status: "ok"` → 进入阶段 2
- `status: "fail"`（passRate < 0.6）→ Glob 回退失败项，从 stage1-context.json 中移除失败的 entryPoints

### 扫描合并（阶段 2 → 合并）

```bash
python3 $plugin_root/scripts/merge_findings.py merge-scan \
  --batch-dir security-scan-output/{batch}
```

读取阶段 2 agent 输出，验证字段，按 `file+line+riskType` 去重，分配 `findingId`，输出 `merged-scan.json`。编排器仅解析 stdout JSON。

### 扫描检查点（阶段 2 → 阶段 3）

```bash
python3 $plugin_root/scripts/checkpoint_verify.py verify-scan \
  --batch-dir security-scan-output/{batch}
```

`hallucinations[]` 中的 findingId 标记为待移除。`status: "fail"` → 发出警告但继续阶段 3。

### 验证合并（阶段 3 → 输出）

```bash
python3 $plugin_root/scripts/merge_findings.py merge-verify \
  --batch-dir security-scan-output/{batch}
```

应用 ahAction/verificationStatus/challengeVerdict，执行高置信度门控，输出 `finding-{slug}.json` + `summary.json`。

### 跨仓库源关联（可选）

当 `crossRepoDependencies` 非空且含高/严重级别时触发：
1. 向用户展示断点摘要
2. 用户选择：关联全部 / 部分 / 跳过
3. 浅克隆到 `.tmp-cross-repo/`，仅对受影响链重新 deep-scan
4. 阶段 3 前清理；每模块克隆超时 60 秒

---

## 覆盖率评估与补漏调度

扫描合并后，基于 `merge_findings.py` stdout 和 `stage1-context.json` 攻击面信息评估维度覆盖。

| 维度 | 代号 | 覆盖来源 |
|------|------|---------|
| 注入类 | D1 | deep-scan + quick-scan |
| 凭证/密钥 | D2 | quick-scan D1 |
| 认证/授权 | D3 | deep-scan 子任务B |
| 配置安全 | D4 | quick-scan D3 |
| 文件操作 | D5 | deep-scan |
| SSRF/反序列化 | D6 | deep-scan |
| 业务逻辑 | D7 | deep-scan D9 |
| 依赖安全 | D8 | quick-scan D2 |
| 云安全 | D9 | deep-scan（当存在 cloudServices） |
| 加密安全 | D10 | quick-scan D3 |

标记状态：**已覆盖**（有 findings 或 Fast Exclusion 确认 0-hit）、**未覆盖**（有攻击面但无 findings 且非 fast-excluded）、**浅覆盖**（仅 Grep 模式匹配）。

| 未覆盖维度数 | 操作 |
|-------------|------|
| 0-2 | 继续阶段 3，在 verification Phase D 中标记 |
| ≥3 | 启动 1 个补漏 deep-scan Agent（max_turns=15） |

---

## 按技术栈加载框架安全知识

reconnaissance 完成后，根据检测到的技术栈按需加载对应知识文件。未检测到的技术栈**不加载**。

| 技术栈 | 知识文件 |
|--------|---------|
| Java + Spring | `resource/rule-details/spring-security.yaml` |
| Java + MyBatis | `resource/rule-details/mybatis-injection.yaml` |
| Python + Flask/Django/FastAPI | `resource/rule-details/python-web.yaml` |
| Node.js + Express/Koa/NestJS | `resource/rule-details/nodejs-web.yaml` |
| Go + Gin/Echo/Fiber | `resource/rule-details/go-web.yaml` |
| 存在 SSRF 攻击面 | `resource/rule-details/ssrf.yaml` |

知识文件路径记录到 `stage1-context.json > frameworkKnowledge[]`。Agent 按需 Read 相关章节——**绝不注入完整内容到提示词**。

**推理优先原则**：知识文件是参考资料，Agent 的分析能力**不受限于**知识文件中列出的风险类型。发现未列出的风险时正常报告。
