# Amazon Cognito - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Cognito provides authentication, authorization, and user management for web and mobile applications. It has two main components: user pools, which manage sign-up/sign-in and identity federation, and identity pools, which exchange authenticated or guest identities for temporary AWS credentials.

## Key concepts

- **User pool**: a user directory with sign-up and sign-in flows, password policies, MFA (TOTP, SMS), account recovery, and managed login pages. It supports federation with social IdPs (Apple, Facebook, Google, Amazon) and OIDC/SAML providers, and issues JWTs to app clients.
- **App client**: an application configuration in the user pool with an ID/secret and allowed OAuth scopes and callback URLs.
- **Identity pool**: exchanges tokens from user pools or external IdPs for temporary AWS credentials through AWS Security Token Service (STS); supports role-based access (roles mapped per identity) and attribute-based access control; unauthenticated (guest) identities can receive scoped credentials.
- **User pool + identity pool flow**: users authenticate in the user pool, then the identity pool grants them AWS credentials authorized for your app's AWS resources (for example, S3, DynamoDB, API Gateway).
- **Hosted/managed login**: Cognito-hosted sign-in pages that can be customized and used with OAuth 2.0 and OIDC flows.

## Common operations (AWS CLI)

```bash
# User pool and app client
aws cognito-idp create-user-pool --pool-name app-users \
  --policies "PasswordPolicy={MinimumLength=12,RequireUppercase=true}"
aws cognito-idp create-user-pool-client --user-pool-id <pool-id> \
  --client-name web --no-generate-secret

# Admin user operations
aws cognito-idp admin-create-user --user-pool-id <pool-id> --username alice
aws cognito-idp admin-set-user-password --user-pool-id <pool-id> \
  --username alice --password 'ChangeMe-123!' --permanent
aws cognito-idp list-users --user-pool-id <pool-id>

# Identity pool
aws cognito-identity create-identity-pool --identity-pool-name app \
  --allow-unauthenticated-identities \
  --cognito-identity-providers ProviderName=cognito-idp.us-east-1.amazonaws.com/<pool-id>,ClientId=<client-id>
aws cognito-identity list-identity-pools --max-results 10
```

## Best practices

- Use user pools for sign-up/sign-in and identity pools only when the app needs AWS credentials; keep the two roles separate.
- Enforce strong password policies and MFA for sensitive applications; choose TOTP over SMS where possible.
- Restrict app client scopes, origins, and callback URLs; use separate clients per platform.
- Use attribute-based access control in identity pools to minimize the permissions granted per user.
- Disable unauthenticated identities unless guests genuinely need scoped access; never grant broad policies to unauthenticated roles.
- Store secrets (app client secret, IdP credentials) in Secrets Manager and rotate them; monitor sign-in failures.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Login fails | Check the user status (for example, FORCE_CHANGE_PASSWORD), account confirmation, and MFA configuration. |
| Token rejected by API Gateway/ALB | Verify the authorizer/JWT audience matches the app client ID and the token is not expired. |
| No AWS credentials from identity pool | Confirm the identity pool is linked to the user pool/IdP and the role mapping and trust policy are correct. |
| Guest access errors | Verify unauthenticated identities are enabled and the unauthenticated role has the needed scoped permissions. |
| Federation callback fails | Check allowed callback URLs, scopes, and the IdP configuration (client ID/secret, metadata). |

## Limits

User pools per Region, users per pool, app clients per pool, identity pools per Region, and API request rates have quotas. See the Amazon Cognito endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Cognito?](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
- [Amazon Cognito user pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
- [Amazon Cognito identity pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-identity.html)
- [Amazon Cognito endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/cognito_identity.html)
- [Amazon Cognito pricing](https://aws.amazon.com/cognito/pricing/)
- [AWS CLI: cognito-idp and cognito-identity commands](https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/)
