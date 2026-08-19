# Amazon CodeGuru - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon CodeGuru is a machine learning service with two capabilities: CodeGuru Reviewer, which analyzes code for defects and security issues, and CodeGuru Profiler, which identifies the most expensive lines of code at runtime. Note: as of November 7, 2025, you can no longer create new repository associations in CodeGuru Reviewer; existing functionality and similar services are documented by AWS.

## Key concepts

- **CodeGuru Reviewer**: uses program analysis and machine learning to detect complex defects in Java and Python code and suggest improvements (resource leaks, security issues, best practices); integrates with GitHub, Bitbucket, and S3 (via GitHub Actions).
- **Secrets detection**: Reviewer can find unprotected secrets in code, integrating with AWS Secrets Manager.
- **CodeGuru Profiler**: profiles applications in production, visualizes performance, and identifies the most expensive lines of code and inefficiencies; helps reduce cost and latency.
- **Availability change**: new repository associations in Reviewer are no longer supported (since November 7, 2025); see the AWS announcement for alternative services with similar capabilities.

## Common operations (AWS CLI)

```bash
# CodeGuru Profiler: create a profiling group and check findings
aws codeguruprofiler create-profiling-group --profiling-group-name prod-app
aws codeguruprofiler list-profile-times --profiling-group-name prod-app \
  --start-time 2026-08-18T00:00:00Z --end-time 2026-08-19T00:00:00Z
aws codeguruprofiler get-policy --profiling-group-name prod-app

# Reviewer (existing associations): list code reviews
aws codeguru-reviewer list-code-reviews --type RepositoryAnalysis
aws codeguru-reviewer describe-code-review --code-review-arn <review-arn>
```

## Best practices

- Run Reviewer on pull requests (where still available) so recommendations land in review workflows.
- Fix high-confidence recommendations (security, resource leaks) before merge; track recommendation backlog.
- Run Profiler continuously in production to catch regressions and expensive code paths; profile representative traffic.
- Keep IAM least privilege: separate roles for profiling agent and console access.
- Monitor profiler findings and set alarms for performance regressions.
- Follow the AWS guidance for alternatives if you need repository analysis beyond existing Reviewer associations.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No recommendations | Check repository association status, supported languages (Java/Python), and review scope. |
| Cannot create repository association | New associations are no longer supported (November 7, 2025); use documented alternatives. |
| Profiler shows no data | Verify the agent is installed/running and IAM permissions allow `codeguruprofiler:PostAgentProfile`. |
| Profile times empty | Confirm the profiling group name and the time range used. |
| Recommendations noisy | Focus on high-confidence/security detectors and maintain a backlog with owners. |

## Limits

Profiling groups per account, profile retention, and API request rates have quotas; Reviewer availability is subject to the announced service changes. See the Amazon CodeGuru endpoints and quotas page for current values.

## Official references

- [What is Amazon CodeGuru Reviewer?](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html)
- [Amazon CodeGuru Profiler user guide](https://docs.aws.amazon.com/codeguru/latest/profiler-ug/what-is-codeguru-profiler.html)
- [Amazon CodeGuru endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/codeguru.html)
- [Amazon CodeGuru pricing](https://aws.amazon.com/codeguru/pricing/)
- [AWS CLI: codeguru-reviewer and codeguruprofiler commands](https://docs.aws.amazon.com/cli/latest/reference/codeguru-reviewer/)
