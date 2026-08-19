# Foundations of Cloud Computing - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Cloud computing delivers on-demand IT resources over the internet with pay-as-you-go pricing. AWS provides compute, storage, databases, networking, analytics, and many other services on a global infrastructure, replacing large up-front capital expenses with variable costs that scale with usage.

## Key concepts

- **On-demand self-service**: provision resources when you need them without human interaction, and release them when done.
- **Pay-as-you-go**: pay only for what you use, converting capital expense into variable operating expense.
- **Economies of scale**: AWS aggregates demand across many customers, reducing per-unit costs.
- **Elasticity and scalability**: scale capacity up/down or out/in automatically; vertical (larger instances) and horizontal (more instances) scaling.
- **High availability and fault tolerance**: design across Availability Zones and Regions to survive failures.
- **Global infrastructure**: Regions (geographic areas), Availability Zones (isolated data centers within Regions), and edge locations for content delivery.
- **Service models**: IaaS (EC2: infrastructure), PaaS (Elastic Beanstalk, RDS: platform managed), SaaS (fully managed applications).
- **Agility**: develop, test, and deploy faster with self-service infrastructure and managed services.
- **Shared responsibility**: AWS secures the cloud; customers secure what they put in the cloud (see the Shared Responsibility Model runbook).

## Common operations

The foundation is concepts rather than a single API; apply it with:

```bash
# Examples: elasticity and managed services in practice
aws ec2 describe-regions                          # global infrastructure
aws autoscaling describe-auto-scaling-groups      # elasticity
aws elasticbeanstalk describe-applications        # PaaS model
aws lambda list-functions                         # serverless compute
```

## Best practices

- Design for failure: multi-AZ/Region architectures, health checks, and automated recovery.
- Use elasticity: match capacity to demand with Auto Scaling and serverless options.
- Choose the right service model (IaaS/PaaS/SaaS) per workload to reduce operational burden.
- Track cost from day one with budgets, tags, and Cost Explorer.
- Follow the Well-Architected Framework pillars when designing new workloads.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Capacity surprises at launch | Use Elastic Beanstalk/Auto Scaling and test scaling behavior in staging. |
| Costs grow with idle resources | Release or scale down unused resources; use managed/serverless where possible. |
| Single point of failure | Spread workloads across AZs and add health-checked redundancy. |

## Limits

Concepts are general; actual behavior depends on service quotas and architecture choices. See the AWS Cloud overview and the per-service runbooks in this knowledge base.

## Official references

- [AWS Cloud overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
- [Types of cloud computing](https://aws.amazon.com/types-of-cloud-computing/)
