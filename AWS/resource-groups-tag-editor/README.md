# AWS Resource Groups & Tag Editor - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Resource Groups lets you organize AWS resources (EC2 instances, CloudFormation stacks, S3 buckets, and more) into groups so you can view and manage many resources at once. Tag Editor lets you search resources by tags and add, remove, or replace tags in bulk. Together they support tagging best practices, cost allocation, and automation.

## Key concepts

- **Resource**: an entity you can work with in AWS (for example, an EC2 instance, a CloudFormation stack, or an S3 bucket).
- **Tags**: key/value metadata pairs for organizing resources; used for billing and administration. Do not store PII or confidential data in tags.
- **Resource group**: a collection of resources in the same Region that match a query.
  - **Tag-based**: membership from a query of resource types and tags (AND semantics).
  - **CloudFormation stack-based**: membership from a single stack (optionally limited to resource types within it).
  - **Service-linked**: groups some services define and manage themselves.
  - **Nesting**: a resource group can contain other resource groups in the same Region.
- **Tag Editor**: search supported resources by tag/resource type and bulk edit tags.
- **Permissions**: Resource Groups permissions are account-level; IAM principals with the right permissions can work with groups.

## Common operations (AWS CLI)

```bash
# Create a tag-based resource group
aws resource-groups create-group --name prod-ec2 \
  --resource-query '{"Type":"TAG_FILTERS_1_0","Query":"{\"ResourceTypeFilters\":[\"AWS::EC2::Instance\"],\"TagFilters\":[{\"Key\":\"Env\",\"Values\":[\"prod\"]}]}"}'

# List and get groups
aws resource-groups list-groups
aws resource-groups get-group --group-name prod-ec2

# Tag resources in bulk with Tag Editor (resourcegroupstaggingapi)
aws resourcegroupstaggingapi get-resources --tag-filters Key=Env,Values=prod
aws resourcegroupstaggingapi tag-resources \
  --resource-arn-list arn:aws:ec2:us-east-1:123456789012:instance/i-0123456789abcdef0 \
  --tags Owner=platform
aws resourcegroupstaggingapi get-tag-values --key Env
```

## Best practices

- Define a company-wide tagging taxonomy (environment, owner, cost center, application) and enforce it with tag policies in Organizations.
- Use tags for cost allocation: activate cost allocation tags in Billing so Cost Explorer groups by tag.
- Use tag-based resource groups for operational views (by environment or application) and bulk actions.
- Never put sensitive data in tags; tags are metadata visible to billing and administration.
- Clean up obsolete tags and enforce mandatory tags on new resources (tag-on-create policies).
- Use Resource Groups with Systems Manager to run commands/patching on grouped instances.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Group returns no resources | Check tag spelling/values, resource types, and that resources are in the same Region. |
| Tags not applied | Confirm the resource supports tagging and the IAM permission for the service's tagging API. |
| Costs not grouped by tag | Activate the cost allocation tags in Billing for the accounts. |
| Tag Editor search empty | Widen resource type filters; Tag Editor indexes supported resources by Region. |
| Cross-service group empty | Confirm each service supports Resource Groups queries for the types selected. |

## Limits

Resource groups per account, tags per resource, and API request rates have quotas. See the AWS Resource Groups quotas page and Service Quotas console for current values.

## Official references

- [What are resource groups?](https://docs.aws.amazon.com/ARG/latest/userguide/resource-groups.html)
- [Tag Editor user guide](https://docs.aws.amazon.com/tag-editor/latest/userguide/tag-editor.html)
- [AWS Tagging best practices](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)
- [AWS CLI: resource-groups and resourcegroupstaggingapi commands](https://docs.aws.amazon.com/cli/latest/reference/resource-groups/)
