# ZooKeeper Disk-Full Recovery Runbook

Chinese version: [README_ZH.md](README_ZH.md)

Use this generic procedure when one ZooKeeper member cannot start because a full disk left a local transaction log incomplete. The commands use the Apache binary-distribution layout shown in the [Getting Started Guide](https://zookeeper.apache.org/doc/r3.8.6/zookeeperStarted.html): run them from `<apache-zookeeper-home>`, whose sample configuration is `conf/zoo.cfg`, with `dataDir=/var/lib/zookeeper` and `clientPort=2181`. Replace only the host values after confirming the active configuration and recovery authority.

## Safety Boundary

Typical errors:

```text
Last transaction was partial.
Unable to load database on disk
java.io.EOFException
```

Freeing disk space removes the write blockage; it does not repair a truncated log. Do not loop on `zkServer.sh restart`.

Proceed only if exactly one member is damaged, the other members form a healthy quorum, the configured `dataDir` and optional `dataLogDir` are known, the damaged member is stopped, and disk/inode capacity is sufficient for a backup and a fresh sync. Stop and escalate if quorum is unavailable, data freshness is uncertain, or more than one member needs rebuilding.

## Diagnose and Confirm Quorum

From the unpacked Apache ZooKeeper distribution root, set only incident-specific hosts locally; never commit them:

```bash
cd <apache-zookeeper-home>
export ZK_CLIENT_PORT=2181
export HEALTHY_HOSTS='<healthy-host-1> <healthy-host-2>'
export FAILED_HOST='<failed-host>'
export DATA_DIR=/var/lib/zookeeper
```

Check capacity and the startup log:

```bash
df -h "$DATA_DIR"
df -i "$DATA_DIR"
grep -iE 'error|exception|partial|unable|snapshot|transaction' \
  '<configured-zookeeper-log-file>'
```

Confirm the failed member is stopped before touching data:

```bash
ps -ef | grep '[Q]uorumPeerMain'
ss -lntp | grep ":$ZK_CLIENT_PORT"
```

Both commands must show no ZooKeeper process or listener. Then verify the healthy members:

Before using Four Letter Words, confirm that `srvr` and, if used, `ruok` are allowed by `4lw.commands.whitelist` and that the endpoint is a plaintext client port. ZooKeeper 3.5.3 and later require commands to be explicitly allowlisted. Do not weaken the whitelist during an incident only to run these probes. For a TLS-only client port, use the configured TLS client settings with `bin/zkServer.sh status` as documented in the [ZooKeeper tools guide](https://zookeeper.apache.org/doc/current/zookeeperTools.html), rather than `nc`.

```bash
for host in $HEALTHY_HOSTS; do
  echo "===== $host ====="
  echo ruok | nc -w 5 "$host" "$ZK_CLIENT_PORT"
  echo srvr | nc -w 10 "$host" "$ZK_CLIENT_PORT" \
    | grep -E 'Zxid:|Mode:|Node count:|Outstanding:'
done
```

Expect one leader and one follower, `Outstanding: 0`, and matching or quickly converging `Zxid` and `Node count`. Where `ruok` is allowlisted, `imok` confirms only that the process is running and bound to the client port; it does not prove quorum membership. If `srvr` is unavailable, use local `bin/zkServer.sh status` instead of changing the whitelist during recovery.

## Preserve Data and Resync One Member

Read the active configuration rather than inferring paths from logs:

```bash
grep -nE '^[[:space:]]*(dataDir|dataLogDir|server\.)[[:space:]]*=' conf/zoo.cfg
cat "$DATA_DIR/myid"
```

Stop ZooKeeper and reconfirm process and port are gone:

```bash
bin/zkServer.sh stop
ps -ef | grep '[Q]uorumPeerMain'
ss -lntp | grep ":$ZK_CLIENT_PORT"
```

Move, do not delete, the damaged `version-2`. Keep `myid` unchanged:

```bash
backup_dir="$DATA_DIR/version-2.corrupt.$(date +%Y%m%d-%H%M%S)"
test ! -e "$backup_dir" || { echo "Backup target exists: $backup_dir"; exit 1; }
mv "$DATA_DIR/version-2" "$backup_dir"
ls -ld "$DATA_DIR"/version-2* "$DATA_DIR/myid"
cat "$DATA_DIR/myid"
```

If `dataLogDir` is distinct, move its `version-2` separately; if it resolves to `dataDir`, move it only once. Do not manually create a new `version-2`.

```bash
bin/zkServer.sh start
```

Inspect console output or the configured ZooKeeper log after starting. Successful recovery normally shows leader discovery and DIFF, SNAP, TRUNC, or snapshot synchronization, then a follower role without the earlier EOF error. Apache documents that log output is sent to the console by default and/or to a file according to the logging configuration; do not assume a package-specific log path.

## Acceptance and Dependent Service Validation

Verify locally and across the ensemble:

```bash
bin/zkServer.sh status
echo ruok | nc -w 5 "$FAILED_HOST" "$ZK_CLIENT_PORT"

for host in $HEALTHY_HOSTS "$FAILED_HOST"; do
  echo "===== $host ====="
  echo srvr | nc -w 10 "$host" "$ZK_CLIENT_PORT" \
    | grep -E 'Zxid:|Mode:|Node count:|Outstanding:'
done
```

Acceptance criteria: one leader, two followers, `Outstanding: 0`, matching `Node count`, and matching or quickly converging `Zxid` values.

ZooKeeper recovery does not prove it was the sole cause of an application failure. Repeatedly exercise the original authorized dependent-service request and keep only sanitized status and timing evidence:

```bash
for i in $(seq 1 20); do
  curl -sS --connect-timeout 3 --max-time 20 \
    -o "/tmp/dependent-service-${i}.out" \
    -w 'http=%{http_code} total=%{time_total}s\n' \
    '<dependent-service-url>'
  sleep 2
done
```

If failures remain, inspect application logs and downstream dependencies before restarting services.

## Prohibited Operations and Follow-up

- Do not rebuild before confirming healthy quorum and configured data directories.
- Do not clear `version-2` on two or more members.
- Do not delete damaged data, overwrite `myid`, or copy another member's `myid`.
- Do not use broad permission changes such as `chmod 777` as recovery.
- Do not delete the backup immediately after the member rejoins.

`dataDir` stores snapshots and, unless `dataLogDir` is configured, transaction logs; `myid` identifies the server. These storage rules are described in the [Apache ZooKeeper Administrator's Guide](https://zookeeper.apache.org/doc/r3.7.0/zookeeperAdmin.html). Record only sanitized evidence after recovery: error signature, quorum checks, backup location class instead of its path, recovery time, and dependent-service validation. Add disk and inode alerts, review snapshot/log retention, and treat upgrades as a separate controlled change.
