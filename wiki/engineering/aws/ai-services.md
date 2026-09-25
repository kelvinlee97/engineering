---
type: Service
title: AWS AI services
description: Pre-trained AWS APIs for language, vision, speech, translation, chatbots, and enterprise search.
tags: [aws, machine-learning, ai]
sources:
  - id: aws-comprehend
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/comprehend/README.md
    title: "Amazon Comprehend - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-rekognition
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/rekognition/README.md
    title: "Amazon Rekognition - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-polly
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/polly/README.md
    title: "Amazon Polly - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-transcribe
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/transcribe/README.md
    title: "Amazon Transcribe - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-translate
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/translate/README.md
    title: "Amazon Translate - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-lex
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/lex/README.md
    title: "Amazon Lex - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-kendra
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/kendra/README.md
    title: "Amazon Kendra - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:37:31Z }
status: draft
---
AWS AI services are pre-trained models behind an API: you send text, images, video, or audio and get back structured results, with no model to train or host. Most also accept your own terms or labeled examples to adapt the model to your domain. For training your own models, see [Machine learning](machine-learning.md).

## Choosing a service

| Input | Output | Service | Small or interactive work | Large or long work | Adapt it with |
| --- | --- | --- | --- | --- | --- |
| Text | Entities, key phrases, sentiment, PII, language, syntax | [Comprehend](#amazon-comprehend) | `Detect*` APIs | Asynchronous analysis jobs | Custom classifiers and entity recognizers |
| Images, video | Labels, text, faces, unsafe content | [Rekognition](#amazon-rekognition) | Images: one synchronous call | Video: asynchronous job, completion via SNS | Custom Labels, moderation adapters |
| Text | Speech | [Polly](#amazon-polly) | `synthesize-speech` | `start-speech-synthesis-task` | SSML and lexicons |
| Audio | Text | [Transcribe](#amazon-transcribe) | Streaming | Batch jobs from S3 | Custom vocabularies and language models |
| Text, documents | Text in another language | [Translate](#amazon-translate) | `translate-text` | Batch jobs from S3 | Custom terminology, parallel data |
| Voice or text conversation | Intents and slots, fulfilled by Lambda | [Lex](#amazon-lex) | Per request | n/a | Sample utterances, slot types |
| A question | Answers from your documents | [Kendra](#amazon-kendra) | Per query | n/a | Metadata and FAQs; closed to new customers |

The same rule holds for every row: use the synchronous API for interactive work, and jobs for bulk work, as the Comprehend note recommends to control cost. Keep inputs in S3 with KMS encryption, and scope each service's IAM role to the buckets it reads.

## Amazon Comprehend

Comprehend applies natural language processing to text. Its pre-trained insights are entities (people, places, organizations), key phrases, PII, dominant language, sentiment (positive, neutral, negative, mixed), targeted sentiment per entity, and syntax. Try the pre-trained detectors first; train a custom classifier or entity recognizer only when your categories or terms are too specific for them, and use a flywheel to retrain and evaluate new versions over time.

- Dominant-language detection covers more languages than the other features; check support per feature.
- Delete idle custom model endpoints, which keep costing money.[^aws-comprehend]

## Amazon Rekognition

Rekognition analyzes images and videos in S3: objects and scenes, text, faces, celebrities, unsafe content, and image quality; for video, also people pathing and segmentation. Face collections index faces for search and identity verification, and Face Liveness checks that a live person is present, detecting photos, videos, 3D masks, and deepfakes. It is HIPAA-eligible.

- Set confidence thresholds for content moderation, and customize its labels with adapters.
- Follow privacy law and get consent where required before using face features.
- A stuck video job usually means SNS topic permissions.[^aws-rekognition]

## Amazon Polly

Polly turns text into speech in MP3, OGG, or PCM. Voices come in generative (most natural, for long-form narration), neural (including a Newscaster style), and standard (lowest cost) types. SSML controls pronunciation, pauses, emphasis, and rate; lexicons fix how brand names and acronyms are said; speech marks give word timings for synchronizing with text. You pay per character synthesized, and replaying cached audio is free, so cache output in S3 or CloudFront. It is HIPAA-eligible and PCI DSS certified.[^aws-polly]

## Amazon Transcribe

Transcribe converts speech to text, either streaming with partial and final results or as batch jobs that write JSON, VTT, or SRT to S3. You pay per second of audio. Speaker diarization separates speakers, and PII redaction and vocabulary filters clean the output. HIPAA eligibility applies with a BAA.

- Improve accuracy on domain terms and accents with custom vocabularies or a custom language model.
- If PII is not redacted, check the redaction settings, language support, and output type (`redacted` or `redacted_and_unredacted`).[^aws-transcribe]

## Amazon Translate

Translate translates text in real time or documents (HTML, DOCX, XLSX, PPTX, TXT) in S3 as batch jobs, priced per character with no commitment. Custom terminology fixes product and brand names; parallel data trains an Active Custom Translation (ACT) model for domain accuracy. Have a person review customer-facing output.[^aws-translate]

## Amazon Lex

Lex V2 builds voice and text chatbots with speech recognition and language understanding. A bot has intents (what the user wants, such as BookAppointment), each with sample utterances and slots, the values the bot must collect. Lambda fulfills the request; bots created after August 17, 2022 can also branch conditionally without Lambda.

- Start with a few high-value intents, then add utterances from conversation logs where the bot falls back.
- If a bot does not respond in a channel, check which alias and version the channel uses.[^aws-lex]

## Amazon Kendra

Kendra is semantic enterprise search: connectors crawl SharePoint, S3, databases, and other repositories into an index (GenAI Enterprise, Basic Enterprise, or Basic Developer edition), and queries return answers, snippets, or documents. It is closed to new customers; AWS recommends Amazon Bedrock Knowledge Bases for similar needs. For existing indexes, apply access control lists so results respect document permissions, and watch data source sync jobs.[^aws-kendra]

## Related

- [Machine learning](machine-learning.md): SageMaker AI for models you train yourself.
- [Application integration](application-integration.md): Amazon Connect, which uses Lex for self-service.
- [Domain index](index.md)

[^aws-comprehend]: [Amazon Comprehend - Runbook & Reference](../../sources/aws-comprehend.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/comprehend/README.md)
[^aws-rekognition]: [Amazon Rekognition - Runbook & Reference](../../sources/aws-rekognition.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/rekognition/README.md)
[^aws-polly]: [Amazon Polly - Runbook & Reference](../../sources/aws-polly.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/polly/README.md)
[^aws-transcribe]: [Amazon Transcribe - Runbook & Reference](../../sources/aws-transcribe.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/transcribe/README.md)
[^aws-translate]: [Amazon Translate - Runbook & Reference](../../sources/aws-translate.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/translate/README.md)
[^aws-lex]: [Amazon Lex - Runbook & Reference](../../sources/aws-lex.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/lex/README.md)
[^aws-kendra]: [Amazon Kendra - Runbook & Reference](../../sources/aws-kendra.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/kendra/README.md)
