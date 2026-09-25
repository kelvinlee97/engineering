---
type: Service
title: CI/CD on AWS
description: AWS's code services for source hosting, builds, deployments, pipelines, package repositories, and code review.
tags: [aws, ci-cd, developer-tools]
sources:
  - id: aws-codecommit
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codecommit/README.md
    title: "AWS CodeCommit - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-codebuild
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codebuild/README.md
    title: "AWS CodeBuild - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-codedeploy
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codedeploy/README.md
    title: "AWS CodeDeploy - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-codepipeline
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codepipeline/README.md
    title: "AWS CodePipeline - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-codeartifact
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codeartifact/README.md
    title: "AWS CodeArtifact - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-codestar
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codestar/README.md
    title: "AWS CodeStar - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-codeguru
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/codeguru/README.md
    title: "Amazon CodeGuru - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
AWS's code services cover each stage of a delivery pipeline: source, build, package, deploy, and orchestrate the whole flow. Several of these services have changed availability over time; each section records what its note says.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS CodeCommit](#aws-codecommit) | CodeCommit is Git with AWS standing in for the server |
| [AWS CodeBuild](#aws-codebuild) | A CodeBuild run is entirely scripted by one file |
| [AWS CodeDeploy](#aws-codedeploy) | CodeDeploy's real product is the AppSpec lifecycle hook sequence |
| [AWS CodePipeline](#aws-codepipeline) | A pipeline is a strict sequence of stages, each an ordered list of actions, connected only by artifacts |
| [AWS CodeArtifact](#aws-codeartifact) | CodeArtifact repositories form a directed graph, not a flat list |
| [AWS CodeStar](#aws-codestar) | AWS CodeStar is a retired product, not a deprecated feature with a grace period |
| [Amazon CodeGuru](#amazon-codeguru) | CodeGuru is two unrelated ML tools sharing a brand name |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS CodeCommit

CodeCommit is Git with AWS standing in for the server: every local Git command works unchanged, and the parts that differ from a self-hosted Git server are exactly the AWS-specific layers: IAM for who can push, KMS for encryption at rest, and CloudTrail/SNS for auditing and notifications. AWS CodeCommit is a managed version control service that hosts private Git repositories in the cloud. It supports the full Git workflow (clone, branch, commit, push, pull, pull requests), integrates with IAM for access control, encrypts data at rest and in transit, and scales to large repositories with no limits on repository size or file types.

Key points:

- Repository: a private Git repository hosted by AWS; you create it in the console or CLI and clone/push over HTTPS or SSH (SSH with a key or HTTPS with Git credentials).
- Git operations: CodeCommit is Git-compatible, so existing Git tools and workflows work unchanged.
- Pull requests: review and comment on code changes before merging; CodeCommit can notify reviewers by email/SNS.
- Branches and tags: standard Git references; prune branches/tags you no longer need to keep operations fast.
- Encryption: repositories are encrypted at rest (KMS) and in transit (TLS).

Practices:

- Use IAM roles or temporary credentials; prefer short-lived credentials over long-lived Git credentials.
- Enable repository encryption with a KMS key you control where policy requires it.
- Keep repositories focused on code; do not store databases, backups, or large frequently-changing binaries (use S3 for those).

| Symptom | Check |
| --- | --- |
| Clone/push authentication failure | Check Git credentials or SSH key setup, and IAM permissions for the repository. |
| Repository not visible | Confirm the Region and that the IAM principal has `codecommit:ListRepositories`/`GetRepository`. |
| Large files slow operations | Move large binaries to S3; Git delta chains degrade performance for frequently changing large files. |
| Pull request notifications missing | Verify SNS topic subscription and notification rules. |

Repositories per account, repository size, file sizes, and API request rates have quotas. See the AWS CodeCommit quotas page and Service Quotas console for current values.[^aws-codecommit]


## AWS CodeBuild

A CodeBuild run is entirely scripted by one file: the buildspec's phases execute in a fixed order in a fresh container, so a failure at "install" versus "build" versus "post_build" points to a completely different part of that same file, not a different system. AWS CodeBuild is a fully managed build service that compiles source code, runs unit tests, and produces deployable artifacts. It removes the need to provision, patch, and scale build servers: CodeBuild provides prepackaged build environments for popular languages and tools, supports custom environments, and scales automatically to handle peak build demand. You pay only for the build minutes you consume.

Key points:

- Build project: the configuration for a build, including source, environment (image, compute), build commands (`buildspec`), artifacts, and logs.
- Buildspec: a YAML file (`buildspec.yml`) in the source that defines install/pre_build/build/post_build phases and artifacts.
- Build environment: a managed or custom Docker image with the runtime and tools (Maven, Gradle, npm, etc.).
- Source providers: AWS CodeCommit, S3, GitHub/GitHub Enterprise, Bitbucket, or no source.
- Artifacts: build outputs uploaded to S3 or available in the build environment.

Practices:

- Put build logic in `buildspec.yml` so builds are reproducible and reviewable in code.
- Use specific, pinned image versions and custom images for deterministic environments.
- Upload artifacts to versioned S3 buckets and keep a retention policy.

| Symptom | Check |
| --- | --- |
| Build fails at install/pre_build | Check dependency versions and network access for package registries; review build logs. |
| Artifact not uploaded | Verify the S3 bucket, IAM permissions, and artifact configuration. |
| Build stuck | Check timeout settings, resource limits (compute), and Docker hub pulls. |
| Secrets needed in build | Store them in Secrets Manager/Parameter Store and reference them with permission boundaries. |

Build projects per account, concurrent builds, build minutes, and artifact sizes have quotas. See the AWS CodeBuild quotas page and Service Quotas console for current values.[^aws-codebuild]


## AWS CodeDeploy

CodeDeploy's real product is the AppSpec lifecycle hook sequence: in-place and blue/green deployments both walk through the same named hooks (BeforeInstall, AfterInstall, ApplicationStart, ValidateService...), and ValidateService's exit code, together with the deployment configuration, decides whether the rollout continues or auto-rolls-back. AWS CodeDeploy automates application deployments to EC2 instances, on-premises servers, Lambda functions, and Amazon ECS services. You package your application with an AppSpec file; CodeDeploy rolls out the revision, tracks health, and can stop and roll back on errors. It supports in-place and blue/green deployment strategies.

Key points:

- Compute platforms: EC2/On-Premises, AWS Lambda, and Amazon ECS.
- Application and deployment group: an application is a collection of deployment groups; a deployment group defines the target instances (tags, ASG) or the Lambda/ECS service configuration.
- Revision: an application bundle plus an AppSpec file; stored in S3 or GitHub.
- AppSpec: the YAML/JSON file that defines lifecycle event hooks (BeforeInstall, AfterInstall, ApplicationStart, ValidateService, etc.) and the deployment behavior per platform.
- Deployment types:

Practices:

- Keep deployments small and frequent; use blue/green for critical workloads to minimize risk and enable fast rollback.
- Define health checks and validation hooks (ValidateService) so unhealthy deployments roll back automatically.
- Use IAM roles for the CodeDeploy agent and the service; encrypt revision bundles in S3.

| Symptom | Check |
| --- | --- |
| Instance deployment fails | Check the CodeDeploy agent logs (`/var/log/aws/codedeploy-agent`), IAM instance role, and S3 revision access. |
| Hooks not running | Verify the AppSpec file path, permissions, and script exit codes (non-zero fails the hook). |
| Deployment stuck | Check deployment configuration (healthy instance minimum), load balancer deregistration, and agent connectivity. |
| Rollback not triggered | Confirm auto-rollback settings and alarm/validation criteria. |

Applications, deployment groups, concurrent deployments, and revision sizes per account have quotas. See the AWS CodeDeploy quotas page and Service Quotas console for current values.[^aws-codedeploy]


## AWS CodePipeline

A pipeline is a strict sequence of stages, each an ordered list of actions, connected only by artifacts: an action can only see the artifacts the actions before it explicitly output, so a missing input in stage N almost always traces back to a name mismatch in stage N-1's output. AWS CodePipeline is a continuous delivery service that models, visualizes, and automates the stages of a software release. A pipeline describes how code changes flow from source through build and test to deployment; each stage contains actions provided by AWS services (CodeCommit, CodeBuild, CodeDeploy, Lambda, S3) or third-party integrations (GitHub, Jenkins, etc.).

Key points:

- Pipeline: a workflow with stages executed in order; pipelines run automatically when the source changes or on demand.
- Stage: a logical phase (for example, Source, Build, Test, Deploy) containing one or more actions.
- Action: a step in a stage (source, build, test, deploy, approval, invoke); actions have input/output artifacts.
- Artifact: the files passed between stages (for example, source bundle or build output), stored in an S3 artifact bucket.
- Approval action: manual gate that pauses the pipeline until someone approves or rejects.

Practices:

- Keep the pipeline definition in code (CloudFormation or CLI JSON) and version it with your application.
- Model clear stages (Source, Build, Test, Deploy) with approvals before production deployment.
- Use CodeBuild for build/test actions and CodeDeploy/ECS/Lambda/CloudFormation for deployment actions.

| Symptom | Check |
| --- | --- |
| Pipeline stuck on approval | Check that the approver(s) received the notification and the action is not expired. |
| Action failed | Open the action details/execution logs; verify source, build, or deployment configuration. |
| Artifacts missing between stages | Confirm artifact names match between action inputs/outputs and the artifact bucket policy. |
| Source change not triggering | Verify the source action (CodeCommit event, GitHub webhook, S3) and pipeline configuration. |

Pipelines per account, stages and actions per pipeline, artifact sizes, and executions have quotas. See the AWS CodePipeline quotas page and Service Quotas console for current values.[^aws-codepipeline]


## AWS CodeArtifact

CodeArtifact repositories form a directed graph, not a flat list: a repository can declare another repository (including one backed by an external public registry) as its upstream, so a single package manager endpoint can transparently resolve packages that actually live in several different repositories. AWS CodeArtifact is a managed artifact repository service for storing and sharing software packages. It works with popular package managers (npm, yarn, pip, twine, Maven, Gradle, NuGet), supports private packages and external connections to public repositories, and has no limits on the number or total size of packages you store.

Key points:

- Domain: the top-level container that groups repositories and provides organizational boundaries and policy; use one production domain with one or more repositories.
- Repository: a polyglot collection of packages (any supported package type); repositories are members of exactly one domain.
- Upstream repository: makes packages from one repository available to another repository in the same domain, including packages fetched via external connections.
- External connection: links a repository to a public repository (npmjs.com, Maven Central, PyPI, NuGet Gallery); packages are fetched and stored on demand.
- Authentication: users authenticate with authorization tokens created from AWS credentials; packages cannot be made publicly available.

Practices:

- Use one production domain per organization and separate repositories per team/project.
- Connect repositories to public sources as upstreams so builds never depend on a single internet source; control which versions flow in.
- Use resource policies on domains to control cross-account access; apply least-privilege IAM.

| Symptom | Check |
| --- | --- |
| Package manager auth failed | Get a fresh authorization token and verify the repository endpoint/region. |
| Cannot publish | Check IAM permissions (`codeartifact:PublishPackageVersion`) and repository policies. |
| Upstream package missing | Verify the upstream repository configuration and external connection status. |
| npm/yarn cache stale | Clear the local package manager cache or bump the version. |

Domains and repositories per account, upstream repositories per repository, and API request rates have quotas. See the AWS CodeArtifact quotas page and Service Quotas console for current values.[^aws-codeartifact]


## AWS CodeStar

AWS CodeStar is a retired product, not a deprecated feature with a grace period: since July 31, 2024 the console and SDK are gone entirely, so this article exists only to help teams recognize legacy CodeStar resources and migrate them to CodeCatalyst or the underlying Code suite services directly. AWS CodeStar was a unified interface for setting up software development projects with a project dashboard, issue tracking, and integrated CI/CD (CodeCommit, CodeBuild, CodeDeploy, CodePipeline). AWS ended support for creating and viewing CodeStar projects on July 31, 2024: the CodeStar console is no longer accessible and new projects cannot be created. The AWS SDK client for CodeStar was also removed. Existing teams should use the underlying services (CodeCommit, CodeBuild, CodeDeploy, CodePipeline) and AWS CodeCatalyst for project-level collaboration.

Key points:

- Project: CodeStar grouped code repositories, build/deploy pipelines, and team members under one dashboard.
- Status (retired): as of July 31, 2024, you cannot create or view CodeStar projects; the console is inaccessible and the SDK package is deprecated/removed.
- Successors: use CodeCatalyst for project planning/collaboration and the Code suite (CodeCommit, CodeBuild, CodeDeploy, CodePipeline) for CI/CD.

Practices:

- Do not start new projects on CodeStar; it is discontinued.
- Build project collaboration on AWS CodeCatalyst (planning, repos, CI/CD) or the Code suite directly.
- Archive or delete legacy CodeStar resources through their underlying services and remove unused IAM roles.

| Symptom | Check |
| --- | --- |
| Cannot access CodeStar console | Expected: CodeStar is discontinued (July 31, 2024); use CodeCatalyst or the Code suite. |
| SDK calls fail | The CodeStar SDK client was removed; migrate to CodeCommit/CodeBuild/CodeDeploy/CodePipeline APIs. |
| Old project resources exist | Locate them via the underlying services and migrate or delete deliberately. |

CodeStar is discontinued; no new resources can be created. See the AWS CodeStar user guide release notes and the underlying service quotas for historical resource management.[^aws-codestar]


## Amazon CodeGuru

CodeGuru is two unrelated ML tools sharing a brand name: Reviewer looks at source code before it runs, Profiler looks at running processes in production, and as of November 7, 2025, only one of them (Profiler) still accepts new setups. Amazon CodeGuru is a machine learning service with two capabilities: CodeGuru Reviewer, which analyzes code for defects and security issues, and CodeGuru Profiler, which identifies the most expensive lines of code at runtime. Note: as of November 7, 2025, you can no longer create new repository associations in CodeGuru Reviewer; existing functionality and similar services are documented by AWS.

Practices:

- Run Reviewer on pull requests (where still available) so recommendations land in review workflows.
- Fix high-confidence recommendations (security, resource leaks) before merge; track recommendation backlog.
- Run Profiler continuously in production to catch regressions and expensive code paths; profile representative traffic.

| Symptom | Check |
| --- | --- |
| No recommendations | Check repository association status, supported languages (Java/Python), and review scope. |
| Cannot create repository association | New associations are no longer supported (November 7, 2025); use documented alternatives. |
| Profiler shows no data | Verify the agent is installed/running and IAM permissions allow `codeguruprofiler:PostAgentProfile`. |
| Profile times empty | Confirm the profiling group name and the time range used. |

Profiling groups per account, profile retention, and API request rates have quotas; Reviewer availability is subject to the announced service changes. See the Amazon CodeGuru endpoints and quotas page for current values.[^aws-codeguru]


## Related

- [AWS developer tools](developer-tools.md)
- [Domain index](index.md)

[^aws-codecommit]: [AWS CodeCommit - Runbook & Reference](../../sources/aws-codecommit.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codecommit/README.md)
[^aws-codebuild]: [AWS CodeBuild - Runbook & Reference](../../sources/aws-codebuild.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codebuild/README.md)
[^aws-codedeploy]: [AWS CodeDeploy - Runbook & Reference](../../sources/aws-codedeploy.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codedeploy/README.md)
[^aws-codepipeline]: [AWS CodePipeline - Runbook & Reference](../../sources/aws-codepipeline.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codepipeline/README.md)
[^aws-codeartifact]: [AWS CodeArtifact - Runbook & Reference](../../sources/aws-codeartifact.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codeartifact/README.md)
[^aws-codestar]: [AWS CodeStar - Runbook & Reference](../../sources/aws-codestar.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codestar/README.md)
[^aws-codeguru]: [Amazon CodeGuru - Runbook & Reference](../../sources/aws-codeguru.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/codeguru/README.md)
