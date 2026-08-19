# AWS Certified Solutions Architect - Associate (SAA-C03) - Study Outline

> Facts verified against official AWS documentation: 2026-08-19

## Exam overview

The SAA-C03 exam is for individuals in a solutions architect role. It validates the ability to design solutions based on the AWS Well-Architected Framework: meeting current and projected business requirements while keeping architectures secure, resilient, high-performing, and cost-optimized, and reviewing existing solutions for improvement.

- **Format**: 65 questions (50 scored + 15 unscored), multiple choice and multiple response.
- **Duration**: 130 minutes.
- **Scoring**: scaled score 100-1,000; minimum passing score 720; compensatory scoring (no per-section pass required).
- **Recommended experience**: at least one year of hands-on experience designing solutions with AWS services.

## Official resources

- [SAA-C03 exam guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html)
- [AWS Certification overview](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/)

## Content domains

The official exam guide defines four content domains and their weightings:

1. Design secure architectures.
2. Design resilient architectures.
3. Design high-performing architectures.
4. Design cost-optimized architectures.

Read the exam guide for the detailed task statements; this outline mirrors the original knowledge base structure.

## Cloud Practitioner foundation (CLF-C02)

The original knowledge base starts with Cloud Practitioner material, which remains a useful foundation:

- Cloud benefits: on-demand, pay-as-you-go, elasticity, global reach.
- Design principles of the AWS Cloud.
- Security and compliance concepts, IAM, and access management.
- Core technology and services: compute, storage, database, networking, AI/ML, analytics.
- Billing, pricing, and support.

Official guide: [CLF-C02 exam guide](https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html)

## Foundations of cloud computing

- On-demand self-service and pay-as-you-go pricing.
- Economies of scale and variable vs. capital expense.
- Service models: IaaS, PaaS, SaaS.
- Elasticity, scalability, and agility compared with traditional data centers.

## Cloud technology and services

- Global infrastructure: Regions, Availability Zones, edge locations.
- Core services by category: compute, storage, database, networking, security, analytics, integration.
- Related runbooks in this knowledge base cover each service in depth (see the index).

## AWS ecosystem and shared responsibility model

- Shared responsibility: AWS secures the cloud; the customer secures what they put in the cloud.
- AWS Partner Network, AWS Marketplace, and support plans.
- AWS Artifact for compliance reports and agreements.

## AWS Well-Architected Framework

Six pillars:

1. Operational excellence
2. Security
3. Reliability
4. Performance efficiency
5. Cost optimization
6. Sustainability

Official whitepaper: [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

## Characteristics and advantages of cloud compute

- Elasticity and scalability (vertical and horizontal).
- High availability and fault tolerance across AZs and Regions.
- Decoupled, loosely coupled architectures and serverless options.
- Managed services that reduce operational burden.

## AWS pricing models

- On-Demand: pay per use, no commitment.
- Savings Plans and Reserved Instances: commit for a discount.
- Spot Instances: spare capacity at lower cost for interruptible workloads.
- Dedicated Hosts/Instances: physical isolation needs.
- Free Tier, consolidated billing, and Cost Explorer for tracking.

## Study plan

1. Read the official SAA-C03 exam guide and note the task statements.
2. Review the Well-Architected Framework whitepaper.
3. Work through the runbooks in this knowledge base, hands-on in your own account.
4. Take official practice questions on AWS Skill Builder and review weak domains.
5. Recheck the exam guide before booking; AWS updates exam scope over time.

## Practice resources

Official practice questions and courses are available on AWS Skill Builder. Question-bank content is intentionally not published here.

## Related runbooks in this knowledge base

- Compute: [EC2](../../ec2/README.md), [ECS](../../ecs/README.md), [EKS](../../eks/README.md), [Lambda](../../lambda/README.md)
- Storage: [S3](../../s3/README.md), [FSx](../../fsx/README.md), [Storage Gateway](../../storage-gateway/README.md)
- Database: [RDS](../../rds/README.md), [DynamoDB](../../dynamodb/README.md), [ElastiCache](../../elasticache/README.md)
- Networking: [VPC](../../vpc/README.md), [Route 53](../../route53/README.md), [ELB](../../elb/README.md), [CloudFront](../../cloudfront/README.md)
- Security: [IAM](../../iam/README.md), [KMS](../../kms/README.md), [Secrets Manager](../../secrets-manager/README.md), [WAF](../../waf/README.md), [Shield](../../shield/README.md), [GuardDuty](../../guardduty/README.md), [Security Hub CSPM](../../security-hub/README.md)
- Integration: [SQS](../../sqs/README.md), [SNS](../../sns/README.md), [Step Functions](../../step-functions/README.md), [EventBridge](../../eventbridge/README.md)
