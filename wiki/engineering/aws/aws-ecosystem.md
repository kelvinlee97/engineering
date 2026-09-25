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
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:32:06Z }
status: draft
---
This page covers what surrounds the individual AWS services: the ideas behind cloud computing, the ecosystem of partners, marketplace, support, and compliance evidence, and the two kinds of ready-made help AWS publishes, deployable reference solutions and partner consulting offers.

## Cloud computing basics

Cloud computing delivers IT resources on demand over the internet with pay-as-you-go pricing, replacing large up-front capital expenses with variable costs that follow usage. Five properties recur in the rest of the AWS pages:

| Property | What it means in practice |
| --- | --- |
| On-demand self-service | Provision resources when needed, without a human in the loop, and release them when done |
| Pay-as-you-go | Capital expense becomes variable operating expense |
| Economies of scale | AWS pools demand across many customers, lowering per-unit cost |
| Elasticity | Scale up (larger instances) or out (more instances), and back, automatically |
| High availability | Survive failures by spreading across Availability Zones and Regions |

The practices that follow are to design for failure (multi-AZ or multi-Region, health checks, automated recovery), to match capacity to demand with Auto Scaling or serverless options, and to pick the service model (IaaS, PaaS, or SaaS) that removes the most operational work for each workload. Idle resources are the usual source of cost growth; single points of failure are fixed by spreading across Availability Zones.[^aws-foundations-cloud-computing]

## What the ecosystem includes

The AWS ecosystem has no single product or entry point. It is the platform (compute, storage, database, networking, analytics, security, and AI/ML services on global infrastructure) plus:

- The AWS Partner Network (APN) and AWS Marketplace, where partners sell software and services.
- Support plans.
- AWS Artifact, which provides compliance evidence for the controls AWS runs; controls on your side are your team's to evidence.
- The Well-Architected Framework and the shared responsibility model, which guide how to use all of it (see [AWS foundations](aws-foundations.md)).

Choose services by workload requirements and the Well-Architected pillars rather than by feature list, use consolidated billing and tagging for cost visibility, and check a Marketplace or partner offering's support path, IAM, and network requirements before deploying it. Some services are not available in every Region; check the service's Regional availability first.[^aws-aws-ecosystem]

## Ready-made help: build it yourself or hire a partner

AWS publishes two kinds of packaged help that complement each other and [Solutions Constructs](developer-tools.md#aws-solutions-constructs), the library of prebuilt CDK patterns.

| | Solutions Library | Consulting Offers |
| --- | --- | --- |
| What you get | Reference implementations for use cases such as data lakes, security, DevOps, and analytics | Fixed-scope engagements with defined deliverables, for outcomes such as migration, modernization, security assessments, and data analytics |
| Who does the work | You, in your own account | A validated AWS Partner |
| Delivered as | CloudFormation templates or CDK code plus an implementation guide | A purchase in AWS Marketplace, then a statement of work |
| Vetting | Reviewed by AWS architects for reliability, security, and cost | Partners validated through competency programs |
| Watch for | Regional support, and keeping your changes across upgrades | Scope and exclusions agreed before purchase |

### AWS Solutions Library

The Solutions Library, formerly AWS Solutions Implementations, is open-source code you can fork and customize. Read the implementation guide first for prerequisites, Regions, and cost estimates; deploy in a test account, then adapt the code for production (VPC, encryption, logging). Keep custom changes in a fork so upgrades do not overwrite them, and when a deployment fails, read the CloudFormation stack events.[^aws-solutions-implementations]

### AWS Consulting Offers

Consulting Offers are part of the APN and Marketplace. Browse them in Marketplace by use case, industry, and partner, or on a partner's own site. Before buying, define the outcome you need, check the partner's competencies and customer references, and agree on access, security, and data-handling rules for the engagement; afterwards, track deliverables against the agreed scope.[^aws-solutions-consulting-offers]

## Related

- [AWS foundations](aws-foundations.md): the shared responsibility model and Well-Architected Framework.
- [AWS certifications](certifications.md): the exams that test these basics.
- [Cost](cost.md): pricing models behind pay-as-you-go.
- [Domain index](index.md)

[^aws-foundations-cloud-computing]: [Foundations of Cloud Computing - Runbook & Reference](../../sources/aws-foundations-cloud-computing.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/foundations-cloud-computing/README.md)
[^aws-aws-ecosystem]: [AWS Ecosystem - Runbook & Reference](../../sources/aws-aws-ecosystem.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/aws-ecosystem/README.md)
[^aws-solutions-implementations]: [AWS Solutions Library (Solutions Implementations) - Runbook & Reference](../../sources/aws-solutions-implementations.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-implementations/README.md)
[^aws-solutions-consulting-offers]: [AWS Consulting Offers - Runbook & Reference](../../sources/aws-solutions-consulting-offers.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/solutions-consulting-offers/README.md)
