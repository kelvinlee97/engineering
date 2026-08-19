# AWS Data Pipeline - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Data Pipeline is a web service for automating the movement and transformation of data between AWS services and on-premises data sources. You define a pipeline definition with data-driven activities and dependencies; the pipeline schedules and runs tasks on EC2 instances. Note: AWS Data Pipeline is no longer available to new customers and is in maintenance mode; existing customers can continue using it, and AWS provides migration guidance for moving workloads to other services.

## Key concepts

- **Pipeline definition**: specifies the business logic of the data management (activities, schedules, preconditions, resources) in a definition file.
- **Pipeline**: schedules and runs tasks by provisioning EC2 instances to perform the defined work; you activate the pipeline to start it.
- **Task Runner**: polls for and performs tasks (for example, copying logs to S3, launching EMR clusters); AWS provides a Task Runner and you can write custom task runners.
- **Dependencies**: tasks can depend on the successful completion of previous tasks (for example, EMR analysis waits for the last day's data upload).
- **Pricing**: pay based on how often activities and preconditions are scheduled and where they run; a limited free tier applies to accounts less than 12 months old.

## Common operations (AWS CLI)

```bash
# Create and activate a pipeline
aws datapipeline create-pipeline --name log-archive --unique-id log-archive
aws datapipeline put-pipeline-definition --pipeline-id <pipeline-id> \
  --pipeline-definition file://definition.json
aws datapipeline activate-pipeline --pipeline-id <pipeline-id>

# Inspect pipelines and runs
aws datapipeline list-pipelines
aws datapipeline describe-pipelines --pipeline-ids <pipeline-id>
aws datapipeline describe-run --pipeline-id <pipeline-id> \
  --pipeline-object-id <object-id>

# Deactivate and delete
aws datapipeline deactivate-pipeline --pipeline-id <pipeline-id>
aws datapipeline delete-pipeline --pipeline-id <pipeline-id>
```

## Best practices

- Keep pipeline definitions versioned and test them on a subset of data before production schedules.
- Use preconditions to gate dependent activities instead of hard-coded timing.
- Monitor pipeline runs and set alarms for failed activities; inspect run logs in S3.
- Right-size the EC2 resource definitions for the work to control cost.
- Existing customers: plan migration to current services (for example, AWS Glue, Step Functions, EventBridge Scheduler) since the service is in maintenance mode and new customers cannot onboard.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Pipeline stuck | Check precondition status and dependent activity failures in the console/describe-run. |
| Task Runner not running | Verify the task runner is installed/running on the resource and can reach AWS. |
| Activity failed | Review the activity's log output in S3 and the role permissions for the resources used. |
| Definition rejected | Validate the pipeline definition file syntax and object references. |
| Cannot onboard new pipelines | The service is closed to new customers; use current AWS data orchestration services instead. |

## Limits

Pipelines per account, activities/preconditions per pipeline, and API request rates have quotas. See the AWS Data Pipeline endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Data Pipeline?](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/what-is-datapipeline.html)
- [Migrating workloads from AWS Data Pipeline](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/migrate.html)
- [AWS Data Pipeline pricing](https://aws.amazon.com/datapipeline/pricing/)
- [AWS CLI: datapipeline commands](https://docs.aws.amazon.com/cli/latest/reference/datapipeline/)
