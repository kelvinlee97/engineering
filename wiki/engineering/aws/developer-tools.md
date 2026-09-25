---
type: Service
title: AWS developer tools
description: The command line, SDKs, infrastructure-as-code frameworks, cloud IDE, and front-end hosting tools for building on AWS.
tags: [aws, developer-tools]
sources:
  - id: aws-cli
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cli/README.md
    title: "AWS CLI - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-sdk
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sdk/README.md
    title: "AWS SDKs and Tools - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-boto3
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/boto3/README.md
    title: "boto3 (AWS SDK for Python) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cdk
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cdk/README.md
    title: "AWS Cloud Development Kit (CDK) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-sam
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/sam/README.md
    title: "AWS Serverless Application Model (SAM) & Serverless Application Repository - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-solutions-constructs
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-constructs/README.md
    title: "AWS Solutions Constructs - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cloud9
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloud9/README.md
    title: "AWS Cloud9 - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-amplify
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/amplify/README.md
    title: "AWS Amplify - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These are the tools developers use to talk to AWS and define infrastructure: the CLI and SDKs for API calls, CDK and SAM for infrastructure as code on top of [CloudFormation](operations-tooling.md), and hosted environments for writing and shipping apps.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS CLI](#aws-cli) | The AWS CLI is a thin shell layer over the same APIs the console uses |
| [AWS SDKs and Tools](#aws-sdks-and-tools) | AWS SDKs are language-specific libraries for calling AWS service APIs from your application code |
| [boto3 (AWS SDK for Python)](#boto3-aws-sdk-for-python) | boto3 resolves credentials once, through a fixed fallback chain, before any client call |
| [AWS Cloud Development Kit (CDK)](#aws-cloud-development-kit-cdk) | CDK never talks to AWS directly |
| [AWS Serverless Application Model (SAM) & Serverless Application Repository](#aws-serverless-application-model-sam--serverless-application-repository) | A SAM template is CloudFormation with serverless shorthand that the SAM transform expands into standard resources |
| [AWS Solutions Constructs](#aws-solutions-constructs) | AWS Solutions Constructs is an open-source extension of the AWS Cloud Development Kit (AWS CDK) |
| [AWS Cloud9](#aws-cloud9) | Cloud9 is a browser-based IDE glued to one compute resource per environment |
| [AWS Amplify](#aws-amplify) | Amplify splits into two mostly independent halves |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS CLI

The AWS CLI is a thin shell layer over the same APIs the console uses: it resolves credentials from a fixed chain and a chosen profile before every call, so most CLI problems are really profile/credential problems, not command problems. The AWS Command Line Interface (AWS CLI) is an open source tool for interacting with AWS services from your shell. Version 2 is the current major version and supports all the latest features; it is installed with the official bundled installer. The CLI exposes the same service APIs as the console, plus higher-level customizations for several services.

Key points:

- Credentials chain: the CLI resolves credentials from CLI options, environment variables, shared `~/.aws/credentials`, IAM roles (EC2/EKS/ECS), SSO, and container roles, in order.
- Profiles: named credential/region sets in `~/.aws/config` and `~/.aws/credentials`; select with `--profile` or `AWS_PROFILE`.
- Regions and output: set default region and output (`json`, `yaml`, `text`, `table`) with `aws configure`.
- SSO: `aws configure sso` sets up IAM Identity Center sessions; `aws sso login` refreshes them.
- Query and filtering: `--query` (JMESPath) and `--output` shape command results for scripting.

Practices:

- Never put long-term access keys in scripts or source code; use IAM roles or SSO.
- Use named profiles per environment/account and separate roles with least privilege.
- Pin and upgrade the CLI: v1 is in maintenance and lacks v2 features; use the official installer.

| Symptom | Check |
| --- | --- |
| `Unable to locate credentials` | Configure credentials/profile or set environment variables; check the credentials chain order. |
| `AccessDenied` | Verify the IAM policy and that you're using the intended profile/role. |
| Expired SSO session | Run `aws sso login --profile <profile>` again. |
| Wrong region results | Set `--region` explicitly or fix the profile default. |

The CLI itself has no service quotas; API rate limits and quotas apply per service. See the Service Quotas console for service-specific values.[^aws-cli]


## AWS SDKs and Tools

AWS SDKs are language-specific libraries for calling AWS service APIs from your application code: Python (boto3), Java, JavaScript (v3), Go, . NET, Ruby, PHP, C++, and more. SDKs handle request signing, retries, and error mapping. The AWS SDKs and Tools Reference Guide documents the shared configuration, credentials, and maintenance policies across all SDKs and tools.

Key points:

- Credentials resolution: the same chain as the CLI - env vars, shared config/credentials files, IAM roles, SSO, container credentials.
- Signature Version 4: SDKs sign every request with your credentials; temporary credentials from STS are supported.
- Retries and timeouts: SDKs retry transient failures by default; configure retry mode (`standard`, `adaptive`, `legacy`) per SDK.
- Identity providers: EC2 instance roles, EKS IRSA, ECS task roles, Lambda execution roles, and IAM Identity Center SSO.
- AWS Common Runtime (CRT): shared libraries that provide HTTP/2, event streams, and retry/checksum implementations to several SDKs.

Practices:

- Prefer IAM roles over static keys: EC2 instance profiles, EKS IRSA, ECS/Lambda execution roles, or SSO.
- Use short-lived STS credentials where static keys are unavoidable (CI/CD secrets managers).
- Set timeouts, retry mode, and max retries explicitly for latency-sensitive paths.

| Symptom | Check |
| --- | --- |
| Credentials not found in code | Check env vars, shared files, and role configuration; verify the resolution order. |
| Intermittent failures | Configure retry mode and exponential backoff; check throttling and quotas. |
| Clock skew / signature errors | Verify system time is synchronized (NTP). |
| Regional endpoints wrong | Set region in config/credential chain or per client. |

SDKs have no service quotas; service APIs and IAM policies define what your code can do. See the Service Quotas console for service-specific values.[^aws-sdk]


## boto3 (AWS SDK for Python)

boto3 resolves credentials once, through a fixed fallback chain, before any client call: so a working request usually means the chain, not the call, is misconfigured when it fails. boto3 is the AWS SDK for Python. It provides low-level service clients (a nearly 1:1 mapping to service APIs), higher-level resource abstractions for some services, and core features like pagination, waiters, retries, and multi-session credential handling.

Key points:

- Client: low-level interface; `boto3.client('s3')` returns a client whose methods map to API operations.
- Resource: higher-level object interface; `boto3.resource('s3')` provides collections and attributes (available for a subset of services).
- Session: manages configuration and credentials; `boto3.session.Session()` or the default module-level session.
- Credentials chain: env vars, shared credentials/config files, IAM roles, SSO, container credentials.
- Paginators: handle multi-page API responses with `client.get_paginator(...)`.

Practices:

- Prefer IAM roles and SSO over hard-coded keys; never commit credentials.
- Reuse clients/sessions instead of creating them per call; boto3 manages connection pooling.
- Use paginators for list APIs and waiters instead of sleep loops.

| Symptom | Check |
| --- | --- |
| `NoCredentialsError` | Check the credential chain: env vars, shared files, roles. |
| `ClientError: AccessDenied` | Verify the IAM policy and the role/profile in use. |
| Slow list operations | Use paginators with `PageSize`, filters, and narrow prefixes. |
| Throttling (`ThrottlingException`) | Increase retry attempts/backoff; request higher quotas if legitimate. |

boto3 has no service quotas; service API limits apply. See the Service Quotas console for service-specific values.[^aws-boto3]


## AWS Cloud Development Kit (CDK)

CDK never talks to AWS directly: it compiles your code into a CloudFormation template, and CloudFormation does the actual provisioning; every CDK command is really a step before or around a CloudFormation deployment. The AWS Cloud Development Kit (AWS CDK) is an open source framework for defining cloud infrastructure in code (TypeScript, JavaScript, Python, Java, C#/.NET, or Go) and provisioning it through AWS CloudFormation. CDK v2 is the current major version; v1 entered maintenance on June 1, 2022 and ended support on June 1, 2023.

Key points:

- Construct: the basic building block; L1 constructs map to CloudFormation resources, L2 constructs add sensible defaults, L3 constructs are patterns.
- Stack: a unit of deployment that maps to a CloudFormation stack.
- App: a container of one or more stacks; the entry point of a CDK project.
- Synthesis: `cdk synth` converts your app into a CloudFormation template.
- Bootstrap: `cdk bootstrap` provisions the staging bucket and roles a Region needs for deployment.

Practices:

- Use CDK v2 and pin construct library versions; track the maintenance policy.
- Start from L2 constructs for secure defaults; drop to L1 only when you need an exact property.
- Split applications into stacks with clear dependency boundaries (state, networking, app).

| Symptom | Check |
| --- | --- |
| `BootstrapError` | Run `cdk bootstrap` for the target account/Region with the right credentials. |
| Stack update failed | Review the CloudFormation event log; fix resource constraints and redeploy. |
| Asset upload fails | Verify S3 bucket policy for the staging bucket and IAM permissions. |
| Construct version mismatch | Keep the CDK CLI and libraries on compatible versions. |

CloudFormation quotas apply (for example, template size and resource counts per stack). See the Service Quotas console for current values.[^aws-cdk]


## AWS Serverless Application Model (SAM) & Serverless Application Repository

A SAM template is CloudFormation with serverless shorthand that the SAM transform expands into standard resources; the SAM CLI takes that same template through build, local test, and deploy, and SAR is simply a catalog for sharing the finished template. AWS Serverless Application Model (AWS SAM) is an open-source infrastructure-as-code framework for building serverless applications. It extends CloudFormation with simplified syntax for Lambda functions, API Gateway APIs, DynamoDB tables, and other serverless resources, and provides the SAM CLI for local development, testing, building, and deployment. The AWS Serverless Application Repository (SAR) is a catalog for publishing and deploying serverless applications using SAM templates.

Key points:

- SAM template: a CloudFormation template with SAM shorthand (`AWS::Serverless::Function`, `AWS::Serverless::Api`, `AWS::Serverless::SimpleTable`, etc.); SAM transforms it into standard CloudFormation resources.
- SAM CLI: commands for the full lifecycle, including `sam init`, `sam build`, `sam local invoke/start-api` (local testing), `sam deploy`, `sam sync` (continuous sync), and Terraform support for local Lambda debugging.
- SAM connectors: declare resource-to-resource permissions in the template; SAM generates the required IAM permissions.
- Policies: simplified IAM policy templates (for example, S3 read/write, DynamoDB CRUD) attached to functions.
- Serverless Application Repository: publish applications publicly or privately (shared within teams/orgs), deploy with a few clicks from the Lambda console, and version apps with metadata (readme, source code).

Practices:

- Keep SAM templates in code with the application and version them; use `sam build` for deterministic packaging.
- Test locally with `sam local` and add integration tests before deployment.
- Use connectors and policy templates to scope IAM permissions precisely; avoid broad policies.

| Symptom | Check |
| --- | --- |
| `sam build` fails | Check runtime/package dependencies and the build environment (Docker for native modules). |
| Local invoke errors | Verify the event JSON, environment variables, and IAM role emulation. |
| Deploy fails | Review CloudFormation events; check template transform (`AWS::Serverless-2016-10-31`) and permissions. |
| SAR publish rejected | Fix metadata validation (semantic version, readme, source URL) and retry. |

SAM templates are subject to CloudFormation limits; SAR has application/version limits per account and Region. See the AWS SAM and Serverless Application Repository documentation for current values.[^aws-sam]


## AWS Solutions Constructs

AWS Solutions Constructs is an open-source extension of the AWS Cloud Development Kit (AWS CDK). It provides pre-built, well-architected patterns that combine AWS services for common use cases, so you can define infrastructure with familiar programming languages and existing development workflows.

Key points:

- Constructs: reusable, well-architected patterns that perform common actions across AWS services (for example, API Gateway + Lambda + DynamoDB, S3 + Lambda).
- Languages: TypeScript, JavaScript, Python, and Java are supported at this time.
- Built on CDK: constructs are CDK construct libraries; use logic, object-oriented modeling, and code review workflows.
- Catalog: browse the full construct catalog to find patterns for your use case.
- Reuse and sharing: organize solutions into logical modules, share them as libraries within your team/company, and publish them.

Practices:

- Prefer constructs for common, well-tested patterns instead of wiring services manually.
- Review construct options and defaults for security (encryption, logging) and cost before deploying.
- Keep construct libraries updated; follow upstream releases for fixes and new patterns.

| Symptom | Check |
| --- | --- |
| Construct not found | Verify the package name/language and the construct catalog for availability. |
| Synthesis fails | Check the CDK version, construct version compatibility, and TypeScript/Python syntax. |
| Unexpected resources created | Review construct defaults and props; override with your own settings. |
| Region-specific errors | Confirm the construct's services are available in your target Region. |

Constructs are code libraries; quotas depend on the AWS services used. See the construct documentation for each pattern and the service runbooks in this knowledge base for quotas.[^aws-solutions-constructs]


## AWS Cloud9

Cloud9 is a browser-based IDE glued to one compute resource per environment: either an EC2 instance it manages for you, or your own server reached over SSH, and it is now a maintenance-mode service: existing environments keep working, but no new customers can start. AWS Cloud9 is a cloud-based integrated development environment (IDE) accessed from a web browser. It provides code editing, debugging, a built-in terminal, and direct integration with AWS services. Cloud9 is no longer available to new customers; existing customers can continue to use the service as normal.

Practices:

- Note the current lifecycle: new customer onboarding is closed; plan alternatives (for example, IDE toolkits + EC2/CloudShell) for new projects.
- For existing environments, use EC2 environments with a managed instance and keep the IDE/instance patched.
- Attach an IAM instance profile with least privilege; never store long-term keys in the environment.

| Symptom | Check |
| --- | --- |
| Cannot open IDE | Check environment status and browser/network access to the environment URL. |
| EC2 environment slow | Right-size the instance type or stop/restart the environment. |
| Permissions errors | Verify the instance profile/role policies for the services you use. |
| SSH environment unreachable | Check the server SSH config, keys, and security group rules. |

Environments per account and EC2 environment instance sizes are subject to quotas. See the Service Quotas console for current values.[^aws-cloud9]


## AWS Amplify

Amplify splits into two mostly independent halves: Hosting, a Git-triggered CI/CD pipeline to the AWS CDN, and a backend generation (Gen 1 CLI vs. Gen 2 `ampx`), which turns TypeScript resource definitions into cloud infrastructure. AWS Amplify helps you build and host full-stack web and mobile applications on AWS. Amplify Hosting provides a Git-based workflow with continuous deployment to the AWS global CDN. Amplify Gen 2 is the current code-first backend experience: you define data, auth, and functions in TypeScript and manage them with `ampx`. Gen 1 apps use the legacy Amplify CLI and Studio.

Key points:

- Amplify Hosting: connects a Git repo (GitHub, Bitbucket, GitLab, or CodeCommit) and deploys the frontend with CI/CD.
- Feature branches: each connected branch becomes an environment (production/staging) with its own backend.
- PR previews: preview apps for pull requests; atomic deployments and custom domains included.
- Amplify Gen 2 backend: TypeScript-defined `data`, `auth`, `storage`, and `functions` resources with automatic cloud infrastructure.
- Amplify Libraries: client SDKs (JS, React, Swift, Android, Flutter) that connect to the backend.

Practices:

- Use Amplify Gen 2 for new projects; Gen 1 is legacy and only for existing apps.
- Connect branches per environment and protect production branches; use PR previews for review.
- Define auth rules in the backend schema and test access patterns with the sandbox.

| Symptom | Check |
| --- | --- |
| Build fails | Check build logs, dependency versions, and environment variables. |
| Backend not updated | Run `ampx deploy` (or `amplify push` for Gen 1) and redeploy the frontend. |
| Auth issues | Verify auth rules, user pool/client config, and client library versions. |
| Custom domain not resolving | Check DNS records and the certificate status in Amplify Hosting. |

Build minutes, hosting storage/transfer, and backend resource usage have account limits; see AWS Amplify pricing for current tiers and quotas.[^aws-amplify]


## Related

- [CI/CD on AWS](ci-cd.md)
- [Operations tooling](operations-tooling.md)
- [Domain index](index.md)

[^aws-cli]: [AWS CLI - Runbook & Reference](../../sources/aws-cli.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cli/README.md)
[^aws-sdk]: [AWS SDKs and Tools - Runbook & Reference](../../sources/aws-sdk.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/sdk/README.md)
[^aws-boto3]: [boto3 (AWS SDK for Python) - Runbook & Reference](../../sources/aws-boto3.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/boto3/README.md)
[^aws-cdk]: [AWS Cloud Development Kit (CDK) - Runbook & Reference](../../sources/aws-cdk.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cdk/README.md)
[^aws-sam]: [AWS Serverless Application Model (SAM) & Serverless Application Repository - Runbook & Reference](../../sources/aws-sam.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/sam/README.md)
[^aws-solutions-constructs]: [AWS Solutions Constructs - Runbook & Reference](../../sources/aws-solutions-constructs.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-constructs/README.md)
[^aws-cloud9]: [AWS Cloud9 - Runbook & Reference](../../sources/aws-cloud9.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cloud9/README.md)
[^aws-amplify]: [AWS Amplify - Runbook & Reference](../../sources/aws-amplify.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/amplify/README.md)
