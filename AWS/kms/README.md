# AWS KMS - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Key Management Service (AWS KMS) lets you create and control the keys used to encrypt and sign your data. KMS keys are protected by FIPS 140-3 Security Level 3 validated hardware security modules (HSMs) and never leave the service unencrypted.

## Key concepts

- **KMS keys**: symmetric and asymmetric keys, plus HMAC keys; created, managed, used, and deleted inside KMS.
- **Key policies and grants**: control who can use and manage a key.
- **Aliases**: friendly names (`alias/my-key`) that map to a key; applications should reference aliases.
- **Rotation**: automatic annual rotation for symmetric keys; on-demand rotation for asymmetric and HMAC keys.
- **Data keys and envelope encryption**: `GenerateDataKey` returns a plaintext data key plus an encrypted copy; encrypt data locally with the data key.
- **Encryption contexts**: additional authenticated data bound to a cryptographic operation.
- **Integration**: SSE-KMS for S3, EBS, RDS, and many other services.

## Common operations (AWS CLI)

```bash
# Create a key and alias
aws kms create-key --description "app encryption key"
aws kms create-alias --alias-name alias/my-key --target-key-id <key-id>

# Encrypt / decrypt (binary input via fileb://)
aws kms encrypt --key-id alias/my-key --plaintext fileb://secret.bin \
  --encryption-context env=prod --output text --query CiphertextBlob > secret.enc
aws kms decrypt --ciphertext-blob fileb://secret.enc \
  --encryption-context env=prod --output text --query Plaintext > secret.bin

# Envelope encryption with data keys
aws kms generate-data-key --key-id alias/my-key --key-spec AES_256 \
  --output json > data-key.json

# Rotation and deletion
aws kms enable-key-rotation --key-id <key-id>
aws kms schedule-key-deletion --key-id <key-id> --pending-window-in-days 7

# Audit
aws kms list-keys
aws kms describe-key --key-id alias/my-key
```

## Best practices

- Use **envelope encryption** with data keys for large or local data; never encrypt large payloads directly with KMS.
- Reference keys by **alias** so rotation doesn't break applications.
- Give **least-privilege** key policies/grants; separate keys per environment and team.
- Enable **rotation** and use **encryption contexts** to bind ciphertext to its purpose.
- Audit all key use with **CloudTrail**; monitor for unexpected `kms:Decrypt` calls.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| `AccessDenied` on `kms:Decrypt` | Check key policy and grants; verify the caller's IAM permissions. |
| `InvalidCiphertextBlob` | Confirm the correct key and encryption context were used; ciphertext is region- and key-bound. |
| Key deleted | Keys are unrecoverable after the pending deletion window; restore from backups or re-encrypt. |
| Throttling | KMS request quotas are low by design; retry with exponential backoff or reduce call volume. |
| Key not found | Verify the alias/key ARN and Region; aliases and keys are regional. |

## Limits

Request quotas apply per second per Region (for example, 5,500 symmetric encrypt/decrypt requests per second by default, adjustable). See Service Quotas.

## Official references

- [AWS Key Management Service - KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [AWS KMS pricing](https://aws.amazon.com/kms/pricing/)
- [AWS CLI: kms commands](https://docs.aws.amazon.com/cli/latest/reference/kms/)
