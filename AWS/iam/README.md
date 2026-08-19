# AWS IAM - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-18

## Overview

AWS Identity and Access Management (IAM) controls authentication (who is signed in) and authorization (who has permissions) for AWS resources. IAM, IAM Identity Center, and AWS STS are included with your AWS account at no additional charge. IAM is eventually consistent.

## Core concepts

- **Root user**: the initial account identity with full access; do not use it for everyday tasks.
- **IAM users, groups, roles**: identities you create to grant access to people and workloads. Roles provide temporary credentials.
- **Policies**: JSON documents attached to identities or resources that define permissions.
- **Identity providers and federation**: human users should sign in through an identity provider (AWS recommends IAM Identity Center for centralized access).
- **AWS STS**: issues temporary credentials (for example, `AssumeRole`).
- **Permissions boundaries**: cap the maximum permissions an identity-based policy can grant.
- **Organization guardrails**: AWS Organizations service control policies (SCPs) and resource control policies (RCPs) set cross-account boundaries; they do not grant permissions by themselves.

## Common operations (AWS CLI)

```bash
# Who am I
aws sts get-caller-identity

# Users and groups
aws iam create-user --user-name alice
aws iam create-group --group-name developers
aws iam add-user-to-group --user-name alice --group-name developers

# Policies
aws iam create-policy --policy-name s3-read-only --policy-document file://policy.json
aws iam attach-user-policy --user-name alice --policy-arn arn:aws:iam::123456789012:policy/s3-read-only

# Roles: create with a trust policy, then attach permissions
aws iam create-role --role-name app-role --assume-role-policy-document file://trust.json
aws iam attach-role-policy --role-name app-role --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Assume a role and list rotated access keys
aws sts assume-role --role-arn arn:aws:iam::123456789012:role/app-role --role-session-name my-session
aws iam list-access-keys --user-name alice
```

## Security best practices

- Require **temporary credentials**: federated sign-in (IAM Identity Center) for human users, IAM roles for workloads (EC2 instance profiles, Lambda execution roles, ECS/EKS task roles).
- Require **MFA** for root users and any long-term credentials.
- Protect root user credentials; never use the root user for routine work.
- Apply **least privilege**; start from AWS managed policies and move to customer managed policies.
- Use **IAM Access Analyzer** to generate least-privilege policies from CloudTrail activity, validate policies, and detect public/cross-account access.
- Review and remove unused users, roles, policies, and access keys (use last accessed information).
- Use **conditions** (for example, require TLS) and **permissions boundaries** when delegating permission management.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| `AccessDenied` | Check identity policy, resource policy, SCP/RCP, permission boundary, and any session policy; IAM is eventually consistent, so retry after propagation. |
| `AssumeRole` fails | Verify the role trust policy allows the principal; check external ID and that the requested session duration does not exceed the role's maximum (up to 12 hours). |
| Cannot delete a user/role | Remove attached and inline policies, access keys, and memberships first. |
| Access key rotation | Use `aws iam list-access-keys` and last accessed information to deactivate and delete unused keys. |

## Quotas (per account, defaults)

| Resource | Default quota |
|----------|---------------|
| Roles | 1,000 |
| Customer managed policies | 1,500 |
| Groups | 300 |
| Instance profiles | 1,000 |
| Managed policies per role / user | 20 / 10 |
| Managed policy size | 6,144 characters |
| Inline policy size (user / role / group) | 2,048 / 10,240 / 5,120 characters |
| Role trust policy size | 2,048 characters (max 8,192) |
| Maximum role session duration | 12 hours |
| STS requests | 600 per second per account per Region |

See Service Quotas for adjustable quotas and current values.

## Official references

- [What is IAM? - IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM and AWS STS quotas](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html)
- [AWS CLI: iam commands](https://docs.aws.amazon.com/cli/latest/reference/iam/)
