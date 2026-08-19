# AWS Cloud9 - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Cloud9 is a cloud-based integrated development environment (IDE) accessed from a web browser. It provides code editing, debugging, a built-in terminal, and direct integration with AWS services. **Cloud9 is no longer available to new customers**; existing customers can continue to use the service as normal.

## Key concepts

- **Environment**: a place storing your project files and running your development tools; connected to a compute resource.
- **EC2 environment**: Cloud9 creates and manages an EC2 instance for you (recommended).
- **SSH environment**: Cloud9 connects to an existing cloud instance or your own server over SSH.
- **IDE**: browser-based editor with language support, debuggers, and a terminal.
- **Integration**: clone repositories (CodeCommit, GitHub), run Docker, develop with the AWS CDK, and deploy serverless applications.

## Common operations (AWS CLI)

```bash
# Create an EC2 environment
aws cloud9 create-environment-ec2 --name devbox \
  --instance-type t3.micro --image-id amazonlinux-2023-x86_64 \
  --subnet-id subnet-0123456789abcdef0

# Describe and update environments
aws cloud9 describe-environments --environment-ids <env-id>
aws cloud9 describe-environment-memberships --environment-id <env-id>
aws cloud9 update-environment --environment-id <env-id> --name devbox-v2

# Share with a user
aws cloud9 create-environment-membership --environment-id <env-id> \
  --user-arn arn:aws:iam::123456789012:user/developer --permissions read-write

# Delete
aws cloud9 delete-environment --environment-id <env-id>
```

## Best practices

- Note the current lifecycle: new customer onboarding is closed; plan alternatives (for example, IDE toolkits + EC2/CloudShell) for new projects.
- For existing environments, use EC2 environments with a managed instance and keep the IDE/instance patched.
- Attach an IAM instance profile with least privilege; never store long-term keys in the environment.
- Use shared environments with `read-write`/`read-only` memberships for pairing, and remove members when done.
- Store code in a repository (CodeCommit/GitHub) so environments are disposable.
- Stop EC2 environments when idle to control cost; delete unused environments.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cannot open IDE | Check environment status and browser/network access to the environment URL. |
| EC2 environment slow | Right-size the instance type or stop/restart the environment. |
| Permissions errors | Verify the instance profile/role policies for the services you use. |
| SSH environment unreachable | Check the server SSH config, keys, and security group rules. |
| Environment full | Increase instance disk or clean up workspaces. |

## Limits

Environments per account and EC2 environment instance sizes are subject to quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Cloud9?](https://docs.aws.amazon.com/cloud9/latest/user-guide/welcome.html)
- [AWS Cloud9 service quotas](https://docs.aws.amazon.com/cloud9/latest/user-guide/limits.html)
- [AWS CLI: cloud9 commands](https://docs.aws.amazon.com/cli/latest/reference/cloud9/)
