# AWS SDKs and Tools - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS SDKs are language-specific libraries for calling AWS service APIs from your application code: Python (boto3), Java, JavaScript (v3), Go, .NET, Ruby, PHP, C++, and more. SDKs handle request signing, retries, and error mapping. The AWS SDKs and Tools Reference Guide documents the shared configuration, credentials, and maintenance policies across all SDKs and tools.

## Key concepts

- **Credentials resolution**: the same chain as the CLI - env vars, shared config/credentials files, IAM roles, SSO, container credentials.
- **Signature Version 4**: SDKs sign every request with your credentials; temporary credentials from STS are supported.
- **Retries and timeouts**: SDKs retry transient failures by default; configure retry mode (`standard`, `adaptive`, `legacy`) per SDK.
- **Identity providers**: EC2 instance roles, EKS IRSA, ECS task roles, Lambda execution roles, and IAM Identity Center SSO.
- **AWS Common Runtime (CRT)**: shared libraries that provide HTTP/2, event streams, and retry/checksum implementations to several SDKs.
- **Maintenance policy**: AWS maintains SDK major versions with defined support windows; upgrade before end of support.

## Common setup (shared config)

```ini
# ~/.aws/config
[default]
region = us-east-1
output = json

[profile dev]
role_arn = arn:aws:iam::123456789012:role/Developer
source_profile = default

[profile sso-dev]
sso_session = my-sso
sso_account_id = 123456789012
sso_role_name = AdministratorAccess
region = ap-southeast-1

[sso-session my-sso]
sso_start_url = https://example.awsapps.com/start
sso_region = us-east-1
```

```bash
# Environment variables
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...        # only for temporary credentials
export AWS_DEFAULT_REGION=us-east-1
```

## Best practices

- Prefer IAM roles over static keys: EC2 instance profiles, EKS IRSA, ECS/Lambda execution roles, or SSO.
- Use short-lived STS credentials where static keys are unavoidable (CI/CD secrets managers).
- Set timeouts, retry mode, and max retries explicitly for latency-sensitive paths.
- Enable SDK logging/telemetry only as needed; never log credentials or signed payloads.
- Pin SDK versions and track the maintenance policy; test upgrades in staging.
- Use paginators/waiters provided by the SDK instead of hand-rolled polling.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Credentials not found in code | Check env vars, shared files, and role configuration; verify the resolution order. |
| Intermittent failures | Configure retry mode and exponential backoff; check throttling and quotas. |
| Clock skew / signature errors | Verify system time is synchronized (NTP). |
| Regional endpoints wrong | Set region in config/credential chain or per client. |
| Deprecated SDK APIs | Follow the SDK maintenance policy and migrate to current major versions. |

## Limits

SDKs have no service quotas; service APIs and IAM policies define what your code can do. See the Service Quotas console for service-specific values.

## Official references

- [AWS SDKs and Tools Reference Guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html)
- [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Tools to Build on AWS](https://aws.amazon.com/developer/tools/)
