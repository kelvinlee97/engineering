# AWS CLI - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

The AWS Command Line Interface (AWS CLI) is an open source tool for interacting with AWS services from your shell. Version 2 is the current major version and supports all the latest features; it is installed with the official bundled installer. The CLI exposes the same service APIs as the console, plus higher-level customizations for several services.

## Key concepts

- **Credentials chain**: the CLI resolves credentials from CLI options, environment variables, shared `~/.aws/credentials`, IAM roles (EC2/EKS/ECS), SSO, and container roles, in order.
- **Profiles**: named credential/region sets in `~/.aws/config` and `~/.aws/credentials`; select with `--profile` or `AWS_PROFILE`.
- **Regions and output**: set default region and output (`json`, `yaml`, `text`, `table`) with `aws configure`.
- **SSO**: `aws configure sso` sets up IAM Identity Center sessions; `aws sso login` refreshes them.
- **Query and filtering**: `--query` (JMESPath) and `--output` shape command results for scripting.
- **Return codes and dry-run**: nonzero exit codes indicate failures; `--dry-run` validates permissions without making changes where supported.

## Common operations (AWS CLI)

```bash
# Install (macOS/Linux bundled installer)
curl "https://awscli.amazonaws.com/AWSIV2.pkg" -o "AWSIV2.pkg"   # macOS
sudo installer -pkg AWSIV2.pkg -target /

# Configure
aws configure
aws configure set default.region us-east-1
aws configure set default.output json

# Profiles and SSO
aws configure --profile dev
aws configure sso --profile dev-sso
aws sso login --profile dev-sso

# Verify identity and permissions
aws sts get-caller-identity
aws iam get-user

# Common patterns
aws s3 ls --profile dev
aws ec2 describe-instances --region ap-southeast-1 \
  --query 'Reservations[].Instances[].{Id:InstanceId,State:State.Name}' --output table
aws s3 cp file.txt s3://bucket/ --dryrun
```

## Best practices

- Never put long-term access keys in scripts or source code; use IAM roles or SSO.
- Use named profiles per environment/account and separate roles with least privilege.
- Pin and upgrade the CLI: v1 is in maintenance and lacks v2 features; use the official installer.
- Use `--query` and `--output` to keep scripts deterministic; parse with `jq` or JSON where possible.
- Enable CloudTrail to audit CLI-driven changes; use `--dry-run` before destructive operations.
- Prefer infrastructure as code (CloudFormation/CDK/Terraform) over ad-hoc CLI changes for lasting resources.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| `Unable to locate credentials` | Configure credentials/profile or set environment variables; check the credentials chain order. |
| `AccessDenied` | Verify the IAM policy and that you're using the intended profile/role. |
| Expired SSO session | Run `aws sso login --profile <profile>` again. |
| Wrong region results | Set `--region` explicitly or fix the profile default. |
| JSON parse errors in scripts | Validate `--query` syntax (JMESPath) and use `--output json`. |

## Limits

The CLI itself has no service quotas; API rate limits and quotas apply per service. See the Service Quotas console for service-specific values.

## Official references

- [What is the AWS Command Line Interface?](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [AWS CLI command reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS SDKs and Tools Reference Guide](https://docs.aws.amazon.com/sdkref/latest/guide/overview.html)
