# AWS Organizations - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Organizations lets you centrally manage multiple AWS accounts: create and invite accounts, group them into organizational units (OUs), apply governance policies, share resources across accounts, and consolidate billing onto a single invoice. It is a global service hosted in the US East (N. Virginia) Region (us-east-1).

## Key concepts

- **Management account**: the account that created the organization; used for billing and administration.
- **Member accounts**: accounts in the organization, either created or invited.
- **Root**: the top-level container; every organization has exactly one.
- **Organizational unit (OU)**: a group of accounts used to apply policies and structure.
- **Service control policies (SCPs)**: set permission boundaries for member accounts; they restrict, never grant, permissions.
- **Resource control policies (RCPs)**: centrally prevent unintended external access to your resources.
- **Other policy types**: tag policies, backup policies, AI services opt-out policies, and chat applications policies.
- **Delegated administrator**: a member account that manages a supported AWS service for the organization.
- **All features vs. consolidated billing only**: all features adds policy, integration, and account-management capabilities.

## Common operations (AWS CLI)

```bash
# Create an organization with all features
aws organizations create-organization --feature-set ALL

# List accounts and roots
aws organizations list-accounts
aws organizations list-roots

# Create an OU
aws organizations create-ou --parent-id <root-id> --name Production

# Create a member account (asynchronous)
aws organizations create-account --email admin-prod@example.com --account-name prod-account

# Create and attach an SCP
aws organizations create-policy --name DenyUnapprovedRegions \
  --type SERVICE_CONTROL_POLICY --content file://scp.json
aws organizations attach-policy --policy-id <policy-id> --target-id <ou-id>

# Inspect policies
aws organizations list-policies --filter SERVICE_CONTROL_POLICY
aws organizations list-targets-for-policy --policy-id <policy-id>

# Move an account between OUs
aws organizations move-account --account-id <account-id> \
  --source-parent-id <source-ou-id> --destination-parent-id <dest-ou-id>

# Register a delegated administrator
aws organizations register-delegated-administrator --account-id <account-id> \
  --service-principal guardduty.amazonaws.com
```

## Best practices

- Use a multi-account environment: accounts are natural boundaries for security, cost, and blast radius.
- Keep the management account for billing and administration only; don't run workloads in it.
- Structure accounts into OUs by environment (dev/staging/prod) and apply SCPs as deny lists; SCPs are a boundary, IAM still grants the permissions.
- Enable all features and use CloudTrail organization trails so member accounts can't disable or modify audit logs.
- Use delegated administrators (GuardDuty, Security Hub CSPM, Config, IAM Identity Center) instead of operating services from the management account.
- Use AWS Control Tower for pre-packaged guardrails on top of Organizations.
- Share common resources (VPCs, subnets, catalogs) with AWS Resource Access Manager (RAM) and centralize licensing with License Manager.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Account creation fails | Check the account quota and the concurrent-create limit (5 in progress); request a quota increase via Service Quotas. |
| SCP has no effect | SCPs don't grant permissions and don't apply to the management account; verify the account is a member and IAM allows the action. |
| Cannot remove an account | Created accounts must be at least 4 days old; invitations expire after 15 days. |
| API calls fail in other Regions | Organizations is global; make CLI/API calls from us-east-1. |
| Policy errors | Check SCP size (10,240 characters) and attachment limits (10 SCPs per entity). |

## Limits

Default maximum of 10 accounts per organization (adjustable up to 50,000); 1 root; 2,000 OUs; OU nesting up to 5 levels; 10,000 SCPs; 10 SCPs attached per entity; 50 tags per root/OU/account. Quotas apply organization-wide; request increases via Service Quotas in us-east-1.

## Official references

- [What is AWS Organizations?](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html)
- [Quotas and service limits for AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html)
- [AWS Organizations pricing](https://aws.amazon.com/organizations/pricing/)
- [AWS CLI: organizations commands](https://docs.aws.amazon.com/cli/latest/reference/organizations/)
