# Amazon Detective - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Detective helps you analyze, investigate, and identify the root cause of security findings and suspicious activity. It automatically extracts time-based events (logins, API calls, network traffic) from AWS CloudTrail and VPC Flow Logs, ingests GuardDuty findings, and uses machine learning and graph analysis to build interactive visualizations for security investigations.

## Key concepts

- **Behavior graph**: a linked dataset of extracted and analyzed events from one or more accounts; the account that enables Detective becomes the administrator of the graph and invites members (or uses AWS Organizations).
- **Data sources**: CloudTrail management events, VPC Flow Logs, and GuardDuty findings; up to a year of historical event data is retained.
- **Finding groups**: related findings and entities grouped around a potential security event for root cause analysis of high-severity GuardDuty findings.
- **Detective Investigation**: triage IAM users/roles against indicators of compromise (IOCs); can be started from the console or with the `StartInvestigation` API.
- **Security Lake integration**: query and retrieve raw logs (CloudTrail, VPC Flow Logs, EKS audit logs) stored in Amazon Security Lake.
- **VPC flow volume**: visual summaries of network flows per EC2 instance or Kubernetes pod.
- **Multi-account**: administrator account manages the graph; member accounts contribute data. Integrates with Security Hub CSPM for pivoting from findings.

## Common operations (AWS CLI)

```bash
# Create a behavior graph
aws detective create-graph
aws detective list-graphs

# Run an investigation and review results
aws detective start-investigation --graph-arn <graph-arn> \
  --entity-arn <entity-arn> --scope-start-time 2026-08-18T00:00:00Z
aws detective list-investigations --graph-arn <graph-arn>
aws detective get-investigation --graph-arn <graph-arn> --investigation-id <id>

# Manage members
aws detective list-members --graph-arn <graph-arn>
aws detective create-members --graph-arn <graph-arn> --accounts file://accounts.json
```

## Best practices

- Enable Detective in the administrator account and enroll all accounts that generate GuardDuty findings or sensitive traffic.
- Investigate high-severity GuardDuty findings with finding groups to see the full attack sequence and scope.
- Use Detective Investigation to triage users/roles quickly before deep-diving into raw data.
- Integrate with Security Hub CSPM so analysts can pivot from findings into Detective.
- Enable the Security Lake integration where you need raw-log queries for forensics.
- Monitor behavior graph health and member enrollment; remove accounts that leave the organization.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No data in behavior graph | Verify CloudTrail and VPC Flow Logs are enabled for the accounts and that members accepted/enrolled. |
| GuardDuty findings missing | Confirm the GuardDuty integration is enabled and findings are generated in the same Region. |
| Investigation returns nothing | Check the scope time range and that the entity (user/role/IP) has activity in the graph. |
| Member not contributing data | Confirm the member account is in the graph and permissions allow data collection. |
| Cost higher than expected | Detective charges per GB of analyzed data; review data volume and disable unneeded accounts. |

## Limits

Behavior graphs per account, members per graph, and investigation quotas apply; there is a 30-day free trial on first enablement. See the Amazon Detective endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Detective?](https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html)
- [Amazon Detective endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/detective.html)
- [Amazon Detective pricing](https://aws.amazon.com/detective/pricing/)
- [AWS CLI: detective commands](https://docs.aws.amazon.com/cli/latest/reference/detective/)
