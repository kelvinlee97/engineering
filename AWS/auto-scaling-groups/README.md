# Amazon EC2 Auto Scaling (Auto Scaling Groups) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon EC2 Auto Scaling helps you keep the correct number of EC2 instances available for your application's load. Instances are organized into Auto Scaling groups, which you size with a minimum, a desired, and a maximum capacity. As demand changes, scaling policies launch or terminate instances within those boundaries, and the service replaces unhealthy instances automatically.

## Key concepts

- **Auto Scaling group (ASG)**: a logical collection of EC2 instances managed as one unit; it never goes below the minimum or above the maximum capacity you set.
- **Launch template**: the configuration template for instances (AMI, instance type, key pair, security groups, user data); launch configurations are the legacy alternative.
- **Health checks**: EC2 status checks plus optional custom health checks (for example, application-level); unhealthy instances are terminated and replaced to maintain desired capacity.
- **AZ balancing**: instances are distributed evenly across the Availability Zones you specify for high availability.
- **Multiple instance types and purchase options**: launch several instance types and mix On-Demand with Spot; Capacity Rebalancing proactively replaces Spot Instances at elevated risk of interruption.
- **Load balancer integration**: Elastic Load Balancing registers and deregisters instances automatically as the group scales.
- **Instance refresh**: rolling or canary (phased) updates when you change the AMI or launch template.
- **Lifecycle hooks**: run custom actions when instances launch or before termination; combine with scale-in protection for stateful workloads.

## Common operations (AWS CLI)

```bash
# Create an Auto Scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --launch-template LaunchTemplateName=web-lt,Version=1 \
  --min-size 2 --max-size 10 --desired-capacity 4 \
  --vpc-zone-identifier subnet-0123456789abcdef0,subnet-1234567890abcdef0

# Update capacity or configuration
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web-asg \
  --min-size 3 --max-size 12 --desired-capacity 6
aws autoscaling set-desired-capacity --auto-scaling-group-name web-asg \
  --desired-capacity 8

# Inspect and terminate an instance
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names web-asg
aws autoscaling describe-scaling-activities --auto-scaling-group-name web-asg
aws autoscaling terminate-instance-in-auto-scaling-group \
  --instance-id i-0123456789abcdef0 --should-decrement-desired-capacity

# Rolling update with instance refresh
aws autoscaling start-instance-refresh --auto-scaling-group-name web-asg \
  --preferences '{"MinHealthyPercentage": 90}'
```

## Best practices

- Use launch templates (not launch configurations) and version them for controlled changes.
- Set min/max/desired based on tested capacity; use target tracking policies on good metrics (CPU, requests per target, queue depth).
- Spread instances across multiple Availability Zones and enable ELB health checks for application-aware replacement.
- Mix On-Demand and Spot with Capacity Rebalancing for cost savings on fault-tolerant workloads.
- Use lifecycle hooks for draining/registration and scale-in protection for stateful instances.
- Pre-warm AMIs and use instance refresh for safe rolling/canary deployments.
- Monitor scaling activities and set alarms on the group's MinSize/MaxSize/InService counts.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Instances not launching | Check launch template validity, subnet/az capacity, instance type availability, and IAM permissions. |
| Desired capacity not maintained | Review scaling activities, health check status, and that instances are not protected from scale-in unexpectedly. |
| Unbalanced across AZs | Confirm the group spans the AZs you intend and there is capacity in each. |
| Scaling policy never triggers | Verify the CloudWatch metric name/namespace and alarm thresholds for the policy. |
| Instance refresh fails | Check MinHealthyPercentage and instance readiness; adjust preferences and retry. |

## Limits

Auto Scaling groups, launch templates, and scaling policies per account have quotas; group sizes are constrained by EC2 instance limits. See the Service Quotas console for current values. EC2 Auto Scaling itself has no additional charge; you pay for the underlying resources.

## Official references

- [What is Amazon EC2 Auto Scaling?](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [Amazon EC2 Auto Scaling quotas](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-quotas.html)
- [Amazon EC2 Auto Scaling pricing](https://aws.amazon.com/ec2/autoscaling/pricing/)
- [AWS CLI: autoscaling commands](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/)
