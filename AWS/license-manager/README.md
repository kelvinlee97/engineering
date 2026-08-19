# AWS License Manager - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS License Manager helps you manage software licenses from vendors such as Microsoft, SAP, Oracle, and IBM across AWS accounts and Regions. It provides consolidated visibility and reporting, supports Bring Your Own License (BYOL), enforces license limits with rules, and helps independent software vendors (ISVs) distribute and track licenses through managed entitlements.

## Key concepts

- **License configuration**: rules that define hard or soft limits on license consumption (vCPU, physical cores, sockets, number of machines) for a product.
- **License rules and enforcement**: administrators set limits so non-compliant server usage is stopped before it happens; violations are reported.
- **License asset groups**: centrally manage and track licenses across multiple Regions/accounts in an organization.
- **Self-managed licenses**: define rules based on your enterprise agreements within a single account.
- **Granted licenses**: govern licenses from AWS Marketplace, AWS Data Exchange, or sellers integrated with managed entitlements.
- **Managed entitlements**: ISVs create licenses, distribute them to end users via IAM identities or signed tokens, and track check-out/check-in with quantities and time periods.
- **Inventory**: discover on-premises applications and licenses using Systems Manager Inventory and licensing rules.
- **Integrations**: Amazon EC2, Amazon RDS (Oracle/Db2 vCPU BYOL), AWS Marketplace, Systems Manager, Organizations, and user-based subscriptions.

## Common operations (AWS CLI)

```bash
# Create a license configuration and list it
aws license-manager create-license-configuration --name sql-byol \
  --license-counting-type vCPU --license-count 100 \
  --license-rules '{"hardLimit":true}'
aws license-manager list-license-configurations

# Manage grants for managed entitlements
aws license-manager create-license --license-configuration-arn <config-arn> \
  --license-name prod --product-name my-product --issuer file://issuer.json \
  --entitlements file://entitlements.json --consumption-configuration file://consumption.json
aws license-manager list-licenses
aws license-manager check-in-license --license-arn <license-arn> \
  --beneficiary 123456789012 --principal 123456789012
```

## Best practices

- Model your vendor agreements as license configurations with hard/soft limits and assign them to EC2/RDS resources.
- Use license asset groups for multi-account/multi-Region governance; manage centrally from the management account.
- Integrate with Systems Manager Inventory to track on-premises usage before migration.
- Use user-based subscriptions for supported products to simplify per-user licensing.
- Monitor license usage dashboards and set alarms when usage approaches limits.
- For ISVs, use managed entitlements for distribution and track check-out data for audits.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| License usage not tracked | Verify the resource is associated with the license configuration and in a supported Region. |
| Rules not enforced | Check the license configuration's hard/soft limit settings and resource associations. |
| Grants not visible | Confirm the grant status, beneficiary account, and IAM permissions. |
| RDS BYOL mismatch | Use the RDS integration for Oracle/Db2 vCPU-based licenses; verify instance class and license model. |
| Inventory missing | Confirm Systems Manager Inventory is running on the on-premises servers and they are registered. |

## Limits

License configurations, licenses, and grants per account have quotas. See the AWS License Manager endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS License Manager?](https://docs.aws.amazon.com/license-manager/latest/userguide/license-manager.html)
- [AWS License Manager endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/license-manager.html)
- [AWS License Manager pricing](https://aws.amazon.com/license-manager/pricing/)
- [AWS CLI: license-manager commands](https://docs.aws.amazon.com/cli/latest/reference/license-manager/)
