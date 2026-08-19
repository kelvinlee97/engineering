# AWS Artifact - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Artifact provides on-demand access to AWS security and compliance documents, including ISO, PCI, and SOC reports, and certifications from accreditation bodies. You can also review, accept, and track agreements with AWS for your account and organization, and use Assurance Assistant to answer compliance and due-diligence questions. AWS Artifact documents and agreements are provided free of charge.

## Key concepts

- **Compliance reports**: downloadable reports such as ISO, PCI DSS, SOC 1/2/3, and region/service-specific compliance documents that you can submit to auditors.
- **Agreements**: AWS agreements (for example, Business Associate Addendum) that you review, accept, and track per account or across your organization.
- **Marketplace Vendor Insights**: access security and compliance documents for independent software vendors (ISVs) selling on AWS Marketplace.
- **Assurance Assistant**: AI-powered answers to your compliance and due-diligence questions based on AWS compliance documentation.
- **Shared responsibility context**: Artifact documents demonstrate AWS's controls; you remain responsible for obtaining and producing documents for your own organization's compliance.

## Common operations (AWS CLI)

```bash
# List and download reports
aws artifact list-customer-agreements
aws artifact get-report --report-id <report-id>

# Manage agreements
aws artifact list-agreements
aws artifact get-customer-agreement --agreement-id <agreement-id>
aws artifact accept-agreement --agreement-id <agreement-id>
```

## Best practices

- Download current reports each audit cycle; compliance reports are periodically reissued and previous versions may not be accepted.
- Accept and track agreements centrally in the management account so organization-wide agreements are visible.
- Use Assurance Assistant for initial due-diligence questions, then verify answers against the underlying reports.
- Combine Artifact documents with your own compliance evidence (AWS Config rules, backup policies, access reviews) for a complete audit package.
- Restrict Artifact access with IAM; monitor downloads with CloudTrail.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Report not found | Verify the report ID and that your account is eligible for that report/region. |
| Agreement cannot be accepted | Confirm you have the required IAM permissions and the agreement is not already terminated. |
| Vendor documents missing | Access Marketplace Vendor Insights from the AWS Marketplace console for that ISV. |
| Assurance Assistant unavailable | Check that the feature is enabled for your account/region. |
| Organization agreements not visible | Manage organization-wide agreements from the management account. |

## Limits

AWS Artifact documents and agreements are free; access permissions and API quotas apply. See the AWS Artifact user guide and IAM documentation for current details.

## Official references

- [What is AWS Artifact?](https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html)
- [AWS Artifact agreements](https://docs.aws.amazon.com/artifact/latest/ug/managing-agreements.html)
- [AWS Artifact FAQ](https://aws.amazon.com/artifact/faq/)
- [AWS CLI: artifact commands](https://docs.aws.amazon.com/cli/latest/reference/artifact/)
