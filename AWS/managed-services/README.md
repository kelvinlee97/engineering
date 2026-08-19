# AWS Managed Services (AMS) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Managed Services (AMS) is an enterprise service that provides ongoing management of your AWS infrastructure: provisioning, running, monitoring, patching, security, and backup, following AWS best practices and ITSM processes. AMS implements change management and security policies so your team can focus on building applications. Note: AWS has announced end of support for AMS Advanced on June 30, 2027; plan accordingly.

## Key concepts

- **Landing zone**: AMS onboarding environments; single-account or multi-account architectures that apply AMS baselines and guardrails.
- **Change requests**: AMS processes and implements changes to your environment through a controlled request workflow (including your own changes with approval gates).
- **Operations**: 24x7 monitoring, patch management, security monitoring, backup, and incident response as part of the service.
- **ITSM alignment**: AMS follows IT service management practices to align IT services with business needs.
- **Service requests**: submit requests for new features or service improvements; AWS evaluates them.
- **End of support (AMS Advanced)**: after June 30, 2027, the AMS Advanced console and resources will no longer be accessible; review AWS guidance for the transition.

## Common operations

AMS is operated through its console and service request process rather than direct customer-run APIs. Administrators work with:

- The AMS console for change requests, service requests, and environment status.
- AWS Service Catalog and CloudFormation products for provisioned infrastructure.
- Your own accounts for application development and deployment with AMS-managed guardrails.

## Best practices

- Use a multi-account landing zone to separate environments and align with AMS-managed controls.
- Route infrastructure changes through the AMS change process to keep guardrails and compliance intact.
- Keep AMS-owned baselines (monitoring, patching, backup) configured and review dashboards regularly.
- Integrate application deployments with your CI/CD and use AMS-supported services only.
- Track the AMS Advanced end-of-support timeline and plan migration/transition before June 30, 2027.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Change request rejected | Review the request details against AMS policy and re-submit with correct scope/approval. |
| Monitoring alerts | Check the AMS dashboard for the affected resource and follow the runbook in the change portal. |
| Patching not applied | Confirm maintenance windows and the patch baseline in the AMS console. |
| Access denied to resources | AMS uses managed roles; request changes through the AMS change process. |
| AMS Advanced end of support | Review AWS transition guidance and migrate managed workloads before June 30, 2027. |

## Limits

AMS is an enterprise offering with onboarding and operational agreements; supported Regions and operating systems are documented by AWS. See the AMS user guide for current supported configurations.

## Official references

- [What is AWS Managed Services?](https://docs.aws.amazon.com/managedservices/latest/userguide/what-is-ams.html)
- [AWS Managed Services user guide](https://docs.aws.amazon.com/managedservices/latest/userguide/welcome.html)
- [AWS Managed Services pricing](https://aws.amazon.com/managed-services/pricing/)
