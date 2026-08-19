# AWS IAM Identity Center - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS IAM Identity Center (successor to AWS Single Sign-On, renamed in July 2022) centrally manages workforce identities and access to AWS accounts and cloud applications. It is the recommended service for multi-account access: you create users/groups or connect an external identity provider, assign permission sets, and users sign in through the access portal.

## Key concepts

- **Instance**: an Identity Center instance; for multi-account access, create the instance in the organization management account so it can manage accounts in AWS Organizations (best practice).
- **Permission set**: a named collection of IAM policies (AWS managed, customer managed, or inline) plus session duration that defines what a user can do in an AWS account; assigned to accounts.
- **Account assignment**: grants a user or group access to an AWS account with a permission set; assign to groups rather than individuals.
- **Access portal**: the end-user URL where users sign in (with MFA) and launch accounts/applications.
- **Identity sources**: Identity Center directory, or an external IdP (Okta, Microsoft Entra ID, etc.) with SCIM automatic provisioning and/or SAML 2.0 federation.
- **Trusted identity propagation**: passes the end-user identity and context from Identity Center to applications (for example, Amazon Q Business) instead of a shared service account.
- **Legacy namespaces**: the service APIs still use `sso`, `sso-admin`, and `identitystore` namespaces; CLI commands for Identity Center are `aws sso-admin ...` and `aws identitystore ...`, and CLI login uses `aws sso login`.

## Common operations (AWS CLI)

```bash
# List instances and create a permission set
aws sso-admin list-instances
aws sso-admin create-permission-set \
  --instance-arn <instance-arn> --name PowerUser \
  --session-duration PT2H

# Attach a managed policy and assign access
aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn <instance-arn> --permission-set-arn <ps-arn> \
  --managed-policy-arn arn:aws:iam::aws:policy/PowerUserAccess
aws sso-admin create-account-assignment \
  --instance-arn <instance-arn> --target-type AWS_ACCOUNT \
  --target-id 123456789012 --principal-type GROUP \
  --principal-id <group-id> --permission-set-arn <ps-arn>

# List users/groups in the identity store
aws identitystore list-users --identity-store-id <store-id>
aws identitystore list-groups --identity-store-id <store-id>

# Sign in to a CLI session (browser flow)
aws configure sso
aws sso login --sso-session prod
```

## Best practices

- Put the Identity Center instance in the management account of your organization and assign access by group, not by individual.
- Use permission sets with least-privilege policies and appropriate session duration; prefer AWS managed job-function policies as a baseline.
- Connect an external IdP as the source of truth and use SCIM for automated user/group provisioning.
- Require MFA and configure the access portal with your own domain.
- Assign access to application accounts (for example, analytics, security) separately from production accounts.
- Monitor sign-in and assignment activity with CloudTrail; review assignments periodically.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| User can't access a portal/account | Check the account assignment, group membership, permission set, and that the instance is in the management account. |
| External IdP users missing | Verify SCIM provisioning is enabled and the bearer token is valid; confirm SAML metadata is up to date. |
| Sign-in fails with MFA | Check MFA enrollment and the access portal URL/domain configuration. |
| CLI login error | Re-run `aws configure sso`; confirm the SSO session name and start URL match. |
| New account not visible | Confirm the account is in AWS Organizations and re-run provisioning/assignments. |

## Limits

Permission sets, account assignments, users/groups in the Identity Center directory, and instance quotas apply. See the IAM Identity Center quotas documentation and Service Quotas console for current values.

## Official references

- [What is AWS IAM Identity Center?](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [AWS IAM Identity Center permission sets](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html)
- [AWS IAM Identity Center quotas](https://docs.aws.amazon.com/singlesignon/latest/userguide/quotas.html)
- [AWS IAM Identity Center pricing](https://aws.amazon.com/iam/identity-center/pricing/)
- [AWS CLI: sso-admin and identitystore commands](https://docs.aws.amazon.com/cli/latest/reference/sso-admin/)
