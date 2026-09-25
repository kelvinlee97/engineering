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
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services expose pre-trained models as APIs: call them with text, images, or audio and get results back without training anything.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Amazon Comprehend](#amazon-comprehend) | Comprehend is a set of pre-trained NLP detectors (entities, sentiment, PII, syntax...) plus an optional AutoML layer on top |
| [Amazon Rekognition](#amazon-rekognition) | Rekognition analyzes images synchronously in a single API call, but video always runs as an asynchronous job that reports completion through SNS |
| [Amazon Polly](#amazon-polly) | Polly converts text to speech synchronously for short requests and asynchronously for long-form content, with SSML and lexicons layered on top to control exactly how the chosen voice sounds |
| [Amazon Transcribe](#amazon-transcribe) | Amazon Transcribe is an automatic speech recognition (ASR) service that converts audio to text using machine learning |
| [Amazon Translate](#amazon-translate) | Amazon Translate is a text translation service using advanced machine learning for high-quality, on-demand translation |
| [Amazon Lex](#amazon-lex) | Amazon Lex V2 is a service for building conversational interfaces (chatbots) using voice and text |
| [Amazon Kendra](#amazon-kendra) | Amazon Kendra is a managed intelligent search service that uses natural language processing and semantic ranking to retrieve answers from your documents, going beyond keyword search |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Amazon Comprehend

Comprehend is a set of pre-trained NLP detectors (entities, sentiment, PII, syntax...) plus an optional AutoML layer on top: reach for the `Detect*` APIs first, and only build a custom classifier or entity recognizer when your categories or terms are specific enough that the pre-trained models can't name them. Amazon Comprehend uses natural language processing (NLP) to extract insights from documents: entities, key phrases, language, sentiment, syntax, and PII. You can run real-time analysis for small workloads or asynchronous jobs for large document sets, and train custom models for classification and entity recognition.

Key points:

- Insights: pre-trained model outputs covering entities (people, places, organizations), key phrases, PII, dominant language, sentiment (positive/neutral/negative/mixed), targeted sentiment (sentiment per entity), and syntax (parts of speech).
- Real-time vs. asynchronous: `Detect*` APIs for small workloads; analysis jobs for large document sets.
- Custom classification: AutoML-built classifiers that organize documents into your own categories.
- Custom entity recognition: recognizers trained to detect your specific terms and phrases.
- Flywheels: orchestrate training and evaluation of new custom model versions over time.

Practices:

- Store documents in S3 and use KMS encryption for jobs and volumes; scope IAM roles to the buckets used.
- Use real-time APIs only for interactive workloads; use jobs for bulk analysis to control cost.
- For domain-specific text, train custom classifiers/recognizers with representative labeled data.

| Symptom | Check |
| --- | --- |
| Job fails | Check S3 input path, IAM role permissions, and document format (UTF-8). |
| Language not detected | Verify the feature supports the language; dominant language covers more languages than other features. |
| Custom model accuracy low | Add more representative labeled data and retrain/evaluate with a flywheel. |
| Endpoint cost high | Delete idle custom model endpoints; use jobs for batch workloads. |

Document size, batch sizes, custom model training quotas, and API request rates have limits. See the Amazon Comprehend endpoints and quotas page and Service Quotas console for current values.[^aws-comprehend]


## Amazon Rekognition

Rekognition analyzes images synchronously in a single API call, but video always runs as an asynchronous job that reports completion through SNS: both call into the same underlying detection features (labels, text, faces, moderation). Amazon Rekognition is a cloud-based image and video analysis service powered by deep learning. With simple APIs you can detect objects, scenes, text, faces, celebrities, and unsafe content in images and videos stored in S3, without ML expertise. It is HIPAA-eligible and uses pay-as-you-go pricing.

Key points:

- Image analysis: object/scene/concept detection, text detection, unsafe content moderation, celebrity recognition, facial analysis, image properties (quality, color, sharpness), and Custom Labels classifiers.
- Video analysis: object/scene/concept detection, text detection, people pathing, face analysis, celebrity recognition, unsafe content, video segmentation, and face liveness.
- Face collections: containers for indexing and searching faces for facial search and identity verification.
- Face Liveness: fully managed feature that verifies a live user is physically present, detecting spoofs (photos, videos, 3D masks, deepfakes).
- Content moderation: hierarchical labels with confidence scores for filtering user-generated content; customizable with adapters.

Practices:

- Store media in S3 with lifecycle policies; analyze in place with IAM-scoped roles.
- Use content moderation with adapters for user-generated content platforms; set confidence thresholds.
- Use Face Liveness for identity verification to deter spoofing; follow applicable privacy laws and get consent where required.

| Symptom | Check |
| --- | --- |
| API errors on S3 image | Check bucket permissions, object key, and Region. |
| No faces found | Verify image quality/orientation and face size requirements. |
| Video job stuck | Check the SNS topic permissions and job status; re-submit if needed. |
| Custom Labels accuracy low | Add more labeled training images per category. |

Image size, face collections per account, video duration, and API request rates have quotas. See the Amazon Rekognition endpoints and quotas page and Service Quotas console for current values.[^aws-rekognition]


## Amazon Polly

Polly converts text to speech synchronously for short requests and asynchronously for long-form content, with SSML and lexicons layered on top to control exactly how the chosen voice sounds. Amazon Polly is a cloud service that converts text into lifelike speech (text-to-speech, TTS). It supports multiple languages and voices, including generative, long-form, neural, and standard voices. You pay only for the text you synthesize, and you can cache and replay generated speech at no additional cost. Polly is HIPAA-eligible and PCI DSS certified for regulated workloads.

Key points:

- Voices: generative (most natural, supports long-form narration), neural, and standard voices across many languages; neural TTS includes a Newscaster speaking style for news narration.
- Speech marks: timestamps/word boundaries for synchronizing speech with content (for example, karaoke-style apps).
- SSML: Speech Synthesis Markup Language for controlling pronunciation, pauses, emphasis, and speaking rate.
- Lexicons: custom pronunciation dictionaries (for example, brand names and acronyms).
- Synthesis: synchronous `synthesize-speech` for short text, asynchronous tasks (`start-speech-synthesis-task`) for longer text; supports MP3, OGG, and PCM formats.

Practices:

- Choose neural or generative voices for customer-facing audio; standard voices only for low-cost needs.
- Use SSML and lexicons to control pronunciation of product names and acronyms.
- Cache generated audio (S3/CloudFront) to avoid re-synthesizing the same content.

| Symptom | Check |
| --- | --- |
| Synthesize fails | Check the voice ID, language, text length, and output format. |
| Pronunciation wrong | Add a lexicon or use SSML phoneme tags. |
| Long text error | Use `start-speech-synthesis-task` instead of synchronous synthesis. |
| Audio not generated for task | Verify the S3 bucket policy and task status; check output path. |

Characters per request, concurrent synthesis requests, lexicons per account, and task quotas apply. See the Amazon Polly endpoints and quotas page and Service Quotas console for current values.[^aws-polly]


## Amazon Transcribe

Amazon Transcribe is an automatic speech recognition (ASR) service that converts audio to text using machine learning. You can transcribe media in real time (streaming) or in batch from S3, with features for language customization, content filtering, speaker separation, and multi-channel audio. You pay per second of transcribed audio; HIPAA eligibility applies with a BAA.

Key points:

- Batch transcription: transcribe audio files stored in S3 as a job; results are written to S3 (JSON, VTT, SRT).
- Streaming transcription: real-time speech-to-text with partial and final results; supports websocket/HTTP2 and SDKs.
- Language customization: custom language models, custom vocabularies, and vocabulary filters to improve accuracy for your domain.
- Content filtering: PII redaction and vocabulary filtering for audience-appropriate or privacy-safe output.
- Speaker diarization: partition speech by speaker for meetings and interviews.

Practices:

- Store audio in S3 with KMS encryption; grant Transcribe access with a scoped IAM role.
- Use custom vocabularies/language models for domain terms and accents to improve accuracy.
- Enable PII redaction for call recordings and customer-facing content; verify output.

| Symptom | Check |
| --- | --- |
| Job fails | Check the audio format/codec, S3 permissions, and media file URI. |
| Accuracy poor | Add custom vocabularies or a custom language model for the domain. |
| PII not redacted | Confirm redaction settings and language support; verify output type (redacted vs redacted_and_unredacted). |
| Streaming errors | Check audio encoding, sample rate, and SDK/websocket configuration. |

Transcription job quotas, media duration, concurrent jobs, and API request rates apply; some quotas are adjustable. See the Amazon Transcribe endpoints and quotas page and Service Quotas console for current values.[^aws-transcribe]


## Amazon Translate

Amazon Translate is a text translation service using advanced machine learning for high-quality, on-demand translation. You can translate unstructured text, translate documents stored in S3, or integrate translation into applications that work in multiple languages. There are no contracts or minimum commitments; you pay per character translated.

Key points:

- Real-time translation: `translate-text` API for small text units (single sentences, UI strings) with low latency.
- Batch translation: translate documents (HTML, DOCX, XLSX, PPTX, TXT) stored in S3 with a translation job; results are written to S3.
- Languages: many supported languages and language codes; see the supported languages table for details.
- Customization: custom terminology and parallel data to control domain-specific translations.
- Active custom translation (ACT): train a custom translation model with parallel data for higher accuracy in your domain.

Practices:

- Use real-time API for interactive/UI text; use batch jobs for document repositories.
- Import custom terminology for product names and brand language; use parallel data/ACT for domain accuracy.
- Validate translated output with human review for customer-facing content.

| Symptom | Check |
| --- | --- |
| Translation fails | Check language codes, text length limits, and API quota. |
| Terminology not applied | Confirm the terminology was imported for the source language and the job/API uses it. |
| Batch job failed | Verify S3 paths, IAM role permissions, and supported document types. |
| Accuracy issues | Add parallel data and retrain an ACT model; use terminology for recurring terms. |

Text length per request, batch job sizes, terminologies per account, and API request rates have quotas. See the Amazon Translate endpoints and quotas page and Service Quotas console for current values.[^aws-translate]


## Amazon Lex

Amazon Lex V2 is a service for building conversational interfaces (chatbots) using voice and text. It provides natural language understanding (NLU) and automatic speech recognition (ASR), so developers can build, test, and publish bots that understand user intent and fulfill tasks, without deep learning expertise. You pay only for the text or speech requests made.

Key points:

- Bot: the conversational application; you define the conversation flow in the console or via APIs.
- Intent: what the user wants to do (for example, BookAppointment); intents have sample utterances and slots.
- Slot and slot type: a variable the bot collects (for example, date, city); slot types can be built-in or custom.
- Fulfillment: Lambda functions (or conditional branching) that complete the user's request.
- Conditional branching: control conversation flow without writing Lambda code (for bots created after August 17, 2022).

Practices:

- Start with a few high-value intents and sample utterances; iterate based on conversation logs.
- Use slots with validation and Lambda fulfillment for business logic; use conditional branching for simple flows.
- Monitor bot analytics and CloudWatch logs for fallback/confusion; improve utterances and add edge cases.

| Symptom | Check |
| --- | --- |
| Intent not recognized | Add more sample utterances and check the locale; review conversation logs. |
| Slot not collected | Validate slot prompting/message configuration and slot types. |
| Fulfillment fails | Check the Lambda function, IAM permissions, and timeout settings. |
| Bot not responding in channel | Verify the alias/version deployed to the channel and channel credentials. |

Bots, intents, slots, versions, and API request rates per account have quotas. See the Amazon Lex endpoints and quotas page and Service Quotas console for current values.[^aws-lex]


## Amazon Kendra

Amazon Kendra is a managed intelligent search service that uses natural language processing and semantic ranking to retrieve answers from your documents, going beyond keyword search. Note: Amazon Kendra is no longer open to new customers; for similar capabilities, AWS recommends Amazon Bedrock Knowledge Bases.

Key points:

- Index: the searchable store of documents; Kendra offers GenAI Enterprise, Basic Enterprise, and Basic Developer edition indices.
- Data sources: connectors to repositories such as SharePoint, S3, and databases for crawling and syncing documents.
- Semantic search: understands the context of questions and returns the most relevant answers, snippets, or documents.
- Query types: factoid questions (single-word/phrase answers from FAQs/documents), descriptive questions, and keyword/natural-language questions.
- Intelligent ranking: re-rank results from another search service using Kendra semantic capabilities.

Practices:

- Choose the GenAI Enterprise index for production RAG and enterprise search workloads.
- Curate metadata and FAQs to improve answer quality; use access control lists for document security.
- Sync data sources on a schedule and monitor sync job status.

| Symptom | Check |
| --- | --- |
| No results | Check index status, data source sync, and query/access filter configuration. |
| Sync job failed | Review the data source configuration, credentials, and document format support. |
| Answers inaccurate | Improve metadata, FAQs, and document quality; re-index after changes. |
| Search returns restricted docs | Verify ACL/user-group filtering is configured in the index. |

Indices per account, document and metadata limits, and data source sync quotas apply. See the Amazon Kendra endpoints and quotas page and Service Quotas console for current values.[^aws-kendra]


## Related

- [AWS machine learning platforms](machine-learning.md)
- [Domain index](index.md)

[^aws-comprehend]: [Amazon Comprehend - Runbook & Reference](../../sources/aws-comprehend.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/comprehend/README.md)
[^aws-rekognition]: [Amazon Rekognition - Runbook & Reference](../../sources/aws-rekognition.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/rekognition/README.md)
[^aws-polly]: [Amazon Polly - Runbook & Reference](../../sources/aws-polly.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/polly/README.md)
[^aws-transcribe]: [Amazon Transcribe - Runbook & Reference](../../sources/aws-transcribe.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/transcribe/README.md)
[^aws-translate]: [Amazon Translate - Runbook & Reference](../../sources/aws-translate.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/translate/README.md)
[^aws-lex]: [Amazon Lex - Runbook & Reference](../../sources/aws-lex.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/lex/README.md)
[^aws-kendra]: [Amazon Kendra - Runbook & Reference](../../sources/aws-kendra.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/kendra/README.md)
