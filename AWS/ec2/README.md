# Amazon EC2 - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-18

## Overview

Amazon Elastic Compute Cloud (Amazon EC2) provides on-demand, scalable compute capacity in the AWS Cloud. An EC2 instance is a virtual server; the instance type you choose determines the balance of compute, memory, network, and storage available to it.

## Instance lifecycle and billing

| State | Meaning | Instance usage billing |
|-------|---------|------------------------|
| `pending` | Instance is preparing to enter `running` | Not billed |
| `running` | Instance is running and ready for use | Billed per second, 1-minute minimum |
| `stopping` | Instance is preparing to stop | Not billed (billed while stopping only when hibernating) |
| `stopped` | Instance is shut down, can be restarted | Not billed (EBS volumes and Elastic IPs still incur charges) |
| `shutting-down` | Instance is preparing to terminate | Not billed |
| `terminated` | Instance is permanently deleted | Not billed |

- **Reboot**: the instance stays on the same host, keeps its public DNS name and private IP, and keeps instance-store data; no new billing period starts.
- **Stop/start** (EBS-backed only): the instance moves to a new host, keeps its private IPv4 and Elastic IP, and gets a new public IPv4 unless an Elastic IP is associated. Instance-store data is erased.
- **Hibernate** (EBS-backed only): RAM contents are saved to the EBS root volume; the instance is billed while in `stopping`, then not billed while stopped.
- **Terminate**: permanent and unrecoverable. The root EBS volume is deleted by default (`DeleteOnTermination`); other volumes are preserved. The `InstanceInitiatedShutdownBehavior` attribute controls whether an OS shutdown stops or terminates the instance (default: stop for EBS-backed).

## Common operations (AWS CLI)

```bash
# Launch an instance
aws ec2 run-instances --image-id ami-0123456789abcdef0 \
  --instance-type t3.micro --key-name my-key \
  --security-group-ids sg-0123456789abcdef0 --subnet-id subnet-0123456789abcdef0

# List running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,PublicIpAddress]' \
  --output table

# Start / stop / reboot / terminate
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 reboot-instances --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# Status checks and tags
aws ec2 describe-instance-status --instance-ids i-0123456789abcdef0
aws ec2 create-tags --resources i-0123456789abcdef0 --tags Key=Name,Value=web-01

# Elastic IP
aws ec2 allocate-address
aws ec2 associate-address --instance-id i-0123456789abcdef0 --allocation-id eipalloc-0123456789abcdef0
aws ec2 release-address --allocation-id eipalloc-0123456789abcdef0
```

## Pricing

- **On-Demand**: pay per second, 60-second minimum, no commitment.
- **Savings Plans / Reserved Instances**: commit to 1 or 3 years for lower rates.
- **Spot Instances**: unused capacity at significantly reduced rates; can be reclaimed.
- **Dedicated Hosts / On-Demand Capacity Reservations**: for software licensing and guaranteed capacity.
- Free Tier covers a limited amount of usage for new accounts.

## Security and best practices

- Use security groups as a virtual firewall with least-privilege rules (specific ports and source CIDRs).
- Store private key pairs securely; AWS keeps only the public key.
- Attach IAM roles to instances instead of distributing long-term access keys.
- Enable termination protection on critical instances.
- Take regular EBS snapshots and use AMIs for recovery.
- Patch instances through AWS Systems Manager and monitor with CloudWatch and EC2 status checks.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Instance status check fails | Reboot first; if it persists, stop and start the instance. |
| Cannot connect over SSH/RDP | Verify security group inbound rules (port 22/3389 and source CIDR), route table/NACL, OS-level service, and key pair. |
| Public IPv4 changed after stop/start | Expected unless an Elastic IP is associated; associate an Elastic IP for a stable address. |
| Data disappeared on instance store | Expected: instance-store data is erased on stop/hibernate/terminate; use EBS for persistent data. |
| Instance terminated accidentally | Cannot be recovered; restore from AMIs/snapshots/backups. |
| Burstable CPU credits exhausted (t2/t3) | Switch to unlimited mode or a larger instance type. |
| Instance unreachable but status checks pass | Check CloudWatch metrics, OS memory/disk (CloudWatch agent), and EBS status. |

## Limits

Per-Region instance quotas vary by instance type and are adjustable. New accounts start with reduced quotas. Check the Service Quotas console for current values and request increases there.

## Official references

- [What is Amazon EC2? - Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [Amazon EC2 instance state changes](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
- [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/)
- [AWS CLI: ec2 commands](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
