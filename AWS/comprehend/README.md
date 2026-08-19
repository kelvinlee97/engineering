# Amazon Comprehend - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Comprehend uses natural language processing (NLP) to extract insights from documents: entities, key phrases, language, sentiment, syntax, and PII. You can run real-time analysis for small workloads or asynchronous jobs for large document sets, and train custom models for classification and entity recognition.

## Key concepts

- **Insights**: pre-trained model outputs — entities (people, places, organizations), key phrases, PII, dominant language, sentiment (positive/neutral/negative/mixed), targeted sentiment (sentiment per entity), and syntax (parts of speech).
- **Real-time vs. asynchronous**: `Detect*` APIs for small workloads; analysis jobs for large document sets.
- **Custom classification**: AutoML-built classifiers that organize documents into your own categories.
- **Custom entity recognition**: recognizers trained to detect your specific terms and phrases.
- **Flywheels**: orchestrate training and evaluation of new custom model versions over time.
- **Topic modeling (document clustering)**: organize a corpus into topics based on word frequency.
- **Input**: UTF-8 text; custom classification/entity recognition also accept image, PDF, and Word files.
- **Security and cost**: output and volume data can be encrypted with your KMS key; pay per analyzed document and custom model training/endpoint usage.

## Common operations (AWS CLI)

```bash
# Real-time analysis
aws comprehend detect-sentiment --text "The service is excellent" \
  --language-code en
aws comprehend detect-entities --text "AWS announced new services in Singapore" \
  --language-code en
aws comprehend detect-pii-entities --text "Contact alice at 123-456-7890" \
  --language-code en

# Async analysis job
aws comprehend start-dominant-language-detection-job \
  --job-name docs-lang --input-data-config S3Uri=s3://bucket/docs \
  --output-data-config S3Uri=s3://bucket/out
aws comprehend list-dominant-language-detection-jobs
```

## Best practices

- Store documents in S3 and use KMS encryption for jobs and volumes; scope IAM roles to the buckets used.
- Use real-time APIs only for interactive workloads; use jobs for bulk analysis to control cost.
- For domain-specific text, train custom classifiers/recognizers with representative labeled data.
- Use flywheels to manage model versions and evaluation rather than retraining ad hoc.
- Redact or mask PII (comprehend PII detection) before storing or publishing text.
- Combine with Firehose, Lambda, and EventBridge for real-time text pipelines.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Job fails | Check S3 input path, IAM role permissions, and document format (UTF-8). |
| Language not detected | Verify the feature supports the language; dominant language covers more languages than other features. |
| Custom model accuracy low | Add more representative labeled data and retrain/evaluate with a flywheel. |
| Endpoint cost high | Delete idle custom model endpoints; use jobs for batch workloads. |
| PII not detected | Confirm the text language is supported and use `detect-pii-entities` with the right language code. |

## Limits

Document size, batch sizes, custom model training quotas, and API request rates have limits. See the Amazon Comprehend endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Comprehend?](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html)
- [Amazon Comprehend endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/comprehend.html)
- [Amazon Comprehend pricing](https://aws.amazon.com/comprehend/pricing/)
- [AWS CLI: comprehend commands](https://docs.aws.amazon.com/cli/latest/reference/comprehend/)
