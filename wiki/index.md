---
okf_version: "0.2"
---
# Engineering Wiki

A wiki the LLM compiles from the sources in `raw/` and the legacy articles, following the conventions in the repository's `CLAUDE.md`. Every page lists its sources; pages marked `status: draft` have not been reviewed yet.

* [Domains](engineering/index.md) - Concept pages grouped by domain.
* [Sources](sources/index.md) - One summary page per ingested source.
* [Syntheses](syntheses/index.md) - Answers filed back from queries.
* [Log](log.md) - What changed and when, newest first.

# Concept

* [Agent skill](engineering/claude-code/agent-skill.md) - A folder of task-specific instructions and optional resources that Claude Code loads only when a request matches its description.
* [AI adoption maturity](engineering/ai-engineering/ai-adoption-maturity.md) - A four-stage ladder from individual chat use to end-to-end processes, driven by growing user fluency, system access, and governance.
* [AI-native company](engineering/ai-engineering/ai-native-company.md) - A company designed around AI loops from the start, with work made legible to agents and people at the boundary with reality, as argued in several founder and investor talks.
* [Auto Mode](engineering/claude-code/auto-mode.md) - A Claude Code permission mode where low-risk actions run directly and a separate classifier reviews higher-risk ones against user intent and a configured trust boundary.
* [AWS pricing models](engineering/aws/pricing-models.md) - AWS pricing trades flexibility for discount: On-Demand is flexible and dearest, commitments are cheaper, and Spot is cheapest but reclaimable.
* [AWS shared responsibility model](engineering/aws/shared-responsibility-model.md) - AWS secures the cloud itself; the customer secures what they put in it, and the split moves toward AWS as services become more managed.
* [AWS Well-Architected Framework](engineering/aws/well-architected.md) - AWS's six-pillar set of design practices, and the tool for reviewing a workload against them.
* [Backend for frontend](engineering/web-serving/backend-for-frontend.md) - A backend that serves one browser-facing application: it enforces session and authorization rules, adapts requests, and calls downstream services.
* [Claude Code extension mechanisms](engineering/claude-code/extension-mechanisms.md) - How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.
* [Company brain](engineering/ai-engineering/company-brain.md) - An organization's curated memory plus the retrieval that selects what an agent needs, kept useful by provenance, contradiction checks, and pruning.
* [Context isolation](engineering/claude-code/context-isolation.md) - Keeping an agent's intermediate work out of the main context window, at the cost of losing whatever the summary leaves out.
* [Envelope encryption](engineering/aws/envelope-encryption.md) - Encrypt data locally with a data key and store only an encrypted copy of that key, so the key service never handles bulk data.
* [Git's four places](engineering/git/git-four-places.md) - Git moves work between the working tree, the staging area, the local repository, and a remote; most commands inspect or move content between them.
* [IAM policy evaluation](engineering/aws/iam-policy-evaluation.md) - How AWS decides a request: every applicable policy layer is checked, an explicit deny anywhere wins, and nothing is allowed without an explicit allow.
* [Prompt injection](engineering/claude-code/prompt-injection.md) - Instructions hidden in content an agent reads, such as web pages, files, or issue comments, that try to redirect it away from the user's request.
* [Reverse proxy gateway](engineering/web-serving/reverse-proxy-gateway.md) - A server such as Nginx or OpenResty that terminates HTTPS at the edge and forwards requests to an application listening only on a private address.
* [Subagent](engineering/claude-code/subagent.md) - A worker agent that Claude Code hands a bounded task to, which runs in its own context and returns only a focused result.

# Pattern

* [Agents propose, people and policy accept](engineering/ai-engineering/propose-accept-boundary.md) - Route every agent change through pull requests so that required checks, code owners, and approval gates, not the agent, decide what is accepted.
* [AI-native SDLC](engineering/ai-engineering/ai-native-sdlc.md) - A software delivery loop where each stage leaves a committed artifact, agents work between human approval gates, and production evidence returns as new intent.
* [AWS multi-account governance](engineering/aws/multi-account-governance.md) - Run AWS as many accounts under Organizations, with central sign-in, an organization audit trail, and security services run from delegated administrator accounts.
* [AWS security findings pipeline](engineering/aws/security-findings-pipeline.md) - Route GuardDuty and other detector findings through Security Hub CSPM and EventBridge, and export them, because each service keeps only a short fixed history.
* [Database and directory products](engineering/startups/database-directory-products.md) - Small SaaS products that sell a curated database, such as investors or journalists, found through a painful problem and grown with SEO.
* [Delegation contract](engineering/claude-code/delegation-contract.md) - What a subagent must be told up front: when it is used, what its output looks like, and which obstacles it must report.
* [Deterministic checks and model judgment](engineering/ai-engineering/deterministic-vs-model-work.md) - Put enforcement, exact data, and repeatable computation in deterministic code, and use a model only where judgment or interpretation is needed.
* [Git commit workflow](engineering/git/commit-workflow.md) - Review what changed, stage explicit paths, review what is staged, commit, and confirm the result before pushing.
* [Incident closure criteria](engineering/operations/incident-closure-criteria.md) - Close an incident only when written acceptance evidence shows each affected layer is healthy, and the record separates evidence, actions, and hypotheses.
* [Keeping secrets out of Git](engineering/git/secrets-in-git.md) - Never commit credentials; if one leaks, revoke or rotate it first, because deleting the file or rewriting history cannot prove it was not copied.
* [Layered troubleshooting](engineering/operations/layered-troubleshooting.md) - Treat a failure as one broken link in a known chain of layers, and find the first broken link with read-only evidence before changing anything.
* [Least-privilege tool access](engineering/claude-code/least-privilege-tool-access.md) - Grant an agent only the tools its job requires, starting from what it must do.
* [Measuring an AI rollout](engineering/ai-engineering/ai-rollout-measurement.md) - Judge an AI tooling rollout by comparing concurrent cohorts against pre-set baselines, and lead with expansion rather than hours saved.
* [Progressive disclosure](engineering/claude-code/progressive-disclosure.md) - Expose only a short summary up front and load detailed material into context only when the task needs it.
* [Risk-based autonomy](engineering/ai-engineering/risk-based-autonomy.md) - Give agents more autonomy on low-risk, reversible work and keep human approval for high-risk and production changes, widening scope gradually.
* [Safe change procedure](engineering/operations/safe-change-procedure.md) - Make one small, backed-up change at a time, validate it before applying, apply it gracefully, verify each layer, and keep a known-good rollback.
* [Self-improving skill loop](engineering/ai-engineering/self-improving-skill-loop.md) - A scheduled agent reads human feedback on another agent's output and opens a pull request that edits that agent's skill file.
* [Text-processing pipelines](engineering/linux/text-processing-pipelines.md) - Answer log questions by chaining small Unix filters such as awk, cut, sort, uniq, grep, and wc into one pipeline.
* [When to delegate](engineering/claude-code/when-to-delegate.md) - Delegate when only the result matters to the main thread; keep work in one context when its intermediate steps matter.

# Playbook

* [APT package management](engineering/linux/apt-package-management.md) - Install, upgrade, hold, roll back, and troubleshoot Ubuntu packages safely by refreshing, simulating, and inspecting before applying.
* [Express BFF deployment](engineering/web-serving/express-bff-deployment.md) - Deploy an Express backend-for-frontend under PM2 cluster mode as an unprivileged user, with immutable releases and symlink rollback.
* [Express BFF incidents](engineering/web-serving/express-bff-incidents.md) - Ten common failure modes of an Express BFF under PM2 cluster mode, each with first checks, recovery, and verification.
* [GitHub pull request workflow](engineering/git/pull-request-workflow.md) - Publish a change on GitHub through a focused branch, a reviewed pull request, passing checks, and a merge, then clean up.
* [Kubernetes IP or ENI exhaustion](engineering/kubernetes/ip-eni-exhaustion.md) - Diagnose and remediate Pods stuck Pending on ENI or IP capacity in an ENI-based Pod network, in dependency order.
* [Nginx production deployment](engineering/web-serving/nginx-production-deployment.md) - Deploy Nginx on one Ubuntu 24.04 VM to serve static files and reverse-proxy a loopback application, with Certbot HTTPS and layer-by-layer checks.
* [OpenResty production deployment](engineering/web-serving/openresty-production-deployment.md) - Deploy OpenResty on one Ubuntu 24.04 VM with a Lua health endpoint, a loopback reverse proxy, and Certbot HTTPS.
* [Starting a small business](engineering/startups/starting-a-small-business.md) - A seven-part outline for starting a small business: choosing the model, break-even, the customer problem, a plan, product-market fit, finances, and marketing.
* [Syncing a Git branch](engineering/git/branch-sync.md) - Fetch first, compare local and upstream commits, then choose fast-forward, rebase, or merge deliberately, and resolve conflicts on purpose.
* [Undoing and recovering in Git](engineering/git/undo-and-recovery.md) - Choose between restore, reset, revert, and reflog by whether the work is shared, and check a pre-flight list before any destructive Git operation.
* [ZooKeeper production deployment](engineering/zookeeper/production-deployment.md) - Build and operate a three-member ZooKeeper 3.9.5 ensemble with mutual TLS, systemd, JMX metrics, and one-member-at-a-time changes.
* [ZooKeeper quorum-loss restore](engineering/zookeeper/quorum-loss-restore.md) - Restore a three-member ZooKeeper ensemble that lost quorum by loading the same approved snapshot into every member, one at a time, through a temporary loopback-only admin endpoint.
* [ZooKeeper single-member recovery](engineering/zookeeper/single-member-recovery.md) - Rebuild one ZooKeeper member whose transaction log a full disk truncated, by moving its data aside and letting it resync from a healthy quorum.

# Tool

* [Apple Container](engineering/dev-tools/apple-container.md) - Apple's native container tool for Apple silicon Macs, which runs each container in its own lightweight VM instead of one shared Linux VM.
* [Claude Code GitHub Actions](engineering/claude-code/claude-code-github-actions.md) - The anthropics/claude-code-action workflow step that runs Claude Code inside a GitHub Actions job, triggered by @claude mentions or a fixed prompt.
* [Claude Projects](engineering/claude-code/claude-projects.md) - In the September 2026 redesign, a Claude project is one long-running conversation whose coordinator splits a goal into parallel threads sharing memory and a library.
* [Pull request auto-fix](engineering/claude-code/pr-auto-fix.md) - A Claude Code cloud feature that watches a pull request and responds to CI failures and review comments, with known blind spots.

# Service

* [Amazon CloudFront](engineering/aws/cloudfront.md) - AWS's CDN: requests are answered from the nearest edge cache, and only misses reach the origin, so cache settings control both cost and freshness.
* [Amazon CloudWatch](engineering/aws/cloudwatch.md) - AWS's monitoring service: metrics, logs, and traces feed alarms and dashboards, and alarms only ever watch metrics.
* [Amazon DynamoDB](engineering/aws/dynamodb.md) - AWS's serverless key-value and document database, designed around access patterns and partition keys.
* [Amazon EC2](engineering/aws/ec2.md) - AWS's virtual servers: the instance type sets compute, memory, network, and storage, and the lifecycle state decides what you pay and what data survives.
* [Amazon EC2 Auto Scaling](engineering/aws/auto-scaling-groups.md) - Groups of EC2 instances held between a minimum and maximum size, scaled by policies and self-healed by health checks.
* [Amazon ECR](engineering/aws/ecr.md) - AWS's container image registry, with IAM-controlled private repositories, scanning, lifecycle cleanup, and replication.
* [Amazon ECS](engineering/aws/ecs.md) - AWS's own container orchestrator: task definitions run as tasks or long-running services on Fargate, EC2, or on-premises capacity.
* [Amazon EKS](engineering/aws/eks.md) - AWS's managed Kubernetes: AWS runs the control plane, and with Auto Mode also the nodes.
* [Amazon ElastiCache](engineering/aws/elasticache.md) - AWS's managed in-memory cache running Valkey, Redis OSS, or Memcached, serverless or on chosen nodes.
* [Amazon EventBridge](engineering/aws/eventbridge.md) - AWS's serverless event router: buses and rules match JSON events to targets, with Pipes and Scheduler alongside.
* [Amazon GuardDuty](engineering/aws/guardduty.md) - AWS's threat detection service that analyzes CloudTrail, VPC Flow Logs, and DNS logs, plus optional protection plans, to produce findings.
* [Amazon RDS](engineering/aws/rds.md) - AWS's managed relational databases, where Multi-AZ standbys give failover and read replicas give read scaling.
* [Amazon Route 53](engineering/aws/route53.md) - AWS's DNS service: domain registration, hosted zones with routing policies, and health checks that drop unhealthy targets from answers.
* [Amazon S3](engineering/aws/s3.md) - AWS's object storage: private-by-default buckets of objects, storage classes along a cost and latency scale, and lifecycle rules to move data down it.
* [Amazon SNS](engineering/aws/sns.md) - AWS's managed publish/subscribe service that fans one message out to many subscribers.
* [Amazon SQS](engineering/aws/sqs.md) - AWS's managed message queue for decoupling producers from consumers, with standard and FIFO queues.
* [Amazon VPC](engineering/aws/vpc.md) - AWS's logically isolated virtual network: CIDR ranges split into per-AZ subnets, with route tables, gateways, and firewalls deciding where traffic goes.
* [AWS Billing and Cost Management](engineering/aws/billing-cost-management.md) - AWS's billing console: paying, analyzing, tagging, budgeting, and buying commitments, with IAM access off by default.
* [AWS CloudFormation](engineering/aws/cloudformation.md) - AWS's infrastructure as code: templates become stacks, and every update is a computed change set applied as one unit.
* [AWS CloudTrail](engineering/aws/cloudtrail.md) - AWS's audit log of API and console actions, from a free 90-day event history to long-term trails and a queryable data lake.
* [AWS Direct Connect](engineering/aws/direct-connect.md) - A dedicated private network link from on-premises to AWS that bypasses the public internet, carried as virtual interfaces over BGP.
* [AWS Global Accelerator](engineering/aws/global-accelerator.md) - Static anycast IP addresses that carry user traffic over the AWS network to the healthiest, nearest regional endpoint.
* [AWS IAM](engineering/aws/iam.md) - AWS's authentication and authorization service: identities, policies, and temporary credentials that decide who can do what to which resource.
* [AWS IAM Identity Center](engineering/aws/iam-identity-center.md) - AWS's service for workforce sign-in to many accounts: users or an external identity provider, permission sets, and an access portal.
* [AWS KMS](engineering/aws/kms.md) - AWS's managed service for creating and controlling encryption and signing keys, used through envelope encryption.
* [AWS Lambda](engineering/aws/lambda.md) - AWS's serverless compute: functions run per event with no servers to manage, billed per request and GB-second.
* [AWS Organizations](engineering/aws/organizations.md) - AWS's service for managing many accounts as one tree of organizational units with shared billing and policy guardrails.
* [AWS Secrets Manager](engineering/aws/secrets-manager.md) - AWS's service for storing versioned secrets that applications fetch at runtime, with scheduled rotation through Lambda.
* [AWS Security Hub CSPM](engineering/aws/security-hub.md) - AWS's security posture service that gathers findings from other services and runs continuous checks against security standards.
* [AWS Systems Manager](engineering/aws/systems-manager.md) - AWS's toolkit for operating fleets of servers through an agent, without SSH: commands, sessions, patching, parameters, and runbooks.
* [Claude GitHub App](engineering/claude-code/claude-github-app.md) - The GitHub App that gives Claude features repository access, and which features depend on it rather than on other sign-in methods.
* [Claude Managed Agents](engineering/claude-code/claude-managed-agents.md) - An Anthropic-hosted agent harness that runs the agent loop, sandbox, and tools for long-running tasks, driven by events instead of your own runtime.
* [Cloud session](engineering/claude-code/cloud-session.md) - A Claude Code session that runs on an Anthropic-managed VM instead of your machine, cloning your repository from GitHub and running after you disconnect.
* [Elastic Load Balancing](engineering/aws/elb.md) - AWS's load balancers (ALB, NLB, GWLB) that spread traffic across healthy targets in several Availability Zones.
* [ZooKeeper](engineering/zookeeper/zookeeper.md) - A distributed coordination service that keeps a small, consistently replicated tree of data for leader election, membership, and configuration notification.

# Configuration

* [Cloud environment](engineering/claude-code/cloud-environment.md) - The saved configuration that sets network access, environment variables, and setup scripts for Claude Code cloud sessions.
* [Ghostty workstation](engineering/dev-tools/ghostty-workstation.md) - A manual setup of the Ghostty terminal plus starship, zoxide, eza, bat, fzf, fd, and ripgrep on macOS or Ubuntu 26.04.
* [Skill configuration](engineering/claude-code/skill-configuration.md) - The SKILL.md frontmatter fields and directory layout that define a Claude Code agent skill.
* [Subagent configuration file](engineering/claude-code/subagent-configuration.md) - The Markdown file with YAML frontmatter that defines a custom Claude Code subagent, and how to create it with /agents.

# Command

* [awk](engineering/linux/awk.md) - A small per-line language that splits each line into numbered fields and runs condition-action rules against them.
* [Git basic commands](engineering/git/basic-commands.md) - The seven everyday Git commands, init, clone, add, status, commit, log, and diff, with their most useful flags and pitfalls.
* [Moving work between terminal and cloud](engineering/claude-code/terminal-cloud-handoff.md) - The CLI commands that start, message, and pull down Claude Code cloud sessions, and what each one needs.
* [uniq](engineering/linux/uniq.md) - Collapses or counts adjacent identical lines, which is why it almost always follows sort.

# Comparison

* [AWS certifications](engineering/aws/certifications.md) - The Cloud Practitioner, Developer Associate, and Solutions Architect Associate exams compared, with the study path the legacy outlines share.
* [AWS compute options](engineering/aws/compute-options.md) - How EC2, Lambda, ECS, and EKS divide the work between you and AWS, and the hard limits that push a workload from one to another.
* [AWS database choices](engineering/aws/database-choices.md) - RDS for relational workloads, DynamoDB for key-value access at scale, and ElastiCache as a disposable in-memory layer in front of either.
* [AWS global traffic routing](engineering/aws/global-traffic-routing.md) - Route 53, CloudFront, and Global Accelerator all steer users toward healthy endpoints, but at different layers and with different failover speed.
* [AWS messaging choices](engineering/aws/messaging-choices.md) - SQS queues work for one consumer, SNS fans out to many, and EventBridge routes events by content; the limits and delivery guarantees differ.

# Source Summary

* [Amazon CloudFront runbook and reference (summary)](sources/aws-cloudfront.md) - Summary of the legacy AWS runbook and reference note for Amazon CloudFront, verified against AWS documentation on 2026-08-19.
* [Amazon CloudWatch runbook and reference (summary)](sources/aws-cloudwatch.md) - Summary of the legacy AWS runbook and reference note for Amazon CloudWatch, verified against AWS documentation on 2026-08-19.
* [Amazon DynamoDB runbook and reference (summary)](sources/aws-dynamodb.md) - Summary of the legacy AWS runbook and reference note for Amazon DynamoDB, verified against AWS documentation on 2026-08-19.
* [Amazon EC2 Auto Scaling runbook and reference (summary)](sources/aws-auto-scaling-groups.md) - Summary of the legacy AWS runbook and reference note for Amazon EC2 Auto Scaling, verified against AWS documentation on 2026-08-19.
* [Amazon EC2 runbook and reference (summary)](sources/aws-ec2.md) - Summary of the legacy AWS runbook and reference note for Amazon EC2, verified against AWS documentation on 2026-08-18.
* [Amazon ECR runbook and reference (summary)](sources/aws-ecr.md) - Summary of the legacy AWS runbook and reference note for Amazon ECR, verified against AWS documentation on 2026-08-19.
* [Amazon ECS runbook and reference (summary)](sources/aws-ecs.md) - Summary of the legacy AWS runbook and reference note for Amazon ECS, verified against AWS documentation on 2026-08-19.
* [Amazon EKS runbook and reference (summary)](sources/aws-eks.md) - Summary of the legacy AWS runbook and reference note for Amazon EKS, verified against AWS documentation on 2026-08-19.
* [Amazon ElastiCache runbook and reference (summary)](sources/aws-elasticache.md) - Summary of the legacy AWS runbook and reference note for Amazon ElastiCache, verified against AWS documentation on 2026-08-19.
* [Amazon EventBridge runbook and reference (summary)](sources/aws-eventbridge.md) - Summary of the legacy AWS runbook and reference note for Amazon EventBridge, verified against AWS documentation on 2026-08-19.
* [Amazon GuardDuty runbook and reference (summary)](sources/aws-guardduty.md) - Summary of the legacy AWS runbook and reference note for Amazon GuardDuty, verified against AWS documentation on 2026-08-19.
* [Amazon RDS runbook and reference (summary)](sources/aws-rds.md) - Summary of the legacy AWS runbook and reference note for Amazon RDS, verified against AWS documentation on 2026-08-19.
* [Amazon Route 53 runbook and reference (summary)](sources/aws-route53.md) - Summary of the legacy AWS runbook and reference note for Amazon Route 53, verified against AWS documentation on 2026-08-19.
* [Amazon S3 runbook and reference (summary)](sources/aws-s3.md) - Summary of the legacy AWS runbook and reference note for Amazon S3, verified against AWS documentation on 2026-08-18.
* [Amazon SNS runbook and reference (summary)](sources/aws-sns.md) - Summary of the legacy AWS runbook and reference note for Amazon SNS, verified against AWS documentation on 2026-08-19.
* [Amazon SQS runbook and reference (summary)](sources/aws-sqs.md) - Summary of the legacy AWS runbook and reference note for Amazon SQS, verified against AWS documentation on 2026-08-19.
* [Amazon VPC runbook and reference (summary)](sources/aws-vpc.md) - Summary of the legacy AWS runbook and reference note for Amazon VPC, verified against AWS documentation on 2026-08-19.
* [AWS Billing and Cost Management runbook and reference (summary)](sources/aws-billing-cost-management.md) - Summary of the legacy AWS runbook and reference note for AWS Billing and Cost Management, verified against AWS documentation on 2026-08-19.
* [AWS CloudFormation runbook and reference (summary)](sources/aws-cloudformation.md) - Summary of the legacy AWS runbook and reference note for AWS CloudFormation, verified against AWS documentation on 2026-08-19.
* [AWS CloudTrail runbook and reference (summary)](sources/aws-cloudtrail.md) - Summary of the legacy AWS runbook and reference note for AWS CloudTrail, verified against AWS documentation on 2026-08-19.
* [AWS competencies for cloud roles study outline (summary)](sources/aws-cert-competencies.md) - Summary of the legacy AWS competencies for cloud roles study outline, verified against AWS documentation on 2026-08-19.
* [AWS Direct Connect runbook and reference (summary)](sources/aws-direct-connect.md) - Summary of the legacy AWS runbook and reference note for AWS Direct Connect, verified against AWS documentation on 2026-08-19.
* [AWS Global Accelerator runbook and reference (summary)](sources/aws-global-accelerator.md) - Summary of the legacy AWS runbook and reference note for AWS Global Accelerator, verified against AWS documentation on 2026-08-19.
* [AWS IAM Identity Center runbook and reference (summary)](sources/aws-iam-identity-center.md) - Summary of the legacy AWS runbook and reference note for AWS IAM Identity Center, verified against AWS documentation on 2026-08-19.
* [AWS IAM runbook and reference (summary)](sources/aws-iam.md) - Summary of the legacy AWS runbook and reference note for AWS IAM, verified against AWS documentation on 2026-08-18.
* [AWS KMS runbook and reference (summary)](sources/aws-kms.md) - Summary of the legacy AWS runbook and reference note for AWS KMS, verified against AWS documentation on 2026-08-19.
* [AWS Lambda runbook and reference (summary)](sources/aws-lambda.md) - Summary of the legacy AWS runbook and reference note for AWS Lambda, verified against AWS documentation on 2026-08-18.
* [AWS Organizations runbook and reference (summary)](sources/aws-organizations.md) - Summary of the legacy AWS runbook and reference note for AWS Organizations, verified against AWS documentation on 2026-08-19.
* [AWS pricing models runbook and reference (summary)](sources/aws-pricing-models.md) - Summary of the legacy AWS runbook and reference note for AWS pricing models, verified against AWS documentation on 2026-08-19.
* [AWS Secrets Manager runbook and reference (summary)](sources/aws-secrets-manager.md) - Summary of the legacy AWS runbook and reference note for AWS Secrets Manager, verified against AWS documentation on 2026-08-19.
* [AWS Security Hub CSPM runbook and reference (summary)](sources/aws-security-hub.md) - Summary of the legacy AWS runbook and reference note for AWS Security Hub CSPM, verified against AWS documentation on 2026-08-19.
* [AWS Shared Responsibility Model runbook and reference (summary)](sources/aws-shared-responsibility-model.md) - Summary of the legacy AWS runbook and reference note for AWS Shared Responsibility Model, verified against AWS documentation on 2026-08-19.
* [AWS Systems Manager runbook and reference (summary)](sources/aws-systems-manager.md) - Summary of the legacy AWS runbook and reference note for AWS Systems Manager, verified against AWS documentation on 2026-08-19.
* [AWS Well-Architected Framework runbook and reference (summary)](sources/aws-well-architected.md) - Summary of the legacy AWS runbook and reference note for AWS Well-Architected Framework, verified against AWS documentation on 2026-08-19.
* [Bash SRE quick reference (summary)](sources/bash-quick-reference.md) - Summary of the legacy interview quick reference that answers log questions with short Unix filter pipelines.
* [Building an AI-Native Revenue Organization (summary)](sources/ai-native-revenue-org.md) - Summary of Anthropic's 2026-09-15 guide and eBook on rolling Claude out across a sales organization.
* [Building and structuring an AI-native company (summary)](sources/ai-native-company-structure-video.md) - Summary of the legacy note on a talk proposing that companies be built as self-improving AI loops.
* [Claude Code Cloud Sessions (summary of the official docs)](sources/claude-cloud-sessions.md) - Summary of Anthropic's Use Claude Code in the cloud documentation, reviewed on 2026-09-18.
* [Claude Code GitHub Actions (summary of the official docs)](sources/claude-github-actions.md) - Summary of Anthropic's Claude Code GitHub Actions documentation for anthropics/claude-code-action@v1, reviewed on 2026-09-15.
* [Claude Managed Agents (summary of the official overview)](sources/claude-managed-agents.md) - Summary of Anthropic's Claude Managed Agents overview documentation, reviewed on 2026-09-15 while the product was in beta.
* [Claude Projects, Redesigned (announcement summary)](sources/claude-projects.md) - Summary of Anthropic's 2026-09-17 announcement that Claude Projects became one long-running conversation coordinating parallel threads.
* [Cloud Practitioner (CLF-C02) study outline (summary)](sources/aws-cert-cloud-practitioner.md) - Summary of the legacy Cloud Practitioner (CLF-C02) study outline, verified against AWS documentation on 2026-08-19.
* [Common Ubuntu APT operations (summary)](sources/ubuntu-apt-guide.md) - Summary of the legacy guide to installing, upgrading, inspecting, and troubleshooting packages on Ubuntu with APT and dpkg.
* [Developer Associate (DVA-C02) study outline (summary)](sources/aws-cert-developer-associate.md) - Summary of the legacy Developer Associate (DVA-C02) study outline, verified against AWS documentation on 2026-08-19.
* [Elastic Load Balancing runbook and reference (summary)](sources/aws-elb.md) - Summary of the legacy AWS runbook and reference note for Elastic Load Balancing, verified against AWS documentation on 2026-08-19.
* [Essential Git commands for operations (summary)](sources/git-operations-reference.md) - Summary of the legacy operations-oriented Git reference: inspect first, sync deliberately, prefer revert on shared branches.
* [Every company should have a brain (summary)](sources/company-brain-video.md) - Summary of the legacy note on Garry Tan's talk about skills as an organization and a curated company memory.
* [Express BFF incidents runbook (summary)](sources/express-bff-incidents-runbook.md) - Summary of the legacy runbook covering ten common incidents for an Express BFF supervised by PM2 cluster mode.
* [Express BFF production deployment guide (summary)](sources/express-bff-deployment-guide.md) - Summary of the legacy beginner guide for deploying a Node.js Express backend-for-frontend under PM2 cluster mode on a Linux VM.
* [Ghostty workstation (summary)](sources/ghostty-workstation.md) - Summary of the legacy manual setup for the Ghostty terminal and a small set of terminal tools on macOS and Ubuntu 26.04.
* [Git basics: git add (summary)](sources/git-tutorial-02-add.md) - Summary of the legacy beginner chapter on git add, part of a seven-chapter command-line tutorial.
* [Git basics: git clone (summary)](sources/git-tutorial-01-clone.md) - Summary of the legacy beginner chapter on git clone, part of a seven-chapter command-line tutorial.
* [Git basics: git commit (summary)](sources/git-tutorial-04-commit.md) - Summary of the legacy beginner chapter on git commit, part of a seven-chapter command-line tutorial.
* [Git basics: git diff (summary)](sources/git-tutorial-06-diff.md) - Summary of the legacy beginner chapter on git diff, part of a seven-chapter command-line tutorial.
* [Git basics: git init (summary)](sources/git-tutorial-00-init.md) - Summary of the legacy beginner chapter on git init, part of a seven-chapter command-line tutorial.
* [Git basics: git log (summary)](sources/git-tutorial-05-log.md) - Summary of the legacy beginner chapter on git log, part of a seven-chapter command-line tutorial.
* [Git basics: git status (summary)](sources/git-tutorial-03-status.md) - Summary of the legacy beginner chapter on git status, part of a seven-chapter command-line tutorial.
* [GitHub Certified: Agentic AI Developer (study notes)](sources/gh-600-study-notes.md) - Study notes for GitHub's GH-600 exam and its Microsoft Learn course, with one architecture module read in full.
* [How Claude Code Auto Mode Works (video summary)](sources/claude-auto-mode.md) - Summary of Claude's 2026-08-04 video explaining how Auto Mode reviews higher-risk actions with a separate classifier.
* [How to actually start your own business (summary)](sources/start-a-business-video.md) - Summary of the legacy note on a video outlining seven steps for starting a small business.
* [How to build a company with AI from the ground up (summary)](sources/ai-company-ground-up-video.md) - Summary of the legacy note on a Y Combinator talk treating AI as the company's operating system.
* [How Warp Builds Self-Improving Agents on Claude (summary)](sources/warp-self-improving-agents.md) - Summary of an Anthropic post and Warp webinar on agents that improve their own skill files through reviewed pull requests.
* [Introduction to Claude Code Agent Skills (course study guide)](sources/claude-agent-skills-course.md) - Study guide covering all six lessons of Anthropic Academy's Introduction to agent skills course.
* [Introduction to Claude Code Subagents (course study guide)](sources/claude-subagents-course.md) - Study guide covering all four lessons of Anthropic Academy's Introduction to subagents course.
* [Kubernetes IP or ENI exhaustion runbook (summary)](sources/k8s-ip-eni-runbook.md) - Summary of the legacy runbook for Pods stuck Pending on ENI or IP capacity in an ENI-based Kubernetes network.
* [Modern BFF architecture assessment (summary)](sources/modern-bff-assessment.md) - Summary of the legacy guide for deciding whether and how to modernize a gateway, Node.js BFF, and downstream request path.
* [Nginx production deployment guide (summary)](sources/nginx-production-guide.md) - Summary of the legacy beginner guide for deploying Nginx as a static server and reverse proxy with HTTPS on one Ubuntu 24.04 VM.
* [OpenResty production deployment guide (summary)](sources/openresty-production-guide.md) - Summary of the legacy beginner guide for deploying OpenResty with a Lua health endpoint and reverse proxy on one Ubuntu 24.04 VM.
* [Publish changes to GitHub (summary)](sources/git-publish-guide.md) - Summary of the legacy beginner guide to the branch, commit, push, pull request, and merge workflow on GitHub.
* [Solutions Architect Associate (SAA-C03) study outline (summary)](sources/aws-cert-solutions-architect.md) - Summary of the legacy Solutions Architect Associate (SAA-C03) study outline, verified against AWS documentation on 2026-08-19.
* [The AI-Native SDLC Playbook (summary)](sources/ai-native-sdlc-playbook.md) - Summary of Anthropic's 2026-08-21 playbook that redesigns software delivery as a loop of versioned artifacts with human approval gates.
* [The awk command (summary)](sources/bash-awk.md) - Summary of the legacy note on awk: fields, conditions, delimiters, and finding a field number in a log.
* [The uniq command (summary)](sources/bash-uniq.md) - Summary of the legacy note on uniq and why it almost always follows sort.
* [Three simple database websites (summary)](sources/database-websites-video.md) - Summary of the legacy note on a Starter Story interview about a portfolio of database and directory SaaS products.
* [Understanding Apple Container (summary)](sources/apple-container.md) - Summary of the legacy overview of apple/container, Apple's native macOS container tool that runs each container in its own lightweight VM.
* [What happens when AI agents run the business (summary)](sources/kavak-agents-video.md) - Summary of the legacy note on an a16z video in which Kavak describes running sales, lending, and operations with agents.
* [ZooKeeper beginner tutorial (summary)](sources/zookeeper-getting-started.md) - Summary of the legacy beginner tutorial explaining what ZooKeeper is for and trying its CLI against a local server.
* [ZooKeeper disk-full recovery runbook (summary)](sources/zookeeper-disk-full-runbook.md) - Summary of the legacy runbook for rebuilding one ZooKeeper member whose transaction log was truncated by a full disk.
* [ZooKeeper production deployment guide (summary)](sources/zookeeper-production-guide.md) - Summary of the legacy reference guide for a three-member ZooKeeper 3.9.5 ensemble on Ubuntu 24.04 with TLS, systemd, and monitoring.
* [ZooKeeper quorum-loss snapshot restore runbook (summary)](sources/zookeeper-quorum-loss-runbook.md) - Summary of the legacy incident runbook for restoring a three-member ZooKeeper ensemble from one approved snapshot after quorum loss.
