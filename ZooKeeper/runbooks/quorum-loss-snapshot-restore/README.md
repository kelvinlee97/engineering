# ZooKeeper Quorum-Loss Snapshot Restore Runbook

Chinese version: [README_ZH.md](README_ZH.md)

Use this incident-only Runbook when a three-member ZooKeeper ensemble has lost quorum and cannot accept updates. It is not for a normal restart, a single damaged member, or a disk-full follower repair; use the [single-member disk-full recovery runbook](../disk-full-transaction-log-recovery/README.md) for that case.

## Safety Boundary

This procedure is destructive to the members' current local database state. It may lose writes made after the selected snapshot. The incident commander, ZooKeeper owner, application owners, and security owner must approve it before Step 4. Do not proceed if a healthy majority might still exist, the snapshot provenance is unknown, or the root znode ACL has not been verified.

The normal systemd service keeps AdminServer disabled. This Runbook temporarily enables it only as `127.0.0.1:8443`, forces HTTPS, and requires a client certificate. Access it only through an approved SSH tunnel; never add a firewall rule or public listener for the recovery endpoint.

## Preconditions and Inputs

- [ ] Incident time, affected ensemble, member hostnames, configured `dataDir` and `dataLogDir` are recorded.
- [ ] Client traffic is blocked at the approved load-balancer, firewall, or application layer; applications are stopped or placed in safe mode.
- [ ] No two members report a healthy leader/follower quorum. If two do, stop and use single-member recovery instead.
- [ ] One approved snapshot and its SHA-512 checksum are available in controlled storage. It is known to be the intended recovery point.
- [ ] The administrator x509 client certificate has approved `ALL` permission on `/`, proven before the incident by `getAcl /` and a separate-certificate `NoAuth` test; a distinct control-host PEM certificate/key and CA file are available through the approved secret mechanism for HTTPS mTLS.
- [ ] The service configuration explicitly enables `-Dzookeeper.serializeLastProcessedZxid.enabled=true`; restore and snapshot fail when this prerequisite is disabled.
- [ ] The recovery has been rehearsed in an isolated environment for this ZooKeeper version and configuration.

Record fixed, non-secret variables on the control host. The placeholders are not credentials.

```bash
export ZK_VERSION=3.9.5
export ZK_HOME="/opt/apache-zookeeper-${ZK_VERSION}"
export DR_ADMIN_PORT=8443
export SNAPSHOT=/secure/recovery/approved-snapshot.bin
export SNAPSHOT_SHA512=/secure/recovery/approved-snapshot.bin.sha512
export DR_CA_CERT_PEM=/secure/recovery/ca.pem
export DR_CLIENT_CERT_PEM=/secure/recovery/admin-client.pem
export DR_CLIENT_KEY_PEM=/secure/recovery/admin-client-key.pem
```

Verify the selected snapshot before changing any member. Stop if it does not match.

```bash
expected_sha512=$(awk '{print $1}' "$SNAPSHOT_SHA512")
actual_sha512=$(sha512sum "$SNAPSHOT" | awk '{print $1}')
test "$actual_sha512" = "$expected_sha512" || {
  echo 'Snapshot checksum verification failed'; exit 1;
}
```

## 1. Confirm Quorum Loss and Preserve Evidence

On all three hosts, collect `systemctl status zookeeper`, the latest 200 journal lines, `df -hT`, `df -i`, and `findmnt /var/lib/zookeeper /srv/zookeeper-txn`. Run the TLS-aware `zkServer.sh status` command from the production guide on every member. Do not use `ruok` as quorum evidence.

Attach the evidence and snapshot checksum to the incident. Do not delete, reinitialize, or copy another member's `myid`, `version-2`, or transaction-log data.

## 2. Temporarily Enable a Local Recovery AdminServer

Perform this on one member at a time. Create `/etc/systemd/system/zookeeper.service.d/90-disaster-recovery.conf` with the following content; it replaces the normal `SERVER_JVMFLAGS` value only for the incident. The server's existing `ssl.quorum.*` keystore/truststore settings provide HTTPS material, and the truststore must trust the recovery administrator certificate.

```ini
[Service]
Environment="SERVER_JVMFLAGS=-Dzookeeper.db.autocreate=false -Dzookeeper.serializeLastProcessedZxid.enabled=true -Dzookeeper.admin.enableServer=true -Dzookeeper.admin.serverAddress=127.0.0.1 -Dzookeeper.admin.serverPort=8443 -Dzookeeper.admin.forceHttps=true -Dzookeeper.admin.needClientAuth=true"
```

Reload systemd and restart only the member currently being prepared. This restart is required even if the process is still running: `systemctl start` would not apply the new JVM flags. Client traffic is already blocked. Confirm the journal states that AdminServer bound `127.0.0.1:8443`; if it reports another address, stop and remove the drop-in before continuing.

```bash
sudo install -d -m 0755 /etc/systemd/system/zookeeper.service.d
sudoedit /etc/systemd/system/zookeeper.service.d/90-disaster-recovery.conf
sudo systemctl daemon-reload
sudo systemctl restart zookeeper
sudo journalctl -u zookeeper -n 100 --no-pager
```

From the control host, create a tunnel that preserves the server FQDN for TLS hostname verification:

```bash
ssh -N -L 8443:127.0.0.1:8443 zookeeper-admin@zk-1.example.internal
```

In a second control-host shell, use the tunnel with mTLS. `--resolve` makes the TLS name match the server certificate while the TCP connection remains local to the tunnel.

```bash
curl --fail --silent --show-error \
  --cacert "$DR_CA_CERT_PEM" \
  --cert "$DR_CLIENT_CERT_PEM" --key "$DR_CLIENT_KEY_PEM" \
  --resolve "zk-1.example.internal:${DR_ADMIN_PORT}:127.0.0.1" \
  "https://zk-1.example.internal:${DR_ADMIN_PORT}/commands/leader"
```

The request must succeed only through the tunnel. A request without the client certificate must fail. If either check is not true, stop and engage the security owner.

## 3. Restore Every Member From the Same Snapshot

Run this member-by-member under the incident commander. Before restoring a member, stop it and preserve both `version-2` directories under a timestamped sibling name. Do not remove these preserved directories; they are rollback and forensic evidence. Because the service keeps database-existence validation enabled, create the one-time `initialize` marker only after this preservation and only while client traffic is blocked. It lets this deliberately empty member vote long enough to restore the approved snapshot; ZooKeeper consumes the marker at startup. Confirm the configured paths before substituting them below.

```bash
export RECOVERY_TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
sudo systemctl stop zookeeper
sudo mv /var/lib/zookeeper/version-2 \
  "/var/lib/zookeeper/version-2.pre-restore-${RECOVERY_TIMESTAMP}"
sudo mv /srv/zookeeper-txn/version-2 \
  "/srv/zookeeper-txn/version-2.pre-restore-${RECOVERY_TIMESTAMP}"
sudo install -d -o zookeeper -g zookeeper -m 0750 \
  /var/lib/zookeeper/version-2 /srv/zookeeper-txn/version-2
sudo -u zookeeper touch /var/lib/zookeeper/initialize
sudo systemctl start zookeeper
test ! -e /var/lib/zookeeper/initialize || {
  echo 'initialize marker was not consumed'; exit 1;
}
```

After the local HTTPS AdminServer is available through the tunnel, send the *same verified snapshot* to that member. The recovery administrator certificate must be authorized with `ALL` on `/`. Record the successful response's `last_zxid` in the incident; a non-2xx response is a stop condition.

```bash
curl --fail --silent --show-error \
  --cacert "$DR_CA_CERT_PEM" \
  --cert "$DR_CLIENT_CERT_PEM" --key "$DR_CLIENT_KEY_PEM" \
  --resolve "zk-1.example.internal:${DR_ADMIN_PORT}:127.0.0.1" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary "@$SNAPSHOT" \
  "https://zk-1.example.internal:${DR_ADMIN_PORT}/commands/restore"
```

Immediately persist the restored in-memory database to the member's new data directory. The response headers must include `last_zxid`; record it and confirm it matches the restore response because client traffic remains blocked.

```bash
curl --fail --silent --show-error --output /dev/null --dump-header - \
  --cacert "$DR_CA_CERT_PEM" \
  --cert "$DR_CLIENT_CERT_PEM" --key "$DR_CLIENT_KEY_PEM" \
  --resolve "zk-1.example.internal:${DR_ADMIN_PORT}:127.0.0.1" \
  "https://zk-1.example.internal:${DR_ADMIN_PORT}/commands/snapshot?streaming=false"
```

Wait for the restore and snapshot journal evidence before moving to the next member. Repeat the tunnel, preservation, one-time marker, restore, and persistence sequence for `zk-2` and `zk-3`, changing only the FQDN. Do not mix snapshots between members and do not run members in parallel.

## 4. Re-form Quorum and Close the Recovery Interface

After all three members have restored and persisted the same snapshot, do not restart them merely to re-form quorum: they are already running. Keep client traffic blocked and wait for election. Use the TLS-aware status command from the production guide on every member. If exactly one leader and two followers do not form, stop and escalate with the restore responses and journals; do not retry restore or restart nodes as an experiment.

Only after the quorum check succeeds, remove the incident-only drop-in and restart one member at a time. After each restart, wait for it to rejoin as leader or follower before continuing. Accept recovery only when exactly one reports `leader`, two report `follower`, the recorded restore and local-snapshot `last_zxid` values match on every member, and application owners approve their ACL and dependency checks.

Remove the incident-only drop-in on every member, reload systemd, and restart one member at a time so the normal service once again contains `-Dzookeeper.admin.enableServer=false`. Confirm no listener remains on `8443` before reopening client traffic.

```bash
sudo mv /etc/systemd/system/zookeeper.service.d/90-disaster-recovery.conf \
  /etc/systemd/system/zookeeper.service.d/90-disaster-recovery.conf.completed
sudo systemctl daemon-reload
sudo systemctl restart zookeeper
if sudo ss -ltnp | grep -q ':8443'; then
  echo 'AdminServer is still listening'
  exit 1
fi
```

Finally, run each application's approved `getAcl` and authorized-operation checks. Reopen client traffic gradually, observe application errors and ZooKeeper metrics, then retain the preserved pre-restore directories and incident evidence until the incident commander closes the case.

## References

- [Apache Snapshot and Restore Guide](https://zookeeper.apache.org/doc/current/zookeeperSnapshotAndRestore.html)
- [Apache Administrator's Guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html)
- [Production deployment guide](../../guides/production-deployment/README.md)
