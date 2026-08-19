# AWS Transfer Family - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Transfer Family is a fully managed service for transferring files into and out of AWS storage (Amazon S3 and Amazon EFS) over SFTP, FTPS, FTP, AS2, and browser-based web transfers. You keep your existing clients, authentication, and firewall configurations; AWS manages the servers and scales them automatically. You pay only for what you use.

## Key concepts

- **Server**: a managed endpoint (public or VPC) that accepts one or more protocols (SFTP v3, FTPS, FTP, AS2); associate your hostname and DNS with the endpoint.
- **Storage**: data lives in Amazon S3 (data lakes, third-party uploads, distribution) or Amazon EFS (content management, supply chain, web serving).
- **Identity providers**: service-managed users, AWS Directory Service, or custom identity providers (Lambda-backed, API Gateway) for user authentication.
- **Web apps**: managed browser-based transfer interface for S3 with centralized access management.
- **Managed workflows (MFTW)**: serverless, automated processing of uploaded files (copy, tag, scan, filter, compress/decompress, encrypt/decrypt) with end-to-end visibility.
- **AS2**: B2B protocol for compliance-sensitive workflows (supply chain, payments, ERP/CRM integrations).
- **Ports**: FTP/FTPS data connections use the port range 8192-8200.

## Common operations (AWS CLI)

```bash
# Create a server and a user
aws transfer create-server --protocols SFTP --identity-provider-type SERVICE_MANAGED \
  --endpoint-type PUBLIC --region us-east-1
aws transfer create-user --server-id <server-id> --user-name uploader \
  --role arn:aws:iam::123456789012:role/transfer-role \
  --home-directory /bucket/home/uploader

# List and manage
aws transfer list-servers
aws transfer describe-server --server-id <server-id>
aws transfer update-user --server-id <server-id> --user-name uploader \
  --role arn:aws:iam::123456789012:role/transfer-role
aws transfer delete-server --server-id <server-id>
```

## Best practices

- Use VPC endpoints for private transfer and restrict security groups to the ports/protocols in use.
- Enforce strong authentication: service-managed with strong passwords, MFA where supported, or integrate with Directory Service/custom IdPs.
- Scope IAM roles for users with a home directory and least-privilege S3/EFS access; use logical directories for isolation.
- Enable CloudTrail and CloudWatch for auditing transfer activity; use managed workflows to process files automatically.
- Use AS2 for B2B compliance workflows and web apps for broad business-user access to S3.
- Monitor server health and transfer metrics; set alarms on login failures and transfer errors.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Client cannot connect | Check endpoint type (public/VPC), security groups, DNS, and protocol configuration. |
| Login denied | Verify the identity provider configuration, user name/password, and IAM role for the user. |
| Uploads fail | Check the user's home directory, S3/EFS permissions, and the server's role. |
| FTP/FTPS data connection fails | Ensure the 8192-8200 port range is open for data connections. |
| Managed workflow not running | Review workflow step configuration, IAM role, and execution logs. |

## Limits

Servers, users, managed workflows, and API request rates per account have quotas; FTP/FTPS data connections use a fixed port range. See the AWS Transfer Family endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Transfer Family?](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html)
- [AWS Transfer Family endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/transfer.html)
- [AWS Transfer Family pricing](https://aws.amazon.com/aws-transfer-family/pricing/)
- [AWS CLI: transfer commands](https://docs.aws.amazon.com/cli/latest/reference/transfer/)
