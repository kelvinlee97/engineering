# AWS Direct Connect - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Direct Connect establishes a dedicated private network connection between your on-premises network and AWS. It bypasses the public internet, provides consistent network experience, and can reduce network costs when transferring large volumes of data. Connections terminate at AWS Direct Connect locations in dedicated or hosted configurations.

## Key concepts

- **Dedicated connection**: a physical Ethernet port (1, 2, 5, or 10 Gbps) provisioned by AWS at a Direct Connect location; capacity can be increased with a Link Aggregation Group (LAG) of up to four connections.
- **Hosted connection**: capacity provisioned by an AWS Direct Connect Delivery Partner in increments (50 Mbps to 10 Gbps); you request it from the partner and can associate it with a Direct Connect gateway.
- **Virtual interface (VIF)**: the logical segment over the connection, using 802.1Q VLAN tags and BGP peering (BGP MD5 authentication supported, BFD optional).
  - **Private VIF**: connects to a single VPC in the same account/Region.
  - **Public VIF**: connects to public AWS services (for example, S3, DynamoDB) by public IP.
  - **Transit VIF**: connects to a Direct Connect gateway for multiple VPCs, accounts, and Regions.
- **Direct Connect gateway**: a global resource that associates transit VIFs with VPCs across accounts and Regions, including inter-Region routing to a VPC.
- **MACsec**: optional IEEE 802.1AE encryption at the physical layer for dedicated connections.

## Common operations (AWS CLI)

```bash
# List connections and virtual interfaces
aws directconnect describe-connections
aws directconnect describe-virtual-interfaces

# Create a virtual interface (configuration is passed via a file)
aws directconnect create-virtual-interface \
  --connection-id dxcon-0123456789abcdef0 \
  --new-virtual-interface-name prod-vif \
  --new-virtual-interface file://vif.json

# Describe a Direct Connect gateway and its associations
aws directconnect describe-direct-connect-gateways
aws directconnect describe-direct-connect-gateway-associations \
  --direct-connect-gateway-id dxgw-0123456789abcdef0

# List LAGs
aws directconnect describe-lags
```

## Best practices

- Use redundant connections in at least two Direct Connect locations and configure BGP so failover is automatic.
- Prefer a transit VIF with a Direct Connect gateway when you have multiple VPCs, accounts, or Regions.
- Keep BGP sessions monitored (up/down, prefixes advertised) and enable BFD where supported for faster convergence.
- Use MACsec on dedicated connections when the physical path crosses untrusted facilities.
- Size bandwidth from measured utilization; consider public VIF for high-volume S3/DynamoDB traffic to avoid internet transfer costs.
- Combine Direct Connect with VPN as a backup path where availability requirements justify it.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Connection state `down` | Verify cross-connect is complete and the device at the facility is connected; contact AWS/partner if the port stays down. |
| BGP not establishing | Check VLAN, peer IPs, ASN, BGP MD5 password, and that the correct VIF is used. |
| VIF state `pending` or `confirming` | Complete the required acceptance (dedicated connections) or confirm partner-created hosted VIFs. |
| Traffic not routing | Verify Direct Connect gateway association, route propagation, and advertised prefixes. |
| Latency higher than expected | Confirm traffic is actually using Direct Connect (not VPN/internet fallback). |

## Limits

Connections, LAGs, virtual interfaces, and Direct Connect gateways per account have quotas; VIFs per connection and gateways per account also apply. See the Service Quotas console for current values.

## Official references

- [What is AWS Direct Connect?](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
- [AWS Direct Connect virtual interfaces](https://docs.aws.amazon.com/directconnect/latest/UserGuide/WorkingWithVirtualInterfaces.html)
- [AWS Direct Connect quotas](https://docs.aws.amazon.com/directconnect/latest/UserGuide/limits.html)
- [AWS Direct Connect pricing](https://aws.amazon.com/directconnect/pricing/)
- [AWS CLI: directconnect commands](https://docs.aws.amazon.com/cli/latest/reference/directconnect/)
