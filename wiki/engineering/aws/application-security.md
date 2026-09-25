---
type: Service
title: AWS application security
description: "Protecting internet-facing AWS applications: web filtering, DDoS protection, TLS certificates, app sign-in, directories, and hardware key storage."
tags: [aws, security]
sources:
  - id: aws-waf
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/waf/README.md
    title: "AWS WAF - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-shield
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/shield/README.md
    title: "AWS Shield - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-acm
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/acm/README.md
    title: "AWS Certificate Manager (ACM) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cognito
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cognito/README.md
    title: "Amazon Cognito - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-directory-service
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/directory-service/README.md
    title: "AWS Directory Service - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cloudhsm
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudhsm/README.md
    title: "AWS CloudHSM - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services protect an application at its edges: filtering and absorbing hostile traffic, serving TLS, signing users in, and holding keys in dedicated hardware. They complement the account-level controls on [AWS IAM](iam.md) and [encryption and secrets](encryption-and-secrets.md).

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS WAF](#aws-waf) | AWS WAF is a web application firewall that monitors HTTP(S) requests to protected resources and controls access based on rules (IP addresses, query strings, headers, body) |
| [AWS Shield](#aws-shield) | AWS Shield is a managed Distributed Denial of Service (DDoS) protection service |
| [AWS Certificate Manager (ACM)](#aws-certificate-manager-acm) | ACM is a certificate lifecycle machine, not just a certificate store |
| [Amazon Cognito](#amazon-cognito) | Cognito answers two different questions with two different components |
| [AWS Directory Service](#aws-directory-service) | AWS Directory Service provides managed directory options for using Microsoft Active Directory (AD) and LDAP with AWS services and workloads |
| [AWS CloudHSM](#aws-cloudhsm) | CloudHSM splits control into two planes that never overlap |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS WAF

AWS WAF is a web application firewall that monitors HTTP(S) requests to protected resources and controls access based on rules (IP addresses, query strings, headers, body). It responds with the content, an HTTP 403, or a custom response.

Key points:

- Web ACL: the container of rules associated with a protected resource.
- Rules and rule groups: individual match statements or reusable groups; AWS managed rule groups cover common threats.
- Rate-based rules: limit requests from an IP within a window; useful against DDoS/bot traffic.
- Actions: allow, block, count, or custom response; use `count` to test before blocking.
- Labels and logging: label matching requests and send logs to S3, CloudWatch Logs, or Kinesis Data Firehose.

Practices:

- Start with AWS managed rule groups and add custom rules for your use case.
- Add rate-based rules for DDoS/bot protection.
- Test rules in count mode first, then switch to block after reviewing logs.

| Symptom | Check |
| --- | --- |
| Legitimate traffic blocked | Review the matching rule in logs; run in count mode; adjust IP sets or rule scope. |
| Unexpected `403` | Check web ACL association, rule actions, and managed rule group behavior. |
| Logs not appearing | Verify logging configuration and destination permissions. |
| Performance impact | Keep rule count manageable and use efficient match statements. |

Rule, rule group, and web ACL quotas apply per account and scope. See the Service Quotas console for current values.[^aws-waf]


## AWS Shield

AWS Shield is a managed Distributed Denial of Service (DDoS) protection service. Shield Standard is enabled automatically for all AWS customers at no additional cost and protects internet-facing applications against common volumetric attacks (for example, UDP reflection and TCP SYN floods). Shield Advanced is a paid tier that adds enhanced detection and mitigation, protection groups, health-based detection, cost protection, and access to the AWS Shield Response Team (SRT).

Key points:

- Volumetric attack: floods bandwidth (UDP reflection, SYN floods); mostly absorbed by the AWS edge.
- State-exhaustion / application-layer attack: targets connection state or the application; mitigated with Shield Advanced and AWS WAF.
- Protection: a Shield Advanced configuration that monitors a specific resource ARN, such as CloudFront distributions, Route 53 hosted zones, Global Accelerator accelerators, Elastic IPs, and load balancers.
- Protection group: a collection of protections aggregated for monitoring and attack response; patterns include `ALL`, `ARBITRARY`, and `BY_RESOURCE_TYPE`.
- Health-based detection: uses Route 53 health checks and CloudWatch metrics to detect attacks that affect availability.

Practices:

- Design for DDoS resiliency: put traffic behind CloudFront, Global Accelerator, or a load balancer; never expose origin IPs publicly.
- Use Shield Advanced for business-critical, customer-facing applications and add protections for every relevant resource ARN.
- Combine with AWS WAF (managed rule groups, rate-based rules) for application-layer attacks.

| Symptom | Check |
| --- | --- |
| Attack reaches the origin | Verify origin IPs are not exposed; route all traffic through CloudFront/ALB/Global Accelerator and restrict direct access. |
| Shield Advanced not detecting an attack | Confirm the resource ARN is protected and health checks/metrics are configured and healthy. |
| Cost spike during an attack | Enable cost protection and billing alerts; review usage after the event. |
| Application-layer attacks still succeed | Add AWS WAF rate-based rules and managed rule groups; keep the resource protected with Shield Advanced. |

Shield Advanced: up to 1,000 protected resources per account per resource type (adjustable), up to 100 protection groups, and up to 1,000 individually listed members per protection group. Check the Service Quotas console for current values.[^aws-shield]


## AWS Certificate Manager (ACM)

ACM is a certificate lifecycle machine, not just a certificate store: it issues or imports a certificate, proves domain ownership through validation, and: only for certificates it issued itself, keeps renewing that proof forever. AWS Certificate Manager (ACM) handles the complexity of creating, storing, and renewing public and private SSL/TLS X.509 certificates for AWS services. It issues certificates directly, or imports third-party certificates for management, and supports single domains, multiple names, and wildcard certificates.

Key points:

- Certificate: an X.509 certificate bound to one or more domain names (SANs).
- Validation: DNS validation (recommended) or email validation proves domain ownership; certificates are revalidated for renewal.
- Automated renewal: ACM renews and revalidates ACM-issued certificates automatically; imported certificates are not renewed automatically.
- Regional resources: certificates are regional; you must request/import a certificate in each Region (CloudFront requires us-east-1).
- ACM Private CA: issue private certificates for internal PKI use cases.

Practices:

- Use DNS validation so renewal happens automatically without manual email steps.
- Create certificates in the same Region as the consuming resource; use us-east-1 for CloudFront.
- Use wildcard certificates carefully; scope them to the domains you own.

| Symptom | Check |
| --- | --- |
| Certificate stuck in pending validation | Verify the DNS record matches the value shown and DNS propagation completed. |
| Renewal failed | Revalidate DNS/email; confirm the domain still resolves to the expected validation record. |
| Certificate not found for a service | Confirm the certificate is in the same Region as the resource (CloudFront: us-east-1). |
| Import fails | Check PEM format and that the private key matches the certificate. |

Certificates per account per Region, domain names per certificate, and ACM Private CA quotas apply. See the Service Quotas console for current values. ACM public certificates issued for AWS services have no additional ACM charge.[^aws-acm]


## Amazon Cognito

Cognito answers two different questions with two different components: a user pool answers "who is this person" and hands back a JWT, while an identity pool answers "what AWS resources can they touch" and hands back temporary AWS credentials: an app that only needs the first component never needs an identity pool at all. Amazon Cognito provides authentication, authorization, and user management for web and mobile applications. It has two main components: user pools, which manage sign-up/sign-in and identity federation, and identity pools, which exchange authenticated or guest identities for temporary AWS credentials.

Key points:

- User pool: a user directory with sign-up and sign-in flows, password policies, MFA (TOTP, SMS), account recovery, and managed login pages. It supports federation with social IdPs (Apple, Facebook, Google, Amazon) and OIDC/SAML providers, and issues JWTs to app clients.
- App client: an application configuration in the user pool with an ID/secret and allowed OAuth scopes and callback URLs.
- Identity pool: exchanges tokens from user pools or external IdPs for temporary AWS credentials through AWS Security Token Service (STS); supports role-based access (roles mapped per identity) and attribute-based access control; unauthenticated (guest) identities can receive scoped credentials.
- User pool + identity pool flow: users authenticate in the user pool, then the identity pool grants them AWS credentials authorized for your app's AWS resources (for example, S3, DynamoDB, API Gateway).
- Hosted/managed login: Cognito-hosted sign-in pages that can be customized and used with OAuth 2.0 and OIDC flows.

Practices:

- Use user pools for sign-up/sign-in and identity pools only when the app needs AWS credentials; keep the two roles separate.
- Enforce strong password policies and MFA for sensitive applications; choose TOTP over SMS where possible.
- Restrict app client scopes, origins, and callback URLs; use separate clients per platform.

| Symptom | Check |
| --- | --- |
| Login fails | Check the user status (for example, FORCE_CHANGE_PASSWORD), account confirmation, and MFA configuration. |
| Token rejected by API Gateway/ALB | Verify the authorizer/JWT audience matches the app client ID and the token is not expired. |
| No AWS credentials from identity pool | Confirm the identity pool is linked to the user pool/IdP and the role mapping and trust policy are correct. |
| Guest access errors | Verify unauthenticated identities are enabled and the unauthenticated role has the needed scoped permissions. |

User pools per Region, users per pool, app clients per pool, identity pools per Region, and API request rates have quotas. See the Amazon Cognito endpoints and quotas page and Service Quotas console for current values.[^aws-cognito]


## AWS Directory Service

AWS Directory Service provides managed directory options for using Microsoft Active Directory (AD) and LDAP with AWS services and workloads. You can run a fully managed Microsoft AD in the cloud, connect AWS applications to your existing on-premises AD, or use a low-cost AD-compatible directory, depending on your needs.

Key points:

- AWS Managed Microsoft AD: a real Microsoft Windows Server Active Directory managed by AWS; supports AD-aware applications, EC2 domain join, RDS for SQL Server, WorkSpaces, Group Policy, schema extensions, LDAPS, MFA, and trusts with on-premises AD.
- AD Connector: a proxy that lets compatible AWS applications (WorkSpaces, EC2 Windows domain join, console sign-in) authenticate against your existing on-premises AD, without directory sync or federation infrastructure.
- Simple AD: a low-cost Microsoft AD-compatible directory powered by Samba 4 for basic user/group management, domain join, Kerberos-based SSO, and group policy; does not support MFA, trusts, schema extensions, LDAPS, or RDS SQL Server.
- Managed operations: AWS provides monitoring, daily snapshots, and recovery for Managed Microsoft AD and Simple AD.
- Identity options: for high-scale SaaS user directories with social identities, AWS recommends Amazon Cognito.

Practices:

- Choose Managed Microsoft AD when you need real AD features, RDS SQL Server, trusts, or LDAPS; use Simple AD only for basic, low-cost needs.
- Use AD Connector when your source of truth must remain on-premises and you only need authentication for AWS applications.
- Deploy domain controllers across multiple Availability Zones (Managed Microsoft AD does this for you) and monitor directory health.

| Symptom | Check |
| --- | --- |
| Domain join fails | Check DNS resolution to the directory, security group rules (TCP/UDP 389, 445, 88, 464, 3268), and credentials. |
| Users cannot authenticate | Verify the directory status is ACTIVE, the trust (if any) is configured, and password policies are correct. |
| LDAPS not working | Ensure a CA certificate is imported and the LDAPS port (636) is reachable. |
| AD Connector errors | Confirm the service account in on-premises AD has the required read permissions and connectivity. |

Directories per account per Region, objects per directory (by edition), and domain controllers have quotas. See the AWS Directory Service endpoints and quotas page and Service Quotas console for current values.[^aws-directory-service]


## AWS CloudHSM

CloudHSM splits control into two planes that never overlap: IAM governs who can call the CloudHSM API to manage clusters and HSMs, while HSM users: created and managed inside the HSM itself, invisible to IAM, govern who can use the keys. AWS cannot see either your keys or your HSM users. AWS CloudHSM provides dedicated, single-tenant hardware security modules (HSMs) in the AWS Cloud. HSMs process cryptographic operations and store keys in tamper-resistant hardware. CloudHSM gives you full control over keys and algorithms, with AWS managing HSM provisioning, backups, configuration, and maintenance. It is the right choice when you need your own HSMs; for a managed key service, use AWS KMS instead.

Key points:

- Cluster: a group of HSMs in one VPC; clusters run in FIPS mode (FIPS 140-2/140-3 Level 3 validated keys and algorithms only) or non-FIPS mode (all supported keys/algorithms).
- Single tenant and private: HSMs are dedicated to your account, and the data plane is end-to-end encrypted so AWS cannot see your keys.
- HSM users: you manage users and permissions inside the HSM (outside IAM); IAM controls the CloudHSM API, HSM users control keys.
- Client SDKs: integrate applications using PKCS #11, Java Cryptography Extension (JCE), Cryptography API: Next Generation (CNG), or Key Storage Provider (KSP).
- Full key control: generate, store, import, export, and use symmetric keys and asymmetric key pairs; control algorithms.

Practices:

- Use at least two HSMs in different Availability Zones for high availability.
- Choose FIPS mode only when FIPS validation is required; use non-FIPS mode when your workloads need other algorithms.
- Separate duties: IAM for the CloudHSM API, HSM users for keys, and least-privilege policies for both.

| Symptom | Check |
| --- | --- |
| Cluster initialization fails | Verify the signed certificate matches the cluster and the trust anchor is a valid CA certificate. |
| Clients cannot connect | Check security groups, client SDK configuration, and that HSMs are active in the cluster. |
| HSM user login denied | Confirm the user exists in the HSM and the password policy/retry limits are understood. |
| Backup restore slow | Restore to a new cluster in the same Region; cross-Region restore has additional constraints. |

HSMs per cluster, clusters per account per Region, and backup limits apply. See the AWS CloudHSM endpoints and quotas page and Service Quotas console for current values.[^aws-cloudhsm]


## Related

- [Global traffic](global-traffic.md): CloudFront and Global Accelerator, where WAF and Shield usually sit.
- [Encryption and secrets](encryption-and-secrets.md)
- [Domain index](index.md)

[^aws-waf]: [AWS WAF - Runbook & Reference](../../sources/aws-waf.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/waf/README.md)
[^aws-shield]: [AWS Shield - Runbook & Reference](../../sources/aws-shield.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/shield/README.md)
[^aws-acm]: [AWS Certificate Manager (ACM) - Runbook & Reference](../../sources/aws-acm.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/acm/README.md)
[^aws-cognito]: [Amazon Cognito - Runbook & Reference](../../sources/aws-cognito.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cognito/README.md)
[^aws-directory-service]: [AWS Directory Service - Runbook & Reference](../../sources/aws-directory-service.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/directory-service/README.md)
[^aws-cloudhsm]: [AWS CloudHSM - Runbook & Reference](../../sources/aws-cloudhsm.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudhsm/README.md)
