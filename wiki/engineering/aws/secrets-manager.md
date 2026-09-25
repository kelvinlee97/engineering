---
type: Service
title: AWS Secrets Manager
description: AWS's service for storing versioned secrets that applications fetch at runtime, with scheduled rotation through Lambda.
tags: [aws, security, secrets]
sources:
  - id: aws-secrets-manager
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/secrets-manager/README.md
    title: "AWS Secrets Manager - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

Secrets Manager stores versioned secret values behind an API call, so applications fetch credentials at runtime instead of hard-coding them, and a Lambda function can rotate them on a schedule without code changes.[^aws-secrets-manager]

## Concepts

- Versions carry staging labels (`AWSCURRENT`, `AWSPREVIOUS`).[^aws-secrets-manager]
- Encryption with the AWS managed key `aws/secretsmanager` or a customer KMS key; see [envelope encryption](envelope-encryption.md).[^aws-secrets-manager]
- Service boundaries it recommends: AWS credentials in IAM, encryption keys in KMS, SSH keys through EC2 Instance Connect, certificates in ACM, and non-secret configuration in SSM Parameter Store.[^aws-secrets-manager]

## Practices

- Rotate database and application credentials automatically every 30 to 90 days.[^aws-secrets-manager]
- Grant `secretsmanager:GetSecretValue` only on specific secret ARNs.[^aws-secrets-manager]
- Never store secrets in plain-text config files or environment variables.[^aws-secrets-manager]
- Keep the deletion recovery window of 7 to 30 days unless the secret is disposable.[^aws-secrets-manager]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Rotation fails | Rotation Lambda logs, permissions, rotation config |
| `GetSecretValue` denied | Caller's IAM policy and the secret's resource policy |
| KMS decryption errors | The key policy grants `kms:Decrypt` to the caller |
| Deleted by accident | `restore-secret` within the recovery window |

As tabled in the note.[^aws-secrets-manager]

## Related

- Source: [AWS Secrets Manager - Runbook & Reference](../../sources/aws-secrets-manager.md)

[^aws-secrets-manager]: AWS Secrets Manager - Runbook & Reference
