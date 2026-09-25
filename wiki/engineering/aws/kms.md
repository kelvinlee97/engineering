---
type: Service
title: AWS KMS
description: AWS's managed service for creating and controlling encryption and signing keys, used through envelope encryption.
tags: [aws, security, encryption]
sources:
  - id: aws-kms
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/kms/README.md
    title: "AWS KMS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

AWS Key Management Service (KMS) creates and controls keys used to encrypt and sign data. Keys are protected by FIPS 140-3 Security Level 3 validated HSMs and never leave the service unencrypted.[^aws-kms] The core pattern is [envelope encryption](envelope-encryption.md).

## Concepts

- Symmetric, asymmetric, and HMAC keys, controlled by key policies and grants.[^aws-kms]
- Aliases such as `alias/my-key`; applications should reference aliases so rotation does not break them.[^aws-kms]
- Automatic annual rotation for symmetric keys; on-demand rotation for asymmetric and HMAC keys.[^aws-kms]
- Encryption contexts: additional authenticated data bound to an operation.[^aws-kms]
- Integrated as SSE-KMS in S3, EBS, RDS, and many other services.[^aws-kms]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `AccessDenied` on `kms:Decrypt` | Key policy, grants, caller's IAM permissions |
| `InvalidCiphertextBlob` | Right key and encryption context; ciphertext is Region- and key-bound |
| Key deleted | Unrecoverable after the pending window; restore or re-encrypt |
| Throttling | Quotas are low by design; back off or reduce calls |

As tabled in the note.[^aws-kms] The default quota is 5,500 symmetric encrypt/decrypt requests per second per Region, adjustable.[^aws-kms]

## Related

- Source: [AWS KMS - Runbook & Reference](../../sources/aws-kms.md)

[^aws-kms]: AWS KMS - Runbook & Reference
