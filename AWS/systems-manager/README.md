# AWS Systems Manager - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Systems Manager helps you centrally view, manage, and operate nodes at scale across AWS, on-premises, and multicloud environments. Nodes run the SSM Agent and are registered as managed nodes; you then use tools like Run Command, Session Manager, Patch Manager, Parameter Store, Automation, and OpsCenter without logging into servers.

## Key concepts

- **Managed nodes**: EC2 instances, on-premises servers, and edge devices with SSM Agent installed and able to reach Systems Manager.
- **Run Command**: run scripts/commands on many nodes at once without SSH/RDP.
- **Session Manager**: secure, audited interactive shells (no inbound ports, no bastion hosts).
- **Patch Manager**: define patch baselines and apply OS patches at scale; report compliance.
- **Automation**: run predefined or custom runbooks (SSM documents) for operational tasks and remediation.
- **Parameter Store**: centralized, versioned storage for configuration and secrets (plaintext or SecureString with KMS).
- **State Manager**: apply and maintain a consistent node state on a schedule.
- **Inventory**: collect metadata (OS, patches, applications) from nodes.
- **OpsCenter / OpsItems**: aggregate operational issues and run remediation.

## Common operations (AWS CLI)

```bash
# List managed nodes
aws ssm describe-instance-information

# Run a command on targeted instances
aws ssm send-command --document-name "AWS-RunShellScript" \
  --targets "Key=instanceids,Values=i-0123456789abcdef0" \
  --parameters '{"commands":["df -h","uptime"]}'
aws ssm get-command-invocation --command-id <command-id> --instance-id i-0123456789abcdef0

# Start a session (requires Session Manager permissions)
aws ssm start-session --target i-0123456789abcdef0

# Parameters
aws ssm put-parameter --name /app/config/db-url --value "postgresql://db.internal:5432" --type String
aws ssm put-parameter --name /app/config/api-key --value "$(openssl rand -hex 32)" --type SecureString
aws ssm get-parameter --name /app/config/db-url

# Automation
aws ssm start-automation-execution --document-name "AWS-StopEC2Instance" \
  --parameters '{"InstanceId":["i-0123456789abcdef0"]}'
```

## Best practices

- Install the latest SSM Agent and grant nodes an IAM role with the AmazonSSMManagedInstanceCore policy.
- Use Session Manager instead of SSH/RDP and record sessions (S3 or CloudWatch Logs) for audit.
- Use Parameter Store for configuration; use SecureString (KMS) for secrets or prefer Secrets Manager.
- Apply patch baselines with maintenance windows and report compliance continuously.
- Use Automation runbooks with runbook permissions (run as roles) and test before broad rollout.
- Restrict control-plane actions (SendCommand, StartSession) with IAM and SCPs.
- Monitor managed-node health and set alarms when nodes become unmanaged.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Node not managed | Confirm SSM Agent is installed/running, the instance role is attached, and outbound access to the SSM endpoints works. |
| Command times out | Check network connectivity, agent version, and command output size. |
| Session fails to start | Verify Session Manager configuration, IAM permissions, and the SSM VPC endpoint (or NAT). |
| Parameters not found | Check path, parameter name, and IAM permissions on the parameter. |
| Patching not applied | Verify patch baseline, maintenance window, and node registration. |

## Limits

Managed-node counts, concurrent commands, parameter throughput, and document sizes have quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Systems Manager?](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [AWS Systems Manager quotas](https://docs.aws.amazon.com/general/latest/gr/ssm.html)
- [AWS Systems Manager pricing](https://aws.amazon.com/systems-manager/pricing/)
- [AWS CLI: ssm commands](https://docs.aws.amazon.com/cli/latest/reference/ssm/)
