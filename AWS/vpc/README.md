# Amazon VPC - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Virtual Private Cloud (Amazon VPC) lets you launch AWS resources in a logically isolated virtual network that you define. Each AWS Region includes a default VPC ready for immediate use. There is no charge for the VPC itself; charges apply to some components such as NAT gateways.

## Key concepts

- **VPC**: a virtual network with an IP CIDR range (IPv4 and/or IPv6).
- **Subnets**: ranges of IP addresses inside a VPC; a subnet lives in a single Availability Zone.
- **Route tables**: determine where traffic from a subnet or gateway goes.
- **Gateways and endpoints**: internet gateway for public access; VPC endpoints for private access to AWS services; NAT gateway for outbound-only internet from private subnets.
- **Peering and Transit Gateway**: connect VPCs; transit gateway acts as a central hub.
- **VPN / Direct Connect**: connect VPCs to on-premises networks.
- **Security**: security groups (stateful, instance-level) and network ACLs (stateless, subnet-level); VPC Flow Logs capture IP traffic metadata.

## Common operations (AWS CLI)

```bash
# VPC and subnet
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 --availability-zone ap-southeast-1a

# Internet access
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id igw-xxx --vpc-id vpc-xxx
aws ec2 create-route-table --vpc-id vpc-xxx
aws ec2 create-route --route-table-id rtb-xxx --destination-cidr-block 0.0.0.0/0 --gateway-id igw-xxx
aws ec2 associate-route-table --route-table-id rtb-xxx --subnet-id subnet-xxx

# NAT gateway for private subnets
aws ec2 create-nat-gateway --subnet-id subnet-xxx --allocation-id eipalloc-xxx

# Private access to AWS services
aws ec2 create-vpc-endpoint --vpc-id vpc-xxx --service-name com.amazonaws.ap-southeast-1.s3

# Observability
aws ec2 create-flow-logs --resource-type VPC --resource-id vpc-xxx \
  --traffic-type ALL --log-group-name my-flow-logs --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flowlogs
```

## Best practices

- Plan CIDR blocks to avoid overlap across VPCs and on-premises networks; avoid `10.0.0.0/16` collisions if you peer later.
- Use multiple Availability Zones; put databases and internal services in **private subnets**.
- Use **VPC endpoints** (gateway for S3/DynamoDB, interface for other services) instead of NAT for private access.
- Enable **VPC Flow Logs** and analyze them for security and troubleshooting.
- Default-deny security groups; use security groups for instance-level and NACLs for subnet-level guardrails.
- Use Transit Gateway as a hub when connecting many VPCs.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Instance cannot reach the internet | Check route table (default route to IGW), security group egress, NACL, and public IPv4 assignment. |
| Private instance cannot reach the internet | Verify NAT gateway is in a public subnet with an Elastic IP and route exists. |
| Cannot connect to RDS in private subnet | Check the RDS security group source (app security group/CIDR) and subnet routing. |
| AWS service access blocked | Add a VPC endpoint and its security group; verify endpoint policy. |
| DNS not resolving | Check VPC DNS settings (`enableDnsSupport`, `enableDnsHostnames`) and Resolver rules. |

## Limits

Default quotas include 5 VPCs per Region (adjustable) and 200 subnets per VPC. See the Service Quotas console for current values.

## Official references

- [What is Amazon VPC? - Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Amazon VPC pricing](https://aws.amazon.com/vpc/pricing/)
- [AWS CLI: ec2 commands (VPC)](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
