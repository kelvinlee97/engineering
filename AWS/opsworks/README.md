# AWS OpsWorks - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS OpsWorks (OpsWorks Stacks) was a configuration management service that used Chef to automate the configuration and operation of EC2 instances, including layers, stacks, auto-healing, and deployments. OpsWorks Stacks reached end of life: it stopped accepting new customers and was discontinued for all customers on May 26, 2024. Do not build new workloads on OpsWorks.

## Key concepts (historical)

- **Stack**: a container for resources and configuration that belongs to one Region.
- **Layer**: a group of EC2 instances with the same configuration and recipes (for example, app, web, database layers).
- **Recipes and cookbooks**: Chef scripts that configure instances; OpsWorks ran them during lifecycle events (setup, configure, deploy, undeploy, shutdown).
- **Auto healing and scaling**: OpsWorks replaced failed instances and scaled layers with load-based or time-based instances.
- **Deployments**: deploys updated application code to instances in a layer.
- **Status**: service discontinued on May 26, 2024 for new and existing customers; AWS recommends migrating workloads to other solutions.

## Common operations

No new OpsWorks resources can be created. If you still operate legacy resources, AWS's end-of-life guidance applies; plan migration using current alternatives:

```bash
# Manage the underlying resources directly with current services
aws ec2 describe-instances
aws cloudformation list-stacks
aws ssm describe-instance-information
aws codedeploy list-applications
```

## Migration options

- **Configuration management**: use AWS Systems Manager (Run Command, State Manager, Patch Manager) instead of Chef lifecycle recipes.
- **Infrastructure as code**: AWS CloudFormation or Terraform for stack/layer-style templates; EC2 user data or custom AMIs for bootstrap.
- **Deployments**: AWS CodeDeploy or CI/CD pipelines (CodePipeline) for application releases.
- **Containers**: Amazon ECS/EKS or AWS App Runner for containerized workloads that OpsWorks may have hosted.
- **Managed platforms**: Elastic Beanstalk for web/worker applications that previously used OpsWorks stacks.

## Best practices

- Do not start new projects on OpsWorks; it is discontinued.
- Inventory legacy OpsWorks-managed instances and map them to current services (SSM for operations, CloudFormation for infrastructure, CodeDeploy for deployment).
- Test the migration on a subset of workloads before decommissioning the old stacks.
- Remove unused OpsWorks IAM roles and resources after migration.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cannot create a stack | Expected: OpsWorks Stacks is discontinued (May 26, 2024); use current configuration management services. |
| Legacy stacks still running | Migrate workloads to Systems Manager, CloudFormation, CodeDeploy, and container/managed platforms; then decommission. |
| Chef recipes in use | Port recipes to SSM documents (or user data), and application deployments to CodeDeploy. |

## Limits

OpsWorks Stacks is discontinued; no new resources can be created. See the AWS OpsWorks end-of-life guidance and current service quotas for migration targets.

## Official references

- [AWS OpsWorks Stacks end of life notice](https://docs.aws.amazon.com/opsworks/latest/userguide/opsworks-stacks-eol.html)
- [AWS Systems Manager user guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [AWS CodeDeploy user guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)
