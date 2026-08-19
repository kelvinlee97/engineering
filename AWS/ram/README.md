# AWS Resource Access Manager (RAM) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Resource Access Manager (AWS RAM) lets you share AWS resources across AWS accounts, organizational units, or your entire organization. You create a resource share, choose principals, and attached managed permissions control what recipients can do with the shared resources, avoiding duplicate infrastructure in every account.

## Key concepts

- **Resource share**: a unit of sharing that contains resources and principals (accounts, OUs, or the whole organization).
- **Principals**: accounts that receive access; when sharing outside your organization, an invitation is sent and the recipient must accept it.
- **Managed permissions**: service-defined or customer-defined permissions that specify allowed actions on shared resources (for example, read-only versus read-write for a subnet); customer managed permissions use RAM-managed policies.
- **Home Region**: for global resources such as Aurora global databases, the resource share is created in the Home Region (us-east-1 for global resources), and sharing is available from that Region.
- **Tags and sharing**: use tags to organize resource shares and manage access with tag policies.

Resources commonly shared with RAM include VPC subnets, Transit Gateways, Route 53 Resolver rules, License Manager licenses, Aurora/DocumentDB/Neptune/RDS databases, SageMaker notebooks, and more.

## Common operations (AWS CLI)

```bash
# Create a resource share
aws ram create-resource-share --name shared-subnets \
  --resource-arns arn:aws:ec2:us-east-1:123456789012:subnet/subnet-0123456789abcdef0 \
  --principals 210987654321

# List and inspect shares
aws ram list-resource-shares --resource-owner SELF
aws ram list-resources --resource-share-owner SELF

# Invitations (when sharing outside the organization)
aws ram get-resource-share-invitations
aws ram accept-resource-share-invitation \
  --resource-share-invitation-arn <invitation-arn>

# Delete a share
aws ram delete-resource-share --resource-share-arn <share-arn>
```

## Best practices

- Share by OU or organization when possible so new accounts get access automatically, instead of maintaining account lists.
- Use managed permissions with least privilege; prefer service-managed read-only permissions where sufficient.
- For VPC sharing, share subnets with the target accounts and let them launch resources directly; do not create overlapping VPCs.
- Keep resource owners responsible for lifecycle; recipients cannot modify or delete the shared resource itself.
- Review resource shares and principals periodically; remove stale shares.
- Monitor sharing activity with CloudTrail for audit.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Recipient cannot see shared resource | Confirm the resource is in the same Region/Home Region, the principal was added, and the invitation was accepted. |
| Actions denied on shared resource | Check the managed permission attached to the share and the recipient's IAM permissions. |
| Share failed to create | Verify the resource supports sharing and the ARN/principal values are correct. |
| Global resource not shared | Create/associate the share in the Home Region (us-east-1) for global resources. |
| Share deletion fails | Disassociate all principals/resources first, or the share may be in `deleting` state; wait before retrying. |

## Limits

AWS RAM itself has no additional charge; you pay for the shared resources. Resource shares, principals per share, and shared resources per account have quotas. See the AWS RAM endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Resource Access Manager?](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)
- [AWS RAM supported resources](https://docs.aws.amazon.com/ram/latest/userguide/shareable.html)
- [AWS RAM quotas](https://docs.aws.amazon.com/ram/latest/userguide/quotas.html)
- [AWS RAM pricing](https://aws.amazon.com/ram/pricing/)
- [AWS CLI: ram commands](https://docs.aws.amazon.com/cli/latest/reference/ram/)
