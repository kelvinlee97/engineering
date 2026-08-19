# Amazon Translate - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Translate is a text translation service using advanced machine learning for high-quality, on-demand translation. You can translate unstructured text, translate documents stored in S3, or integrate translation into applications that work in multiple languages. There are no contracts or minimum commitments; you pay per character translated.

## Key concepts

- **Real-time translation**: `translate-text` API for small text units (single sentences, UI strings) with low latency.
- **Batch translation**: translate documents (HTML, DOCX, XLSX, PPTX, TXT) stored in S3 with a translation job; results are written to S3.
- **Languages**: many supported languages and language codes; see the supported languages table for details.
- **Customization**: custom terminology and parallel data to control domain-specific translations.
- **Active custom translation (ACT)**: train a custom translation model with parallel data for higher accuracy in your domain.
- **Integrations**: combine with Comprehend (analyze translated text), Transcribe (subtitles/captioning), Polly (speak translated content), Lambda, and Glue.
- **Use cases**: multilingual user experiences, translation of support/knowledge-base content, eDiscovery search across languages, social media/news analysis.

## Common operations (AWS CLI)

```bash
# Real-time translation
aws translate translate-text --source-language-code en \
  --target-language-code zh --text "Welcome to our platform"

# Batch translation of documents in S3
aws translate start-text-translation-job --job-name docs-zh \
  --data-role-arn arn:aws:iam::123456789012:role/translate-role \
  --input-data-config '{"S3Uri":"s3://bucket/in/"}' \
  --output-data-config '{"S3Uri":"s3://bucket/out/"}' \
  --source-language-code en --target-language-codes zh
aws translate describe-text-translation-job --job-id <job-id>

# Custom terminology
aws translate import-terminology --name product-terms \
  --merge-strategy OVERWRITE --terminology-data file://terms.json \
  --language-code en
```

## Best practices

- Use real-time API for interactive/UI text; use batch jobs for document repositories.
- Import custom terminology for product names and brand language; use parallel data/ACT for domain accuracy.
- Validate translated output with human review for customer-facing content.
- Combine with Comprehend for sentiment/entity analysis of multilingual text and Polly for audio.
- Secure S3 buckets with IAM roles and KMS encryption; monitor jobs with CloudWatch.
- Track cost by volume: review translated character volume per workload.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Translation fails | Check language codes, text length limits, and API quota. |
| Terminology not applied | Confirm the terminology was imported for the source language and the job/API uses it. |
| Batch job failed | Verify S3 paths, IAM role permissions, and supported document types. |
| Accuracy issues | Add parallel data and retrain an ACT model; use terminology for recurring terms. |
| Unsupported language pair | Check the supported languages table for the pair you need. |

## Limits

Text length per request, batch job sizes, terminologies per account, and API request rates have quotas. See the Amazon Translate endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Translate?](https://docs.aws.amazon.com/translate/latest/dg/what-is.html)
- [Amazon Translate endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/translate.html)
- [Amazon Translate pricing](https://aws.amazon.com/translate/pricing/)
- [AWS CLI: translate commands](https://docs.aws.amazon.com/cli/latest/reference/translate/)
