# Amazon Managed Blockchain (AMB) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Managed Blockchain (AMB) provides access to public blockchain networks (Ethereum and Bitcoin) and lets you create private, permissioned blockchain networks with the Hyperledger Fabric framework. AMB Access offers fully managed, dedicated (single-tenant), and serverless multi-tenant API operations for public nodes, and fully managed private networks for use cases requiring access controls.

## Key concepts

- **AMB Access**: standardized API access to blockchain infrastructure.
  - **Public networks**: Ethereum and Bitcoin nodes with multi-tenant API access or dedicated nodes.
  - **Private networks**: permissioned Hyperledger Fabric networks created in minutes with members and peer nodes.
- **Network**: the private blockchain network (Fabric) or public network membership.
- **Member**: an organization in a Fabric network; members run peer nodes and can propose changes (chaincode, membership) with voting.
- **Peer node**: the Fabric component that hosts the ledger and chaincode; deploy multiple peers for high availability.
- **Accessor and tokens**: token-based access to Ethereum nodes (accessors are containers with token-based access information).
- **Use cases**: consortium networks, supply chain, financial applications, and development/testing networks with simulated members.

## Common operations (AWS CLI)

```bash
# Create a Fabric network and a member
aws managedblockchain create-network --framework HYPERLEDGER_FABRIC \
  --framework-version 2.2 --voting-policy file://voting.json \
  --member-configuration file://member.json
aws managedblockchain create-member --network-id <network-id> \
  --member-configuration file://member.json

# Nodes and accessors
aws managedblockchain create-node --network-id <network-id> \
  --member-id <member-id> --node-configuration file://node.json
aws managedblockchain create-accessor --accessor-type BILLING_TOKEN \
  --accessor-name ethereum-mainnet

# Inspect resources
aws managedblockchain list-networks
aws managedblockchain list-members --network-id <network-id>
aws managedblockchain list-nodes --network-id <network-id> --member-id <member-id>
```

## Best practices

- Choose the deployment model by requirement: public API access (AMB Access), dedicated nodes, or a private Fabric network for permissioned use cases.
- Run multiple peer nodes across Availability Zones for high availability in Fabric networks.
- Manage membership carefully: proposals and votes control who can join and change the network.
- Secure access with IAM and token-based access for Ethereum; rotate and protect accessor tokens.
- Monitor node health and ledger activity; set alarms for failures.
- For public-network usage, size API/throughput needs and use serverless multi-tenant access to control cost.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Node unavailable | Check network/member status, node health, and IAM permissions. |
| Token access denied | Verify the accessor exists and the token is valid for the network. |
| Chaincode proposal fails | Confirm voting policy thresholds and member permissions. |
| Fabric network creation fails | Validate the member configuration (admin user, password policy, instance type). |
| API throttled | Review request rates and increase quotas as needed. |

## Limits

Networks, members, nodes, and accessors per account have quotas; framework versions are fixed at network creation. See the Amazon Managed Blockchain endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Managed Blockchain?](https://docs.aws.amazon.com/managed-blockchain/latest/hyperledger-fabric-dev/what-is-managed-blockchain.html)
- [Amazon Managed Blockchain endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/managedblockchain.html)
- [Amazon Managed Blockchain pricing](https://aws.amazon.com/managed-blockchain/pricing/)
- [AWS CLI: managedblockchain commands](https://docs.aws.amazon.com/cli/latest/reference/managedblockchain/)
