# Amazon Elastic Container Registry (ECR) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Elastic Container Registry (Amazon ECR) is a managed container image registry. It supports private repositories with IAM-based access and public repositories, and stores Docker, Open Container Initiative (OCI) images, and OCI-compatible artifacts.

## Key concepts

- **Registry and repository**: a registry is per-account per-Region; repositories hold image versions.
- **Image scanning**: identify software vulnerabilities; scan on push (basic) or enhanced scanning with Amazon Inspector.
- **Lifecycle policies**: automate cleanup of unused images by age or count; test rules before applying.
- **Replication**: cross-Region and cross-account registry replication.
- **Pull-through cache**: cache images from upstream registries into your private ECR.
- **Managed signing**: automatically sign images on push with cryptographic signatures.
- **Repository policies**: resource-based IAM policies controlling who can pull/push.

## Common operations (AWS CLI)

```bash
# Create a repository with scan-on-push
aws ecr create-repository --repository-name app \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256

# Authenticate Docker to the registry
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Tag, push, and inspect
docker tag app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest
aws ecr describe-images --repository-name app

# Lifecycle policy
aws ecr put-lifecycle-policy --repository-name app \
  --lifecycle-policy-text file://lifecycle.json

# Scan and get findings
aws ecr start-image-scan --repository-name app --image-id imageTag=latest
aws ecr describe-image-scan-findings --repository-name app --image-id imageTag=latest

# Replication (registry setting)
aws ecr put-replication-configuration --replication-configuration file://replication.json
```

## Best practices

- Use private repositories and IAM/repository policies; never make production images public.
- Enable scan on push (enhanced scanning with Inspector for deep coverage) and fix critical/high findings before deploy.
- Use lifecycle policies to prune untagged and old images; test rules first.
- Use immutable tags to prevent overwrites of deployed images.
- Replicate images across Regions for DR and to avoid cross-Region pull latency.
- Sign images for supply-chain integrity where compliance requires it.
- Use pull-through cache rules for upstream registries you depend on.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| `denied: Your Authorization Token has expired` | Re-run `aws ecr get-login-password` and `docker login`. |
| Push/pull access denied | Check repository policy and IAM permissions (`ecr:BatchGetImage`, `ecr:PutImage`). |
| Scan shows no results | Verify scan configuration, image pushed after enabling, and region. |
| Images not cleaned up | Check lifecycle policy rules and test with `--dry-run` style preview. |
| Replication not working | Verify registry settings, destination account/region, and IAM. |

## Limits

Repositories per registry, image size, and API rates have quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon Elastic Container Registry?](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Amazon ECR service quotas](https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html)
- [Amazon ECR pricing](https://aws.amazon.com/ecr/pricing/)
- [AWS CLI: ecr commands](https://docs.aws.amazon.com/cli/latest/reference/ecr/)
