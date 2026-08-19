# Amazon Polly - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Polly 是将文本转换为逼真语音（text-to-speech，TTS）的云服务。它支持多种语言和声音，包括生成式（generative）、长文（long-form）、神经（neural）和标准（standard）声音。你只为合成的文本付费，且可以免费缓存和回放生成的语音。Polly 适用于 HIPAA 并在 PCI DSS 下认证，可用于受监管工作负载。

## 核心概念

- **声音（Voices）**：跨多种语言的生成式（最自然，支持长文朗读）、神经和标准声音；神经 TTS 提供面向新闻播报的 Newscaster 说话风格。
- **Speech marks**：时间戳/词边界，用于语音与内容同步（例如卡拉 OK 式应用）。
- **SSML**：语音合成标记语言，控制发音、停顿、强调和语速。
- **Lexicons**：自定义发音词典（例如品牌名和缩写）。
- **合成方式**：短文本用同步 `synthesize-speech`，长文本用异步任务（`start-speech-synthesis-task`）；支持 MP3、OGG 和 PCM 格式。
- **用途**：新闻阅读、eLearning、游戏、无障碍应用、IoT 语音回复、IVR。

## 常用操作（AWS CLI）

```bash
# 合成语音（默认声音）
aws polly synthesize-speech --output-format mp3 \
  --voice-id Joanna --text "Hello, welcome to our service." speech.mp3

# 列出声音和 lexicon
aws polly describe-voices --language-code en-US
aws polly list-lexicons

# 长文本异步合成
aws polly start-speech-synthesis-task --output-format mp3 \
  --voice-id Matthew --text file://long-text.txt \
  --output-s3-bucket-name audio-bucket
aws polly get-speech-synthesis-task --task-id <task-id>

# 使用 SSML 控制
aws polly synthesize-speech --output-format mp3 --voice-id Amy \
  --text-type ssml --text '<speak>Pause <break time="500ms"/> now.</speak>' out.mp3
```

## 最佳实践

- 面向客户的音频用神经或生成式声音；低成本需求用标准声音。
- 用 SSML 和 lexicon 控制产品名和缩写的发音。
- 缓存生成的音频（S3/CloudFront），避免重复合成相同内容。
- 长文内容用异步合成任务并监控任务状态。
- 合规工作负载确认 HIPAA/PCI 要求，并对静态音频加密。
- 商业分发前查看服务文档中的声音许可和使用说明。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 合成失败 | 检查声音 ID、语言、文本长度和输出格式。 |
| 发音错误 | 添加 lexicon 或使用 SSML phoneme 标签。 |
| 长文本报错 | 用 `start-speech-synthesis-task` 替代同步合成。 |
| 任务未生成音频 | 核对 S3 桶策略和任务状态；检查输出路径。 |
| 该语言无此声音 | 确认声音支持请求的语言/locale。 |

## 配额

每次请求字符数、并发合成请求、每账户 lexicon 数和任务配额有限制。以 Amazon Polly 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Polly？- 开发者指南](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)
- [Amazon Polly 端点和配额](https://docs.aws.amazon.com/general/latest/gr/polly.html)
- [Amazon Polly 定价](https://aws.amazon.com/polly/pricing/)
- [AWS CLI：polly 命令](https://docs.aws.amazon.com/cli/latest/reference/polly/)
