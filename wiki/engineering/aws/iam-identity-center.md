---
type: Service
title: AWS IAM Identity Center
description: "AWS's service for workforce sign-in to many accounts: users or an external identity provider, permission sets, and an access portal."
tags: [aws, security, identity]
sources:
  - id: aws-iam-identity-center
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/iam-identity-center/README.md
    title: "AWS IAM Identity Center - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

IAM Identity Center (the successor to AWS Single Sign-On, renamed in July 2022) centrally manages workforce identities and their access to AWS accounts and cloud applications. It is AWS's recommended service for multi-account access.[^aws-iam-identity-center]

## How access is granted

Users and groups come from the Identity Center directory or an external IdP (such as Okta or Microsoft Entra ID, via SCIM provisioning and SAML 2.0). An **account assignment** gives a user or group a **permission set** (a named collection of IAM policies plus a session duration) in an account, and people sign in through the **access portal** with MFA.[^aws-iam-identity-center] The APIs keep the old `sso`, `sso-admin`, and `identitystore` namespaces; CLI login is `aws sso login`.[^aws-iam-identity-center]

## Practices

- Create the instance in the organization's management account and assign access to groups, not individuals.[^aws-iam-identity-center]
- Use an external IdP as the source of truth with SCIM provisioning; require MFA.[^aws-iam-identity-center]
- Keep permission sets least-privilege with a suitable session duration, and review assignments with CloudTrail.[^aws-iam-identity-center]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| No access to an account | Assignment, group membership, permission set, instance in the management account |
| External IdP users missing | SCIM enabled, bearer token valid, SAML metadata current |
| CLI login error | Re-run `aws configure sso`; session name and start URL match |
| New account invisible | Account is in the organization; re-run assignments |

As tabled in the note.[^aws-iam-identity-center] See also [Multi-account governance](multi-account-governance.md).

## Related

- Source: [AWS IAM Identity Center - Runbook & Reference](../../sources/aws-iam-identity-center.md)

[^aws-iam-identity-center]: AWS IAM Identity Center - Runbook & Reference
