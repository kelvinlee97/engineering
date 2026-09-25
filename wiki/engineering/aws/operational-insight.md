---
type: Service
title: AWS operational insight
description: Tracing requests, AWS service health, account best-practice checks, and configuration management with X-Ray, Health, Trusted Advisor, and OpsWorks.
tags: [aws, operations, observability]
sources:
  - id: aws-x-ray
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/x-ray/README.md
    title: "AWS X-Ray - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-health
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/health/README.md
    title: "AWS Health - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-trusted-advisor
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/trusted-advisor/README.md
    title: "AWS Trusted Advisor - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-opsworks
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/opsworks/README.md
    title: "AWS OpsWorks - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services tell operators what is happening: where a request spent its time, whether AWS itself has an event affecting you, and which account settings break best practice. OpsWorks, a configuration management service, is included for completeness.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [AWS X-Ray](#aws-x-ray) | AWS X-Ray collects data about requests your application serves and provides tools to view, filter, and analyze that data |
| [AWS Health](#aws-health) | AWS Health provides visibility into the performance and availability of your AWS services and accounts |
| [AWS Trusted Advisor](#aws-trusted-advisor) | AWS Trusted Advisor inspects your AWS environment and recommends actions to save money, improve system availability and performance, and close security gaps |
| [AWS OpsWorks](#aws-opsworks) | OpsWorks Stacks is discontinued (May 26, 2024) |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## AWS X-Ray

AWS X-Ray collects data about requests your application serves and provides tools to view, filter, and analyze that data. It shows the full request path through your front end, microservices, databases, and downstream AWS APIs, helping you identify bottlenecks, latency spikes, and errors.

Key points:

- Segments and subsegments: units of trace data describing work done by a service (or a call within it).
- Traces: a complete request path composed of segments/subsegments across services.
- Service map: a visual graph of services and calls with latency and error data.
- Sampling: control how many requests are traced to manage cost; default rules plus custom rules.
- Instrumentation: X-Ray SDKs (Java, Python, Node.js, Go, .NET, Ruby) send segment documents to the X-Ray daemon, which batches and uploads them over UDP.

Practices:

- Instrument at service boundaries: HTTP clients, AWS SDK calls, and database queries get subsegments automatically with the SDKs.
- Run the X-Ray daemon on EC2/on-premises (it is included on Lambda and Elastic Beanstalk platforms).
- Set sampling rules so high-traffic services trace a representative sample without breaking the budget.

| Symptom | Check |
| --- | --- |
| No traces visible | Check SDK instrumentation, daemon status, and IAM permissions for the X-Ray service. |
| Missing downstream calls | Verify SDK version and that HTTP/AWS SDK clients are instrumented. |
| Cost too high | Reduce sampling rate or add sampling rules for lower-value endpoints. |
| Trace context lost | Confirm the trace header is propagated across services (proxies/Lambda). |

Trace retention (30 days), segments per trace, and API request rates have quotas. See the Service Quotas console for current values.[^aws-x-ray]


## AWS Health

AWS Health provides visibility into the performance and availability of your AWS services and accounts. It delivers events about service disruptions, scheduled changes, and account notifications so you can prepare for planned activities, troubleshoot in-progress issues, and automate responses. The AWS Health Dashboard is available to all customers at no additional cost.

Key points:

- Health events: notifications about service issues, scheduled maintenance, and account-specific events that may affect your resources.
- AWS Health Dashboard: the console view of events affecting your account; no setup or code required.
- EventBridge: all customers can receive AWS Health events through Amazon EventBridge at no additional cost; use rules to trigger automation and alerts.
- AWS Health API: programmatic access for integrating with internal/third-party systems; available with Business Support+ (or Business/Enterprise plans in some Regions) and above.
- Event types: account notifications (security, billing), scheduled changes, and ongoing service events; each event can have affected resources and guidance.

Practices:

- Subscribe to AWS Health events via EventBridge for all accounts/Regions and route to SNS/Slack/incident tooling.
- Set up the Health API integration in your operations tooling to build a single pane of glass for events.
- Monitor scheduled changes and account notifications early so maintenance windows don't surprise you.

| Symptom | Check |
| --- | --- |
| No events visible | Confirm the Region and account filter; the dashboard is account-specific. |
| EventBridge rule not firing | Check the event pattern (`aws.health` source) and the rule's target permissions. |
| API access denied | Verify your support plan and IAM permissions for `health:DescribeEvents`. |
| Event details missing | Use `describe-event-details` and check affected entities for scope. |

The dashboard and EventBridge events are free; the Health API has request-rate quotas and requires a qualifying support plan. See the AWS Health endpoints and quotas page for current values.[^aws-health]


## AWS Trusted Advisor

AWS Trusted Advisor inspects your AWS environment and recommends actions to save money, improve system availability and performance, and close security gaps. It checks your account against best practices across five categories: cost optimization, security, fault tolerance, performance, and service limits.

Key points:

- Checks: automated best-practice evaluations per category (for example, underutilized EC2 instances, MFA on root account, RDS backup enabled, service limit usage).
- Support plans and access: all checks plus the Trusted Advisor API are available with AWS Business Support+, Enterprise Support, or AWS Unified Operations; Basic Support provides Service Limits checks and selected Security/Fault tolerance checks, with manual refresh for Security.
- Console: the Trusted Advisor console shows check status (green/red/yellow) and recommended actions; you can refresh checks manually.
- API and EventBridge: Business Support+ and above can read check results via the Support API and monitor check status changes with Amazon EventBridge.
- Service limits: the service limits category tracks your usage against quotas and notifies you before you hit limits.

Practices:

- Review Trusted Advisor on a regular schedule and assign owners to each recommendation.
- Prioritize security and service-limits checks; act on critical findings (for example, MFA on the root account, open security groups) first.
- Use the API/EventBridge integration to track check status changes and alert your team automatically.

| Symptom | Check |
| --- | --- |
| Cannot access all checks | Confirm your support plan; full checks and API require Business Support+ or above. |
| Check result stale | Refresh the specific check; Basic Support requires manual refresh for Security checks. |
| API access denied | Verify IAM permissions for `support:DescribeTrustedAdvisorChecks` and related actions. |
| EventBridge not receiving events | Enable the Trusted Advisor integration and check the event pattern in the region. |

Trusted Advisor availability depends on your AWS Support plan, and API request rates have quotas. See the AWS Support API reference and your support plan details for current values.[^aws-trusted-advisor]


## AWS OpsWorks

OpsWorks Stacks is discontinued (May 26, 2024): treat this article purely as a migration map from its Chef-based stack/layer model onto current services (Systems Manager, CloudFormation, CodeDeploy, containers, Elastic Beanstalk). AWS OpsWorks (OpsWorks Stacks) was a configuration management service that used Chef to automate the configuration and operation of EC2 instances, including layers, stacks, auto-healing, and deployments. OpsWorks Stacks reached end of life: it stopped accepting new customers and was discontinued for all customers on May 26, 2024. Do not build new workloads on OpsWorks.

Key points:

- Stack: a container for resources and configuration that belongs to one Region.
- Layer: a group of EC2 instances with the same configuration and recipes (for example, app, web, database layers).
- Recipes and cookbooks: Chef scripts that configure instances; OpsWorks ran them during lifecycle events (setup, configure, deploy, undeploy, shutdown).
- Auto healing and scaling: OpsWorks replaced failed instances and scaled layers with load-based or time-based instances.
- Deployments: deploys updated application code to instances in a layer.

Practices:

- Do not start new projects on OpsWorks; it is discontinued.
- Inventory legacy OpsWorks-managed instances and map them to current services (SSM for operations, CloudFormation for infrastructure, CodeDeploy for deployment).
- Test the migration on a subset of workloads before decommissioning the old stacks.

| Symptom | Check |
| --- | --- |
| Cannot create a stack | Expected: OpsWorks Stacks is discontinued (May 26, 2024); use current configuration management services. |
| Legacy stacks still running | Migrate workloads to Systems Manager, CloudFormation, CodeDeploy, and container/managed platforms; then decommission. |
| Chef recipes in use | Port recipes to SSM documents (or user data), and application deployments to CodeDeploy. |

OpsWorks Stacks is discontinued; no new resources can be created. See the AWS OpsWorks end-of-life guidance and current service quotas for migration targets.[^aws-opsworks]


## Related

- [Operations tooling](operations-tooling.md)
- [Domain index](index.md)

[^aws-x-ray]: [AWS X-Ray - Runbook & Reference](../../sources/aws-x-ray.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/x-ray/README.md)
[^aws-health]: [AWS Health - Runbook & Reference](../../sources/aws-health.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/health/README.md)
[^aws-trusted-advisor]: [AWS Trusted Advisor - Runbook & Reference](../../sources/aws-trusted-advisor.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/trusted-advisor/README.md)
[^aws-opsworks]: [AWS OpsWorks - Runbook & Reference](../../sources/aws-opsworks.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/opsworks/README.md)
