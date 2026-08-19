# AWS Application Migration Service (MGN) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Application Migration Service (MGN, now documented as AWS Transform MGN) automates the migration of physical, virtual, and cloud servers to AWS with minimal downtime, typically cutover windows of minutes. MGN performs continuous block-level replication of source servers, converts them for launch on AWS, and supports large-scale migrations through templates, applications, and waves.

## Key concepts

- **Source server**: the on-premises, virtual, or cloud server being migrated; install the MGN agent to start replication.
- **Replication**: continuous block-level replication to a staging area in your AWS account; the target is prepared for launch without stopping the source.
- **Templates**: replication, launch, and post-launch templates control how servers are replicated, launched, and configured after migration; settings can be overridden per server.
- **Applications and waves**: group servers into applications and applications into waves to run actions (launch, cutover, archive) in bulk.
- **Cutover**: the controlled switch that stops replication and launches the migrated instances (usually in minutes); test launches (blue/green) validate before cutover.
- **OS and network support**: Windows Server and Linux distributions; IPv4 and IPv6; standard Availability Zones and Local Zones.

## Common operations (CLI)

```bash
# List source servers and start replication
aws mgn list-source-servers --filters '{"isArchived":["false"]}'
aws mgn start-replication --source-server-id <source-server-id>

# Launch a test instance and then cutover
aws mgn start-test --source-server-ids <source-server-id>
aws mgn describe-launch-configuration-templates
aws mgn start-cutover --source-server-ids <source-server-id>

# Finalize and manage
aws mgn finalize-cutover --source-server-id <source-server-id>
aws mgn archive-application --application-id <application-id>
```

## Best practices

- Test migrations on a representative sample of servers before mass cutover; use test launches to validate boot, networking, and applications.
- Plan waves by dependency and business priority; avoid cutting over dependent servers out of order.
- Use launch templates for consistent instance sizing and post-launch templates for agents/config after boot.
- Keep the staging area network isolated and enforce least-privilege IAM for MGN roles.
- Monitor replication health (lag, failures) and fix disk/network issues before cutover windows.
- After cutover, run the application through its normal checks, then finalize and archive the source.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Replication lag | Check source network bandwidth, disk I/O, and the agent status on the source server. |
| Test launch fails | Review launch template settings, AMI/target subnet, and post-launch scripts. |
| Agent not installed | Install the MGN agent on the source and confirm connectivity to AWS endpoints. |
| Cutover fails | Verify the staging area, replication health, and that the source was not archived. |
| Applications not migrated | Check application/wave membership and the order of cutover actions. |

## Limits

Source servers per account, concurrent launches, and API request rates have quotas. See the AWS Application Migration Service endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Transform MGN?](https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html)
- [AWS Application Migration Service endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/mgn.html)
- [AWS Application Migration Service pricing](https://aws.amazon.com/application-migration-service/pricing/)
- [AWS CLI: mgn commands](https://docs.aws.amazon.com/cli/latest/reference/mgn/)
