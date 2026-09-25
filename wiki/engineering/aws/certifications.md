---
type: Comparison
title: AWS certifications
description: The Cloud Practitioner, Developer Associate, and Solutions Architect Associate exams compared, with the study path the legacy outlines share.
tags: [aws, certification, learning]
sources:
  - id: aws-cert-cloud-practitioner
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/cloud-practitioner/README.md
    title: AWS Certified Cloud Practitioner (CLF-C02) - Study Outline
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cert-developer-associate
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/developer-associate/README.md
    title: AWS Certified Developer - Associate (DVA-C02) - Study Outline
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cert-solutions-architect
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/solutions-architect/README.md
    title: AWS Certified Solutions Architect - Associate (SAA-C03) - Study Outline
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cert-competencies
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/competencies/README.md
    title: AWS Competencies for Cloud Roles - Study Outline
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

The legacy study outlines cover three AWS certification exams and the wider credential landscape. Recheck the official exam guide before booking; AWS changes scope over time.

| | Cloud Practitioner (CLF-C02) | Developer Associate (DVA-C02) | Solutions Architect Associate (SAA-C03) |
| --- | --- | --- | --- |
| Questions | 65 (50 scored + 15 unscored) | Not stated in the outline | 65 (50 scored + 15 unscored) |
| Duration | 90 minutes | Not stated | 130 minutes |
| Passing score | 700 of 1,000 | Not stated | 720 of 1,000 |
| Experience | Six months foundational[^aws-cert-cloud-practitioner] | Not stated | At least one year designing on AWS[^aws-cert-solutions-architect] |

## Domains

- CLF-C02: Cloud Concepts 24%, Security and Compliance 30%, Cloud Technology and Services 34%, Billing, Pricing, and Support 12%.[^aws-cert-cloud-practitioner]
- DVA-C02: development with AWS services, security, deployment, troubleshooting and optimization; heavy on Lambda, API Gateway, DynamoDB, and the Code* CI/CD services.[^aws-cert-developer-associate]
- SAA-C03: design secure, resilient, high-performing, and cost-optimized architectures, based on the [Well-Architected Framework](aws-foundations.md#aws-well-architected-framework).[^aws-cert-solutions-architect]

## Shared study path

Every outline gives the same steps: read the official exam guide, practice hands-on in your own account using the service pages, take official practice questions on AWS Skill Builder, and recheck the guide before booking.[^aws-cert-cloud-practitioner][^aws-cert-developer-associate][^aws-cert-solutions-architect] The competencies outline suggests starting with Cloud Practitioner and then an associate exam matched to your role, and notes certifications typically need renewal every three years. AWS Partner competencies are a separate program for partner organizations, with levels such as Select, Advanced, and Specialty.[^aws-cert-competencies]

## Related

- [AWS ecosystem](aws-ecosystem.md): cloud computing basics behind the exams.
- [Domain index](index.md): other pages in this domain.

[^aws-cert-cloud-practitioner]: [AWS Certified Cloud Practitioner (CLF-C02) - Study Outline](../../sources/aws-cert-cloud-practitioner.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/cloud-practitioner/README.md)
[^aws-cert-developer-associate]: [AWS Certified Developer - Associate (DVA-C02) - Study Outline](../../sources/aws-cert-developer-associate.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/developer-associate/README.md)
[^aws-cert-solutions-architect]: [AWS Certified Solutions Architect - Associate (SAA-C03) - Study Outline](../../sources/aws-cert-solutions-architect.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/solutions-architect/README.md)
[^aws-cert-competencies]: [AWS Competencies for Cloud Roles - Study Outline](../../sources/aws-cert-competencies.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/certifications/competencies/README.md)
