---
type: Service
title: AWS networking
description: Amazon VPC for private networks in AWS, and Direct Connect for private links from on-premises.
tags:
- aws
- networking
aliases:
- engineering/aws/vpc
- engineering/aws/direct-connect
sources:
- id: aws-vpc
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/vpc/README.md
  title: Amazon VPC - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-direct-connect
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/direct-connect/README.md
  title: AWS Direct Connect - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Amazon VPC gives each workload a private network inside AWS, and AWS Direct Connect links that network to an on-premises site over a dedicated connection instead of the internet.

## Amazon VPC

Amazon Virtual Private Cloud (VPC) lets you launch AWS resources in a logically isolated virtual network you define. Each Region has a default VPC; the VPC itself is free, but some components such as NAT gateways cost money.[^aws-vpc]

### Building blocks

| Piece | Role |
| --- | --- |
| VPC | A network with an IPv4 and/or IPv6 CIDR range |
| Subnet | An address range inside one Availability Zone |
| Route table | Decides where traffic from a subnet or gateway goes |
| Internet gateway | Public internet access |
| NAT gateway | Outbound-only internet for private subnets |
| VPC endpoint | Private access to AWS services |
| Peering, Transit Gateway | VPC to VPC; Transit Gateway is a central hub |
| VPN, [Direct Connect](#aws-direct-connect) | VPC to on-premises |
| Security group, network ACL | Stateful instance-level and stateless subnet-level firewalls |

As listed in the note. VPC Flow Logs capture IP traffic metadata.[^aws-vpc]

### Practices

- Plan CIDR blocks so they never overlap across VPCs and on-premises networks.
- Use several Availability Zones and put databases and internal services in private subnets.
- Prefer VPC endpoints (gateway endpoints for S3 and DynamoDB, interface endpoints for others) over NAT for private service access.
- Enable Flow Logs; default-deny security groups; Transit Gateway when connecting many VPCs.[^aws-vpc]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Public instance has no internet | Default route to the IGW, SG egress, NACL, public IPv4 |
| Private instance has no internet | NAT gateway in a public subnet with an Elastic IP, and a route to it |
| Cannot reach RDS in a private subnet | RDS security group source and subnet routing |
| AWS service access blocked | Add a VPC endpoint; check its security group and policy |
| DNS not resolving | `enableDnsSupport`, `enableDnsHostnames`, Resolver rules |

As tabled in the note. Default quotas are 5 VPCs per Region (adjustable) and 200 subnets per VPC.[^aws-vpc]

## AWS Direct Connect

Direct Connect is a dedicated private connection between an on-premises network and AWS. It bypasses the public internet, gives more consistent network performance, and can cut transfer costs for large volumes.[^aws-direct-connect]

### Connections and virtual interfaces

| Piece | Detail |
| --- | --- |
| Dedicated connection | A physical port of 1, 2, 5, or 10 Gbps; a LAG bundles up to four |
| Hosted connection | From a Delivery Partner, 50 Mbps to 10 Gbps |
| Private VIF | One VPC in the same account and Region |
| Public VIF | Public AWS services such as S3 and DynamoDB |
| Transit VIF | A Direct Connect gateway reaching many VPCs, accounts, and Regions |
| MACsec | Optional layer-1 encryption on dedicated connections |

As described in the note. Virtual interfaces use 802.1Q VLAN tags and BGP peering, with optional MD5 authentication and BFD.[^aws-direct-connect]

### Practices

- Redundant connections in at least two Direct Connect locations, with BGP set for automatic failover; VPN as a backup path where justified.
- A transit VIF with a Direct Connect gateway for multi-VPC setups.[^aws-direct-connect]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Connection `down` | Cross-connect complete, device connected at the facility |
| BGP not establishing | VLAN, peer IPs, ASN, MD5 password, correct VIF |
| VIF `pending` or `confirming` | Accept or confirm the VIF |
| Traffic not routing | Gateway association, route propagation, advertised prefixes |
| Latency high | Traffic may be falling back to VPN or internet |

As tabled in the note.[^aws-direct-connect]

## Related
- [Domain index](index.md): other pages in this domain.

[^aws-vpc]: [Amazon VPC - Runbook & Reference](../../sources/aws-vpc.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/vpc/README.md)
[^aws-direct-connect]: [AWS Direct Connect - Runbook & Reference](../../sources/aws-direct-connect.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/direct-connect/README.md)
