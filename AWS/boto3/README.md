# boto3 (AWS SDK for Python) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

boto3 is the AWS SDK for Python. It provides low-level service clients (a nearly 1:1 mapping to service APIs), higher-level resource abstractions for some services, and core features like pagination, waiters, retries, and multi-session credential handling.

## Key concepts

- **Client**: low-level interface; `boto3.client('s3')` returns a client whose methods map to API operations.
- **Resource**: higher-level object interface; `boto3.resource('s3')` provides collections and attributes (available for a subset of services).
- **Session**: manages configuration and credentials; `boto3.session.Session()` or the default module-level session.
- **Credentials chain**: env vars, shared credentials/config files, IAM roles, SSO, container credentials.
- **Paginators**: handle multi-page API responses with `client.get_paginator(...)`.
- **Waiters**: poll until a resource reaches a desired state (for example, EC2 instance running).
- **botocore exceptions**: `botocore.exceptions.ClientError` carries the error code and message.

## Common operations

```python
import boto3
from botocore.exceptions import ClientError

# Clients and resources
s3 = boto3.client("s3", region_name="ap-southeast-1")
s3r = boto3.resource("s3")

# List objects with pagination
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket="my-bucket", Prefix="logs/"):
    for obj in page.get("Contents", []):
        print(obj["Key"], obj["Size"])

# Upload and download
s3.upload_file("/tmp/file.txt", "my-bucket", "data/file.txt")
s3.download_file("my-bucket", "data/file.txt", "/tmp/file.txt")

# Describe EC2 instances
ec2 = boto3.client("ec2")
instances = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])

# Error handling
try:
    s3.get_object(Bucket="my-bucket", Key="missing.txt")
except ClientError as e:
    print(e.response["Error"]["Code"], e.response["Error"]["Message"])

# Assume a role with a session
sts = boto3.client("sts")
creds = sts.assume_role(RoleArn="arn:aws:iam::123456789012:role/AppRole", RoleSessionName="job")
session = boto3.Session(
    aws_access_key_id=creds["Credentials"]["AccessKeyId"],
    aws_secret_access_key=creds["Credentials"]["SecretAccessKey"],
    aws_session_token=creds["Credentials"]["SessionToken"],
)
```

## Best practices

- Prefer IAM roles and SSO over hard-coded keys; never commit credentials.
- Reuse clients/sessions instead of creating them per call; boto3 manages connection pooling.
- Use paginators for list APIs and waiters instead of sleep loops.
- Set explicit region and retry configuration (`botocore.config.Config(retries={"max_attempts": 5, "mode": "standard"})`).
- Catch `ClientError` and branch on `Error.Code` rather than broad exception handlers.
- Pin boto3/botocore versions and test upgrades in staging.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| `NoCredentialsError` | Check the credential chain: env vars, shared files, roles. |
| `ClientError: AccessDenied` | Verify the IAM policy and the role/profile in use. |
| Slow list operations | Use paginators with `PageSize`, filters, and narrow prefixes. |
| Throttling (`ThrottlingException`) | Increase retry attempts/backoff; request higher quotas if legitimate. |
| `EndpointConnectionError` | Check network, VPC endpoints, and region configuration. |

## Limits

boto3 has no service quotas; service API limits apply. See the Service Quotas console for service-specific values.

## Official references

- [boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [boto3 quickstart](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
- [botocore exceptions reference](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/exceptions.html)
