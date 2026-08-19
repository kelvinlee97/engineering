# AWS Serverless Application Model (SAM) & Serverless Application Repository - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Serverless Application Model (AWS SAM) is an open-source infrastructure-as-code framework for building serverless applications. It extends CloudFormation with simplified syntax for Lambda functions, API Gateway APIs, DynamoDB tables, and other serverless resources, and provides the SAM CLI for local development, testing, building, and deployment. The AWS Serverless Application Repository (SAR) is a catalog for publishing and deploying serverless applications using SAM templates.

## Key concepts

- **SAM template**: a CloudFormation template with SAM shorthand (`AWS::Serverless::Function`, `AWS::Serverless::Api`, `AWS::Serverless::SimpleTable`, etc.); SAM transforms it into standard CloudFormation resources.
- **SAM CLI**: commands for the full lifecycle — `sam init`, `sam build`, `sam local invoke/start-api` (local testing), `sam deploy`, `sam sync` (continuous sync), and Terraform support for local Lambda debugging.
- **SAM connectors**: declare resource-to-resource permissions in the template; SAM generates the required IAM permissions.
- **Policies**: simplified IAM policy templates (for example, S3 read/write, DynamoDB CRUD) attached to functions.
- **Serverless Application Repository**: publish applications publicly or privately (shared within teams/orgs), deploy with a few clicks from the Lambda console, and version apps with metadata (readme, source code).
- **CI/CD**: deploy SAM templates through CodePipeline for staging/production environments.

## Common operations (SAM CLI)

```bash
# Initialize, build, and test locally
sam init --runtime python3.12 --name my-app
sam build
sam local invoke MyFunction --event event.json

# Deploy (guided) and sync
sam deploy --guided
sam sync --stack-name my-app --watch

# Publish to the Serverless Application Repository
sam publish -t template.yaml --region us-east-1
```

## Best practices

- Keep SAM templates in code with the application and version them; use `sam build` for deterministic packaging.
- Test locally with `sam local` and add integration tests before deployment.
- Use connectors and policy templates to scope IAM permissions precisely; avoid broad policies.
- Use `sam sync` during development and `sam deploy` with change sets for production.
- Set up CI/CD (CodePipeline + CodeBuild) for serverless applications; use stages with approvals.
- For SAR, publish with complete metadata (readme, source URL, license) and keep versions immutable.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| `sam build` fails | Check runtime/package dependencies and the build environment (Docker for native modules). |
| Local invoke errors | Verify the event JSON, environment variables, and IAM role emulation. |
| Deploy fails | Review CloudFormation events; check template transform (`AWS::Serverless-2016-10-31`) and permissions. |
| SAR publish rejected | Fix metadata validation (semantic version, readme, source URL) and retry. |
| Permissions too broad | Replace generic policies with SAM policy templates or connectors. |

## Limits

SAM templates are subject to CloudFormation limits; SAR has application/version limits per account and Region. See the AWS SAM and Serverless Application Repository documentation for current values.

## Official references

- [What is the AWS Serverless Application Model?](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS Serverless Application Repository developer guide](https://docs.aws.amazon.com/serverlessrepo/latest/devguide/what-is-serverlessrepo.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
- [AWS SAM pricing](https://aws.amazon.com/serverless/sam/pricing/)
