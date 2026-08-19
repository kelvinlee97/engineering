# AWS Ecosystem - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

The AWS ecosystem includes the AWS Cloud platform itself (compute, storage, database, networking, analytics, security, and AI/ML services on global infrastructure), plus the AWS Partner Network (APN), AWS Marketplace, support plans, compliance resources (AWS Artifact), and the Well-Architected and Shared Responsibility frameworks that guide how you use it.

## Key concepts

- **Global infrastructure**: Regions, Availability Zones, and edge locations; services are Region-scoped unless stated otherwise.
- **Service categories**: compute (EC2, Lambda, ECS, EKS), storage (S3, EBS, EFS, FSx), databases (RDS, DynamoDB, Aurora), networking (VPC, Route 53, ELB, CloudFront), analytics (Athena, Redshift, EMR), security (IAM, KMS, GuardDuty, Security Hub CSPM), integration (SQS, SNS, EventBridge), and AI/ML (SageMaker, Lex, Rekognition, and more).
- **AWS Partner Network (APN)**: consulting and technology partners offering solutions, services, and competencies validated by AWS.
- **AWS Marketplace**: a digital catalog of third-party software and services that you can procure and deploy in AWS.
- **Support plans**: Basic, Developer, Business, Enterprise (and Business Support+, Enterprise Support, AWS Unified Operations under the current plan transition); plans define support access and tools like Trusted Advisor.
- **Compliance resources**: AWS Artifact for reports and agreements, and the Shared Responsibility Model for understanding obligations.
- **Frameworks**: the Well-Architected Framework guides architecture reviews; the AWS Cloud Adoption Framework guides organizational adoption.

## Common operations

The ecosystem is navigated through the console and programmatic services:

```bash
# Examples: discover what runs where and what is available
aws ec2 describe-regions
aws organizations list-accounts
aws service-quotas list-services
aws marketplace-catalog list-entities --catalog AWSMarketplace --entity-type Products
```

## Best practices

- Choose services by workload requirements and the Well-Architected pillars, not by feature list.
- Use consolidated billing and tagging for cost visibility across the ecosystem.
- Evaluate Marketplace/partner offerings against support, security, and compliance requirements.
- Align support plan to your production needs; enable Trusted Advisor and Health monitoring.
- Keep certifications and partner competencies aligned with your team's actual roles.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Service unavailable in Region | Check the service's Regional availability page; some services are not global. |
| Partner solution issues | Verify the offering's support path and IAM/network requirements before deploying. |
| Compliance evidence needed | Use AWS Artifact; AWS-side controls are covered by AWS, customer-side by your team. |

## Limits

The ecosystem is governed by per-service quotas and agreements; see the AWS index and per-service runbooks in this knowledge base for details.

## Official references

- [AWS Cloud overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [AWS Partner Network](https://aws.amazon.com/partners/)
- [AWS Marketplace](https://aws.amazon.com/marketplace)
- [AWS Support plans](https://aws.amazon.com/premiumsupport/plans/)
- [AWS Artifact](https://aws.amazon.com/artifact/)
- [AWS index in this knowledge base](../README.md)
