---
type: Service
title: AWS application integration
description: APIs, GraphQL, workflows, message brokers, email, and contact centers for connecting application components.
tags: [aws, integration, messaging]
sources:
  - id: aws-api-gateway
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/api-gateway/README.md
    title: "Amazon API Gateway - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-appsync
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/appsync/README.md
    title: "AWS AppSync - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-step-functions
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/step-functions/README.md
    title: "AWS Step Functions - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-mq
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/mq/README.md
    title: "Amazon MQ - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-ses
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ses/README.md
    title: "Amazon SES - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-connect
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/connect/README.md
    title: "Amazon Connect - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T18:30:00Z }
status: draft
---
These services connect application components and users: HTTP and GraphQL front doors, workflow orchestration, standard-protocol message brokers, email, and a cloud contact center.

## Choosing a service

| Service | What it is for |
| --- | --- |
| [Amazon API Gateway](#amazon-api-gateway) | API Gateway is a policy-enforcing front door |
| [AWS AppSync](#aws-appsync) | AppSync sits between a single GraphQL schema and several independent data sources |
| [AWS Step Functions](#aws-step-functions) | AWS Step Functions is a serverless orchestration service |
| [Amazon MQ](#amazon-mq) | Amazon MQ is a drop-in managed broker |
| [Amazon SES](#amazon-ses) | Amazon Simple Email Service (Amazon SES) is a scalable email platform for sending transactional email (order confirmations, password resets), marketing email (offers, newsletters), and for receiving email |
| [Amazon Connect](#amazon-connect) | A contact's entire journey is scripted by one flow object, and it never reaches an agent directly |

Analysis: this table condenses each note's opening line; the sections below carry the details and citations.

## Amazon API Gateway

API Gateway is a policy-enforcing front door: every request passes through authentication, throttling, and a stage before it ever reaches an integration, so backend code never has to implement those cross-cutting concerns itself. Amazon API Gateway is a managed service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket APIs at any scale. It acts as a "front door" to backends such as Lambda functions, EC2 workloads, or any HTTP endpoint.

Key points:

- API types: REST APIs (full-featured), HTTP APIs (lighter, for serverless), and WebSocket APIs (stateful, full-duplex).
- Resources and methods: URL paths with HTTP methods mapped to integrations.
- Integrations: AWS Lambda (proxy), HTTP endpoints, AWS services, or mock.
- Stages and deployments: publish API versions; canary deployments for gradual rollout.
- Authentication: IAM, Lambda authorizers, Amazon Cognito user pools.

Practices:

- Use HTTP APIs for simple serverless backends; REST APIs when you need the full feature set.
- Enable throttling and use API keys + usage plans for client quotas.
- Authenticate with Cognito or Lambda authorizers; never leave routes open by default.

| Symptom | Check |
| --- | --- |
| `429 Too Many Requests` | Check account/per-API throttling limits and usage plans; raise quotas or add caching. |
| `500` from Lambda integration | Check Lambda function logs and the execution role; verify the integration URI/ARN. |
| `403 Forbidden` | Check IAM authorization, authorizer configuration, WAF rules, and API key requirements. |
| CORS errors | Configure CORS on the method/API and verify preflight (`OPTIONS`) handling. |

Default account-level throttling is 10,000 requests per second per Region (adjustable); per-API limits and regional availability apply. See Service Quotas.[^aws-api-gateway]


## AWS AppSync

AppSync sits between a single GraphQL schema and several independent data sources: every field resolves through its own resolver, so a query can fan out to DynamoDB, Lambda, RDS, and HTTP in one round trip, while subscriptions push the same schema's mutations back out over WebSockets. AWS AppSync is a managed GraphQL and Pub/Sub API service. It connects your applications to data and events through a single GraphQL endpoint backed by one or more data sources (DynamoDB, Lambda, RDS, HTTP), with real-time updates via subscriptions and AppSync Events (WebSocket pub/sub, available since March 2025).

Key points:

- GraphQL API: the endpoint your clients query; schemas define types, queries, mutations, and subscriptions.
- Data sources: DynamoDB tables, Lambda functions, RDS clusters, OpenSearch, HTTP endpoints.
- Resolvers: functions that map GraphQL fields to data source operations; written in VTL or JavaScript/TypeScript.
- Subscriptions: real-time updates pushed to clients over WebSockets when mutations occur.
- AppSync Events: WebSocket-based pub/sub channels for real-time messaging.

Practices:

- Define schema-first and keep resolvers thin; use JS/TS resolvers for complex logic.
- Choose authorization per API: Cognito for user-facing apps, IAM for service-to-service, API keys for public/development.
- Batch and paginate DynamoDB data source requests to avoid per-item latency.

| Symptom | Check |
| --- | --- |
| Resolver returns null | Check data source permissions (IAM role) and resolver mapping templates. |
| Subscription not receiving events | Verify subscription auth, WebSocket connection, and that the mutation publishes to the topic. |
| `401/403` on requests | Check API key validity, Cognito tokens, and IAM signing. |
| Slow queries | Enable caching, review N+1 resolver patterns, and index the underlying data source. |

API count, resolvers per API, request/response sizes, subscription connection counts, and caching have per-account quotas. See the Service Quotas console for current values.[^aws-appsync]


## AWS Step Functions

AWS Step Functions is a serverless orchestration service. You define workflows (state machines) as a series of steps to coordinate Lambda functions, AWS services, and human approval flows. It supports visual debugging, retries, parallel processing, and long-running workflows.

Key points:

- State machine (workflow): a JSON definition (Amazon States Language) of the workflow.
- States: Task, Choice, Parallel, Map, Wait, Pass, Succeed, and Fail.
- Executions: running instances of a state machine.
- Standard workflows: exactly-once execution, run up to 1 year, up to 2,000 executions/second; ideal for long-running, auditable processes.
- Express workflows: at-least-once execution, run up to 5 minutes, up to 100,000 executions/second; ideal for high-volume streaming/ingestion.

Practices:

- Choose Standard for auditable, long-running workflows and Express for high-volume, short workflows.
- Prefer AWS SDK/optimized integrations over custom Lambda glue code.
- Use `Retry` with backoff for transient errors and `Catch` for business failures.

| Symptom | Check |
| --- | --- |
| Execution fails | Inspect `get-execution-history` error output and the failed state. |
| Lambda not invoked | Check the state machine IAM role and Lambda permissions. |
| Callback never returns | Verify the worker sends the task token back to Step Functions. |
| Timeout errors | Adjust state timeout/`heartbeatSeconds` for long tasks. |

Executions per second, state transitions, execution history size, and payload sizes have quotas that differ between Standard and Express workflows. See the Service Quotas console for current values.[^aws-step-functions]


## Amazon MQ

Amazon MQ is a drop-in managed broker: pick ActiveMQ or RabbitMQ, choose single-instance or a highly-available topology, and AWS handles maintenance, patching, and failover underneath your existing broker-protocol clients. Amazon MQ is a managed message broker service for Apache ActiveMQ and RabbitMQ. It provides brokers with managed maintenance, version upgrades, CloudWatch monitoring, encryption at rest and in transit, and private VPC endpoints, so you can migrate existing message-broker workloads without rewriting applications.

Key points:

- Broker: the managed message broker environment; the basic unit of Amazon MQ (ActiveMQ or RabbitMQ engine).
- Deployment mode (ActiveMQ): single-instance for development or active/standby for high availability.
- Storage: EBS-backed storage; choose instance type and storage size when creating the broker.
- Quorum queues (RabbitMQ): replicated queue type with leader/follower nodes across AZs for durability and poison-message handling.
- Cross-Region data replication (ActiveMQ): asynchronous replication from a primary broker Region to a replica broker Region with failover promotion.

Practices:

- Use active/standby (ActiveMQ) or quorum queues (RabbitMQ) for production; single instance only for dev.
- Keep brokers in private subnets and connect through VPC endpoints; restrict with security groups.
- Enable encryption at rest (KMS) and require TLS in transit; rotate broker user credentials.

| Symptom | Check |
| --- | --- |
| Clients can't connect | Check security group rules (ports 61617/61614 for ActiveMQ, 5671/443 for RabbitMQ), TLS, and VPC routing. |
| Queue depth grows | Check consumer health, message TTL, and broker capacity; scale instance/storage. |
| Failover not working | Verify active/standby or quorum queue configuration and replica health. |
| Storage full | Increase EBS storage or reduce retention; monitor `StorageUsed` in CloudWatch. |

Brokers per account, instance types, storage, and connections have quotas. See the Service Quotas console for current values.[^aws-mq]


## Amazon SES

Amazon Simple Email Service (Amazon SES) is a scalable email platform for sending transactional email (order confirmations, password resets), marketing email (offers, newsletters), and for receiving email. You can send through the SES API, the SMTP interface, or AWS SDKs, and receive email into S3, SNS, or Lambda. You pay per email sent and received.

Key points:

- Email identity: a verified domain or email address that you are authorized to send from; DKIM and SPF/DMARC are configured for the domain.
- Easy DKIM: SES manages DKIM signing for your domain (especially simple when DNS is in Route 53); required for production sending.
- Configuration sets: group sending settings and event destinations (CloudWatch, Amazon Data Firehose, SNS, EventBridge, Pinpoint) for tracking bounces, complaints, deliveries, and opens/clicks.
- Suppression and reputation: SES tracks bounce and complaint rates, applies sending limits, and lets you manage a suppression list.
- Receiving: incoming email routes to S3 (optionally KMS-encrypted), SNS, or Lambda through receipt rules in a rule set.

Practices:

- Verify and configure Easy DKIM (and SPF/DMARC) for all sending domains; never send from unverified identities.
- Warm up new sending identities gradually and keep bounce/complaint rates low; act on feedback notifications.
- Use configuration sets for every workload and alert on bounce/complaint spikes.

| Symptom | Check |
| --- | --- |
| Sending from unverified identity | Verify the domain/email identity and complete DKIM setup; wait for propagation. |
| Daily quota exceeded | Check `get-send-quota`; request a limit increase after demonstrating low complaint/bounce rates. |
| Emails landing in spam | Verify DKIM/SPF/DMARC, warm up the identity, and review content and sending patterns. |
| Bounce/complaint events missing | Confirm the configuration set is attached and the event destination is configured correctly. |

Daily sending quota, maximum send rate, message size, and identities per account have limits; SES adjusts quotas based on reputation. See the SES service quotas page and Service Quotas console for current values.[^aws-ses]


## Amazon Connect

A contact's entire journey is scripted by one flow object, and it never reaches an agent directly: the flow puts it in a queue, and the routing profile, rather than the flow, decides which agent picks it up, so routing problems and flow problems have different root causes even though they feel the same to a caller. Amazon Connect is a cloud contact center that lets you build and manage customer communication experiences. Amazon Connect now refers to a portfolio of agentic solutions for business functions; the legacy contact center product is called Amazon Connect Customer (or simply Customer). Connect Customer provides voice, chat, SMS, and task channels, intelligent routing, real-time metrics, and AI-powered capabilities, and you pay only for what you use.

Key points:

- Contact center: the hub where customers reach agents through voice, chat, SMS, or tasks, and where interactions are recorded, routed, and measured.
- Phone numbers and channels: provision phone numbers (local, toll-free, DID) and enable chat/SMS channels for customer entry points.
- Flows (contact flows): visual, drag-and-drop workflows that define how contacts are handled (IVR menus, queueing, attributes, transfers, Lambda integration).
- Queues and routing profiles: queues hold contacts waiting for agents; routing profiles map agents to queues and prioritize contact types.
- Agent workspace: the agent UI for handling contacts, chat, and tasks, with integrated CRM and other applications.

Practices:

- Design flows with clear entry points, error handling, and escalation paths; test flows in a staging instance first.
- Use routing profiles and queues to match contact priority and agent skill instead of manual transfers.
- Integrate Lambda for dynamic data (customer lookup, attribute enrichment) and Lex for self-service.

| Symptom | Check |
| --- | --- |
| Calls not routing | Check the contact flow, queue/routing profile association, and phone number status. |
| Agents cannot receive contacts | Verify agent user setup, routing profile, and channel availability. |
| Flow errors | Test the flow with sample attributes; check Lambda integration and permissions. |
| No metrics | Confirm the queue/agent is in the metrics filters and the instance Region matches. |

Phone numbers per instance, concurrent contacts, and API request rates have quotas; contact limits vary by Region and instance type. See the Amazon Connect endpoints and quotas page and Service Quotas console for current values.[^aws-connect]


## Related

- [AWS messaging](messaging.md)
- [Containers and serverless](containers-and-serverless.md)
- [Domain index](index.md)

[^aws-api-gateway]: [Amazon API Gateway - Runbook & Reference](../../sources/aws-api-gateway.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/api-gateway/README.md)
[^aws-appsync]: [AWS AppSync - Runbook & Reference](../../sources/aws-appsync.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/appsync/README.md)
[^aws-step-functions]: [AWS Step Functions - Runbook & Reference](../../sources/aws-step-functions.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/step-functions/README.md)
[^aws-mq]: [Amazon MQ - Runbook & Reference](../../sources/aws-mq.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/mq/README.md)
[^aws-ses]: [Amazon SES - Runbook & Reference](../../sources/aws-ses.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/ses/README.md)
[^aws-connect]: [Amazon Connect - Runbook & Reference](../../sources/aws-connect.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/connect/README.md)
