# Concept

* [Envelope encryption](envelope-encryption.md) - Encrypt data locally with a data key and store only an encrypted copy of that key, so the key service never handles bulk data.
* [IAM policy evaluation](iam-policy-evaluation.md) - How AWS decides a request: every applicable policy layer is checked, an explicit deny anywhere wins, and nothing is allowed without an explicit allow.

# Pattern

* [AWS multi-account governance](multi-account-governance.md) - Run AWS as many accounts under Organizations, with central sign-in, an organization audit trail, and security services run from delegated administrator accounts.
* [AWS security findings pipeline](security-findings-pipeline.md) - Route GuardDuty and other detector findings through Security Hub CSPM and EventBridge, and export them, because each service keeps only a short fixed history.

# Service

* [Amazon CloudFront](cloudfront.md) - AWS's CDN: requests are answered from the nearest edge cache, and only misses reach the origin, so cache settings control both cost and freshness.
* [Amazon EC2](ec2.md) - AWS's virtual servers: the instance type sets compute, memory, network, and storage, and the lifecycle state decides what you pay and what data survives.
* [Amazon EC2 Auto Scaling](auto-scaling-groups.md) - Groups of EC2 instances held between a minimum and maximum size, scaled by policies and self-healed by health checks.
* [Amazon ECR](ecr.md) - AWS's container image registry, with IAM-controlled private repositories, scanning, lifecycle cleanup, and replication.
* [Amazon ECS](ecs.md) - AWS's own container orchestrator: task definitions run as tasks or long-running services on Fargate, EC2, or on-premises capacity.
* [Amazon EKS](eks.md) - AWS's managed Kubernetes: AWS runs the control plane, and with Auto Mode also the nodes.
* [Amazon GuardDuty](guardduty.md) - AWS's threat detection service that analyzes CloudTrail, VPC Flow Logs, and DNS logs, plus optional protection plans, to produce findings.
* [Amazon Route 53](route53.md) - AWS's DNS service: domain registration, hosted zones with routing policies, and health checks that drop unhealthy targets from answers.
* [Amazon VPC](vpc.md) - AWS's logically isolated virtual network: CIDR ranges split into per-AZ subnets, with route tables, gateways, and firewalls deciding where traffic goes.
* [AWS CloudTrail](cloudtrail.md) - AWS's audit log of API and console actions, from a free 90-day event history to long-term trails and a queryable data lake.
* [AWS Direct Connect](direct-connect.md) - A dedicated private network link from on-premises to AWS that bypasses the public internet, carried as virtual interfaces over BGP.
* [AWS Global Accelerator](global-accelerator.md) - Static anycast IP addresses that carry user traffic over the AWS network to the healthiest, nearest regional endpoint.
* [AWS IAM](iam.md) - AWS's authentication and authorization service: identities, policies, and temporary credentials that decide who can do what to which resource.
* [AWS IAM Identity Center](iam-identity-center.md) - AWS's service for workforce sign-in to many accounts: users or an external identity provider, permission sets, and an access portal.
* [AWS KMS](kms.md) - AWS's managed service for creating and controlling encryption and signing keys, used through envelope encryption.
* [AWS Lambda](lambda.md) - AWS's serverless compute: functions run per event with no servers to manage, billed per request and GB-second.
* [AWS Organizations](organizations.md) - AWS's service for managing many accounts as one tree of organizational units with shared billing and policy guardrails.
* [AWS Secrets Manager](secrets-manager.md) - AWS's service for storing versioned secrets that applications fetch at runtime, with scheduled rotation through Lambda.
* [AWS Security Hub CSPM](security-hub.md) - AWS's security posture service that gathers findings from other services and runs continuous checks against security standards.
* [Elastic Load Balancing](elb.md) - AWS's load balancers (ALB, NLB, GWLB) that spread traffic across healthy targets in several Availability Zones.

# Comparison

* [AWS compute options](compute-options.md) - How EC2, Lambda, ECS, and EKS divide the work between you and AWS, and the hard limits that push a workload from one to another.
* [AWS global traffic routing](global-traffic-routing.md) - Route 53, CloudFront, and Global Accelerator all steer users toward healthy endpoints, but at different layers and with different failover speed.
