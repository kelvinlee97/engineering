---
type: Service
title: AWS compliance and posture
description: Services that record configuration, scan for vulnerabilities, find sensitive data, investigate incidents, and supply AWS compliance reports.
tags: [aws, security, compliance]
sources:
  - id: aws-config
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/config/README.md
    title: "AWS Config - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-inspector
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/inspector/README.md
    title: "Amazon Inspector - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-macie
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/macie/README.md
    title: "Amazon Macie - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-detective
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/detective/README.md
    title: "Amazon Detective - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-artifact
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/artifact/README.md
    title: "AWS Artifact - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services answer compliance and posture questions: what a resource looked like over time, which workloads have known vulnerabilities, where sensitive data lives, how an incident unfolded, and what evidence AWS itself provides to auditors. They feed and complement the [security monitoring](security-monitoring.md) pipeline.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS Config](#aws-config) | AWS Config only knows about a resource if the recorder was running when it changed |
| [Amazon Inspector](#amazon-inspector) | Amazon Inspector is a vulnerability management service that automatically discovers workloads and continuously scans them for software vulnerabilities and unintended network exposure |
| [Amazon Macie](#amazon-macie) | Macie continuously inventories your S3 buckets, samples or scans objects for sensitive data and misconfiguration, and turns what it finds into findings that flow to EventBridge or Security Hub for action |
| [Amazon Detective](#amazon-detective) | Amazon Detective helps you analyze, investigate, and identify the root cause of security findings and suspicious activity |
| [AWS Artifact](#aws-artifact) | AWS Artifact is a read-only evidence and agreements portal, not a compliance service |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS Config

AWS Config only knows about a resource if the recorder was running when it changed: recording, delivery, and rule evaluation are three separate steps in sequence, so a resource can be perfectly real and still invisible to Config, to S3 history, or to compliance rules if any one earlier step was off or unauthorized. AWS Config records the configuration of supported AWS resources in an account and Region, tracks how configurations and relationships change over time, and evaluates compliance with rules. It delivers configuration history and snapshots to S3, sends change notifications through SNS, and supports conformance packs, aggregators, and advanced queries.

Key points:

- Configuration item (CI): a record of a resource state at a point in time, including relationships.
- Configuration recorder: captures changes; one customer managed recorder per account per Region (service-linked recorders are created by integrated services such as Security Hub CSPM).
- Configuration history and snapshot: delivered to an S3 bucket on a schedule or on demand.
- Configuration stream: SNS notifications when recorded resource changes occur.
- Rules: managed or custom (Lambda) evaluations that report compliant/noncompliant.

Practices:

- Record all supported resource types (or at least the ones your compliance scope needs); use continuous recording for real-time monitoring.
- Use managed rules and conformance packs to standardize compliance checks across accounts.
- Keep the delivery S3 bucket private and encrypted; grant AWS Config only the permissions it needs.

| Symptom | Check |
| --- | --- |
| Resources not recorded | Confirm the recorder is started, the IAM role has permissions, and the resource type is supported in the Region. |
| No compliance results | Ensure rules are deployed, the evaluated resource types are recorded, and evaluations have completed. |
| Delivery to S3/SNS failing | Check bucket policy and topic permissions, and the delivery channel configuration. |
| Aggregator shows no data | Verify source accounts authorized the aggregation and required Regions are selected. |

Up to 1,000 rules per Region per account; 50 conformance packs; 130 rules per conformance pack; 50 aggregators (adjustable); 10,000 accounts per aggregator; 300 saved queries; 50 tags per resource; one customer managed configuration recorder per account per Region. Check the Service Quotas console for current values.[^aws-config]


## Amazon Inspector

Amazon Inspector is a vulnerability management service that automatically discovers workloads and continuously scans them for software vulnerabilities and unintended network exposure. It scans EC2 instances, container images in Amazon ECR, and Lambda functions, and produces findings with remediation guidance and an environment-specific risk score.

Key points:

- Findings: detailed reports of detected vulnerabilities or network exposure; include severity, affected resource, and remediation recommendations; findings close automatically when remediated.
- Continuous scanning: Inspector discovers eligible resources and rescans automatically when packages are installed/patched or when a new CVE affecting a resource is published.
- Risk score: severity tailored to your environment using CVSS and your resource context (network reachability, exploitability).
- Coverage and dashboard: view scan coverage, most critical findings, and affected resources; generate CSV/JSON reports.
- Delegated administrator: with AWS Organizations, one account centrally enables and manages Inspector for member accounts.

Practices:

- Enable Inspector across the whole organization with a delegated administrator so new accounts and resources are covered automatically.
- Scan all three resource types (EC2, ECR, Lambda) and review critical/high findings on a schedule.
- Use the risk score and dashboard to prioritize findings with real exploitability and exposure, not just raw CVSS.

| Symptom | Check |
| --- | --- |
| No resources scanned | Verify Inspector is enabled for the scan type, the account is a member, and SSM Agent is running on EC2 (agentless scanning options also apply). |
| Findings missing for Lambda | Confirm Lambda scanning is enabled and functions are in supported runtimes. |
| ECR images not scanned | Check the repository and that images were pushed after enabling scan-on-push or continuous scanning. |
| Delegated admin not working | Designate the delegated administrator in AWS Organizations and enable the service from that account. |

Findings retention, API request rates, and per-account/resource scan quotas apply. See the Amazon Inspector endpoints and quotas page and Service Quotas console for current values.[^aws-inspector]


## Amazon Macie

Macie continuously inventories your S3 buckets, samples or scans objects for sensitive data and misconfiguration, and turns what it finds into findings that flow to EventBridge or Security Hub for action. Amazon Macie is a data security service that discovers sensitive data in Amazon S3 using machine learning and pattern matching, evaluates S3 buckets for security and access-control issues, and generates findings you can review and remediate. It provides a bucket inventory, a dashboard, and automated sensitive data discovery.

Key points:

- Bucket inventory and monitoring: Macie automatically inventories S3 general purpose buckets and evaluates them for public access, shared access, and encryption issues, producing policy findings.
- Sensitive data discovery: automated discovery samples representative objects continuously, or you run discovery jobs for deeper, targeted analysis of specific buckets with defined sampling depth.
- Managed data identifiers: built-in criteria detecting PII, financial information, and credentials for many countries/regions; custom data identifiers use your regex and proximity rules; allow lists exclude known acceptable text.
- Findings: detailed reports with severity, affected resource, and detection details; can be reviewed in the console/API and exported to EventBridge or AWS Security Hub CSPM.
- Multi-account: designate a Macie administrator via AWS Organizations (or invitations) to manage member accounts and inspect their buckets.

Practices:

- Enable Macie before S3 data grows, so the inventory and baseline are established early.
- Use automated discovery for broad coverage and targeted jobs for high-value buckets or compliance deadlines.
- Combine managed and custom data identifiers; use allow lists to reduce noise from known sample data.

| Symptom | Check |
| --- | --- |
| Buckets not inventoried | Confirm Macie is enabled in the bucket's Region and the account is a member. |
| No sensitive data findings | Check job/automated discovery configuration, sampling percentage, and managed identifier scope. |
| Object analysis errors | Verify object permissions, KMS key access for decryption, and supported object types. |
| Findings not in Security Hub CSPM | Enable the Macie integration in Security Hub CSPM in the same Region. |

Classification jobs per account, findings retention, and API quotas apply. See the Amazon Macie endpoints and quotas page and Service Quotas console for current values.[^aws-macie]


## Amazon Detective

Amazon Detective helps you analyze, investigate, and identify the root cause of security findings and suspicious activity. It automatically extracts time-based events (logins, API calls, network traffic) from AWS CloudTrail and VPC Flow Logs, ingests GuardDuty findings, and uses machine learning and graph analysis to build interactive visualizations for security investigations.

Key points:

- Behavior graph: a linked dataset of extracted and analyzed events from one or more accounts; the account that enables Detective becomes the administrator of the graph and invites members (or uses AWS Organizations).
- Data sources: CloudTrail management events, VPC Flow Logs, and GuardDuty findings; up to a year of historical event data is retained.
- Finding groups: related findings and entities grouped around a potential security event for root cause analysis of high-severity GuardDuty findings.
- Detective Investigation: triage IAM users/roles against indicators of compromise (IOCs); can be started from the console or with the `StartInvestigation` API.
- Security Lake integration: query and retrieve raw logs (CloudTrail, VPC Flow Logs, EKS audit logs) stored in Amazon Security Lake.

Practices:

- Enable Detective in the administrator account and enroll all accounts that generate GuardDuty findings or sensitive traffic.
- Investigate high-severity GuardDuty findings with finding groups to see the full attack sequence and scope.
- Use Detective Investigation to triage users/roles quickly before deep-diving into raw data.

| Symptom | Check |
| --- | --- |
| No data in behavior graph | Verify CloudTrail and VPC Flow Logs are enabled for the accounts and that members accepted/enrolled. |
| GuardDuty findings missing | Confirm the GuardDuty integration is enabled and findings are generated in the same Region. |
| Investigation returns nothing | Check the scope time range and that the entity (user/role/IP) has activity in the graph. |
| Member not contributing data | Confirm the member account is in the graph and permissions allow data collection. |

Behavior graphs per account, members per graph, and investigation quotas apply; there is a 30-day free trial on first enablement. See the Amazon Detective endpoints and quotas page and Service Quotas console for current values.[^aws-detective]


## AWS Artifact

AWS Artifact is a read-only evidence and agreements portal, not a compliance service: it hands you AWS's own audited reports and agreements on demand, but producing your own organization's compliance evidence stays your responsibility. AWS Artifact provides on-demand access to AWS security and compliance documents, including ISO, PCI, and SOC reports, and certifications from accreditation bodies. You can also review, accept, and track agreements with AWS for your account and organization, and use Assurance Assistant to answer compliance and due-diligence questions. AWS Artifact documents and agreements are provided free of charge.

Practices:

- Download current reports each audit cycle; compliance reports are periodically reissued and previous versions may not be accepted.
- Accept and track agreements centrally in the management account so organization-wide agreements are visible.
- Use Assurance Assistant for initial due-diligence questions, then verify answers against the underlying reports.

| Symptom | Check |
| --- | --- |
| Report not found | Verify the report ID and that your account is eligible for that report/region. |
| Agreement cannot be accepted | Confirm you have the required IAM permissions and the agreement is not already terminated. |
| Vendor documents missing | Access Marketplace Vendor Insights from the AWS Marketplace console for that ISV. |
| Assurance Assistant unavailable | Check that the feature is enabled for your account/region. |

AWS Artifact documents and agreements are free; access permissions and API quotas apply. See the AWS Artifact user guide and IAM documentation for current details.[^aws-artifact]


## Related

- [Security monitoring](security-monitoring.md)
- [Multi-account governance](multi-account-governance.md)
- [Domain index](index.md)

[^aws-config]: [AWS Config - Runbook & Reference](../../sources/aws-config.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/config/README.md)
[^aws-inspector]: [Amazon Inspector - Runbook & Reference](../../sources/aws-inspector.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/inspector/README.md)
[^aws-macie]: [Amazon Macie - Runbook & Reference](../../sources/aws-macie.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/macie/README.md)
[^aws-detective]: [Amazon Detective - Runbook & Reference](../../sources/aws-detective.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/detective/README.md)
[^aws-artifact]: [AWS Artifact - Runbook & Reference](../../sources/aws-artifact.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/artifact/README.md)
