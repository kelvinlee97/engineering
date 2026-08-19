# AWS Cloud Development Kit (CDK) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

The AWS Cloud Development Kit (AWS CDK) is an open source framework for defining cloud infrastructure in code (TypeScript, JavaScript, Python, Java, C#/.NET, or Go) and provisioning it through AWS CloudFormation. CDK v2 is the current major version; v1 entered maintenance on June 1, 2022 and ended support on June 1, 2023.

## Key concepts

- **Construct**: the basic building block; L1 constructs map to CloudFormation resources, L2 constructs add sensible defaults, L3 constructs are patterns.
- **Stack**: a unit of deployment that maps to a CloudFormation stack.
- **App**: a container of one or more stacks; the entry point of a CDK project.
- **Synthesis**: `cdk synth` converts your app into a CloudFormation template.
- **Bootstrap**: `cdk bootstrap` provisions the staging bucket and roles a Region needs for deployment.
- **Toolkit (CDK CLI)**: commands to synthesize, diff, deploy, and destroy stacks.
- **Asset**: local files (bundled code, images) uploaded during deployment.

## Common operations (AWS CLI)

```bash
# Initialize a project (Python example)
cdk init app --language python

# Install dependencies and bootstrap the target account/Region
python -m pip install -r requirements.txt
cdk bootstrap aws://123456789012/us-east-1

# Synthesize and inspect the CloudFormation template
cdk synth
cdk diff

# Deploy / destroy
cdk deploy
cdk deploy --profile dev
cdk destroy

# List stacks in the app
cdk list
```

```python
# app.py (Python, CDK v2)
from aws_cdk import App, Stack, aws_s3 as s3

class StorageStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        s3.Bucket(self, "DataBucket",
                  versioned=True,
                  encryption=s3.BucketEncryption.S3_MANAGED,
                  enforce_ssl=True)

app = App()
StorageStack(app, "StorageStack")
app.synth()
```

## Best practices

- Use CDK v2 and pin construct library versions; track the maintenance policy.
- Start from L2 constructs for secure defaults; drop to L1 only when you need an exact property.
- Split applications into stacks with clear dependency boundaries (state, networking, app).
- Write tests and run `cdk diff` in CI before deploy; use pipelines (CodePipeline) for repeatable delivery.
- Use `cdk bootstrap` once per account/Region and manage bootstrap permissions tightly.
- Avoid storing secrets in code; use Secrets Manager/SSM Parameters and grant access via IAM.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| `BootstrapError` | Run `cdk bootstrap` for the target account/Region with the right credentials. |
| Stack update failed | Review the CloudFormation event log; fix resource constraints and redeploy. |
| Asset upload fails | Verify S3 bucket policy for the staging bucket and IAM permissions. |
| Construct version mismatch | Keep the CDK CLI and libraries on compatible versions. |
| Resource replacement on update | Check CloudFormation replacement behavior; plan state changes explicitly. |

## Limits

CloudFormation quotas apply (for example, template size and resource counts per stack). See the Service Quotas console for current values.

## Official references

- [What is the AWS CDK?](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [AWS CDK API reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)
- [AWS CDK Workshop](https://cdkworkshop.com/)
