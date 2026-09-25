---
type: Service
title: AWS CloudFormation
description: "AWS's infrastructure as code: templates become stacks, and every update is a computed change set applied as one unit."
tags: [aws, infrastructure-as-code]
sources:
  - id: aws-cloudformation
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudformation/README.md
    title: "AWS CloudFormation - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

CloudFormation provisions AWS resources from YAML or JSON templates as one unit, a stack, resolving dependencies. Every update is really "compute a change set, then execute it"; the change set exists so the diff can be reviewed first, and skipping to `update-stack` removes only that review.[^aws-cloudformation]

## Concepts

- Stacks, stack sets (many accounts and Regions), nested stacks, drift detection.[^aws-cloudformation]
- Templates up to 51,200 bytes inline, 1 MB from S3.[^aws-cloudformation]

## Practices

- Review change sets for production; set `DeletionPolicy` and `UpdateReplacePolicy` on stateful resources.[^aws-cloudformation]
- Parameters and Secrets Manager references instead of hard-coded values; be deliberate with `CAPABILITY_IAM`.[^aws-cloudformation]
- Separate stacks by lifecycle (network, data, application) and run drift detection.[^aws-cloudformation]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Create fails and rolls back | `describe-stack-events`: the first `CREATE_FAILED` is the root cause |
| IAM resource errors | `--capabilities CAPABILITY_NAMED_IAM` |
| Cross-stack dependency errors | Output names and `Fn::ImportValue` |

As tabled in the note.[^aws-cloudformation]

## Related

- [Safe change procedure](../operations/safe-change-procedure.md): the same preview-then-apply discipline in general operations.
- Source: [AWS CloudFormation - Runbook & Reference](../../sources/aws-cloudformation.md)

[^aws-cloudformation]: AWS CloudFormation - Runbook & Reference
