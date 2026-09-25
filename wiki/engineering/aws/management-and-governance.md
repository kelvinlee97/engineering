---
type: Service
title: AWS management and governance
description: Landing zones, service catalogs, quotas, licenses, resource sharing and grouping, and managed operations across AWS accounts.
tags: [aws, governance, multi-account]
sources:
  - id: aws-control-tower
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/control-tower/README.md
    title: "AWS Control Tower - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-service-catalog
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/service-catalog/README.md
    title: "AWS Service Catalog - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-service-quotas
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/service-quotas/README.md
    title: "AWS Service Quotas - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-license-manager
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/license-manager/README.md
    title: "AWS License Manager - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-ram
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ram/README.md
    title: "AWS Resource Access Manager (RAM) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-resource-groups-tag-editor
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/resource-groups-tag-editor/README.md
    title: "AWS Resource Groups & Tag Editor - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-managed-services
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/managed-services/README.md
    title: "AWS Managed Services (AMS) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services govern an AWS estate as it grows: a standard multi-account landing zone, approved product catalogs, quota and license tracking, sharing resources across accounts, and grouping resources by tag.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS Control Tower](#aws-control-tower) | Control Tower is a layer of governance on top of Organizations, not a replacement for it |
| [AWS Service Catalog](#aws-service-catalog) | AWS Service Catalog lets organizations create and manage catalogs of approved IT services, from single resources (AMI-based servers, databases, software) to complete multi-tier application architectures |
| [AWS Service Quotas](#aws-service-quotas) | AWS Service Quotas lets you view and manage the quotas (limits) for AWS services from one place |
| [AWS License Manager](#aws-license-manager) | AWS License Manager helps you manage software licenses from vendors such as Microsoft, SAP, Oracle, and IBM across AWS accounts and Regions |
| [AWS Resource Access Manager (RAM)](#aws-resource-access-manager-ram) | A resource share bundles resources with principals and a managed permission |
| [AWS Resource Groups & Tag Editor](#aws-resource-groups--tag-editor) | Tags are the metadata you attach to resources |
| [AWS Managed Services (AMS)](#aws-managed-services-ams) | AMS is an operations team you consume as a service |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS Control Tower

Control Tower is a layer of governance on top of Organizations, not a replacement for it: it decides what "well-architected" means for your landing zone, and its three control types enforce that definition at three different moments: before a resource can be created, before it can be provisioned by CloudFormation, or after it already exists. AWS Control Tower orchestrates a multi-account AWS environment (landing zone) with governance controls and automation. It builds on AWS Organizations, AWS Service Catalog, and AWS IAM Identity Center to provision accounts, enforce guardrails, and give you a dashboard of your organization's compliance and drift.

Key points:

- Landing zone: the well-architected, multi-account baseline (management account, organizational units, guardrails, and shared accounts) that Control Tower creates and manages.
- Organizational units (OUs): Control Tower manages the root OU and your custom OUs (for example, workload, sandbox) with enrolled accounts.
- Controls (guardrails): governance rules applied to OUs and accounts.
- Account Factory: automates account creation, baselines, and account customization; accounts can be provisioned through the console, AWS Service Catalog, or APIs.
- Drift detection: Control Tower periodically checks for changes that violate the landing zone (for example, manual SCP changes) and reports them on the dashboard.

Practices:

- Plan the OU structure and guardrails before creating the landing zone; changing the structure later requires drift review.
- Use Control Tower-managed accounts for workloads and keep the management account restricted to administrative tasks.
- Enforce preventive controls for high-impact actions (region restrictions, public access) and use detective controls for monitoring.

| Symptom | Check |
| --- | --- |
| Landing zone shows drift | Review the dashboard for non-compliant resources/SCPs and remediate or re-register the affected account. |
| OU cannot be enrolled | Confirm the OU is in the organization's root hierarchy and does not conflict with Control Tower-managed structure. |
| Control status `not applicable` | Check control scope: some controls only apply to certain resource types or Regions. |
| Account Factory failure | Review AWS Service Catalog and CloudFormation stack set status for the account provisioning baseline. |

Control Tower supports specific OU and account structures, and some controls have Regional scope; landing zone, account, and control limits apply. See the AWS Control Tower endpoints and quotas documentation and Service Quotas console for current values.[^aws-control-tower]


## AWS Service Catalog

AWS Service Catalog lets organizations create and manage catalogs of approved IT services, from single resources (AMI-based servers, databases, software) to complete multi-tier application architectures. Administrators assemble portfolios with constraints and access control; end users discover and self-service provision only the approved products.

Key points:

- Product: an IT service that users can provision; products are built from CloudFormation templates (or Terraform open source) and can have multiple versions.
- Portfolio: a collection of products plus constraints (launch, template, stack-set, notification constraints) and resource tags; access to portfolios is granted via IAM users/groups/roles.
- Provisioned product: an instance of a product launched by a user; supports update and termination.
- Self-service discovery: end users browse the products and portfolios they have access to and launch them without direct access to the underlying AWS services.
- Version control and reuse: one product can be added to many portfolios; updating the product version propagates to all portfolios that reference it.

Practices:

- Treat products as versioned artifacts: test a new version in a lower environment before making it available in production portfolios.
- Enforce governance with launch constraints (instance type limits, IAM role), template constraints, and stack-set constraints for multi-account rollout.
- Grant portfolios to groups/roles instead of individuals; use tag options for consistent resource tagging.

| Symptom | Check |
| --- | --- |
| User cannot see a product | Check portfolio association, IAM access to the portfolio, and product version availability. |
| Provisioning fails | Review CloudFormation stack events, launch constraint role permissions, and parameter validation. |
| Update not applied | Confirm the new provisioning artifact is associated and the provisioned product was updated. |
| Constraint not enforced | Verify the constraint is attached to the right portfolio/product combination. |

Products, portfolios, constraints, and provisioned products per account have quotas. See the AWS Service Catalog endpoints and quotas page and Service Quotas console for current values.[^aws-service-catalog]


## AWS Service Quotas

AWS Service Quotas lets you view and manage the quotas (limits) for AWS services from one place. Quotas are the maximum values for resources, actions, and items in your account (for example, IAM roles per account or VPCs per Region). When defaults don't meet your needs, you can request quota increases and monitor usage centrally.

Key points:

- Service quota: the maximum number of resources/operations for an account, Region, or resource; each AWS service defines its own quotas and defaults.
- Default vs. applied quota: the default is the initial value AWS establishes; the applied quota is the value after an increase is approved.
- Adjustable quotas: quotas that can be increased, at the account level or resource level; request through console/CLI/API and AWS support approves, denies, or partially approves.
- Global quotas: account-level quotas available in all Regions; increases are requested from us-east-1 (Public AWS), GovCloud (US-West), or China (Beijing).
- Usage and utilization: Service Quotas shows current resource usage and utilization percentages (for example, 150 of 200 resources = 75%).

Practices:

- Track quotas before launching large workloads; use Automatic Management to be notified near limits.
- Request increases early; approval can take time and may be partial.
- For global quotas, submit increase requests from the correct home Region (us-east-1 for Public AWS).

| Symptom | Check |
| --- | --- |
| Quota increase denied | Check the service's adjustability and the requested value; some quotas are not adjustable or have approval criteria. |
| Quota not found | Verify the service code and Region; some quotas are global or Region-specific. |
| Increase pending for long | Check request status in the console; contact AWS Support for delays. |
| Resource-level quota unavailable | Confirm the service supports resource-level quotas and use CLI version 2.13.20+ if needed. |

Quota increase requests and API request rates have quotas. See the Service Quotas user guide and the per-service quotas pages for current values.[^aws-service-quotas]


## AWS License Manager

AWS License Manager helps you manage software licenses from vendors such as Microsoft, SAP, Oracle, and IBM across AWS accounts and Regions. It provides consolidated visibility and reporting, supports Bring Your Own License (BYOL), enforces license limits with rules, and helps independent software vendors (ISVs) distribute and track licenses through managed entitlements.

Key points:

- License configuration: rules that define hard or soft limits on license consumption (vCPU, physical cores, sockets, number of machines) for a product.
- License rules and enforcement: administrators set limits so non-compliant server usage is stopped before it happens; violations are reported.
- License asset groups: centrally manage and track licenses across multiple Regions/accounts in an organization.
- Self-managed licenses: define rules based on your enterprise agreements within a single account.
- Granted licenses: govern licenses from AWS Marketplace, AWS Data Exchange, or sellers integrated with managed entitlements.

Practices:

- Model your vendor agreements as license configurations with hard/soft limits and assign them to EC2/RDS resources.
- Use license asset groups for multi-account/multi-Region governance; manage centrally from the management account.
- Integrate with Systems Manager Inventory to track on-premises usage before migration.

| Symptom | Check |
| --- | --- |
| License usage not tracked | Verify the resource is associated with the license configuration and in a supported Region. |
| Rules not enforced | Check the license configuration's hard/soft limit settings and resource associations. |
| Grants not visible | Confirm the grant status, beneficiary account, and IAM permissions. |
| RDS BYOL mismatch | Use the RDS integration for Oracle/Db2 vCPU-based licenses; verify instance class and license model. |

License configurations, licenses, and grants per account have quotas. See the AWS License Manager endpoints and quotas page and Service Quotas console for current values.[^aws-license-manager]


## AWS Resource Access Manager (RAM)

A resource share bundles resources with principals and a managed permission; sharing within your organization takes effect immediately, while sharing outside it requires the recipient to accept an invitation first. AWS Resource Access Manager (AWS RAM) lets you share AWS resources across AWS accounts, organizational units, or your entire organization. You create a resource share, choose principals, and attached managed permissions control what recipients can do with the shared resources, avoiding duplicate infrastructure in every account.

Key points:

- Resource share: a unit of sharing that contains resources and principals (accounts, OUs, or the whole organization).
- Principals: accounts that receive access; when sharing outside your organization, an invitation is sent and the recipient must accept it.
- Managed permissions: service-defined or customer-defined permissions that specify allowed actions on shared resources (for example, read-only versus read-write for a subnet); customer managed permissions use RAM-managed policies.
- Home Region: for global resources such as Aurora global databases, the resource share is created in the Home Region (us-east-1 for global resources), and sharing is available from that Region.
- Tags and sharing: use tags to organize resource shares and manage access with tag policies.

Practices:

- Share by OU or organization when possible so new accounts get access automatically, instead of maintaining account lists.
- Use managed permissions with least privilege; prefer service-managed read-only permissions where sufficient.
- For VPC sharing, share subnets with the target accounts and let them launch resources directly; do not create overlapping VPCs.

| Symptom | Check |
| --- | --- |
| Recipient cannot see shared resource | Confirm the resource is in the same Region/Home Region, the principal was added, and the invitation was accepted. |
| Actions denied on shared resource | Check the managed permission attached to the share and the recipient's IAM permissions. |
| Share failed to create | Verify the resource supports sharing and the ARN/principal values are correct. |
| Global resource not shared | Create/associate the share in the Home Region (us-east-1) for global resources. |

AWS RAM itself has no additional charge; you pay for the shared resources. Resource shares, principals per share, and shared resources per account have quotas. See the AWS RAM endpoints and quotas page and Service Quotas console for current values.[^aws-ram]


## AWS Resource Groups & Tag Editor

Tags are the metadata you attach to resources; Resource Groups turns a saved tag/type query into a reusable operational view, and Tag Editor lets you search and bulk-edit the underlying tags directly. AWS Resource Groups lets you organize AWS resources (EC2 instances, CloudFormation stacks, S3 buckets, and more) into groups so you can view and manage many resources at once. Tag Editor lets you search resources by tags and add, remove, or replace tags in bulk. Together they support tagging best practices, cost allocation, and automation.

Key points:

- Resource: an entity you can work with in AWS (for example, an EC2 instance, a CloudFormation stack, or an S3 bucket).
- Tags: key/value metadata pairs for organizing resources; used for billing and administration. Do not store PII or confidential data in tags.
- Resource group: a collection of resources in the same Region that match a query.
- Tag Editor: search supported resources by tag/resource type and bulk edit tags.
- Permissions: Resource Groups permissions are account-level; IAM principals with the right permissions can work with groups.

Practices:

- Define a company-wide tagging taxonomy (environment, owner, cost center, application) and enforce it with tag policies in Organizations.
- Use tags for cost allocation: activate cost allocation tags in Billing so Cost Explorer groups by tag.
- Use tag-based resource groups for operational views (by environment or application) and bulk actions.

| Symptom | Check |
| --- | --- |
| Group returns no resources | Check tag spelling/values, resource types, and that resources are in the same Region. |
| Tags not applied | Confirm the resource supports tagging and the IAM permission for the service's tagging API. |
| Costs not grouped by tag | Activate the cost allocation tags in Billing for the accounts. |
| Tag Editor search empty | Widen resource type filters; Tag Editor indexes supported resources by Region. |

Resource groups per account, tags per resource, and API request rates have quotas. See the AWS Resource Groups quotas page and Service Quotas console for current values.[^aws-resource-groups-tag-editor]


## AWS Managed Services (AMS)

AMS is an operations team you consume as a service: your changes flow through a controlled request process, and AMS's own baselines handle monitoring, patching, security, and backup underneath. AWS Managed Services (AMS) is an enterprise service that provides ongoing management of your AWS infrastructure: provisioning, running, monitoring, patching, security, and backup, following AWS best practices and ITSM processes. AMS implements change management and security policies so your team can focus on building applications. Note: AWS has announced end of support for AMS Advanced on June 30, 2027; plan accordingly.

Key points:

- Landing zone: AMS onboarding environments; single-account or multi-account architectures that apply AMS baselines and guardrails.
- Change requests: AMS processes and implements changes to your environment through a controlled request workflow (including your own changes with approval gates).
- Operations: 24x7 monitoring, patch management, security monitoring, backup, and incident response as part of the service.
- ITSM alignment: AMS follows IT service management practices to align IT services with business needs.
- Service requests: submit requests for new features or service improvements; AWS evaluates them.

Practices:

- Use a multi-account landing zone to separate environments and align with AMS-managed controls.
- Route infrastructure changes through the AMS change process to keep guardrails and compliance intact.
- Keep AMS-owned baselines (monitoring, patching, backup) configured and review dashboards regularly.

| Symptom | Check |
| --- | --- |
| Change request rejected | Review the request details against AMS policy and re-submit with correct scope/approval. |
| Monitoring alerts | Check the AMS dashboard for the affected resource and follow the runbook in the change portal. |
| Patching not applied | Confirm maintenance windows and the patch baseline in the AMS console. |
| Access denied to resources | AMS uses managed roles; request changes through the AMS change process. |

AMS is an enterprise offering with onboarding and operational agreements; supported Regions and operating systems are documented by AWS. See the AMS user guide for current supported configurations.[^aws-managed-services]


## Related

- [Multi-account governance](multi-account-governance.md)
- [Domain index](index.md)

[^aws-control-tower]: [AWS Control Tower - Runbook & Reference](../../sources/aws-control-tower.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/control-tower/README.md)
[^aws-service-catalog]: [AWS Service Catalog - Runbook & Reference](../../sources/aws-service-catalog.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/service-catalog/README.md)
[^aws-service-quotas]: [AWS Service Quotas - Runbook & Reference](../../sources/aws-service-quotas.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/service-quotas/README.md)
[^aws-license-manager]: [AWS License Manager - Runbook & Reference](../../sources/aws-license-manager.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/license-manager/README.md)
[^aws-ram]: [AWS Resource Access Manager (RAM) - Runbook & Reference](../../sources/aws-ram.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/ram/README.md)
[^aws-resource-groups-tag-editor]: [AWS Resource Groups & Tag Editor - Runbook & Reference](../../sources/aws-resource-groups-tag-editor.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/resource-groups-tag-editor/README.md)
[^aws-managed-services]: [AWS Managed Services (AMS) - Runbook & Reference](../../sources/aws-managed-services.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/managed-services/README.md)
