# Amazon Polly - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Polly is a cloud service that converts text into lifelike speech (text-to-speech, TTS). It supports multiple languages and voices, including generative, long-form, neural, and standard voices. You pay only for the text you synthesize, and you can cache and replay generated speech at no additional cost. Polly is HIPAA-eligible and PCI DSS certified for regulated workloads.

## Key concepts

- **Voices**: generative (most natural, supports long-form narration), neural, and standard voices across many languages; neural TTS includes a Newscaster speaking style for news narration.
- **Speech marks**: timestamps/word boundaries for synchronizing speech with content (for example, karaoke-style apps).
- **SSML**: Speech Synthesis Markup Language for controlling pronunciation, pauses, emphasis, and speaking rate.
- **Lexicons**: custom pronunciation dictionaries (for example, brand names and acronyms).
- **Synthesis**: synchronous `synthesize-speech` for short text, asynchronous tasks (`start-speech-synthesis-task`) for longer text; supports MP3, OGG, and PCM formats.
- **Use cases**: newsreaders, eLearning, games, accessibility apps, IoT voice responses, IVR.

## Common operations (AWS CLI)

```bash
# Synthesize speech (default voice)
aws polly synthesize-speech --output-format mp3 \
  --voice-id Joanna --text "Hello, welcome to our service." speech.mp3

# List voices and lexicons
aws polly describe-voices --language-code en-US
aws polly list-lexicons

# Async synthesis for longer text
aws polly start-speech-synthesis-task --output-format mp3 \
  --voice-id Matthew --text file://long-text.txt \
  --output-s3-bucket-name audio-bucket
aws polly get-speech-synthesis-task --task-id <task-id>

# Use SSML for control
aws polly synthesize-speech --output-format mp3 --voice-id Amy \
  --text-type ssml --text '<speak>Pause <break time="500ms"/> now.</speak>' out.mp3
```

## Best practices

- Choose neural or generative voices for customer-facing audio; standard voices only for low-cost needs.
- Use SSML and lexicons to control pronunciation of product names and acronyms.
- Cache generated audio (S3/CloudFront) to avoid re-synthesizing the same content.
- Use async synthesis tasks for long-form content and monitor task status.
- For compliance workloads, confirm HIPAA/PCI requirements and encrypt audio at rest.
- Review voice licensing and usage notes in the service documentation for commercial distribution.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Synthesize fails | Check the voice ID, language, text length, and output format. |
| Pronunciation wrong | Add a lexicon or use SSML phoneme tags. |
| Long text error | Use `start-speech-synthesis-task` instead of synchronous synthesis. |
| Audio not generated for task | Verify the S3 bucket policy and task status; check output path. |
| Voice unavailable for language | Confirm the voice supports the requested language/locale. |

## Limits

Characters per request, concurrent synthesis requests, lexicons per account, and task quotas apply. See the Amazon Polly endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Polly?](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)
- [Amazon Polly endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/polly.html)
- [Amazon Polly pricing](https://aws.amazon.com/polly/pricing/)
- [AWS CLI: polly commands](https://docs.aws.amazon.com/cli/latest/reference/polly/)
