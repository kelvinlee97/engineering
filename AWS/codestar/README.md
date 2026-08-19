# AWS CodeStar - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS CodeStar was a unified interface for setting up software development projects with a project dashboard, issue tracking, and integrated CI/CD (CodeCommit, CodeBuild, CodeDeploy, CodePipeline). AWS ended support for creating and viewing CodeStar projects on July 31, 2024: the CodeStar console is no longer accessible and new projects cannot be created. The AWS SDK client for CodeStar was also removed. Existing teams should use the underlying services (CodeCommit, CodeBuild, CodeDeploy, CodePipeline) and AWS CodeCatalyst for project-level collaboration.

## Key concepts

- **Project**: CodeStar grouped code repositories, build/deploy pipelines, and team members under one dashboard.
- **Status (retired)**: as of July 31, 2024, you cannot create or view CodeStar projects; the console is inaccessible and the SDK package is deprecated/removed.
- **Successors**: use CodeCatalyst for project planning/collaboration and the Code suite (CodeCommit, CodeBuild, CodeDeploy, CodePipeline) for CI/CD.

## Common operations

No new CodeStar resources can be created. If you still have historical resources, manage them through the underlying services:

```bash
# Manage the underlying resources directly
aws codecommit list-repositories
aws codepipeline list-pipelines
aws codebuild list-projects
aws codedeploy list-applications
```

## Best practices

- Do not start new projects on CodeStar; it is discontinued.
- Build project collaboration on AWS CodeCatalyst (planning, repos, CI/CD) or the Code suite directly.
- Archive or delete legacy CodeStar resources through their underlying services and remove unused IAM roles.
- Update any automation that calls CodeStar APIs to use the underlying service APIs.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cannot access CodeStar console | Expected: CodeStar is discontinued (July 31, 2024); use CodeCatalyst or the Code suite. |
| SDK calls fail | The CodeStar SDK client was removed; migrate to CodeCommit/CodeBuild/CodeDeploy/CodePipeline APIs. |
| Old project resources exist | Locate them via the underlying services and migrate or delete deliberately. |

## Limits

CodeStar is discontinued; no new resources can be created. See the AWS CodeStar user guide release notes and the underlying service quotas for historical resource management.

## Official references

- [AWS CodeStar user guide (archived)](https://docs.aws.amazon.com/codestar/latest/userguide/welcome.html)
- [AWS CodeStar release notes (retirement)](https://docs.aws.amazon.com/codestar/latest/userguide/history.html)
- [AWS CodeCatalyst](https://codecatalyst.aws/)
