# AWS Step Functions - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Step Functions is a serverless orchestration service. You define workflows (state machines) as a series of steps to coordinate Lambda functions, AWS services, and human approval flows. It supports visual debugging, retries, parallel processing, and long-running workflows.

## Key concepts

- **State machine (workflow)**: a JSON definition (Amazon States Language) of the workflow.
- **States**: Task, Choice, Parallel, Map, Wait, Pass, Succeed, and Fail.
- **Executions**: running instances of a state machine.
- **Standard workflows**: exactly-once execution, run up to 1 year, up to 2,000 executions/second; ideal for long-running, auditable processes.
- **Express workflows**: at-least-once execution, run up to 5 minutes, up to 100,000 executions/second; ideal for high-volume streaming/ingestion.
- **Integrations**: AWS SDK integrations call any AWS API; optimized integrations add patterns for specific services.
- **Integration patterns**: Request Response, Run a Job (`.sync`), and Wait for Callback (`.waitForTaskToken`, human-in-the-loop).
- **Error handling**: `Retry` and `Catch` per state; activities let external workers poll for tasks.
- **Distributed Map**: process large datasets by running concurrent child workflows.

## Common operations (AWS CLI)

```bash
# Create a state machine from a definition file
aws stepfunctions create-state-machine --name order-flow \
  --definition file://state-machine.json \
  --role-arn arn:aws:iam::123456789012:role/stepfunctions-role \
  --type STANDARD

# Start and monitor executions
aws stepfunctions start-execution --state-machine-arn <state-machine-arn> \
  --input '{"orderId":"123"}'
aws stepfunctions describe-execution --execution-arn <execution-arn>
aws stepfunctions list-executions --state-machine-arn <state-machine-arn>

# Inspect history and update
aws stepfunctions get-execution-history --execution-arn <execution-arn>
aws stepfunctions update-state-machine --state-machine-arn <state-machine-arn> \
  --definition file://state-machine-v2.json
```

```json
{
  "StartAt": "Validate",
  "States": {
    "Validate": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:us-east-1:123456789012:function:validate",
        "Payload.$": "$"
      },
      "Retry": [{"ErrorEquals": ["Lambda.ServiceException"], "MaxAttempts": 3}],
      "Next": "Approve"
    },
    "Approve": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:us-east-1:123456789012:function:approval",
        "Payload": {"taskToken.$": "$$.Task.Token"}
      },
      "Next": "Done"
    },
    "Done": {"Type": "Succeed"}
  }
}
```

## Best practices

- Choose Standard for auditable, long-running workflows and Express for high-volume, short workflows.
- Prefer AWS SDK/optimized integrations over custom Lambda glue code.
- Use `Retry` with backoff for transient errors and `Catch` for business failures.
- Model human approvals with `.waitForTaskToken` callbacks.
- Keep execution input/output small; store large payloads in S3 and pass references.
- Use CloudWatch metrics and X-Ray tracing for visibility; set alarms on `ExecutionsFailed`.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Execution fails | Inspect `get-execution-history` error output and the failed state. |
| Lambda not invoked | Check the state machine IAM role and Lambda permissions. |
| Callback never returns | Verify the worker sends the task token back to Step Functions. |
| Timeout errors | Adjust state timeout/`heartbeatSeconds` for long tasks. |
| High cost | Review state transitions; use Express workflows for high-volume workloads. |

## Limits

Executions per second, state transitions, execution history size, and payload sizes have quotas that differ between Standard and Express workflows. See the Service Quotas console for current values.

## Official references

- [What is Step Functions?](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon States Language specification](https://states-language.net/spec.html)
- [AWS Step Functions pricing](https://aws.amazon.com/step-functions/pricing/)
- [AWS CLI: stepfunctions commands](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/)
