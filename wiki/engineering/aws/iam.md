---
type: Service
title: AWS IAM
description: "AWS's authentication and authorization service: identities, policies, and temporary credentials that decide who can do what to which resource."
tags: [aws, security, identity]
sources:
  - id: aws-iam
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/iam/README.md
    title: "AWS IAM - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

AWS Identity and Access Management (IAM) controls authentication (who is signed in) and authorization (what they may do) for AWS resources. IAM, IAM Identity Center, and AWS STS carry no additional charge, and IAM is eventually consistent.[^aws-iam] How a request is decided is on [IAM policy evaluation](iam-policy-evaluation.md).

## Building blocks

| Piece | Role |
| --- | --- |
| Root user | The initial full-access identity; not for everyday work |
| Users, groups, roles | Identities for people and workloads; roles give temporary credentials |
| Policies | JSON documents on identities or resources defining permissions |
| AWS STS | Issues temporary credentials, for example `AssumeRole` |
| Permissions boundaries | Cap what identity-based policies can grant |
| Organization SCPs and RCPs | Cross-account boundaries that grant nothing by themselves |

As defined in the note.[^aws-iam]

## Practices

- Temporary credentials everywhere: federated sign-in through [IAM Identity Center](iam-identity-center.md) for people, roles for workloads (instance profiles, Lambda execution roles, ECS/EKS task roles).[^aws-iam]
- MFA for the root user and any long-term credentials; never use root routinely.[^aws-iam]
- Least privilege, starting from AWS managed policies; IAM Access Analyzer can generate least-privilege policies from CloudTrail activity and detect public or cross-account access.[^aws-iam]
- Remove unused users, roles, policies, and keys using last-accessed information.[^aws-iam]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `AccessDenied` | Identity policy, resource policy, SCP/RCP, boundary, session policy; retry after propagation |
| `AssumeRole` fails | The trust policy allows the principal, external ID, session duration within the role maximum (up to 12 hours) |
| Cannot delete a user or role | Remove policies, keys, and memberships first |

As tabled in the note.[^aws-iam]

## Default quotas

1,000 roles, 1,500 customer managed policies, 300 groups, 20 managed policies per role and 10 per user, a managed policy size of 6,144 characters, a maximum session of 12 hours, and 600 STS requests per second per account per Region.[^aws-iam]

## Related

- Source: [AWS IAM - Runbook & Reference](../../sources/aws-iam.md)

[^aws-iam]: AWS IAM - Runbook & Reference
