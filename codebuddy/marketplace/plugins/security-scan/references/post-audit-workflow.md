# 审计后工作流（共享片段）

> 引用方：commands/project.md（阶段 4）、commands/diff.md（阶段 4）

## 前置条件：`$plugin_root`

所有对 `$plugin_root` 的引用均假设该变量已由 command 入口在阶段 1.1 中设置。

---

## 审计摘要模板

审计完成后输出此简要摘要（技术细节记录在 `summary.json` 中）：

```
代码安全审查完成！

发现 {total_issues} 个问题：{critical_count} 严重 / {high_count} 高危 / {medium_count} 中危 / {low_count} 低危
{scope_line}
{security_score_line (project command only)}

严重/高危漏洞：
1. [{RiskLevel}][{RiskType}] {FilePath}:{LineNumber} -- 置信度 {RiskConfidence}
2. [{RiskLevel}][{RiskType}] {FilePath}:{LineNumber} -- 置信度 {RiskConfidence}
...

审计结果文件：
   finding-sql-injection.json -- 漏洞安全审计 -- SQL 注入（2 个风险）
   finding-hardcoded-secret.json -- 密钥安全审计 -- 硬编码凭证（1 个风险）
   finding-endpoint-exposure.json -- 配置不当安全审计 -- 敏感端点暴露（2 个风险）
  ...

详细报告已保存至 security-scan-output/{batch}/
```

> 文件列表必须包含中文分类说明：` {filename} -- {中文分类}（{N} 个风险）`。

规则：
- 严重/高危列表：最多 10 条；超出部分显示 `... 及其他 {n} 个严重/高危漏洞`。
- 无严重/高危漏洞时省略该部分。
- 批次 ID、agent 数量、耗时、置信度说明仅记录在 `summary.json` 中。

命令特定的审查范围行：
- **project**: `审查范围：{total_files} 个文件`，以及 `安全评分：{score}/100`
- **diff**: `变更文件：{changed_files} 个`（无评分）

---

## 用户交互：下一步操作

摘要输出后，根据是否存在高置信度（>= 90）漏洞展示选项。

**存在高置信度漏洞时：**

```
请选择下一步操作：
1. 修复高危漏洞（自动修复置信度 >= 90 的漏洞）
2. 生成 HTML 详细报告
3. 全部执行（修复 + 报告）
4. 结束审计
```

**不存在高置信度漏洞时：**

```
本次审计未发现置信度 >= 90 的漏洞，无需自动修复。
低置信度漏洞建议人工审查。

请选择下一步操作：
1. 生成 HTML 详细报告
2. 结束审计
```

> 所有破坏性操作（代码修改、文件生成）均需用户明确确认。

---

## 修复漏洞流程

当用户选择选项 1 或选项 3 的修复部分时触发。

**步骤 1：展示修复候选项并请求确认**

列出所有符合条件的漏洞（RiskConfidence >= 90、反幻觉门控通过、challengeVerdict = confirmed/escalated）：

```
以下漏洞符合自动修复条件（置信度 >= 90）：

  序号  风险级别  风险类型    文件                          行号  置信度  修复策略                  兼容性风险
  1     Critical  SQL 注入    src/dao/UserDao.java          45    95     参数化查询替换字符串拼接  none
  2     High      命令注入    src/util/PingUtil.java        23    92     subprocess 参数数组       none
  ...

共 {eligible_count} 个漏洞可自动修复。

 自动修复将直接修改源代码文件，建议确保 Git 工作区干净或已备份。

确认全部修复？(Y/n)
```

- Y/确认：继续执行修复。
- n/取消：跳过，返回菜单。

**步骤 2：执行修复**

使用 Edit 工具逐一应用 remediation agent 的修复方案。每个文件修复后立即验证：
- 确认 Edit 操作成功
- 如修复失败（代码已变更导致 originalCode 不匹配），提示用户并跳过

---

## 生成 HTML 报告流程

当用户选择选项 2 或选项 3 的报告部分时触发。

> `generate_report.py` 只能在此阶段调用。不得提前调用。

**步骤 1：预览并确认**

```
即将生成 HTML 安全审计报告：

报告内容：
- 审计摘要：{total_issues} 个问题（{critical_count} 严重 / {high_count} 高危 / {medium_count} 中危 / {low_count} 低危）
- 高危漏洞详情及修复建议
- 审计覆盖度与质量评估
- 审计批次 ID：{audit_batch_id}

输出路径：security-scan-output/{audit_batch_id}/security-scan-report.html

确认生成报告？(Y/n)
```

**步骤 2：执行**

```bash
python3 $plugin_root/scripts/generate_report.py \
  --input security-scan-output/"$audit_batch_id" \
  --audit-batch-id "$audit_batch_id" \
  --format html \
  --output security-scan-output/"$audit_batch_id"/security-scan-report.html
```

---

## 选项 3：全部执行

先执行修复流程（包含独立确认），再执行报告流程（包含独立确认）。每个流程独立进行确认。

---

## 修复完成摘要

```
修复完成！

已修复：{fixed_count} 个漏洞
跳过（代码已变更无法自动修复）：{failed_count} 个

修复的漏洞：
1. [{RiskLevel}][{RiskType}] {FilePath}:{LineNumber} -- {strategy}
2. [{RiskLevel}][{RiskType}] {FilePath}:{LineNumber} -- {strategy}
...

 建议在修复后运行项目测试，并使用 git diff 审查变更内容。
```
