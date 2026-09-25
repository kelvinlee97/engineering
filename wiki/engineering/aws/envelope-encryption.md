---
type: Concept
title: Envelope encryption
description: Encrypt data locally with a data key and store only an encrypted copy of that key, so the key service never handles bulk data.
tags: [aws, security, encryption]
sources:
  - id: aws-kms
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/kms/README.md
    title: "AWS KMS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-secrets-manager
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/secrets-manager/README.md
    title: "AWS Secrets Manager - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

In envelope encryption, KMS never sees your bulk data, only the small data key that protects it. `GenerateDataKey` returns a plaintext data key and an encrypted copy; you encrypt the data locally, discard the plaintext key, and store the encrypted key beside the ciphertext. To read it, you ask KMS to decrypt the data key.[^aws-kms]

```mermaid
flowchart LR
    accTitle: Envelope encryption with KMS
    accDescr: The application asks KMS for a data key and receives a plaintext copy, used to encrypt data locally and then discarded, and an encrypted copy stored with the ciphertext and sent back to KMS for decryption when needed.
    App[Application] -->|GenerateDataKey| K[KMS key]
    K --> P[Plaintext data key, used then discarded]
    K --> E[Encrypted data key, stored with the data]
    P --> D[Data encrypted locally]
```

## Why and when

- Never encrypt large payloads directly with KMS; KMS request quotas are low by design.[^aws-kms]
- Bind ciphertext to its purpose with an encryption context, and reference keys by alias so rotation is transparent.[^aws-kms]
- Services apply it for you: Secrets Manager encrypts secrets with `aws/secretsmanager` or a customer KMS key, and a decryption failure there usually means the key policy lacks `kms:Decrypt` for the caller.[^aws-secrets-manager]

- [AWS KMS](kms.md)

## Related

- Source: [AWS KMS - Runbook & Reference](../../sources/aws-kms.md)
- Source: [AWS Secrets Manager - Runbook & Reference](../../sources/aws-secrets-manager.md)

[^aws-kms]: AWS KMS - Runbook & Reference
[^aws-secrets-manager]: AWS Secrets Manager - Runbook & Reference
