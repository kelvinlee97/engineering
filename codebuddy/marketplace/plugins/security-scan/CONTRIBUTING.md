# 贡献指南

本文档说明如何为 security-scan 插件添加新功能或修改现有功能。

---

## 如何新增一个 Agent

以新增 `my-audit` agent 为例，需依次修改以下文件：

1. **创建 `agents/my-audit.md`** — 定义 agent 的角色、工具、任务指令。文件头部使用 YAML front-matter 声明 name、description、tools，正文编写具体任务说明（参照已有 agent 格式）
2. **编辑 `references/output-schemas.md`** — 添加该 agent 的输出字段表格
3. **编辑 `references/orchestrator-rules.md`** — 注册到对应阶段的编排流程，明确所属阶段、启动依赖、LSP 使用策略
4. **编辑 `references/post-audit-workflow.md`** — 如该 agent 影响审计后流程，更新相关引用
5. **编辑 `.codebuddy-plugin/plugin.json`** — 更新 `features` 中的 agent 数量描述

---

## 如何新增一个安全规则类别

1. **在 `resource/rule-details/` 创建 YAML 文件**（如 `xxe.yaml`），定义该漏洞类型的参考数据（绕过技术、检测模式等纯数据，不包含 LLM 思维教程）
2. **编辑 `resource/default-rules.yaml`** — 在规则目录注释区添加索引行：
   ```yaml
   # resource/rule-details/xxe.yaml -- XXE 分析
   ```
3. **更新相关 agent prompt** — 在 `agents/deep-scan.md` 等相关 agent 中提及新规则类别，使其按需 Read 该文件

---

## 如何修改现有 Agent 的输出合约

1. **编辑 `references/output-schemas.md`** — 修改该 agent 的输出字段表格
2. **编辑 `agents/{agent-name}.md`** — 确保任务说明与新合约一致
3. **验证下游消费者** — 检查以下文件中对该字段的引用：
   - `references/orchestrator-rules.md`（编排器传递的字段）
   - 下游 agent 定义文件（依赖该字段的 agent）
   - `scripts/generate_report.py`（报告生成脚本）
4. 如影响最终汇总，同步更新 `references/output-schemas.md` 中的摘要格式

---

## 本地测试变更

### 运行插件

1. 确保插件目录位于 `~/.codebuddy/plugins/marketplaces/security-scan/`（或符号链接到开发目录）
2. 执行命令测试：`/security-scan:project`（全项目）或 `/security-scan:diff`（变更文件）
3. 检查 `security-scan-output/{batch}/` 下的中间产物和最终结果

### 验证 Agent 输出

1. 运行完整审计流程后，逐一检查 `agents/{agent-name}.json`
2. 确认输出字段与 `references/output-schemas.md` 中的合约定义一致
3. 确认 `findingId` 引用链完整（如 finding-validator → vulnerability-audit）
4. 确认 `summary.json` 的 `executionMetrics` 中各 agent 均有记录

---

## Code Review 清单

提交 PR 时，请确认以下事项：

- [ ] **合约一致性**：`agents/*.md` 与 `references/output-schemas.md` 字段匹配
- [ ] **编排完整性**：agent 已在 `references/orchestrator-rules.md` 正确注册
- [ ] **风险类型同步**：新增风险类型已在 `resource/risk-type-taxonomy.yaml` 中登记
- [ ] **规则索引同步**：新规则文件已在 `default-rules.yaml` 索引中登记
- [ ] **反幻觉合约兼容**：新 agent 的 prompt 包含反幻觉合约引用注入
- [ ] **LSP 降级兼容**：使用 LSP 的 agent 有 Grep + Read 降级方案
- [ ] **产物目录更新**：`references/output-schemas.md` 的目录树反映最新结构
