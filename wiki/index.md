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

* [Agent skills](engineering/claude-code/agent-skills.md) - What a Claude Code skill is, how progressive disclosure keeps it cheap, and the SKILL.md file that defines it.
* [AI-native organization](engineering/ai-engineering/ai-native-organization.md) - What an AI-native company is and the company brain that feeds its agents, as argued in founder and investor talks.
* [Auto Mode and prompt injection](engineering/claude-code/auto-mode.md) - A Claude Code permission mode where a classifier reviews higher-risk actions, and the prompt-injection threat it is built to contain.
* [AWS foundations](engineering/aws/aws-foundations.md) - The shared responsibility model and the Well-Architected Framework, the two ideas the other AWS pages assume.
* [Claude Code extension mechanisms](engineering/claude-code/extension-mechanisms.md) - How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.
* [Claude Code session cost](engineering/claude-code/session-cost.md) - What sets the cost of a Claude Code task on Opus 5.5, and how effort, model choice, caching, and compaction trade tokens against a finished task.
* [Git fundamentals](engineering/git/git-fundamentals.md) - Git's four places, the everyday commands that move work between them, the commit workflow, and keeping secrets out.
* [Python language fundamentals](engineering/python/fundamentals.md) - Core Python semantics for everyday scripts: names and objects, the built-in collections, control flow, functions, and comprehensions.
* [Python program structure](engineering/python/structure.md) - Python beyond a single script: generators, decorators, error handling, resource cleanup, modules, classes, type hints, and tests.
* [Subagents](engineering/claude-code/subagents.md) - What a Claude Code subagent is, when to delegate to one, how to write its task and tools, and the file that defines it.

# Pattern

* [AI adoption and measurement](engineering/ai-engineering/ai-adoption.md) - The four-stage AI adoption ladder and how to measure whether a rollout is paying off.
* [AI-native SDLC](engineering/ai-engineering/ai-native-sdlc.md) - Putting agents into software delivery: the propose-accept boundary, risk-based autonomy, and which work stays deterministic.
* [AWS cost](engineering/aws/cost.md) - How AWS charges (pricing models) and the Billing and Cost Management tools for tracking and controlling spend.
* [AWS multi-account governance](engineering/aws/multi-account-governance.md) - Running many AWS accounts under AWS Organizations, with guardrails applied from the organization rather than per account.
* [AWS security monitoring](engineering/aws/security-monitoring.md) - Recording API activity with CloudTrail, detecting threats with GuardDuty, and aggregating findings in Security Hub into one response pipeline.
* [Incident operations](engineering/operations/incident-operations.md) - Practices shared across the runbooks: troubleshoot layer by layer, change production safely, and close an incident only on evidence.
* [Self-improving skill loop](engineering/ai-engineering/self-improving-skill-loop.md) - A scheduled agent reads human feedback on another agent's output and opens a pull request that edits that agent's skill file.

# Playbook

* [APT package management](engineering/linux/apt-package-management.md) - Install, upgrade, hold, roll back, and troubleshoot Ubuntu packages safely by refreshing, simulating, and inspecting before applying.
* [Branches and pull requests](engineering/git/branches-and-pull-requests.md) - Keeping a branch in sync with its upstream and taking it through the GitHub pull request workflow.
* [Code modernization with agents](engineering/ai-engineering/code-modernization.md) - Preparing and running an agent-driven code modernization, from choosing the target to the certificate, promotion policy, pilot, and token cost.
* [Express backend for frontend](engineering/web-serving/express-bff.md) - The backend-for-frontend pattern, deploying an Express BFF to production, and handling its common incidents.
* [Kubernetes IP or ENI exhaustion](engineering/kubernetes/ip-eni-exhaustion.md) - Diagnose and remediate Pods stuck Pending on ENI or IP capacity in an ENI-based Pod network, in dependency order.
* [Reverse proxy gateway](engineering/web-serving/reverse-proxy-gateway.md) - Terminating HTTPS at an Nginx or OpenResty gateway in front of a private application, and deploying either in production.
* [SRE Python drills](engineering/python/sre-drills.md) - Six interview-style Python drills on an Nginx access log, each solved with the smallest correct algorithm and its time and space cost.
* [Starting a small business](engineering/startups/starting-a-small-business.md) - Founder advice on starting and growing a small business, including database and directory websites as a first product.
* [Undoing and recovering in Git](engineering/git/undo-and-recovery.md) - Choose between restore, reset, revert, and reflog by whether the work is shared, and check a pre-flight list before any destructive Git operation.
* [ZooKeeper recovery](engineering/zookeeper/zookeeper-recovery.md) - Recovering one failed ZooKeeper member, or a whole ensemble that lost quorum, from snapshots and transaction logs.

# Tool

* [Apple Container](engineering/dev-tools/apple-container.md) - Apple's native container tool for Apple silicon Macs, which runs each container in its own lightweight VM instead of one shared Linux VM.
* [AWS operations tooling](engineering/aws/operations-tooling.md) - Monitoring with CloudWatch, defining infrastructure with CloudFormation, and managing instances with Systems Manager.
* [Claude Code on GitHub](engineering/claude-code/github-integration.md) - The Claude GitHub App, the Claude Code GitHub Actions workflow, and PR auto-fix, and how they fit together.
* [Claude Projects](engineering/claude-code/claude-projects.md) - In the September 2026 redesign, a Claude project is one long-running conversation whose coordinator splits a goal into parallel threads sharing memory and a library.

# Service

* [AWS compute](engineering/aws/compute.md) - Choosing AWS compute, and running EC2 instances behind load balancers in Auto Scaling groups.
* [AWS containers and serverless](engineering/aws/containers-and-serverless.md) - Running containers on ECS or EKS with images in ECR, and running functions on Lambda.
* [AWS encryption and secrets](engineering/aws/encryption-and-secrets.md) - Envelope encryption with AWS KMS keys, and storing and rotating credentials in Secrets Manager.
* [AWS IAM](engineering/aws/iam.md) - How AWS IAM grants access: identities and roles, how a request's policies are evaluated, and IAM Identity Center for workforce sign-in.
* [AWS networking](engineering/aws/networking.md) - Amazon VPC for private networks in AWS, and Direct Connect for private links from on-premises.
* [Claude Managed Agents](engineering/claude-code/claude-managed-agents.md) - An Anthropic-hosted agent harness that runs the agent loop, sandbox, and tools for long-running tasks, driven by events instead of your own runtime.
* [Cloud sessions](engineering/claude-code/cloud-sessions.md) - Running Claude Code in a cloud container: what a session is, how its environment is configured, and how work moves between terminal and cloud.
* [ZooKeeper](engineering/zookeeper/zookeeper.md) - What Apache ZooKeeper is, how its ensemble and quorum work, and how to deploy it in production.

# Configuration

* [Ghostty workstation](engineering/dev-tools/ghostty-workstation.md) - A manual setup of the Ghostty terminal plus starship, zoxide, eza, bat, fzf, fd, and ripgrep on macOS or Ubuntu 26.04.

# Command

* [Text processing on the command line](engineering/linux/text-processing.md) - Building shell pipelines for text, with awk for fields and uniq for duplicates.

# Comparison

* [AWS certifications](engineering/aws/certifications.md) - The Cloud Practitioner, Developer Associate, and Solutions Architect Associate exams compared, with the study path the legacy outlines share.
* [AWS data stores](engineering/aws/data-stores.md) - Choosing an AWS data store, and the main options: RDS, DynamoDB, ElastiCache, and S3.
* [AWS global traffic routing](engineering/aws/global-traffic.md) - Getting users to the right AWS endpoint: Route 53 DNS, CloudFront caching, and Global Accelerator, and how to choose between them.
* [AWS messaging](engineering/aws/messaging.md) - Choosing between SQS queues, SNS topics, and EventBridge event buses for decoupling AWS services.

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
* [Claude Opus 5.5 and longer coding sessions (summary)](sources/claude-opus-5-5-context.md) - Summary of Anthropic's 2026-09-24 post on Claude Code usage trends and why Opus 5.5 costs about 40% less to run than Opus 5.
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
* [How to prepare for AI-driven code modernization projects (summary)](sources/ai-code-modernization.md) - Summary of Anthropic's 2026-09-23 field note on the six steps an enterprise completes before and during an agent-driven code modernization.
* [How Warp Builds Self-Improving Agents on Claude (summary)](sources/warp-self-improving-agents.md) - Summary of an Anthropic post and Warp webinar on agents that improve their own skill files through reviewed pull requests.
* [Introduction to Claude Code Agent Skills (course study guide)](sources/claude-agent-skills-course.md) - Study guide covering all six lessons of Anthropic Academy's Introduction to agent skills course.
* [Introduction to Claude Code Subagents (course study guide)](sources/claude-subagents-course.md) - Study guide covering all four lessons of Anthropic Academy's Introduction to subagents course.
* [Kubernetes IP or ENI exhaustion runbook (summary)](sources/k8s-ip-eni-runbook.md) - Summary of the legacy runbook for Pods stuck Pending on ENI or IP capacity in an ENI-based Kubernetes network.
* [Modern BFF architecture assessment (summary)](sources/modern-bff-assessment.md) - Summary of the legacy guide for deciding whether and how to modernize a gateway, Node.js BFF, and downstream request path.
* [Nginx production deployment guide (summary)](sources/nginx-production-guide.md) - Summary of the legacy beginner guide for deploying Nginx as a static server and reverse proxy with HTTPS on one Ubuntu 24.04 VM.
* [OpenResty production deployment guide (summary)](sources/openresty-production-guide.md) - Summary of the legacy beginner guide for deploying OpenResty with a Lua health endpoint and reverse proxy on one Ubuntu 24.04 VM.
* [Publish changes to GitHub (summary)](sources/git-publish-guide.md) - Summary of the legacy beginner guide to the branch, commit, push, pull request, and merge workflow on GitHub.
* [Python Classes Cheatsheet (summary)](sources/py-classes.md) - Summary of the legacy python classes cheatsheet in this repository.
* [Python Comprehensions Cheatsheet (summary)](sources/py-comprehensions.md) - Summary of the legacy python comprehensions cheatsheet in this repository.
* [Python Context Managers Cheatsheet (summary)](sources/py-context-managers.md) - Summary of the legacy python context managers cheatsheet in this repository.
* [Python Control Flow Cheatsheet (summary)](sources/py-control-flow.md) - Summary of the legacy python control flow cheatsheet in this repository.
* [Python Decorators Cheatsheet (summary)](sources/py-decorators.md) - Summary of the legacy python decorators cheatsheet in this repository.
* [Python Dictionaries Cheatsheet (summary)](sources/py-dictionaries.md) - Summary of the legacy python dictionaries cheatsheet in this repository.
* [Python Exceptions Cheatsheet (summary)](sources/py-exceptions.md) - Summary of the legacy python exceptions cheatsheet in this repository.
* [Python Files and Paths Cheatsheet (summary)](sources/py-files-and-paths.md) - Summary of the legacy python files and paths cheatsheet in this repository.
* [Python Functions Cheatsheet (summary)](sources/py-functions.md) - Summary of the legacy python functions cheatsheet in this repository.
* [Python Iterators and Generators Cheatsheet (summary)](sources/py-iterators-and-generators.md) - Summary of the legacy python iterators and generators cheatsheet in this repository.
* [Python Lists Cheatsheet (summary)](sources/py-lists.md) - Summary of the legacy python lists cheatsheet in this repository.
* [Python Loops Cheatsheet (summary)](sources/py-loops.md) - Summary of the legacy python loops cheatsheet in this repository.
* [Python Modules and Packages Cheatsheet (summary)](sources/py-modules-and-packages.md) - Summary of the legacy python modules and packages cheatsheet in this repository.
* [Python SRE HackerRank quick reference (summary)](sources/py-sre-drills.md) - Summary of the legacy Python index page and its six log-parsing and algorithm drills.
* [Python Strings Cheatsheet (summary)](sources/py-strings.md) - Summary of the legacy python strings cheatsheet in this repository.
* [Python Testing Cheatsheet (summary)](sources/py-testing.md) - Summary of the legacy python testing cheatsheet in this repository.
* [Python Tuples and Sets Cheatsheet (summary)](sources/py-tuples-and-sets.md) - Summary of the legacy python tuples and sets cheatsheet in this repository.
* [Python Type Hints Cheatsheet (summary)](sources/py-typing.md) - Summary of the legacy python type hints cheatsheet in this repository.
* [Python Variables and Types Cheatsheet (summary)](sources/py-variables-and-types.md) - Summary of the legacy python variables and types cheatsheet in this repository.
* [Solutions Architect Associate (SAA-C03) study outline (summary)](sources/aws-cert-solutions-architect.md) - Summary of the legacy Solutions Architect Associate (SAA-C03) study outline, verified against AWS documentation on 2026-08-19.
* [The AI-Native SDLC Playbook (summary)](sources/ai-native-sdlc-playbook.md) - Summary of Anthropic's 2026-08-21 playbook that redesigns software delivery as a loop of versioned artifacts with human approval gates.
* [The awk command (summary)](sources/bash-awk.md) - Summary of the legacy note on awk: fields, conditions, delimiters, and finding a field number in a log.
* [The uniq command (summary)](sources/bash-uniq.md) - Summary of the legacy note on uniq and why it almost always follows sort.
* [Three simple database websites (summary)](sources/database-websites-video.md) - Summary of the legacy note on a Starter Story interview about a portfolio of database and directory SaaS products.
* [Understanding Apple Container (summary)](sources/apple-container.md) - Summary of the legacy overview of apple/container, Apple's native macOS container tool that runs each container in its own lightweight VM.
* [What a task costs on Opus 5.5 (summary)](sources/opus-5-5-task-cost.md) - Summary of Addy Osmani's 2026-09-25 claude.dev post pricing Claude Code tasks on Opus 5.5 against Opus 5, and the settings that move the bill.
* [What happens when AI agents run the business (summary)](sources/kavak-agents-video.md) - Summary of the legacy note on an a16z video in which Kavak describes running sales, lending, and operations with agents.
* [ZooKeeper beginner tutorial (summary)](sources/zookeeper-getting-started.md) - Summary of the legacy beginner tutorial explaining what ZooKeeper is for and trying its CLI against a local server.
* [ZooKeeper disk-full recovery runbook (summary)](sources/zookeeper-disk-full-runbook.md) - Summary of the legacy runbook for rebuilding one ZooKeeper member whose transaction log was truncated by a full disk.
* [ZooKeeper production deployment guide (summary)](sources/zookeeper-production-guide.md) - Summary of the legacy reference guide for a three-member ZooKeeper 3.9.5 ensemble on Ubuntu 24.04 with TLS, systemd, and monitoring.
* [ZooKeeper quorum-loss snapshot restore runbook (summary)](sources/zookeeper-quorum-loss-runbook.md) - Summary of the legacy incident runbook for restoring a three-member ZooKeeper ensemble from one approved snapshot after quorum loss.
