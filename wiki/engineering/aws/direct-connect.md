---
type: Service
title: AWS Direct Connect
description: A dedicated private network link from on-premises to AWS that bypasses the public internet, carried as virtual interfaces over BGP.
tags: [aws, networking, hybrid]
sources:
  - id: aws-direct-connect
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/direct-connect/README.md
    title: "AWS Direct Connect - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Direct Connect is a dedicated private connection between an on-premises network and AWS. It bypasses the public internet, gives more consistent network performance, and can cut transfer costs for large volumes.[^aws-direct-connect]

## Connections and virtual interfaces

| Piece | Detail |
| --- | --- |
| Dedicated connection | A physical port of 1, 2, 5, or 10 Gbps; a LAG bundles up to four |
| Hosted connection | From a Delivery Partner, 50 Mbps to 10 Gbps |
| Private VIF | One VPC in the same account and Region |
| Public VIF | Public AWS services such as S3 and DynamoDB |
| Transit VIF | A Direct Connect gateway reaching many VPCs, accounts, and Regions |
| MACsec | Optional layer-1 encryption on dedicated connections |

As described in the note.[^aws-direct-connect] Virtual interfaces use 802.1Q VLAN tags and BGP peering, with optional MD5 authentication and BFD.[^aws-direct-connect]

## Practices

- Redundant connections in at least two Direct Connect locations, with BGP set for automatic failover; VPN as a backup path where justified.[^aws-direct-connect]
- A transit VIF with a Direct Connect gateway for multi-VPC setups.[^aws-direct-connect]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Connection `down` | Cross-connect complete, device connected at the facility |
| BGP not establishing | VLAN, peer IPs, ASN, MD5 password, correct VIF |
| VIF `pending` or `confirming` | Accept or confirm the VIF |
| Traffic not routing | Gateway association, route propagation, advertised prefixes |
| Latency high | Traffic may be falling back to VPN or internet |

As tabled in the note.[^aws-direct-connect]

## Related

- Source: [AWS Direct Connect - Runbook & Reference](../../sources/aws-direct-connect.md)

[^aws-direct-connect]: AWS Direct Connect - Runbook & Reference
