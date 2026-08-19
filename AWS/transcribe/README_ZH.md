# Amazon Transcribe - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Transcribe 是自动语音识别（ASR）服务，使用机器学习将音频转换为文本。你可以实时（流式）转录，或从 S3 批量转录音频文件，支持语言定制、内容过滤、说话人分离和多声道音频。按转录音频秒数付费；签署 BAA 后适用于 HIPAA。

## 核心概念

- **批量转录**：将 S3 中的音频文件作为任务转录；结果写入 S3（JSON、VTT、SRT）。
- **流式转录**：实时语音转文本，提供中间和最终结果；支持 websocket/HTTP2 和 SDK。
- **语言定制**：自定义语言模型、自定义词汇表和词汇过滤器，提升领域准确率。
- **内容过滤**：PII 脱敏和词汇过滤，输出适合受众或保护隐私。
- **说话人分离**：按说话人切分语音，用于会议和访谈。
- **多声道与多语言支持**：处理多声道音频，并在受支持处支持其他语言。
- **定价**：按转录秒数按用即付（精确 1 秒计费）；PII 脱敏和自定义模型等特性另收费。

## 常用操作（AWS CLI）

```bash
# 批量转录
aws transcribe start-transcription-job --transcription-job-name meeting \
  --language-code en-US --media '{"MediaFileUri":"s3://bucket/meeting.mp3"}' \
  --output-bucket-name bucket --output-key out/meeting.json
aws transcribe get-transcription-job --transcription-job-name meeting

# 说话人分离与 PII 脱敏
aws transcribe start-transcription-job --transcription-job-name support-call \
  --language-code en-US --media '{"MediaFileUri":"s3://bucket/call.wav"}' \
  --settings '{"ShowSpeakerLabels":true,"MaxSpeakerLabels":2,"ContentRedaction":{"RedactionType":"PII","RedactionOutput":"redacted"}}'

# 流式转录（HTTP2 SDK；CLI 用 aws transcribe-streaming）
aws transcribe-streaming start-stream-transcription \
  --language-code en-US --media-encoding pcm --media-sample-rate 16000 \
  --audio-stream file://audio.pcm
```

## 最佳实践

- 音频存 S3 并 KMS 加密；用受限 IAM 角色授予 Transcribe 访问。
- 领域术语和口音用自定义词汇表/语言模型提升准确率。
- 通话录音和面向客户内容启用 PII 脱敏并核对输出。
- 会议/访谈用说话人分离；为下游分析标注说话人。
- 监控批量任务状态，失败设置告警；流式只用于实时场景。
- 合规工作负载确认 HIPAA 资格与 BAA 要求，PHI 静态和传输加密。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 任务失败 | 检查音频格式/编码、S3 权限和媒体文件 URI。 |
| 准确率差 | 为领域添加自定义词汇表或自定义语言模型。 |
| PII 未脱敏 | 确认脱敏设置和语言支持；核对输出类型（redacted vs redacted_and_unredacted）。 |
| 流式报错 | 检查音频编码、采样率和 SDK/websocket 配置。 |
| 区域不支持 | 确认该区域支持所需转录类型（批量/流式）。 |

## 配额

转录任务配额、媒体时长、并发任务和 API 请求速率有限制；部分配额可调整。以 Amazon Transcribe 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Transcribe？- 开发者指南](https://docs.aws.amazon.com/transcribe/latest/dg/what-is-transcribe.html)
- [Amazon Transcribe 端点和配额](https://docs.aws.amazon.com/general/latest/gr/transcribe.html)
- [Amazon Transcribe 定价](https://aws.amazon.com/transcribe/pricing/)
- [AWS CLI：transcribe 和 transcribe-streaming 命令](https://docs.aws.amazon.com/cli/latest/reference/transcribe/)
