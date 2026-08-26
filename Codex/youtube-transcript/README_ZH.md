# YouTube Transcript Skill

English version: [README.md](README.md)

这是一个本地优先的 Codex Skill，只通过一次 Chrome `tab.content.exportYouTubeTranscript()` 调用读取 YouTube 页面暴露的字幕。如果 Chrome 导出或校验失败，就报告失败，不重试也不切换来源。它不下载媒体、不调用 `yt-dlp` 或第三方字幕 API、不使用 Whisper，也不从标题或简介补全缺失内容。

用户只需提供 YouTube 链接。Codex 会导出一份完整 Transcript、验证覆盖范围、保存本地 `transcript.md`，最后才生成面向读者的英文与中文总结。第一次获取失败就停止流程。

## 输出约定

```text
# Git 忽略的本地证据
.local/youtube/<title-slug>--<video-id>/
├── transcript.md
└── validation.json

# 发布给读者的文件
YouTube/<topic>/<title-slug>--<video-id>/
├── summary.md
└── summary_zh.md
```

完整 transcript 和验收账本不会提交 Git。完整字幕可能受版权保护；公开仓库只发布读者总结。

## 捕获验收约定

Chrome 导出保留一份完整、有序的 Transcript。helper 先返回临时文本，再转换为下面的 JSON 输入；本地验证器自行推导读取的条目数、首尾时间和规范化 SHA-256，并要求：segment 不为空，时间戳不倒退且为有限数值（相邻字幕 cue 可以相同）；URL 与 video ID 精确匹配规范化格式；开头接近视频开始；结尾接近视频时长。任何超过 60 秒的间隔都会记录为发布前必须解决的警告。导出或校验失败就停止流程。

验证器会将 Transcript 确定性切成约 1,000 个文本单元的 chunks：英文按词组、中文等 CJK 文字按字符计数，并在本地 `validation.json` 中建立覆盖账本。通过只代表提供的读取覆盖了视频首尾并通过结构检查；不代表浏览器导出真实、总结语义完整，也不代表 YouTube 自动字幕逐字正确。

## 总结验收约定

发布前，Skill 必须处理每一个 chunk，把每项实质内容标记为 `included`、`compressed` 或纯 `cta`，并为非 CTA 项记录来源 segment ID 与原文 quote，再完成双语审计。以下任一项不为零都禁止发布：

```text
未处理的 segments
遗漏的实质内容
没有字幕证据的英文内容
没有字幕证据的中文内容
中英文时间戳不一致
```

总结不得加入建议、行动计划、更正或外部事实。订阅、点赞、留言和分享等纯 CTA 可以省略。

## 本地验证器

验证器只使用 Python 标准库。它接收由浏览器导出的一次完整读取 JSON，并作为 Skill 的内部步骤运行：

```bash
cd Codex/youtube-transcript
uv sync --group dev
uv run yt-transcript capture browser-export.json \
  --output ../../.local/youtube/<title-slug>--<video-id>
```

Skill 将所有 chunk 标记为已处理并完成手工审计后，还必须运行 `validate-publication` 来检查账本结构与连续 chunks、来源 video ID、时间戳范围、来源 segment 绑定、必需时间戳、中英文时间戳一致性、未解决的捕获警告和互相链接；它不能自动判断总结是否语义完整或忠实于来源。

## 开发

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```
