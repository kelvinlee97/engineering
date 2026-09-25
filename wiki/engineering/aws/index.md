# Concept

* [Envelope encryption](envelope-encryption.md) - Encrypt data locally with a data key and store only an encrypted copy of that key, so the key service never handles bulk data.
* [IAM policy evaluation](iam-policy-evaluation.md) - How AWS decides a request: every applicable policy layer is checked, an explicit deny anywhere wins, and nothing is allowed without an explicit allow.

# Pattern

* [AWS multi-account governance](multi-account-governance.md) - Run AWS as many accounts under Organizations, with central sign-in, an organization audit trail, and security services run from delegated administrator accounts.
* [AWS security findings pipeline](security-findings-pipeline.md) - Route GuardDuty and other detector findings through Security Hub CSPM and EventBridge, and export them, because each service keeps only a short fixed history.

# Service

* [Amazon GuardDuty](guardduty.md) - AWS's threat detection service that analyzes CloudTrail, VPC Flow Logs, and DNS logs, plus optional protection plans, to produce findings.
* [AWS CloudTrail](cloudtrail.md) - AWS's audit log of API and console actions, from a free 90-day event history to long-term trails and a queryable data lake.
* [AWS IAM](iam.md) - AWS's authentication and authorization service: identities, policies, and temporary credentials that decide who can do what to which resource.
* [AWS IAM Identity Center](iam-identity-center.md) - AWS's service for workforce sign-in to many accounts: users or an external identity provider, permission sets, and an access portal.
* [AWS KMS](kms.md) - AWS's managed service for creating and controlling encryption and signing keys, used through envelope encryption.
* [AWS Organizations](organizations.md) - AWS's service for managing many accounts as one tree of organizational units with shared billing and policy guardrails.
* [AWS Secrets Manager](secrets-manager.md) - AWS's service for storing versioned secrets that applications fetch at runtime, with scheduled rotation through Lambda.
* [AWS Security Hub CSPM](security-hub.md) - AWS's security posture service that gathers findings from other services and runs continuous checks against security standards.
