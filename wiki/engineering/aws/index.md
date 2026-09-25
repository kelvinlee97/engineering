# Concept

* [AWS foundations](aws-foundations.md) - The shared responsibility model and the Well-Architected Framework, the two ideas the other AWS pages assume.

# Pattern

* [AWS cost](cost.md) - How AWS charges (pricing models) and the Billing and Cost Management tools for tracking and controlling spend.
* [AWS multi-account governance](multi-account-governance.md) - Running many AWS accounts under AWS Organizations, with guardrails applied from the organization rather than per account.
* [AWS security monitoring](security-monitoring.md) - Recording API activity with CloudTrail, detecting threats with GuardDuty, and aggregating findings in Security Hub into one response pipeline.

# Tool

* [AWS operations tooling](operations-tooling.md) - Monitoring with CloudWatch, defining infrastructure with CloudFormation, and managing instances with Systems Manager.

# Service

* [AWS compute](compute.md) - Choosing AWS compute, and running EC2 instances behind load balancers in Auto Scaling groups.
* [AWS containers and serverless](containers-and-serverless.md) - Running containers on ECS or EKS with images in ECR, and running functions on Lambda.
* [AWS encryption and secrets](encryption-and-secrets.md) - Envelope encryption with AWS KMS keys, and storing and rotating credentials in Secrets Manager.
* [AWS IAM](iam.md) - How AWS IAM grants access: identities and roles, how a request's policies are evaluated, and IAM Identity Center for workforce sign-in.
* [AWS networking](networking.md) - Amazon VPC for private networks in AWS, and Direct Connect for private links from on-premises.

# Comparison

* [AWS certifications](certifications.md) - The Cloud Practitioner, Developer Associate, and Solutions Architect Associate exams compared, with the study path the legacy outlines share.
* [AWS data stores](data-stores.md) - Choosing an AWS data store, and the main options: RDS, DynamoDB, ElastiCache, and S3.
* [AWS global traffic routing](global-traffic.md) - Getting users to the right AWS endpoint: Route 53 DNS, CloudFront caching, and Global Accelerator, and how to choose between them.
* [AWS messaging](messaging.md) - Choosing between SQS queues, SNS topics, and EventBridge event buses for decoupling AWS services.
