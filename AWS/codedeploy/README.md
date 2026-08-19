# AWS CodeDeploy - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS CodeDeploy automates application deployments to EC2 instances, on-premises servers, Lambda functions, and Amazon ECS services. You package your application with an AppSpec file; CodeDeploy rolls out the revision, tracks health, and can stop and roll back on errors. It supports in-place and blue/green deployment strategies.

## Key concepts

- **Compute platforms**: EC2/On-Premises, AWS Lambda, and Amazon ECS.
- **Application and deployment group**: an application is a collection of deployment groups; a deployment group defines the target instances (tags, ASG) or the Lambda/ECS service configuration.
- **Revision**: an application bundle plus an AppSpec file; stored in S3 or GitHub.
- **AppSpec**: the YAML/JSON file that defines lifecycle event hooks (BeforeInstall, AfterInstall, ApplicationStart, ValidateService, etc.) and the deployment behavior per platform.
- **Deployment types**:
  - **In-place** (EC2/On-Premises only): instances are updated one group at a time with health tracking.
  - **Blue/green**: new instances/Lambda versions/ECS task sets receive traffic according to canary, linear, or all-at-once configurations.
- **CodeDeploy agent**: installed on EC2/on-premises instances to poll for and run deployments.
- **Deployment configuration**: rules for speed and the minimum number of healthy instances during deployment.

## Common operations (AWS CLI)

```bash
# Create application, deployment group, and push a revision
aws codedeploy create-application --application-name web-app \
  --compute-platform Server
aws codedeploy create-deployment-group --application-name web-app \
  --deployment-group-name prod --service-role-arn arn:aws:iam::123456789012:role/codedeploy-role \
  --ec2-tag-filters Key=env,Type=KEY_AND_VALUE,Value=prod
aws deploy push --application-name web-app --s3-location s3://deploy-bucket/web-app.zip \
  --source .

# Start and monitor a deployment
aws deploy create-deployment --application-name web-app \
  --deployment-group-name prod \
  --s3-location bucket=deploy-bucket,key=web-app.zip,bundleType=zip
aws deploy get-deployment --deployment-id <deployment-id>

# Roll back
aws deploy stop-deployment --deployment-id <deployment-id> --auto-rollback-enabled
```

## Best practices

- Keep deployments small and frequent; use blue/green for critical workloads to minimize risk and enable fast rollback.
- Define health checks and validation hooks (ValidateService) so unhealthy deployments roll back automatically.
- Use IAM roles for the CodeDeploy agent and the service; encrypt revision bundles in S3.
- Store deployment configuration as code (CodePipeline + CodeDeploy) and test in staging first.
- Monitor deployment events and alarms; alert on Failed/Stopped deployments.
- For Lambda/ECS, choose canary/linear traffic shifts and verify metrics before full rollout.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Instance deployment fails | Check the CodeDeploy agent logs (`/var/log/aws/codedeploy-agent`), IAM instance role, and S3 revision access. |
| Hooks not running | Verify the AppSpec file path, permissions, and script exit codes (non-zero fails the hook). |
| Deployment stuck | Check deployment configuration (healthy instance minimum), load balancer deregistration, and agent connectivity. |
| Rollback not triggered | Confirm auto-rollback settings and alarm/validation criteria. |
| ECS/Lambda traffic not shifting | Verify the target group/listener configuration and traffic shifting settings. |

## Limits

Applications, deployment groups, concurrent deployments, and revision sizes per account have quotas. See the AWS CodeDeploy quotas page and Service Quotas console for current values.

## Official references

- [What is AWS CodeDeploy?](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)
- [AWS CodeDeploy quotas](https://docs.aws.amazon.com/codedeploy/latest/userguide/limits.html)
- [AWS CodeDeploy pricing](https://aws.amazon.com/codedeploy/pricing/)
- [AWS CLI: codedeploy commands](https://docs.aws.amazon.com/cli/latest/reference/codedeploy/)
