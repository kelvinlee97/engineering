# 可验证的 YouTube 字幕工具

English version: [README.md](README.md)

这是一套轻量、本地优先的工作流：提取 YouTube 已提供的字幕轨道，验证证据完整性，再通过严格契约让 Codex 生成有证据引用的中英文一页文章。

它使用 `yt-dlp` 获取元数据和字幕；**不会**下载视频或音频，不使用 FFmpeg、Whisper，也不内置 AI 模型。

## 临时验收材料

CLI 将验收材料写入调用方指定的临时目录：

```text
metadata.json              视频与所选字幕轨道的来源信息
extraction-report.json     complete、partial 或 blocked 验证结果
raw/*.vtt                  yt-dlp 返回的原始字幕
transcript.md              带时间与 cue ID 的可读全文
evidence.json              用于写作的结构化证据
summary.en.md              临时英文验收稿
summary.zh.md              临时中文验收稿
```

这些文件只是工作材料，不是最终知识资产。面向读者的 Markdown 发布并检查通过后，应删除临时目录。不得提交原始字幕或内部证据。字幕可能受版权保护，分享前应检查使用权和隐私边界。

## 安装

需要 Python 3.11+、[`uv`](https://docs.astral.sh/uv/) 和 [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)。

```bash
uv tool install yt-dlp
cd Codex/youtube-transcript
uv sync --group dev
```

Python 运行时除标准库外没有其他依赖。

## 使用方法

检查字幕轨道和确定性选择结果：

```bash
uv run yt-transcript probe "https://www.youtube.com/watch?v=VIDEO_ID"
```

使用 `mktemp -d` 创建唯一临时目录后，在不下载媒体的情况下捕获并验证字幕：

```bash
uv run yt-transcript capture "https://www.youtube.com/watch?v=VIDEO_ID" --output TEMP_DIR
uv run yt-transcript verify "TEMP_DIR/VIDEO_ID"
```

验证 Codex 生成的中英文文章：

```bash
uv run yt-transcript validate-summaries \
  TEMP_DIR/VIDEO_ID/evidence.json \
  TEMP_DIR/VIDEO_ID/summary.en.md \
  TEMP_DIR/VIDEO_ID/summary.zh.md
```

退出码 `0` 表示完整；`2` 表示不完整、受阻或验证失败。所有命令同时输出结构化 JSON。

## 字幕轨道选择

默认顺序是：创作者英文字幕、创作者原语言字幕、YouTube 自动英文字幕、YouTube 自动原语言字幕。选择原因会被记录。没有合格字幕轨道时状态为 `blocked`，不会自动改用语音识别。

## 完整性契约

只有 VTT 文件存在、所有 cue 均能解析、时间有效，而且最后一条字幕在允许误差内到达视频结尾，状态才是 `complete`。原始文件与规范化文件都会记录 SHA-256 哈希。

文章验证器还要求：

- 捕获状态为 `complete`；
- 所有引用均指向已知 cue；
- 中英文引用集合完全相同；
- 包含来源、视频内容、实际应用和限制等必需章节。

因此，只有表面流畅但证据不足或只覆盖部分内容的总结无法通过。

## Codex Skill

可复用 Skill 位于 [`skills/youtube-transcript/`](skills/youtube-transcript/)。安装或软链接到 Codex skills 目录后，类似“把这个 YouTube 链接整理成中英文一页笔记”的请求即可触发工作流。

Skill 会让验收过程保持临时，只在 `YouTube/<topic>/<标题>--<视频 ID>/` 下发布面向读者的 `README.md` 和 `README_ZH.md`。

## 开发

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

测试只使用本地 fixture，不会访问 YouTube。
