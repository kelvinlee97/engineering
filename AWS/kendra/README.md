# Amazon Kendra - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Kendra is a managed intelligent search service that uses natural language processing and semantic ranking to retrieve answers from your documents, going beyond keyword search. Note: Amazon Kendra is no longer open to new customers; for similar capabilities, AWS recommends Amazon Bedrock Knowledge Bases.

## Key concepts

- **Index**: the searchable store of documents; Kendra offers GenAI Enterprise, Basic Enterprise, and Basic Developer edition indices.
- **Data sources**: connectors to repositories such as SharePoint, S3, and databases for crawling and syncing documents.
- **Semantic search**: understands the context of questions and returns the most relevant answers, snippets, or documents.
- **Query types**: factoid questions (single-word/phrase answers from FAQs/documents), descriptive questions, and keyword/natural-language questions.
- **Intelligent ranking**: re-rank results from another search service using Kendra semantic capabilities.
- **GenAI integration**: Kendra GenAI indices can back Amazon Q Business and Amazon Bedrock knowledge bases for retrieval-augmented generation (RAG).
- **Security**: results reflect your organization's access model with user/group filtering; you are responsible for authentication and authorization.

## Common operations (AWS CLI)

```bash
# Create an index and a data source
aws kendra create-index --name corp-search --edition ENTERPRISE_EDITOR \
  --role-arn arn:aws:iam::123456789012:role/kendra-role
aws kendra create-data-source --index-id <index-id> --name s3-docs \
  --type S3 --configuration file://ds-config.json
aws kendra start-data-source-sync-job --id <data-source-id> --index-id <index-id>

# Query the index
aws kendra query --index-id <index-id> --query-text "How do I reset my password?"
aws kendra list-indices
```

## Best practices

- Choose the GenAI Enterprise index for production RAG and enterprise search workloads.
- Curate metadata and FAQs to improve answer quality; use access control lists for document security.
- Sync data sources on a schedule and monitor sync job status.
- Use intelligent ranking to improve an existing search engine without migrating.
- For new generative search use cases, evaluate Amazon Bedrock Knowledge Bases as the current recommended service.
- Budget for provisioned indices: you are charged for provisioned indices even when idle.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No results | Check index status, data source sync, and query/access filter configuration. |
| Sync job failed | Review the data source configuration, credentials, and document format support. |
| Answers inaccurate | Improve metadata, FAQs, and document quality; re-index after changes. |
| Search returns restricted docs | Verify ACL/user-group filtering is configured in the index. |
| Cannot create index | Kendra is closed to new customers; use Amazon Bedrock Knowledge Bases. |

## Limits

Indices per account, document and metadata limits, and data source sync quotas apply. See the Amazon Kendra endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Kendra?](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html)
- [Amazon Kendra endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/kendra.html)
- [Amazon Kendra pricing](https://aws.amazon.com/kendra/pricing/)
- [AWS CLI: kendra commands](https://docs.aws.amazon.com/cli/latest/reference/kendra/)
