# AWS CodeCommit - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS CodeCommit is a managed version control service that hosts private Git repositories in the cloud. It supports the full Git workflow (clone, branch, commit, push, pull, pull requests), integrates with IAM for access control, encrypts data at rest and in transit, and scales to large repositories with no limits on repository size or file types.

## Key concepts

- **Repository**: a private Git repository hosted by AWS; you create it in the console or CLI and clone/push over HTTPS or SSH (SSH with a key or HTTPS with Git credentials).
- **Git operations**: CodeCommit is Git-compatible, so existing Git tools and workflows work unchanged.
- **Pull requests**: review and comment on code changes before merging; CodeCommit can notify reviewers by email/SNS.
- **Branches and tags**: standard Git references; prune branches/tags you no longer need to keep operations fast.
- **Encryption**: repositories are encrypted at rest (KMS) and in transit (TLS).
- **Integrations**: works with CodeBuild, CodePipeline, Lambda (triggers), and third-party tools.

## Common operations (AWS CLI)

```bash
# Create a repository
aws codecommit create-repository --repository-name my-app --region us-east-1

# Clone and work with it
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/my-app
git add . && git commit -m "initial commit" && git push

# Create a branch and a pull request
aws codecommit create-branch --repository-name my-app \
  --branch-name feature/x --commit-id <commit-id>
aws codecommit create-pull-request --title "Add feature" \
  --targets repositoryName=my-app,sourceReference=feature/x,destinationReference=main

# List repositories and branches
aws codecommit list-repositories
aws codecommit list-branches --repository-name my-app
```

## Best practices

- Use IAM roles or temporary credentials; prefer short-lived credentials over long-lived Git credentials.
- Enable repository encryption with a KMS key you control where policy requires it.
- Keep repositories focused on code; do not store databases, backups, or large frequently-changing binaries (use S3 for those).
- Use pull requests with reviewers for production branches and protect them with IAM policies/approval rules.
- Set up notifications (SNS) for pull request and push events; monitor repository activity with CloudTrail.
- Prune stale branches and tags; use Git LFS alternatives (S3) for large assets.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Clone/push authentication failure | Check Git credentials or SSH key setup, and IAM permissions for the repository. |
| Repository not visible | Confirm the Region and that the IAM principal has `codecommit:ListRepositories`/`GetRepository`. |
| Large files slow operations | Move large binaries to S3; Git delta chains degrade performance for frequently changing large files. |
| Pull request notifications missing | Verify SNS topic subscription and notification rules. |
| Push rejected | Check branch protection/approval rules and IAM conditions on the branch. |

## Limits

Repositories per account, repository size, file sizes, and API request rates have quotas. See the AWS CodeCommit quotas page and Service Quotas console for current values.

## Official references

- [What is AWS CodeCommit?](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html)
- [AWS CodeCommit quotas](https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html)
- [AWS CodeCommit pricing](https://aws.amazon.com/codecommit/pricing/)
- [AWS CLI: codecommit commands](https://docs.aws.amazon.com/cli/latest/reference/codecommit/)
