# 仅浏览器的 YouTube Transcript Skill

English version: [README.md](README.md)

这是一个本地优先的 Codex Skill，只读取用户在 YouTube 页面点击 **Show transcript** 后展示的字幕。它不下载媒体、不调用 `yt-dlp` 或第三方字幕 API、不使用 Whisper，也不从标题或简介补全缺失内容。

用户只需提供 YouTube 链接。Codex 会在内置浏览器中打开页面、读取两次 Transcript DOM、验证两次结果一致、保存本地 `transcript.md`，最后才生成面向读者的英文与中文总结。

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

浏览器导出保留两份完整、有序的 Transcript。本地验证器自行推导两次读取的条目数、首尾时间和规范化 SHA-256，并要求：segment 不为空，时间戳严格递增且为有限数值；URL 与 video ID 一致；开头接近视频开始；结尾接近视频时长。任何超过 60 秒的间隔都会记录为需人工审计的警告。

验证器会将 Transcript 确定性切成约 1,000 词的 chunks，并在本地 `validation.json` 中建立覆盖账本。通过只代表两份提供的读取在结构上相同；不代表浏览器导出真实、总结语义完整，也不代表 YouTube 自动字幕逐字正确。

## 总结验收约定

发布前，Skill 必须处理每一个 chunk，把每项实质内容标记为 `included`、`compressed` 或纯 `cta`，再独立审计两个总结。以下任一项不为零都禁止发布：

```text
未处理的 segments
遗漏的实质内容
没有字幕证据的英文内容
没有字幕证据的中文内容
中英文时间戳不一致
```

总结不得加入建议、行动计划、更正或外部事实。订阅、点赞、留言和分享等纯 CTA 可以省略。

## 本地验证器

验证器只使用 Python 标准库。它接收由浏览器导出的两次读取 JSON，并作为 Skill 的内部步骤运行：

```bash
cd Codex/youtube-transcript
uv sync --group dev
uv run yt-transcript capture browser-export.json \
  --output ../../.local/youtube/<title-slug>--<video-id>
```

Skill 将所有 chunk 标记为已处理并完成手工审计后，还必须运行 `validate-publication` 来检查覆盖账本结构、必需时间戳、中英文时间戳一致性和互相链接；它不能自动判断总结是否语义完整或忠实于来源。

## 开发

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```
