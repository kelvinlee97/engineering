# AWS Certified Developer - Associate (DVA-C02) - Study Outline

> Facts verified against official AWS documentation: 2026-08-19

## Exam overview

The DVA-C02 exam validates proficiency in developing, testing, deploying, and debugging AWS cloud applications. It covers writing application code, working with AWS services (including Lambda and data stores), implementing security and encryption, and automating deployments with CI/CD.

## Official resources

- [DVA-C02 exam guide](https://docs.aws.amazon.com/aws-certification/latest/developer-associate-02/developer-associate-02.html)
- [AWS Certification overview](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/)

## Content domains

The official exam guide defines four content domains and their weightings:

1. Development with AWS services.
2. Security.
3. Deployment.
4. Troubleshooting and optimization.

Read the exam guide for the detailed task statements; this outline mirrors the original knowledge base structure.

## Version control and collaboration

- **CodeCommit**: managed Git repositories, branches, pull requests, and IAM-based access.
- **CodeStar**: project templates and team dashboards for developing and delivering applications.
- Related runbook: [Git and repository workflows](../../../Git/README.md) where applicable.

## CI/CD

- **CodeBuild**: fully managed build service; builds from source repositories and produces artifacts.
- **CodePipeline**: automated release pipelines with stages for build, test, and deploy; integrates with CodeCommit, CodeBuild, CodeDeploy, and third-party tools.
- **CodeDeploy**: automated application deployments to EC2, Lambda, and on-premises; supports in-place, blue/green, and canary strategies with rollback.
- Related concepts: deployment strategies, health checks, and rollback behavior.

## Infrastructure as code and platforms

- **CloudFormation**: declare and provision resources as stacks; change sets and drift detection.
- **Elastic Beanstalk**: managed platform for deploying web applications without managing the underlying infrastructure.
- **OpsWorks**: configuration management platform (Chef/Puppet) for older-style workloads; evaluate current alternatives before new use.
- Related runbook: [CloudFormation](../../cloudformation/README.md).

## Serverless and APIs

- **Lambda**: functions as a service; triggers, concurrency, environment variables, layers, and IAM roles.
- **Step Functions**: state machines that orchestrate Lambda and other services; Standard vs. Express workflows.
- **API Gateway**: REST, HTTP, and WebSocket APIs in front of Lambda and other backends; caching, throttling, and auth.
- Related runbooks: [Lambda](../../lambda/README.md), [Step Functions](../../step-functions/README.md), [API Gateway](../../api-gateway/README.md).

## Containers

- **ECS**: run containers on Fargate or EC2; tasks, services, and load balancing.
- Related runbook: [ECS](../../ecs/README.md).

## Security for developers

- IAM roles and policies for applications; least privilege.
- Encryption with KMS; secrets and parameters via Secrets Manager and SSM Parameter Store.
- Protecting data in transit (TLS) and at rest.
- Related runbooks: [IAM](../../iam/README.md), [KMS](../../kms/README.md), [Secrets Manager](../../secrets-manager/README.md).

## Study plan

1. Read the official DVA-C02 exam guide and note the task statements.
2. Practice hands-on with Lambda, API Gateway, DynamoDB, and the SDKs (boto3/CLI).
3. Build a small CI/CD pipeline with CodeCommit, CodeBuild, and CodePipeline.
4. Take official practice questions on AWS Skill Builder and review weak domains.
5. Recheck the exam guide before booking; AWS updates exam scope over time.

## Practice resources

Official practice questions and courses are available on AWS Skill Builder. Question-bank content (including third-party practice sets) is intentionally not published here.

## Related runbooks in this knowledge base

- [Lambda](../../lambda/README.md), [API Gateway](../../api-gateway/README.md), [Step Functions](../../step-functions/README.md)
- [ECS](../../ecs/README.md), [EKS](../../eks/README.md)
- [CloudFormation](../../cloudformation/README.md), [CDK](../../cdk/README.md)
- [S3](../../s3/README.md), [DynamoDB](../../dynamodb/README.md), [SQS](../../sqs/README.md), [SNS](../../sns/README.md)
- [CLI](../../cli/README.md), [SDK](../../sdk/README.md), [boto3](../../boto3/README.md)
- [IAM](../../iam/README.md), [KMS](../../kms/README.md), [Secrets Manager](../../secrets-manager/README.md)
