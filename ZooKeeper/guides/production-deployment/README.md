# ZooKeeper Production Deployment Baseline

Chinese version: [README_ZH.md](README_ZH.md)

This is a deployment and verification baseline for the adjacent incident runbooks. It is not a substitute for a version-specific design review, capacity test, or disaster-recovery rehearsal.

## Ensemble and Storage

- Use an odd-sized ensemble on independent hosts. A three-member ensemble tolerates one failed member only.
- Keep the same `server.<id>=host:quorum-port:election-port` membership on every member and keep each member's `myid` unique.
- Set `dataDir`; if `dataLogDir` is separate, place the transaction log on a dedicated device. Record both configured paths before an incident.
- Run the server under a service manager and keep its configuration, certificate locations, and secrets outside this repository.

Apache's [Administrator's Guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html) documents clustered setup, the majority requirement, `myid`, `dataDir`, and `dataLogDir`.

## TLS-aware Status Check

When client TLS is enabled, run the installed distribution's status command on each member using that member's approved service configuration:

```bash
cd <apache-zookeeper-home>
bin/zkServer.sh status
```

Do not replace this with plaintext Four Letter Word probes against a TLS-only client port. Confirm the service account can read the configured trust material without printing certificate paths, passwords, keys, or connection strings. Treat an unsuccessful status check as an investigation signal, not permission to weaken TLS or ACL settings.

## Operational Boundary

- Test one-member restart and failover behavior in an isolated environment before production use.
- Keep AdminServer disabled or locally bound by default; do not expose a recovery interface publicly.
- Use version-specific Apache documentation for TLS and administration behavior, and capture only sanitized evidence during incidents.

## Related Runbooks

- [Quorum-loss snapshot restore](../../runbooks/quorum-loss-snapshot-restore/README.md)
- [Disk-full transaction-log recovery](../../runbooks/disk-full-transaction-log-recovery/README.md)
