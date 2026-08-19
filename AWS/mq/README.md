# Amazon MQ - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon MQ is a managed message broker service for Apache ActiveMQ and RabbitMQ. It provides brokers with managed maintenance, version upgrades, CloudWatch monitoring, encryption at rest and in transit, and private VPC endpoints, so you can migrate existing message-broker workloads without rewriting applications.

## Key concepts

- **Broker**: the managed message broker environment; the basic unit of Amazon MQ (ActiveMQ or RabbitMQ engine).
- **Deployment mode (ActiveMQ)**: single-instance for development or active/standby for high availability.
- **Storage**: EBS-backed storage; choose instance type and storage size when creating the broker.
- **Quorum queues (RabbitMQ)**: replicated queue type with leader/follower nodes across AZs for durability and poison-message handling.
- **Cross-Region data replication (ActiveMQ)**: asynchronous replication from a primary broker Region to a replica broker Region with failover promotion.
- **Security**: SSL/TLS, VPC private endpoints, IAM for API-level control, and username/password for broker users.
- **Monitoring**: metrics pushed to CloudWatch every minute; console, CLI, and API access.

## Common operations (AWS CLI)

```bash
# Create an ActiveMQ broker (active/standby)
aws mq create-broker --broker-name prod-mq --engine-type ACTIVEMQ \
  --engine-version 5.18.6 --host-instance-type mq.m5.large \
  --deployment-mode ACTIVE_STANDBY_MULTI_AZ \
  --users '{"Username":"admin","ConsoleAccess":true,"Groups":["admins"]}' \
  --publicly-accessible

# Create a RabbitMQ broker
aws mq create-broker --broker-name events-mq --engine-type RABBITMQ \
  --engine-version 3.13.12 --host-instance-type mq.m5.large \
  --users '{"Username":"admin"}'

# List and describe brokers
aws mq list-brokers
aws mq describe-broker --broker-id <broker-id>

# Reboot and delete
aws mq reboot-broker --broker-id <broker-id>
aws mq delete-broker --broker-id <broker-id>
```

## Best practices

- Use active/standby (ActiveMQ) or quorum queues (RabbitMQ) for production; single instance only for dev.
- Keep brokers in private subnets and connect through VPC endpoints; restrict with security groups.
- Enable encryption at rest (KMS) and require TLS in transit; rotate broker user credentials.
- Size instance type and storage for peak load and retention; monitor queue depth and broker metrics.
- Use maintenance windows for version upgrades and test client compatibility first.
- For cloud-native apps without broker protocol dependencies, evaluate SQS/SNS or EventBridge instead.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Clients can't connect | Check security group rules (ports 61617/61614 for ActiveMQ, 5671/443 for RabbitMQ), TLS, and VPC routing. |
| Queue depth grows | Check consumer health, message TTL, and broker capacity; scale instance/storage. |
| Failover not working | Verify active/standby or quorum queue configuration and replica health. |
| Storage full | Increase EBS storage or reduce retention; monitor `StorageUsed` in CloudWatch. |
| Maintenance surprise | Configure the maintenance window and monitor the broker state. |

## Limits

Brokers per account, instance types, storage, and connections have quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon MQ?](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html)
- [Amazon MQ service quotas](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/amazon-mq-limits.html)
- [Amazon MQ pricing](https://aws.amazon.com/amazon-mq/pricing/)
- [AWS CLI: mq commands](https://docs.aws.amazon.com/cli/latest/reference/mq/)
