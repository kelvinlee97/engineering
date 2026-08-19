# AWS Consulting Offers - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Consulting Offers are packaged consulting engagements from AWS Partners that address specific business outcomes (for example, migration, modernization, security assessments, and data analytics). They are part of the AWS Partner Network (APN) and AWS Marketplace ecosystem, giving customers a scoped, repeatable way to procure partner expertise.

## Key concepts

- **Consulting offers**: fixed-scope engagements from AWS Partners with defined deliverables and outcomes, listed for discovery.
- **Partner ecosystem**: offers come from validated AWS Partners; competency programs validate partner expertise in solution areas.
- **Discovery**: browse offers in AWS Marketplace and AWS Partner resources; filter by use case, industry, and partner.
- **Procurement and execution**: purchase the offer, engage the partner, and track deliverables against the engagement scope.
- **Relationship to AWS assets**: Consulting Offers complement the AWS Solutions Library (self-deployable code) and Solutions Constructs (CDK patterns); partners deliver the consulting layer.

## Common operations

Consulting offers are procured through the partner/Marketplace process rather than the AWS CLI:

```bash
# Use AWS Marketplace catalog APIs to discover offers and sellers
aws marketplace-catalog list-entities --catalog AWSMarketplace --entity-type DataProduct
aws marketplace-catalog describe-entity --catalog AWSMarketplace --entity-id <entity-id>
```

## Best practices

- Define the expected outcome and deliverables before purchasing; match the offer to a specific business need.
- Validate the partner's credentials (competencies, customer references) before engagement.
- Agree on access, security, and data-handling requirements for the engagement.
- Use the AWS Solutions Library first for self-service implementations; engage partners for scoped consulting work.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cannot find an offer | Broaden filters in AWS Marketplace; check the partner's site for direct offers. |
| Offer scope mismatch | Contact the partner to confirm deliverables and exclusions before purchasing. |
| Deliverables unclear | Reference the offer description and agreed statement of work. |

## Limits

Consulting offers are governed by the partner agreement and Marketplace terms; technical quotas depend on the AWS services involved. See the AWS Partner Network and Marketplace documentation for current details.

## Official references

- [AWS Partner Network](https://aws.amazon.com/partners/)
- [AWS Marketplace](https://aws.amazon.com/marketplace)
- [AWS Partner competencies](../certifications/competencies/README.md)
- [AWS Solutions Library](../solutions-implementations/README.md)
