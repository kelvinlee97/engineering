# AWS Certificate Manager (ACM) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Certificate Manager (ACM) handles the complexity of creating, storing, and renewing public and private SSL/TLS X.509 certificates for AWS services. It issues certificates directly, or imports third-party certificates for management, and supports single domains, multiple names, and wildcard certificates.

## Key concepts

- **Certificate**: an X.509 certificate bound to one or more domain names (SANs).
- **Validation**: DNS validation (recommended) or email validation proves domain ownership; certificates are revalidated for renewal.
- **Automated renewal**: ACM renews and revalidates ACM-issued certificates automatically; imported certificates are not renewed automatically.
- **Regional resources**: certificates are regional; you must request/import a certificate in each Region (CloudFront requires us-east-1).
- **ACM Private CA**: issue private certificates for internal PKI use cases.
- **Export**: certificates signed by AWS Private CA can be exported for use outside AWS; ACM-issued public certificates cannot be exported.

## Common operations (AWS CLI)

```bash
# Request a public certificate with DNS validation
aws acm request-certificate --domain-name example.com \
  --validation-method DNS \
  --subject-alternative-names "*.example.com"

# Check status and get the DNS validation record
aws acm describe-certificate --certificate-arn <certificate-arn>

# List certificates
aws acm list-certificates --certificate-statuses ISSUED

# Import a third-party certificate
aws acm import-certificate --certificate fileb://cert.pem \
  --private-key fileb://private.key \
  --certificate-chain fileb://chain.pem

# Delete a certificate
aws acm delete-certificate --certificate-arn <certificate-arn>
```

## Best practices

- Use DNS validation so renewal happens automatically without manual email steps.
- Create certificates in the same Region as the consuming resource; use us-east-1 for CloudFront.
- Use wildcard certificates carefully; scope them to the domains you own.
- Prefer ACM-issued certificates for AWS services (ALB, CloudFront, API Gateway) so renewal is automated.
- For EC2/on-premises servers, use ACME automation or ACM Private CA instead of ACM public certificates (which can't be exported).
- Rotate imported certificates before expiry and monitor expiry with CloudWatch.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Certificate stuck in pending validation | Verify the DNS record matches the value shown and DNS propagation completed. |
| Renewal failed | Revalidate DNS/email; confirm the domain still resolves to the expected validation record. |
| Certificate not found for a service | Confirm the certificate is in the same Region as the resource (CloudFront: us-east-1). |
| Import fails | Check PEM format and that the private key matches the certificate. |
| Wildcard not covering subdomains | Confirm the certificate covers the exact names you need (including dots). |

## Limits

Certificates per account per Region, domain names per certificate, and ACM Private CA quotas apply. See the Service Quotas console for current values. ACM public certificates issued for AWS services have no additional ACM charge.

## Official references

- [What is AWS Certificate Manager?](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [AWS Certificate Manager quotas](https://docs.aws.amazon.com/acm/latest/userguide/acm-limits.html)
- [AWS Certificate Manager pricing](https://aws.amazon.com/certificate-manager/pricing/)
- [AWS CLI: acm commands](https://docs.aws.amazon.com/cli/latest/reference/acm/)
