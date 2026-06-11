#!/usr/bin/env python3
"""
审计报告生成脚本
根据代码审计结果生成 HTML 报告（可选 JSON）
"""
import json
import argparse
import os
import sys
import subprocess
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from html import escape


class Colors:
    """终端颜色输出"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


BEIJING_TZ = timezone(timedelta(hours=8))
LOCAL_TZ = datetime.now().astimezone().tzinfo or timezone.utc
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def print_colored(message, color=Colors.ENDC):
    """彩色打印"""
    print(f"{color}{message}{Colors.ENDC}", file=sys.stderr)


def _normalize_remediation_to_risklist(data):
    """将 remediation agent 输出格式转换为标准 RiskList 格式"""
    remediations = data.get('remediations', [])
    if not remediations:
        return None

    risk_list = []
    for r in remediations:
        entry = {
            'RiskType': r.get('RiskType', r.get('riskType', '未知风险')),
            'RiskLevel': r.get('RiskLevel', r.get('riskLevel', 'low')),
            'RiskConfidence': r.get('RiskConfidence', r.get('riskConfidence', '')),
            'FilePath': r.get('FilePath', r.get('filePath', '')),
            'LineNumber': r.get('LineNumber', r.get('lineNumber', None)),
            'RiskCode': r.get('RiskCode', r.get('riskCode', '')),
            'RiskDetail': r.get('RiskDetail', r.get('riskDetail', '')),
            'Suggestions': r.get('Suggestions', r.get('suggestion', r.get('recommendation', ''))),
            'CodeSnippet': r.get('CodeSnippet', r.get('codeSnippet', r.get('originalCode', ''))),
            'FixedCode': r.get('FixedCode', r.get('fixedCode', '')),
        }
        # 保留 0-day / AI 推理标记
        merged_id = r.get('mergedId', r.get('findingId', ''))
        if merged_id:
            entry['mergedId'] = merged_id
        audited_by = r.get('auditedBy', [])
        if audited_by:
            entry['auditedBy'] = audited_by
        # 标记发现来源（用于 0-day 判断）
        discovery_method = r.get('discoveryMethod', '')
        if discovery_method:
            entry['discoveryMethod'] = discovery_method
        risk_list.append(entry)

    # 构造 summary
    high = 0
    medium = 0
    low = 0
    for entry in risk_list:
        level = get_risk_level_normalized(entry.get('RiskLevel', 'low'))
        if level == 'high':
            high += 1
        elif level == 'medium':
            medium += 1
        else:
            low += 1

    # 收集涉及的文件
    file_set = {}
    for entry in risk_list:
        fp = entry.get('FilePath', '')
        if fp:
            if fp not in file_set:
                file_set[fp] = {'fileName': os.path.basename(fp), 'filePath': fp, 'issues': 0}
            file_set[fp]['issues'] += 1

    normalized = {
        'metadata': data.get('metadata', {}),
        'summary': {
            'totalIssues': len(risk_list),
            'highRisk': high,
            'mediumRisk': medium,
            'lowRisk': low,
        },
        'RiskList': risk_list,
        '_files': list(file_set.values()),
    }

    # 保留攻击链信息
    attack_chains = data.get('attackChains', data.get('chainVerification', []))
    if attack_chains:
        normalized['attackChains'] = attack_chains

    return normalized


def load_audit_results(input_path, audit_batch_id=None):
    """加载审计结果"""
    results = []
    summary = None

    # 确定输入路径
    if audit_batch_id and not input_path:
        possible_paths = [
            os.path.join(os.getcwd(), "security-scan-output", audit_batch_id),
            os.path.join("/tmp", "security-scan-output", audit_batch_id),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                input_path = path
                break

    if not input_path:
        raise ValueError("未指定输入路径，请使用 --input 或 --audit-batch-id")

    input_path = Path(input_path)

    if input_path.is_file():
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 如果是 remediation agent 格式，先转换
            if 'remediations' in data and 'RiskList' not in data and 'issues' not in data:
                normalized = _normalize_remediation_to_risklist(data)
                if normalized:
                    data = normalized

            results.append(data)
            if 'summary' in data:
                summary = {
                    'auditBatchId': data.get('metadata', {}).get('auditBatchId', audit_batch_id or 'unknown'),
                    'totalFiles': len(data.get('_files', [])) or 1,
                    'totalIssues': data['summary'].get('totalIssues', 0),
                    'highRisk': data['summary'].get('highRisk', 0),
                    'mediumRisk': data['summary'].get('mediumRisk', 0),
                    'lowRisk': data['summary'].get('lowRisk', 0),
                    'files': data.get('_files', []) or [{
                        'fileName': data.get('metadata', {}).get('fileName', 'unknown'),
                        'filePath': data.get('metadata', {}).get('filePath', ''),
                        'issues': data['summary'].get('totalIssues', 0)
                    }]
                }

    elif input_path.is_dir():
        summary_file = input_path / "summary.json"
        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary = json.load(f)
            summary_id = summary.get('auditBatchId') if isinstance(summary, dict) else None
            if audit_batch_id and (not summary_id or summary_id == 'unknown'):
                summary['auditBatchId'] = audit_batch_id
            elif not summary_id or summary_id == 'unknown':
                summary['auditBatchId'] = input_path.name

        for file_path in sorted(input_path.glob("finding-*.json")):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'remediations' in data and 'RiskList' not in data and 'issues' not in data:
                    normalized = _normalize_remediation_to_risklist(data)
                    if normalized:
                        data = normalized
                results.append(data)

        # 如果没有 finding-*.json，尝试加载 agents 子目录中的 remediation.json 或 verification.json
        if not results:
            agents_dir = input_path / "agents"
            if agents_dir.is_dir():
                for candidate in ["remediation.json", "verification.json"]:
                    candidate_path = agents_dir / candidate
                    if candidate_path.exists():
                        with open(candidate_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        if 'remediations' in data or 'verifiedFindings' in data:
                            if 'remediations' in data:
                                normalized = _normalize_remediation_to_risklist(data)
                            elif 'verifiedFindings' in data:
                                # verification 格式也做简单转换
                                vdata = dict(data)
                                vdata['remediations'] = vdata.pop('verifiedFindings', [])
                                normalized = _normalize_remediation_to_risklist(vdata)
                            if normalized:
                                results.append(normalized)
                                break

        if not summary and results:
            total_issues = 0
            high_risk = 0
            medium_risk = 0
            low_risk = 0
            files = []

            for r in results:
                s = r.get('summary', {})
                total_issues += s.get('totalIssues', 0)
                high_risk += s.get('highRisk', 0)
                medium_risk += s.get('mediumRisk', 0)
                low_risk += s.get('lowRisk', 0)
                files.append({
                    'fileName': r.get('metadata', {}).get('fileName', 'unknown'),
                    'filePath': r.get('metadata', {}).get('filePath', ''),
                    'issues': s.get('totalIssues', 0)
                })

            summary = {
                'auditBatchId': audit_batch_id or input_path.name or 'unknown',
                'totalFiles': len(results),
                'totalIssues': total_issues,
                'highRisk': high_risk,
                'mediumRisk': medium_risk,
                'lowRisk': low_risk,
                'files': files
            }
    else:
        raise ValueError(f"输入路径不存在: {input_path}")

    if summary and isinstance(summary, dict):
        summary_id = summary.get('auditBatchId')
        if audit_batch_id and (not summary_id or summary_id == 'unknown'):
            summary['auditBatchId'] = audit_batch_id
        elif not summary_id or summary_id == 'unknown':
            if input_path.is_dir():
                summary['auditBatchId'] = input_path.name
            elif input_path.is_file():
                parent_name = input_path.parent.name
                if parent_name.startswith("audit-"):
                    summary['auditBatchId'] = parent_name

    return results, summary


def calculate_score(high, medium, low):
    """计算安全评分"""
    score = 100 - (high * 20 + medium * 10 + low * 5)
    return max(0, min(100, score))


def resolve_git_base(input_path):
    if not input_path:
        return Path.cwd()
    try:
        path = Path(input_path)
        if path.is_file():
            return path.parent
        return path
    except Exception:
        return Path.cwd()


def get_git_branch(base_path=None):
    base = Path(base_path) if base_path else Path.cwd()
    try:
        result = subprocess.run(
            ["git", "-C", str(base), "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""
    branch = result.stdout.strip()
    if not branch or branch == "HEAD":
        return ""
    return branch


def _parse_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=LOCAL_TZ)
        return value
    if isinstance(value, (int, float)):
        timestamp = float(value)
        if timestamp > 1e12:
            timestamp /= 1000.0
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        try:
            timestamp = int(text)
            if len(text) >= 13:
                timestamp /= 1000.0
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        except (ValueError, OSError):
            return None

    normalized = text.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=LOCAL_TZ)
        return dt
    except ValueError:
        pass

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d",
    ):
        try:
            dt = datetime.strptime(text, fmt)
            return dt.replace(tzinfo=LOCAL_TZ)
        except ValueError:
            continue

    return None


def format_beijing_time(value):
    dt = _parse_datetime(value)
    if not dt:
        return ""
    return dt.astimezone(BEIJING_TZ).strftime(TIME_FORMAT)


def _format_file_entries(files):
    formatted = []
    for item in files or []:
        if isinstance(item, dict):
            entry = dict(item)
            if "timestamp" in entry:
                entry["timestamp"] = format_beijing_time(entry.get("timestamp"))
            formatted.append(entry)
        else:
            formatted.append(item)
    return formatted


def _resolve_issue_file_path(issue_path, fallback_path, file_name):
    issue_path = issue_path or ""
    fallback_path = fallback_path or ""
    if fallback_path:
        normalized = issue_path.replace("\\", "/")
        if not issue_path or normalized.startswith("task/") or issue_path == file_name:
            return fallback_path
    return issue_path or fallback_path


def get_risk_level_normalized(level):
    """标准化风险等级"""
    level_lower = str(level).lower()
    if level_lower in ['high', '高', 'critical', '严重']:
        return 'high'
    elif level_lower in ['medium', '中', 'moderate', '中等']:
        return 'medium'
    else:
        return 'low'


def generate_json_report(results, summary, code_branch=None):
    """生成 JSON 格式报告"""
    audit_batch_id = summary.get('auditBatchId') or 'unknown'
    timestamp = format_beijing_time(datetime.now(timezone.utc))
    code_branch_value = code_branch or "未知"
    total_files = summary.get('totalFiles', 0)
    total_issues = summary.get('totalIssues', 0)
    high_count = summary.get('highRisk', 0)
    medium_count = summary.get('mediumRisk', 0)
    low_count = summary.get('lowRisk', 0)
    score = calculate_score(high_count, medium_count, low_count)

    # 收集所有风险并分类
    all_issues = []
    high_issues = []
    medium_issues = []
    low_issues = []

    all_attack_chains = []

    for result in results:
        file_name = result.get('metadata', {}).get('fileName', '')
        file_path_meta = result.get('metadata', {}).get('filePath', '')

        # 收集攻击链
        attack_chains = result.get('attackChains', result.get('chainVerification', []))
        if attack_chains:
            all_attack_chains.extend(attack_chains)

        issues = result.get('RiskList', result.get('issues', []))

        for issue in issues:
            risk_level = issue.get('RiskLevel', issue.get('riskLevel', ''))
            level_normalized = get_risk_level_normalized(risk_level)
            raw_file_path = issue.get('FilePath', issue.get('filePath', ''))
            file_path = _resolve_issue_file_path(raw_file_path, file_path_meta, file_name)
            file_name_value = file_name or os.path.basename(file_path) or "unknown"

            # 判断是否为 0-day / AI 推理发现的漏洞
            discovery_method = issue.get('discoveryMethod', '')
            audited_by = issue.get('auditedBy', [])
            is_zero_day = (
                discovery_method == '0-day'
                or (isinstance(audited_by, list) and 'deep-scan' in audited_by and 'quick-scan' not in audited_by)
            )

            issue_entry = {
                "issueId": len(all_issues),
                "fileName": file_name_value,
                "filePath": file_path,
                "riskType": issue.get('RiskType', issue.get('riskType', '未知风险')),
                "riskLevel": level_normalized,
                "lineNumber": issue.get('LineNumber', issue.get('lineNumber')),
                "riskCode": issue.get('RiskCode', issue.get('riskCode', '')),
                "riskConfidence": issue.get('RiskConfidence', issue.get('riskConfidence', '')),
                "description": issue.get('RiskDetail', issue.get('Description', issue.get('description', ''))),
                "recommendation": issue.get('Suggestions', issue.get('Recommendation', issue.get('recommendation', ''))),
                "codeSnippet": issue.get('CodeSnippet', issue.get('codeSnippet', '')),
                "fixedCode": issue.get('FixedCode', issue.get('fixedCode', '')),
                "isZeroDay": is_zero_day,
            }
            if issue.get('mergedId'):
                issue_entry["mergedId"] = issue['mergedId']

            all_issues.append(issue_entry)

            if level_normalized == 'high':
                high_issues.append(issue_entry)
            elif level_normalized == 'medium':
                medium_issues.append(issue_entry)
            else:
                low_issues.append(issue_entry)

    # 如果 summary 中的计数为 0 但实际有 issues，用实际数据覆盖
    actual_total = len(all_issues)
    actual_high = len(high_issues)
    actual_medium = len(medium_issues)
    actual_low = len(low_issues)
    if actual_total > 0 and total_issues == 0:
        total_issues = actual_total
        high_count = actual_high
        medium_count = actual_medium
        low_count = actual_low
        score = calculate_score(high_count, medium_count, low_count)

    # 如果 files 列表为空但可以从 _files 或 issues 推导
    files_list = summary.get('files', [])
    if not files_list:
        for result in results:
            files_list.extend(result.get('_files', []))
    if not files_list and all_issues:
        file_map = {}
        for iss in all_issues:
            fp = iss.get('filePath', '')
            if fp and fp not in file_map:
                file_map[fp] = {'fileName': iss.get('fileName', ''), 'filePath': fp, 'issues': 0}
            if fp:
                file_map[fp]['issues'] += 1
        files_list = list(file_map.values())
    total_files = total_files or len(files_list)

    # 计算涉及风险的文件数
    risk_files_count = len(files_list)

    files = _format_file_entries(files_list)
    report = {
        "success": True,
        "metadata": {
            "auditBatchId": audit_batch_id,
            "generatedAt": timestamp,
            "codeBranch": code_branch_value,
            "version": "2.0"
        },
        "summary": {
            "totalFiles": total_files,
            "riskFiles": risk_files_count,
            "totalIssues": total_issues,
            "highRisk": high_count,
            "mediumRisk": medium_count,
            "lowRisk": low_count,
            "securityScore": score
        },
        "files": files,
        "issues": {
            "high": high_issues,
            "medium": medium_issues,
            "low": low_issues
        },
        "allIssues": all_issues,
    }

    if all_attack_chains:
        report["attackChains"] = all_attack_chains

    return report


def resolve_input_path(input_path, audit_batch_id=None):
    """解析输入路径（用于写回 summary.json）"""
    if input_path:
        return Path(input_path)
    if audit_batch_id:
        possible_paths = [
            os.path.join(os.getcwd(), "security-scan-output", audit_batch_id),
            os.path.join("/tmp", "security-scan-output", audit_batch_id),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return Path(path)
    return None


def ensure_summary_file(input_path, summary):
    """确保目录输入生成 summary.json"""
    if not input_path or not input_path.is_dir():
        return
    summary_path = input_path / "summary.json"
    if summary_path.exists() or not isinstance(summary, dict):
        return
    try:
        with summary_path.open("w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
    except Exception:
        return


def _risk_label(level):
    if level == "high":
        return "高"
    if level == "medium":
        return "中"
    return "低"


def _report_status(success, high_count, medium_count, low_count):
    if not success:
        return "failed", "生成失败", "审计结果可能不完整"
    if high_count:
        return "high", "需立即处理", "存在高危风险"
    if medium_count:
        return "medium", "需要关注", "存在中危风险"
    if low_count:
        return "low", "轻微风险", "存在低危风险"
    return "clean", "通过", "未发现风险"


_CODE_FENCE_PATTERN = re.compile(r"```([A-Za-z0-9_-]*)\n?([\s\S]*?)```")


def _format_recommendation_html(recommendation):
    if not recommendation:
        return ""

    sections = []
    last_index = 0
    for match in _CODE_FENCE_PATTERN.finditer(recommendation):
        if match.start() > last_index:
            sections.append(("text", recommendation[last_index:match.start()]))
        sections.append(("code", (match.group(1).strip(), match.group(2))))
        last_index = match.end()
    if last_index < len(recommendation):
        sections.append(("text", recommendation[last_index:]))

    html_parts = []
    for kind, value in sections:
        if kind == "text":
            text = value.strip()
            if not text:
                continue
            escaped = escape(text).replace("\n", "<br>")
            html_parts.append(f"<p>{escaped}</p>")
            continue

        lang, code = value
        if code is None:
            continue
        code = code.rstrip("\n")
        if code.startswith("\n"):
            code = code[1:]
        elif code.startswith(" "):
            code = code[1:]
        if not code.strip():
            continue
        summary = "🛠️ 修复建议代码"
        if lang:
            summary = f"{summary} ({escape(lang)})"
        html_parts.append(
            f"""
                <details class="code-block" open>
                    <summary>{summary}</summary>
                    <pre><code>{escape(code)}</code></pre>
                </details>
            """
        )

    if not html_parts:
        escaped = escape(str(recommendation)).replace("\n", "<br>")
        return f"<p>{escaped}</p>"
    return "\n".join(html_parts)


def _format_issue_html(issue, issue_id=None):
    file_name = escape(str(issue.get("fileName", ""))) or "未知文件"
    file_path = escape(str(issue.get("filePath", "")))
    risk_type = escape(str(issue.get("riskType", ""))) or "未知风险"
    risk_level = escape(str(issue.get("riskLevel", ""))).lower() or "low"
    line_number = issue.get("lineNumber")
    description = escape(str(issue.get("description", ""))) or "无描述"
    recommendation = str(issue.get("recommendation", ""))
    risk_code = escape(str(issue.get("riskCode", "")))
    risk_confidence = issue.get("riskConfidence", "")
    code_snippet = escape(str(issue.get("codeSnippet", "")))
    fixed_code = escape(str(issue.get("fixedCode", "")))
    is_zero_day = issue.get("isZeroDay", False)
    
    # Generate unique ID for the issue card
    id_attr = f' id="issue-{issue_id}"' if issue_id is not None else ""

    line_display = f": {line_number}" if line_number else ""
    location = f"{file_name}{line_display}"
    risk_label = _risk_label(risk_level)
    if file_path and file_path != file_name:
        location = f"{file_path}{line_display}"

    # 0-day tag
    zero_day_tag = ""
    if is_zero_day:
        zero_day_tag = '<span class="zero-day-tag">0-day</span>'

    confidence_html = ""
    if risk_confidence != "":
        confidence_html = f'<div class="issue-info-item"><span class="issue-info-label">置信度:</span><span class="mono">{escape(str(risk_confidence))}</span></div>'

    # Build risk code block
    risk_code_block = ""
    actual_risk_code = risk_code or code_snippet
    if actual_risk_code:
        risk_code_block = f"""
            <div class="issue-section">
                <div class="issue-section-title">风险代码:</div>
                <pre class="issue-code"><code>{actual_risk_code}</code></pre>
            </div>
        """

    # Build recommendation block
    recommendation_block = ""
    recommendation_html = _format_recommendation_html(recommendation)
    if recommendation_html:
        recommendation_block = f"""
            <div class="issue-section">
                <div class="issue-section-title">修复建议:</div>
                <div class="issue-recommendation">{recommendation_html}</div>
            </div>
        """

    # Build fixed code block
    fixed_code_block = ""
    if fixed_code:
        fixed_code_block = f"""
            <div class="issue-section">
                <div class="issue-section-title">修复后代码:</div>
                <pre class="issue-code issue-code-fixed"><code>{fixed_code}</code></pre>
            </div>
        """

    return f"""
        <article class="issue-card issue-{risk_level}"{id_attr}>
            <header class="issue-head">
                <div class="issue-type">{risk_type}{zero_day_tag}</div>
                <span class="severity-pill severity-{risk_level}">{risk_label}</span>
            </header>
            <div class="issue-body">
                <div class="issue-info">
                    <div class="issue-info-item"><span class="issue-info-label">位置:</span><span class="mono">{location}</span></div>
                    {confidence_html}
                </div>
                <div class="issue-section">
                    <div class="issue-section-title">风险描述:</div>
                    <p class="issue-desc">{description}</p>
                </div>
                {risk_code_block}
                {recommendation_block}
                {fixed_code_block}
            </div>
        </article>
    """


def generate_html_report(report):
    """生成 HTML 格式报告"""
    metadata = report.get("metadata", {})
    summary = report.get("summary", {})
    audit_batch_id = escape(str(metadata.get("auditBatchId", "unknown") or "unknown"))
    generated_at = escape(str(metadata.get("generatedAt", "")))
    code_branch = escape(str(metadata.get("codeBranch", ""))) or "未知"
    success = report.get("success", False)
    total_files = summary.get("totalFiles", 0)
    risk_files = summary.get("riskFiles", 0)
    total_issues = summary.get("totalIssues", 0)
    high_count = summary.get("highRisk", 0)
    medium_count = summary.get("mediumRisk", 0)
    low_count = summary.get("lowRisk", 0)
    score = summary.get("securityScore", 0)
    score_value = score if isinstance(score, (int, float)) else 0
    score_display = int(score_value)
    score_bar = max(0, min(100, score_display))
    scope = f"扫描 {total_files} 个文件 · 发现 {total_issues} 个风险"
    status_class, status_label, status_note = _report_status(
        success, high_count, medium_count, low_count
    )

    high_issues = report.get("issues", {}).get("high", [])
    medium_issues = report.get("issues", {}).get("medium", [])
    low_issues = report.get("issues", {}).get("low", [])
    all_issues = report.get("allIssues", [])

    # Build issue ID mapping for linking from the issues table
    issue_id_map = {}
    for idx, issue in enumerate(all_issues):
        issue_id_map[id(issue)] = issue.get("issueId", idx)
    
    high_html = "\n".join(_format_issue_html(i, i.get("issueId", issue_id_map.get(id(i)))) for i in high_issues) or "<p class=\"empty-state\">暂无高危风险。</p>"
    medium_html = "\n".join(_format_issue_html(i, i.get("issueId", issue_id_map.get(id(i)))) for i in medium_issues) or "<p class=\"empty-state\">暂无中危风险。</p>"
    low_html = "\n".join(_format_issue_html(i, i.get("issueId", issue_id_map.get(id(i)))) for i in low_issues) or "<p class=\"empty-state\">暂无低危风险。</p>"

    risk_type_stats = {}
    for issue in all_issues:
        risk_type = issue.get("riskType") or "未知风险"
        level = issue.get("riskLevel") or "low"
        entry = risk_type_stats.setdefault(risk_type, {"count": 0, "max_level": "low"})
        entry["count"] += 1
        if level == "high":
            entry["max_level"] = "high"
        elif level == "medium" and entry["max_level"] == "low":
            entry["max_level"] = "medium"

    risk_type_rows = ""
    for risk_type, stats in sorted(risk_type_stats.items(), key=lambda x: x[0]):
        risk_type_rows += f"""
            <tr>
                <td>{escape(str(risk_type))}</td>
                <td>{stats["count"]}</td>
                <td><span class="severity-pill severity-{stats["max_level"]}">{_risk_label(stats["max_level"])}</span></td>
            </tr>
        """
    if not risk_type_rows:
        risk_type_rows = "<tr><td colspan=\"3\" class=\"empty-state\">暂无风险类型统计</td></tr>"

    all_issues_rows = ""
    for idx, issue in enumerate(all_issues):
        issue_id = issue.get("issueId", idx)
        file_name = escape(str(issue.get("fileName", ""))) or "未知文件"
        file_path = escape(str(issue.get("filePath", "")))
        risk_type = escape(str(issue.get("riskType", ""))) or "未知风险"
        risk_level = escape(str(issue.get("riskLevel", ""))).lower() or "low"
        line_number = issue.get("lineNumber") or "无"
        description = escape(str(issue.get("description", ""))) or "无"
        risk_confidence = escape(str(issue.get("riskConfidence", "无")))
        is_zero_day = issue.get("isZeroDay", False)
        zero_day_td = '<span class="zero-day-tag">0-day</span>' if is_zero_day else ''
        all_issues_rows += f"""
            <tr class="issue-row" data-issue-id="{issue_id}" onclick="scrollToIssue({issue_id})">
                <td><span class="mono">{file_path or file_name}</span></td>
                <td>{risk_type}{zero_day_td}</td>
                <td><span class="severity-pill severity-{risk_level}">{_risk_label(risk_level)}</span></td>
                <td><span class="mono">{line_number}</span></td>
                <td>{risk_confidence}</td>
                <td>{description}</td>
            </tr>
        """
    if not all_issues_rows:
        all_issues_rows = "<tr><td colspan=\"6\" class=\"empty-state\">暂无风险详情</td></tr>"

    # 生成攻击链 HTML
    attack_chains = report.get("attackChains", [])
    attack_chain_html = ""
    if attack_chains:
        chain_cards = ""
        for chain in attack_chains:
            chain_id = escape(str(chain.get("chainId", "")))
            finding_ids = chain.get("findingIds", [])
            combined_severity = chain.get("combinedSeverity", "high")
            severity_normalized = get_risk_level_normalized(combined_severity)
            narrative = escape(str(chain.get("narrative", "")))
            verdict = escape(str(chain.get("verdict", "")))
            ids_display = " → ".join(escape(str(fid)) for fid in finding_ids)

            verdict_html = ""
            if verdict:
                verdict_html = f'<p class="chain-verdict"><strong>结论：</strong>{verdict}</p>'

            chain_cards += f"""
                <div class="attack-chain-card attack-chain-{severity_normalized}">
                    <div class="chain-header">
                        <span class="chain-id">攻击链: {chain_id}</span>
                        <span class="severity-pill severity-{severity_normalized}">{_risk_label(severity_normalized)}</span>
                    </div>
                    <div class="chain-findings">关联漏洞: {ids_display}</div>
                    <p class="chain-narrative">{narrative}</p>
                    {verdict_html}
                </div>
            """
        attack_chain_html = f"""
        <section class="card" style="margin-top: 28px;">
            <div class="card-header">攻击链分析</div>
            {chain_cards}
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>代码安全审查报告 - {audit_batch_id}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600;700&family=Spectral:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {{
            --paper: #f7f2e8;
            --paper-2: #fcfaf5;
            --ink: #1b1a17;
            --muted: #6e665c;
            --border: #e1d7c6;
            --accent: #1f3a5f;
            --accent-soft: rgba(31, 58, 95, 0.16);
            --high: #b23a2f;
            --medium: #d08a27;
            --low: #2f7e59;
            --shadow: 0 24px 60px rgba(17, 14, 10, 0.18);
            --mono: "JetBrains Mono", "Fira Code", monospace;
            --display: "Chakra Petch", "Trebuchet MS", sans-serif;
            --body: "Spectral", "Noto Serif SC", "Songti SC", serif;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: var(--body);
            color: var(--ink);
            background-color: #fff;
            padding: 32px;
            line-height: 1.6;
        }}

        .report {{
            max-width: 1280px;
            margin: 0 auto;
            background: var(--paper-2);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 36px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }}

        .report[data-risk="high"] {{
            --accent: var(--high);
            --accent-soft: rgba(178, 58, 47, 0.14);
        }}

        .report[data-risk="medium"] {{
            --accent: var(--medium);
            --accent-soft: rgba(208, 138, 39, 0.16);
        }}

        .report[data-risk="low"] {{
            --accent: var(--low);
            --accent-soft: rgba(47, 126, 89, 0.16);
        }}

        .report[data-risk="clean"] {{
            --accent: var(--low);
            --accent-soft: rgba(47, 126, 89, 0.16);
        }}

        .report[data-risk="failed"] {{
            --accent: var(--high);
            --accent-soft: rgba(178, 58, 47, 0.18);
        }}

        .report-header {{
            display: grid;
            grid-template-columns: minmax(0, 2.2fr) minmax(240px, 1fr);
            gap: 32px;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 24px;
            margin-bottom: 28px;
        }}

        .kicker {{
            font-family: var(--display);
            text-transform: uppercase;
            letter-spacing: 0.2em;
            font-size: 0.72rem;
            color: var(--muted);
            margin-bottom: 12px;
        }}

        h1 {{
            font-family: var(--display);
            font-size: 2.4rem;
            margin: 0 0 8px;
        }}

        .subtitle {{
            margin: 0 0 20px;
            color: var(--muted);
            font-size: 1rem;
        }}

        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px 20px;
            font-size: 0.9rem;
        }}

        .meta-item {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .meta-label {{
            color: var(--muted);
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-family: var(--display);
        }}

        .meta-value {{
            font-weight: 600;
        }}

        .score-card {{
            background: var(--accent-soft);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            align-self: start;
        }}

        .status-pill {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 14px;
            border-radius: 999px;
            background: #fff;
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent);
            font-family: var(--display);
            font-size: 0.85rem;
        }}

        .status-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent);
        }}

        .status-label {{
            font-weight: 700;
        }}

        .status-note {{
            font-size: 0.75rem;
            color: var(--muted);
        }}

        .score-number {{
            font-family: var(--display);
            font-size: 3rem;
            font-weight: 700;
        }}

        .score-caption {{
            font-size: 0.9rem;
            color: var(--muted);
        }}

        .score-track {{
            position: relative;
            height: 10px;
            background: rgba(0, 0, 0, 0.08);
            border-radius: 999px;
            overflow: hidden;
        }}

        .score-fill {{
            height: 100%;
            width: {score_bar}%;
            background: var(--accent);
        }}

        .score-scale {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--muted);
            font-family: var(--display);
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }}

        .metric {{
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            box-shadow: 0 8px 18px rgba(24, 19, 13, 0.08);
        }}

        .metric-value {{
            font-family: var(--display);
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 6px;
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 0.85rem;
        }}

        .metric.high .metric-value {{ color: var(--high); }}
        .metric.medium .metric-value {{ color: var(--medium); }}
        .metric.low .metric-value {{ color: var(--low); }}

        .section-title {{
            font-family: var(--display);
            font-size: 1.5rem;
            margin: 0 0 14px;
            border-left: 4px solid var(--accent);
            padding-left: 12px;
        }}

        .section-title.section-title-lg {{
            font-size: 1.9rem;
            margin-bottom: 18px;
        }}

        .section-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
        }}

        .card {{
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 10px 24px rgba(24, 19, 13, 0.08);
        }}

        section.card + section.card {{
            margin-top: 28px;
        }}

        .card-header {{
            font-family: var(--display);
            font-size: 1.1rem;
            margin-bottom: 12px;
            color: var(--ink);
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}

        .data-table th,
        .data-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid var(--border);
            text-align: left;
            vertical-align: top;
        }}

        .data-table th {{
            font-family: var(--display);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--muted);
        }}

        .data-table th.sortable {{
            cursor: pointer;
            user-select: none;
            position: relative;
            padding-right: 24px;
            transition: color 0.2s ease, background-color 0.2s ease;
        }}

        .data-table th.sortable:hover {{
            color: var(--ink);
            background-color: var(--accent-soft);
        }}

        .data-table th.sortable::after {{
            content: '⇅';
            position: absolute;
            right: 8px;
            opacity: 0.4;
            font-size: 0.7rem;
        }}

        .data-table th.sortable.asc::after {{
            content: '↑';
            opacity: 1;
            color: var(--accent);
        }}

        .data-table th.sortable.desc::after {{
            content: '↓';
            opacity: 1;
            color: var(--accent);
        }}

        .data-table tbody tr:nth-child(even) {{
            background: rgba(247, 242, 232, 0.6);
        }}

        .data-table tbody tr.issue-row {{
            cursor: pointer;
            transition: background-color 0.2s ease;
        }}

        .data-table tbody tr.issue-row:hover {{
            background: var(--accent-soft);
        }}

        .issue-card.highlight {{
            animation: highlight-pulse 2s ease-out;
        }}

        @keyframes highlight-pulse {{
            0% {{
                box-shadow: 0 0 0 4px var(--accent);
            }}
            100% {{
                box-shadow: 0 8px 20px rgba(24, 19, 13, 0.08);
            }}
        }}

        .mono {{
            font-family: var(--mono);
            font-size: 0.82rem;
        }}

        .empty-state {{
            color: var(--muted);
            font-style: italic;
        }}

        .issues-block {{
            margin: 40px 0 32px;
        }}

        .group-title {{
            font-family: var(--display);
            font-size: 1.1rem;
            margin: 20px 0 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .issue-card {{
            border: 1px solid var(--border);
            border-left: 6px solid var(--accent);
            border-radius: 14px;
            padding: 16px 18px;
            background: #fff;
            margin-bottom: 16px;
            box-shadow: 0 8px 20px rgba(24, 19, 13, 0.08);
        }}

        .issue-card.issue-high {{
            border-left-color: var(--high);
            background: #fff6f4;
        }}

        .issue-card.issue-medium {{
            border-left-color: var(--medium);
            background: #fff8ea;
        }}

        .issue-card.issue-low {{
            border-left-color: var(--low);
            background: #f4fbf7;
        }}

        .issue-head {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
            margin-bottom: 14px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }}

        .issue-type {{
            font-family: var(--display);
            font-size: 1.15rem;
            font-weight: 700;
        }}

        .issue-info {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-bottom: 14px;
            font-size: 0.9rem;
        }}

        .issue-info-item {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .issue-info-label {{
            font-family: var(--display);
            color: #1a1a1a;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .issue-section {{
            margin-bottom: 14px;
        }}

        .issue-section:last-child {{
            margin-bottom: 0;
        }}

        .issue-section-title {{
            font-family: var(--display);
            font-size: 0.9rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 4px;
        }}

        .issue-desc {{
            margin: 0;
            line-height: 1.7;
        }}

        .issue-code {{
            margin: 0;
            padding: 14px;
            background: #1f1c18;
            color: #f5efe6;
            border-radius: 10px;
            font-family: var(--mono);
            font-size: 0.82rem;
            overflow-x: auto;
            border: 1px solid var(--border);
        }}

        .issue-code-fixed {{
            background: #1a2e1a;
            border-color: var(--low);
        }}

        .issue-recommendation {{
            background: #e8f5e9;
            border-left: 4px solid var(--low);
            padding: 12px 14px;
            border-radius: 10px;
        }}

        .issue-recommendation p {{
            margin: 0 0 8px;
        }}

        .issue-recommendation p:last-child {{
            margin-bottom: 0;
        }}

        .severity-pill {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-family: var(--display);
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #fff;
            background: var(--accent);
        }}

        .severity-high {{ background: var(--high); }}
        .severity-medium {{ background: var(--medium); }}
        .severity-low {{ background: var(--low); }}

        .zero-day-tag {{
            display: inline-flex;
            align-items: center;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.65rem;
            font-family: var(--display);
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #fff;
            background: linear-gradient(135deg, #6b21a8, #9333ea);
            margin-left: 8px;
            vertical-align: middle;
        }}

        .attack-chain-card {{
            border: 1px solid var(--border);
            border-left: 5px solid var(--accent);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
            background: #fff;
        }}

        .attack-chain-card.attack-chain-high {{
            border-left-color: var(--high);
            background: #fff6f4;
        }}

        .attack-chain-card.attack-chain-medium {{
            border-left-color: var(--medium);
            background: #fff8ea;
        }}

        .attack-chain-card.attack-chain-low {{
            border-left-color: var(--low);
            background: #f4fbf7;
        }}

        .chain-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .chain-id {{
            font-family: var(--display);
            font-weight: 700;
            font-size: 1rem;
        }}

        .chain-findings {{
            font-family: var(--mono);
            font-size: 0.82rem;
            color: var(--muted);
            margin-bottom: 8px;
        }}

        .chain-narrative {{
            margin: 0;
            line-height: 1.6;
            font-size: 0.9rem;
        }}

        .chain-verdict {{
            margin: 8px 0 0;
            line-height: 1.6;
            font-size: 0.9rem;
            color: var(--ink);
        }}

        .advice {{
            background: var(--accent-soft);
            border-left: 4px solid var(--accent);
            padding: 12px 14px;
            border-radius: 10px;
            margin-bottom: 12px;
        }}

        .advice-title {{
            font-family: var(--display);
            font-size: 0.85rem;
            margin-bottom: 6px;
        }}

        .code-stack {{
            display: grid;
            gap: 12px;
        }}

        .code-block {{
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0;
            overflow: hidden;
            background: #1f1c18;
        }}

        .code-block summary {{
            cursor: pointer;
            padding: 10px 12px;
            font-family: var(--display);
            color: #f5efe6;
            background: rgba(255, 255, 255, 0.08);
        }}

        .code-block pre {{
            margin: 0;
            padding: 14px;
            color: #f5efe6;
            font-family: var(--mono);
            font-size: 0.82rem;
            overflow-x: auto;
        }}

        .inline-details summary {{
            cursor: pointer;
            font-family: var(--display);
            font-size: 0.8rem;
        }}

        .inline-details pre {{
            margin-top: 8px;
            background: #1f1c18;
            color: #f5efe6;
            padding: 12px;
            border-radius: 8px;
            font-family: var(--mono);
            font-size: 0.78rem;
        }}

        .table-scroll {{
            overflow-x: auto;
        }}

        .report-footer {{
            margin-top: 32px;
            padding-top: 18px;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 0.9rem;
            color: var(--muted);
        }}

        @media (max-width: 980px) {{
            body {{ padding: 20px; }}
            .report {{ padding: 24px; }}
            .report-header {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 720px) {{
            h1 {{ font-size: 2rem; }}
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        @media print {{
            body {{
                background: #fff;
                padding: 0;
            }}
            .report {{
                box-shadow: none;
                border: none;
                padding: 0;
            }}
            .issue-card {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="report" data-risk="{status_class}">
        <header class="report-header">
            <div class="header-main">
                <h1>代码安全审查报告</h1>
                <p class="subtitle">批次 {audit_batch_id} · {scope}</p>
                <div class="meta-grid">
                    <div class="meta-item">
                        <span class="meta-label">生成时间</span>
                        <span class="meta-value">{generated_at}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">审计批次</span>
                        <span class="meta-value">{audit_batch_id}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">代码分支</span>
                        <span class="meta-value">{code_branch}</span>
                    </div>
                    <div class="meta-item">
                        <span class="meta-label">生成状态</span>
                        <span class="meta-value">{"成功" if success else "失败"}</span>
                    </div>
                </div>
            </div>
            <div class="score-card">
                <div class="status-pill status-{status_class}">
                    <span class="status-dot"></span>
                    <div>
                        <div class="status-label">{status_label}</div>
                        <div class="status-note">{status_note}</div>
                    </div>
                </div>
                <div class="score-number">{score_display}</div>
                <div class="score-caption">安全评分</div>
                <div class="score-track">
                    <div class="score-fill"></div>
                </div>
                <div class="score-scale">
                    <span>0</span>
                    <span>50</span>
                    <span>100</span>
                </div>
            </div>
        </header>

        <section class="metrics-grid">
            <div class="metric">
                <div class="metric-value">{total_files}</div>
                <div class="metric-label">扫描文件数</div>
            </div>
            <div class="metric">
                <div class="metric-value">{risk_files}</div>
                <div class="metric-label">涉及文件数</div>
            </div>
            <div class="metric">
                <div class="metric-value">{total_issues}</div>
                <div class="metric-label">风险总数</div>
            </div>
            <div class="metric high">
                <div class="metric-value">{high_count}</div>
                <div class="metric-label">严重风险</div>
            </div>
            <div class="metric medium">
                <div class="metric-value">{medium_count}</div>
                <div class="metric-label">中等风险</div>
            </div>
            <div class="metric low">
                <div class="metric-value">{low_count}</div>
                <div class="metric-label">低微风险</div>
            </div>
        </section>

        <section class="section-grid">
            <div class="card">
                <div class="card-header">风险类型分布</div>
                <div class="table-scroll">
                    <table class="data-table" id="risk-type-table">
                        <thead>
                            <tr>
                                <th class="sortable" data-sort="string" onclick="sortTable(this, 0)">风险类型</th>
                                <th class="sortable" data-sort="number" onclick="sortTable(this, 1)">数量</th>
                                <th class="sortable" data-sort="severity" onclick="sortTable(this, 2)">严重程度</th>
                            </tr>
                        </thead>
                        <tbody>
                            {risk_type_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <section class="card">
            <div class="card-header">风险列表</div>
            <div class="table-scroll">
                <table class="data-table" id="risk-list-table">
                    <thead>
                        <tr>
                            <th class="sortable" data-sort="string" onclick="sortTable(this, 0)">文件</th>
                            <th class="sortable" data-sort="string" onclick="sortTable(this, 1)">风险类型</th>
                            <th class="sortable" data-sort="severity" onclick="sortTable(this, 2)">级别</th>
                            <th class="sortable" data-sort="number" onclick="sortTable(this, 3)">行号</th>
                            <th class="sortable" data-sort="number" onclick="sortTable(this, 4)">置信度</th>
                            <th class="sortable" data-sort="string" onclick="sortTable(this, 5)">描述</th>
                        </tr>
                    </thead>
                    <tbody>
                        {all_issues_rows}
                    </tbody>
                </table>
            </div>
        </section>

        {attack_chain_html}

        <section class="issues-block">
            <h2 class="section-title section-title-lg">详细风险列表</h2>
            <h3 class="group-title">🔴 高危风险</h3>
            {high_html}
            <h3 class="group-title">🟡 中危风险</h3>
            {medium_html}
            <h3 class="group-title">🟢 低危风险</h3>
            {low_html}
        </section>

        <footer class="report-footer">
            <div>内容由 AI 生成，仅供参考</div>
        </footer>
    </div>
    <script>
        function scrollToIssue(issueId) {{
            const target = document.getElementById('issue-' + issueId);
            if (target) {{
                target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                target.classList.remove('highlight');
                void target.offsetWidth; // Trigger reflow to restart animation
                target.classList.add('highlight');
            }}
        }}

        function sortTable(header, columnIndex) {{
            const table = header.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const sortType = header.dataset.sort || 'string';
            
            // Severity order mapping (high > medium > low)
            const severityOrder = {{
                '高': 3, 'high': 3, 'HIGH': 3,
                '中': 2, 'medium': 2, 'MEDIUM': 2,
                '低': 1, 'low': 1, 'LOW': 1
            }};
            
            // Check if already sorted and determine direction
            const isAsc = header.classList.contains('asc');
            const direction = isAsc ? -1 : 1;
            
            // Remove sort classes from all headers in this table
            table.querySelectorAll('th.sortable').forEach(th => {{
                th.classList.remove('asc', 'desc');
            }});
            
            // Add appropriate class to current header
            header.classList.add(isAsc ? 'desc' : 'asc');
            
            // Sort rows
            rows.sort((a, b) => {{
                const aCell = a.cells[columnIndex];
                const bCell = b.cells[columnIndex];
                
                if (!aCell || !bCell) return 0;
                
                let aVal = aCell.textContent.trim();
                let bVal = bCell.textContent.trim();
                
                if (sortType === 'number') {{
                    aVal = parseFloat(aVal) || 0;
                    bVal = parseFloat(bVal) || 0;
                    return (aVal - bVal) * direction;
                }} else if (sortType === 'severity') {{
                    aVal = severityOrder[aVal] || 0;
                    bVal = severityOrder[bVal] || 0;
                    return (aVal - bVal) * direction;
                }} else {{
                    return aVal.localeCompare(bVal, 'zh-CN') * direction;
                }}
            }});
            
            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        }}
    </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="根据代码审计结果生成 JSON 或 HTML 报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 从审计目录生成报告
  %(prog)s --input security-scan-output/audit-20250103120000

  # 使用审计批次 ID 自动查找目录
  %(prog)s --audit-batch-id audit-20250103120000

  # 输出 JSON 到文件
  %(prog)s --input security-scan-output/audit-20250103120000 --output report.json

  # 输出 HTML 到文件（保存在 security-scan-output 下）
  %(prog)s --audit-batch-id audit-20250103120000 --format html \\
    --output security-scan-output/audit-20250103120000/report.html
        """
    )

    parser.add_argument('--input', help='输入路径（JSON 文件或审计目录）')
    parser.add_argument('--audit-batch-id', help='审计批次 ID（用于自动定位目录）')
    parser.add_argument('--output', help='输出 JSON 文件路径（默认输出到 stdout）')
    parser.add_argument('--format', choices=['json', 'html'], default='json',
                        help='报告输出格式（默认: json）')
    parser.add_argument('--quiet', action='store_true', help='静默模式（不输出日志）')
    parser.add_argument('--pretty', action='store_true', default=True,
                       help='格式化 JSON 输出（默认: True）')
    parser.add_argument('--compact', action='store_true',
                       help='紧凑 JSON 输出（单行）')

    args = parser.parse_args()

    if args.quiet:
        Colors.HEADER = Colors.BLUE = Colors.CYAN = Colors.GREEN = ''
        Colors.WARNING = Colors.FAIL = Colors.ENDC = Colors.BOLD = ''

    if not args.input and not args.audit_batch_id:
        print_colored("❌ 请指定 --input 或 --audit-batch-id", Colors.FAIL)
        sys.exit(1)

    try:
        # 加载审计结果
        resolved_input = resolve_input_path(args.input, args.audit_batch_id)
        input_for_load = str(resolved_input) if resolved_input else args.input
        results, summary = load_audit_results(input_for_load, args.audit_batch_id)
        ensure_summary_file(resolved_input, summary)

        if not results:
            raise ValueError("未找到审计结果")

        if not args.quiet:
            print_colored(f"✅ 加载了 {len(results)} 个审计结果", Colors.GREEN)

        # 生成报告
        base_path = resolve_git_base(args.input)
        code_branch = get_git_branch(base_path) or "未知"
        report = generate_json_report(results, summary, code_branch=code_branch)

        output_format = args.format
        if args.output and args.output.lower().endswith(".html"):
            output_format = "html"

        if output_format == "html":
            html_output = generate_html_report(report)
            if not args.output:
                output_name = f"security-scan-report-{summary.get('auditBatchId', 'unknown')}.html"
                args.output = os.path.join(os.getcwd(), output_name)
            output_path = os.path.abspath(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
            if not args.quiet:
                print_colored(f"✅ 报告已保存: {output_path}", Colors.GREEN)
        else:
            # 输出 JSON
            indent = None if args.compact else 2
            json_output = json.dumps(report, ensure_ascii=False, indent=indent)

            if args.output:
                output_path = os.path.abspath(args.output)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                if not args.quiet:
                    print_colored(f"✅ 报告已保存: {output_path}", Colors.GREEN)
            else:
                print(json_output)

    except Exception as e:
        error_report = {"success": False, "error": str(e)}
        print(json.dumps(error_report, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  用户中断操作", Colors.WARNING)
        sys.exit(130)
    except Exception as e:
        print_colored(f"\n❌ 未预期的错误: {e}", Colors.FAIL)
        import traceback
        traceback.print_exc()
        sys.exit(1)
