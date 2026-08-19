# AWS Directory Service - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Directory Service provides managed directory options for using Microsoft Active Directory (AD) and LDAP with AWS services and workloads. You can run a fully managed Microsoft AD in the cloud, connect AWS applications to your existing on-premises AD, or use a low-cost AD-compatible directory, depending on your needs.

## Key concepts

- **AWS Managed Microsoft AD**: a real Microsoft Windows Server Active Directory managed by AWS; supports AD-aware applications, EC2 domain join, RDS for SQL Server, WorkSpaces, Group Policy, schema extensions, LDAPS, MFA, and trusts with on-premises AD.
  - **Standard Edition**: for small/midsize organizations, approximately up to 30,000 directory objects.
  - **Enterprise Edition**: for larger organizations, approximately up to 500,000 directory objects.
  - **Hybrid**: extends your existing self-managed AD into the AWS Cloud.
- **AD Connector**: a proxy that lets compatible AWS applications (WorkSpaces, EC2 Windows domain join, console sign-in) authenticate against your existing on-premises AD, without directory sync or federation infrastructure.
- **Simple AD**: a low-cost Microsoft AD-compatible directory powered by Samba 4 for basic user/group management, domain join, Kerberos-based SSO, and group policy; does not support MFA, trusts, schema extensions, LDAPS, or RDS SQL Server.
- **Managed operations**: AWS provides monitoring, daily snapshots, and recovery for Managed Microsoft AD and Simple AD.
- **Identity options**: for high-scale SaaS user directories with social identities, AWS recommends Amazon Cognito.

## Common operations (AWS CLI)

```bash
# Create directories
aws ds create-microsoft-ad --name corp.example.com \
  --password '<admin-password>' --edition Enterprise \
  --vpc-settings VpcId=vpc-0123456789abcdef0,SubnetIds=subnet-0123456789abcdef0,subnet-1234567890abcdef0
aws ds create-connector --name onprem-connector \
  --connect-settings file://connector.json
aws ds create-simple-ad --name small.example.com \
  --password '<admin-password>' --size Small \
  --vpc-settings VpcId=vpc-0123456789abcdef0,SubnetIds=subnet-0123456789abcdef0,subnet-1234567890abcdef0

# Inspect and delete
aws ds describe-directories --directory-ids <directory-id>
aws ds get-directory-limits
aws ds delete-directory --directory-id <directory-id>
```

## Best practices

- Choose Managed Microsoft AD when you need real AD features, RDS SQL Server, trusts, or LDAPS; use Simple AD only for basic, low-cost needs.
- Use AD Connector when your source of truth must remain on-premises and you only need authentication for AWS applications.
- Deploy domain controllers across multiple Availability Zones (Managed Microsoft AD does this for you) and monitor directory health.
- Protect admin credentials and enforce password policy; enable MFA for internet-facing access where supported.
- Join EC2 instances via Systems Manager or directory-aware launch settings; use Group Policy consistently with on-premises.
- Monitor snapshots and test directory recovery before relying on it.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Domain join fails | Check DNS resolution to the directory, security group rules (TCP/UDP 389, 445, 88, 464, 3268), and credentials. |
| Users cannot authenticate | Verify the directory status is ACTIVE, the trust (if any) is configured, and password policies are correct. |
| LDAPS not working | Ensure a CA certificate is imported and the LDAPS port (636) is reachable. |
| AD Connector errors | Confirm the service account in on-premises AD has the required read permissions and connectivity. |
| RDS SQL Server join fails | Use AWS Managed Microsoft AD; Simple AD and AD Connector are not compatible with RDS SQL Server. |

## Limits

Directories per account per Region, objects per directory (by edition), and domain controllers have quotas. See the AWS Directory Service endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Directory Service?](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html)
- [AWS Directory Service quotas](https://docs.aws.amazon.com/directoryservice/latest/admin-guide/limits.html)
- [AWS Directory Service pricing](https://aws.amazon.com/directoryservice/pricing/)
- [AWS CLI: ds commands](https://docs.aws.amazon.com/cli/latest/reference/ds/)
