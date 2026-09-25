---
type: Service
title: Amazon VPC
description: "AWS's logically isolated virtual network: CIDR ranges split into per-AZ subnets, with route tables, gateways, and firewalls deciding where traffic goes."
tags: [aws, networking]
sources:
  - id: aws-vpc
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/vpc/README.md
    title: "Amazon VPC - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Amazon Virtual Private Cloud (VPC) lets you launch AWS resources in a logically isolated virtual network you define. Each Region has a default VPC; the VPC itself is free, but some components such as NAT gateways cost money.[^aws-vpc]

## Building blocks

| Piece | Role |
| --- | --- |
| VPC | A network with an IPv4 and/or IPv6 CIDR range |
| Subnet | An address range inside one Availability Zone |
| Route table | Decides where traffic from a subnet or gateway goes |
| Internet gateway | Public internet access |
| NAT gateway | Outbound-only internet for private subnets |
| VPC endpoint | Private access to AWS services |
| Peering, Transit Gateway | VPC to VPC; Transit Gateway is a central hub |
| VPN, [Direct Connect](direct-connect.md) | VPC to on-premises |
| Security group, network ACL | Stateful instance-level and stateless subnet-level firewalls |

As listed in the note.[^aws-vpc] VPC Flow Logs capture IP traffic metadata.[^aws-vpc]

## Practices

- Plan CIDR blocks so they never overlap across VPCs and on-premises networks.[^aws-vpc]
- Use several Availability Zones and put databases and internal services in private subnets.[^aws-vpc]
- Prefer VPC endpoints (gateway endpoints for S3 and DynamoDB, interface endpoints for others) over NAT for private service access.[^aws-vpc]
- Enable Flow Logs; default-deny security groups; Transit Gateway when connecting many VPCs.[^aws-vpc]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Public instance has no internet | Default route to the IGW, SG egress, NACL, public IPv4 |
| Private instance has no internet | NAT gateway in a public subnet with an Elastic IP, and a route to it |
| Cannot reach RDS in a private subnet | RDS security group source and subnet routing |
| AWS service access blocked | Add a VPC endpoint; check its security group and policy |
| DNS not resolving | `enableDnsSupport`, `enableDnsHostnames`, Resolver rules |

As tabled in the note.[^aws-vpc] Default quotas are 5 VPCs per Region (adjustable) and 200 subnets per VPC.[^aws-vpc]

## Related

- Source: [Amazon VPC - Runbook & Reference](../../sources/aws-vpc.md)

[^aws-vpc]: Amazon VPC - Runbook & Reference
