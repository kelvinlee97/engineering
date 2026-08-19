# Amazon Transcribe - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Transcribe is an automatic speech recognition (ASR) service that converts audio to text using machine learning. You can transcribe media in real time (streaming) or in batch from S3, with features for language customization, content filtering, speaker separation, and multi-channel audio. You pay per second of transcribed audio; HIPAA eligibility applies with a BAA.

## Key concepts

- **Batch transcription**: transcribe audio files stored in S3 as a job; results are written to S3 (JSON, VTT, SRT).
- **Streaming transcription**: real-time speech-to-text with partial and final results; supports websocket/HTTP2 and SDKs.
- **Language customization**: custom language models, custom vocabularies, and vocabulary filters to improve accuracy for your domain.
- **Content filtering**: PII redaction and vocabulary filtering for audience-appropriate or privacy-safe output.
- **Speaker diarization**: partition speech by speaker for meetings and interviews.
- **Channel and multi-language support**: process multi-channel audio and additional languages where supported.
- **Pricing**: pay-as-you-go by seconds transcribed in 1-second increments; additional charges for features like PII redaction and custom models.

## Common operations (AWS CLI)

```bash
# Batch transcription
aws transcribe start-transcription-job --transcription-job-name meeting \
  --language-code en-US --media '{"MediaFileUri":"s3://bucket/meeting.mp3"}' \
  --output-bucket-name bucket --output-key out/meeting.json
aws transcribe get-transcription-job --transcription-job-name meeting

# With speaker diarization and PII redaction
aws transcribe start-transcription-job --transcription-job-name support-call \
  --language-code en-US --media '{"MediaFileUri":"s3://bucket/call.wav"}' \
  --settings '{"ShowSpeakerLabels":true,"MaxSpeakerLabels":2,"ContentRedaction":{"RedactionType":"PII","RedactionOutput":"redacted"}}'

# Streaming (HTTP2 SDK-based; CLI supports via aws transcribe-streaming)
aws transcribe-streaming start-stream-transcription \
  --language-code en-US --media-encoding pcm --media-sample-rate 16000 \
  --audio-stream file://audio.pcm
```

## Best practices

- Store audio in S3 with KMS encryption; grant Transcribe access with a scoped IAM role.
- Use custom vocabularies/language models for domain terms and accents to improve accuracy.
- Enable PII redaction for call recordings and customer-facing content; verify output.
- Use speaker diarization for meetings and interviews; label speakers for downstream analytics.
- Monitor batch job status and set alarms for failures; use streaming only for live use cases.
- For compliance workloads, confirm HIPAA eligibility and BAA requirements, encrypting PHI at rest and in transit.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Job fails | Check the audio format/codec, S3 permissions, and media file URI. |
| Accuracy poor | Add custom vocabularies or a custom language model for the domain. |
| PII not redacted | Confirm redaction settings and language support; verify output type (redacted vs redacted_and_unredacted). |
| Streaming errors | Check audio encoding, sample rate, and SDK/websocket configuration. |
| Region not supported | Confirm the transcription type (batch/streaming) is available in the Region. |

## Limits

Transcription job quotas, media duration, concurrent jobs, and API request rates apply; some quotas are adjustable. See the Amazon Transcribe endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/what-is-transcribe.html)
- [Amazon Transcribe endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/transcribe.html)
- [Amazon Transcribe pricing](https://aws.amazon.com/transcribe/pricing/)
- [AWS CLI: transcribe and transcribe-streaming commands](https://docs.aws.amazon.com/cli/latest/reference/transcribe/)
