---
type: Service
title: AWS ecosystem and cloud foundations
description: Cloud computing basics, the AWS partner ecosystem, and AWS Solutions offerings for starting on AWS.
tags: [aws, foundations]
sources:
  - id: aws-foundations-cloud-computing
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/foundations-cloud-computing/README.md
    title: "Foundations of Cloud Computing - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-aws-ecosystem
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/aws-ecosystem/README.md
    title: "AWS Ecosystem - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-solutions-implementations
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-implementations/README.md
    title: "AWS Solutions Library (Solutions Implementations) - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-solutions-consulting-offers
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-consulting-offers/README.md
    title: "AWS Consulting Offers - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These notes cover what sits around the services: why cloud computing works the way it does, the partner and marketplace ecosystem, and the reference implementations and consulting offers AWS publishes.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Foundations of Cloud Computing](#foundations-of-cloud-computing) | Cloud computing delivers on-demand IT resources over the internet with pay-as-you-go pricing |
| [AWS Ecosystem](#aws-ecosystem) | The AWS ecosystem is the cloud platform plus everything that surrounds it |
| [AWS Solutions Library (Solutions Implementations)](#aws-solutions-library-solutions-implementations) | The AWS Solutions Library (formerly AWS Solutions Implementations) provides vetted solutions and guidance for common business and technical use cases |
| [AWS Consulting Offers](#aws-consulting-offers) | AWS Consulting Offers are packaged consulting engagements from AWS Partners that address specific business outcomes (for example, migration, modernization, security assessments, and data analytics) |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Foundations of Cloud Computing

Cloud computing delivers on-demand IT resources over the internet with pay-as-you-go pricing. AWS provides compute, storage, databases, networking, analytics, and many other services on a global infrastructure, replacing large up-front capital expenses with variable costs that scale with usage.

Key points:

- On-demand self-service: provision resources when you need them without human interaction, and release them when done.
- Pay-as-you-go: pay only for what you use, converting capital expense into variable operating expense.
- Economies of scale: AWS aggregates demand across many customers, reducing per-unit costs.
- Elasticity and scalability: scale capacity up/down or out/in automatically; vertical (larger instances) and horizontal (more instances) scaling.
- High availability and fault tolerance: design across Availability Zones and Regions to survive failures.

Practices:

- Design for failure: multi-AZ/Region architectures, health checks, and automated recovery.
- Use elasticity: match capacity to demand with Auto Scaling and serverless options.
- Choose the right service model (IaaS/PaaS/SaaS) per workload to reduce operational burden.

| Symptom | Check |
| --- | --- |
| Capacity surprises at launch | Use Elastic Beanstalk/Auto Scaling and test scaling behavior in staging. |
| Costs grow with idle resources | Release or scale down unused resources; use managed/serverless where possible. |
| Single point of failure | Spread workloads across AZs and add health-checked redundancy. |

Concepts are general; actual behavior depends on service quotas and architecture choices. See the AWS Cloud overview and the per-service runbooks in this knowledge base.[^aws-foundations-cloud-computing]


## AWS Ecosystem

The AWS ecosystem is the cloud platform plus everything that surrounds it: partners, marketplace, support, compliance evidence, and the frameworks that guide how you use it. There is no single product and no single entry point. The AWS ecosystem includes the AWS Cloud platform itself (compute, storage, database, networking, analytics, security, and AI/ML services on global infrastructure), plus the AWS Partner Network (APN), AWS Marketplace, support plans, compliance resources (AWS Artifact), and the Well-Architected and Shared Responsibility frameworks that guide how you use it.

Practices:

- Choose services by workload requirements and the Well-Architected pillars, not by feature list.
- Use consolidated billing and tagging for cost visibility across the ecosystem.
- Evaluate Marketplace/partner offerings against support, security, and compliance requirements.

| Symptom | Check |
| --- | --- |
| Service unavailable in Region | Check the service's Regional availability page; some services are not global. |
| Partner solution issues | Verify the offering's support path and IAM/network requirements before deploying. |
| Compliance evidence needed | Use AWS Artifact; AWS-side controls are covered by AWS, customer-side by your team. |

The ecosystem is governed by per-service quotas and agreements; see the AWS index and per-service runbooks in this knowledge base for details.[^aws-aws-ecosystem]


## AWS Solutions Library (Solutions Implementations)

The AWS Solutions Library (formerly AWS Solutions Implementations) provides vetted solutions and guidance for common business and technical use cases. Each solution is reviewed by AWS architects for reliability, security, and cost-efficiency and ships with deployment guidance and code you can deploy in your own account.

Key points:

- Solutions: packaged reference implementations covering industry and technical use cases (for example, data lakes, security, DevOps, and analytics).
- Deployment assets: solutions include CloudFormation templates and/or CDK code plus implementation guides with architecture and operational details.
- Vetting: solutions are reviewed by AWS architects against reliability, security, and cost best practices before publication.
- Customization: you can fork and customize the open-source code to fit your environment.
- Relationship to other AWS assets: the Solutions Library complements AWS Solutions Constructs (pre-built CDK patterns) and AWS Partner Consulting Offers (partner-delivered engagements).

Practices:

- Review the implementation guide before deploying; note prerequisites, Regions, and cost estimates.
- Deploy in a test account first, then adapt the code for production (VPC, encryption, logging).
- Track the solution version and AWS service updates; re-deploy or upgrade when the library publishes updates.

| Symptom | Check |
| --- | --- |
| Deployment fails | Check the CloudFormation stack events and the implementation guide prerequisites. |
| Regional limitations | Verify the solution supports your Region; some use services with limited availability. |
| Customization lost on upgrade | Keep custom changes in a fork and track upstream updates. |

Solutions are guidance artifacts; quotas depend on the underlying AWS services they deploy. See the AWS Solutions Library page for current solution lists and the service runbooks in this knowledge base for quotas.[^aws-solutions-implementations]


## AWS Consulting Offers

AWS Consulting Offers are packaged consulting engagements from AWS Partners that address specific business outcomes (for example, migration, modernization, security assessments, and data analytics). They are part of the AWS Partner Network (APN) and AWS Marketplace ecosystem, giving customers a scoped, repeatable way to procure partner expertise.

Key points:

- Consulting offers: fixed-scope engagements from AWS Partners with defined deliverables and outcomes, listed for discovery.
- Partner ecosystem: offers come from validated AWS Partners; competency programs validate partner expertise in solution areas.
- Discovery: browse offers in AWS Marketplace and AWS Partner resources; filter by use case, industry, and partner.
- Procurement and execution: purchase the offer, engage the partner, and track deliverables against the engagement scope.
- Relationship to AWS assets: Consulting Offers complement the AWS Solutions Library (self-deployable code) and Solutions Constructs (CDK patterns); partners deliver the consulting layer.

Practices:

- Define the expected outcome and deliverables before purchasing; match the offer to a specific business need.
- Validate the partner's credentials (competencies, customer references) before engagement.
- Agree on access, security, and data-handling requirements for the engagement.

| Symptom | Check |
| --- | --- |
| Cannot find an offer | Broaden filters in AWS Marketplace; check the partner's site for direct offers. |
| Offer scope mismatch | Contact the partner to confirm deliverables and exclusions before purchasing. |
| Deliverables unclear | Reference the offer description and agreed statement of work. |

Consulting offers are governed by the partner agreement and Marketplace terms; technical quotas depend on the AWS services involved. See the AWS Partner Network and Marketplace documentation for current details.[^aws-solutions-consulting-offers]


## Related

- [AWS foundations](aws-foundations.md)
- [AWS certifications](certifications.md)
- [Domain index](index.md)

[^aws-foundations-cloud-computing]: [Foundations of Cloud Computing - Runbook & Reference](../../sources/aws-foundations-cloud-computing.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/foundations-cloud-computing/README.md)
[^aws-aws-ecosystem]: [AWS Ecosystem - Runbook & Reference](../../sources/aws-aws-ecosystem.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/aws-ecosystem/README.md)
[^aws-solutions-implementations]: [AWS Solutions Library (Solutions Implementations) - Runbook & Reference](../../sources/aws-solutions-implementations.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-implementations/README.md)
[^aws-solutions-consulting-offers]: [AWS Consulting Offers - Runbook & Reference](../../sources/aws-solutions-consulting-offers.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-consulting-offers/README.md)
