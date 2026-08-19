# AWS Secrets Manager - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Secrets Manager helps you manage, retrieve, and rotate database credentials, application credentials, OAuth tokens, API keys, and other secrets across their lifecycles. Secrets are retrieved at runtime instead of being hard-coded in application code.

## Key concepts

- **Secrets**: versioned secret values with staging labels (`AWSCURRENT`, `AWSPREVIOUS`).
- **Automatic rotation**: scheduled rotation with an AWS Lambda function; long-term secrets become short-term.
- **Encryption**: secrets are encrypted with the AWS managed key `aws/secretsmanager` (free) or a customer KMS key.
- **Recommended service boundaries**: AWS credentials → IAM; encryption keys → KMS; SSH keys → EC2 Instance Connect; certificates → ACM.
- **Auditing**: all API calls are logged to CloudTrail as management events.

## Common operations (AWS CLI)

```bash
# Create and retrieve
aws secretsmanager create-secret --name prod/db-password \
  --secret-string '{"username":"admin","password":"ChangeMe123!"}'
aws secretsmanager get-secret-value --secret-id prod/db-password

# Update a version
aws secretsmanager put-secret-value --secret-id prod/db-password \
  --secret-string '{"username":"admin","password":"NewPass456!"}'

# Rotation
aws secretsmanager rotate-secret --secret-id prod/db-password \
  --rotation-lambda-arn arn:aws:lambda:ap-southeast-1:123456789012:function:rotate-db \
  --rotation-rules AutomaticallyAfterDays=30

# List and describe
aws secretsmanager list-secrets
aws secretsmanager describe-secret --secret-id prod/db-password

# Delete (with recovery window) / restore
aws secretsmanager delete-secret --secret-id prod/db-password --recovery-window-in-days 7
aws secretsmanager restore-secret --secret-id prod/db-password
```

## Best practices

- Enable **automatic rotation** (30-90 days) for database and application credentials.
- Grant **least-privilege IAM** (`secretsmanager:GetSecretValue` scoped to specific secret ARNs).
- Retrieve secrets at runtime with the SDK/CLI; never store them in config files or environment variables in plain text.
- Keep the **deletion recovery window** (7-30 days) unless the secret is disposable.
- Use **multi-Region secret replication** where needed; audit with CloudTrail.
- Use SSM Parameter Store for non-secret configuration; Secrets Manager for secrets.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Rotation fails | Check the rotation Lambda function's logs, permissions, and the secret's rotation config. |
| `GetSecretValue` denied | Verify the caller's IAM policy and any resource policy on the secret. |
| Secret not found | Check the Region, ARN/name, and whether it is still in a deletion recovery window. |
| Deleted by accident | Restore within the recovery window (`restore-secret`); otherwise recreate. |
| KMS decryption errors | Ensure the secret's KMS key policy grants `kms:Decrypt` to the caller. |

## Limits

Secrets per account and rotation configuration have quotas; see the Service Quotas console for current values.

## Official references

- [What is AWS Secrets Manager? - Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [AWS Secrets Manager pricing](https://aws.amazon.com/secrets-manager/pricing/)
- [AWS CLI: secretsmanager commands](https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/)
