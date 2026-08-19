# Amazon SageMaker AI - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon SageMaker AI (renamed from Amazon SageMaker on December 3, 2024) is a fully managed machine learning service for building, training, and deploying ML models in production. It provides managed algorithms, distributed training, notebooks and Studio, model deployment, and MLOps tools. The next generation of Amazon SageMaker is a unified platform for data, analytics, and AI that also includes Lakehouse, Data and AI Governance, SQL analytics, data processing, Unified Studio, and Amazon Bedrock.

## Key concepts

- **Legacy names unchanged**: the `sagemaker` API namespace, CLI commands, managed policies, endpoints, CloudFormation resources, service-linked roles, and console/doc URLs remain the same after the rename.
- **SageMaker AI**: build, train, and deploy ML and foundation models with fully managed infrastructure, tools, and workflows.
- **Studio / Unified Studio**: integrated development environments for data preparation, experimentation, and MLOps.
- **Training**: managed algorithms and bring-your-own algorithms/frameworks with flexible distributed training options.
- **Deployment**: deploy models to secure, scalable hosted endpoints with a few steps from the console; supports real-time, serverless, and batch inference.
- **Next-generation SageMaker platform**: unified data access (Lakehouse across S3 and Redshift), data governance (Catalog built on DataZone), SQL analytics (Redshift), data processing (Athena, EMR, Glue), and Bedrock for generative AI.

## Common operations (AWS CLI)

```bash
# Create a notebook instance and start it
aws sagemaker create-notebook-instance --notebook-instance-name ml-env \
  --instance-type ml.t3.medium --role-arn arn:aws:iam::123456789012:role/sagemaker-role
aws sagemaker start-notebook-instance --notebook-instance-name ml-env

# Train a model
aws sagemaker create-training-job --training-job-name my-job \
  --algorithm-specification file://algo.json \
  --role-arn arn:aws:iam::123456789012:role/sagemaker-role \
  --input-data-config file://inputs.json \
  --output-data-config file://output.json \
  --resource-config '{"InstanceType":"ml.m5.large","InstanceCount":1}'

# Deploy an endpoint
aws sagemaker create-endpoint-config --endpoint-config-name my-config \
  --production-variants file://variant.json
aws sagemaker create-endpoint --endpoint-name my-endpoint \
  --endpoint-config-name my-config
aws sagemaker list-endpoints
```

## Best practices

- Use SageMaker Studio/Unified Studio for the full workflow and keep experiments tracked and reproducible.
- Store training data in S3 with versioning; use managed feature stores for feature reuse.
- Choose the smallest sufficient instance and use managed spot training for cost savings.
- Set up model monitoring (data quality, drift) for production endpoints and deploy via CI/CD pipelines.
- Secure notebooks/endpoints with IAM, VPC, and KMS encryption; use SageMaker Role Manager for least-privilege roles.
- Evaluate foundation-model use cases with Amazon Bedrock within the same unified platform where appropriate.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Training job fails | Review the job logs in CloudWatch, input data format, and IAM role permissions. |
| Endpoint creation fails | Check the model artifact path, instance type, and the production variant configuration. |
| Notebook cannot access S3 | Verify the notebook role and instance profile permissions. |
| Slow inference | Right-size the endpoint instance, use serverless inference for spiky traffic, or batch inference for non-real-time loads. |
| Renamed service confusion | The rename to SageMaker AI does not change the `sagemaker` namespaces or existing features. |

## Limits

Notebook instances, training jobs, endpoints, and model sizes per account have quotas. See the Amazon SageMaker endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon SageMaker AI?](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [Amazon SageMaker endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/sagemaker.html)
- [Amazon SageMaker pricing](https://aws.amazon.com/sagemaker/pricing/)
- [AWS CLI: sagemaker commands](https://docs.aws.amazon.com/cli/latest/reference/sagemaker/)
