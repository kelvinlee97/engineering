# ZooKeeper Production Deployment Guide for DevOps Beginners

Chinese version: [README_ZH.md](README_ZH.md)

This guide presents what a three-member Apache ZooKeeper 3.9.5 production environment on Ubuntu 24.04 LTS should look like. It is a reference architecture and operations guide, not evidence that this repository deployed or certified a live environment. The commands show one coherent implementation; adapt the example names, addresses, CIDRs, certificate paths, capacity, and retention values through your own design review and change process.

## Read This First: the 30-Minute Model

ZooKeeper is a small, highly available coordination service. Applications use it to agree on shared facts such as which service instance is leader, which members are alive, or what configuration is current. It is not a general database, message queue, or place for large application data.

This guide builds a production **ensemble**: three ZooKeeper servers holding the same coordination data. One server is the **leader**, which coordinates changes; the other two are **followers**, which keep replicas and vote. A **quorum** is the majority able to communicate: with three servers, two are enough. That is why one member can be restarted safely, but two cannot.

```text
Application ── TLS ──> zk-1, zk-2, zk-3  (client connection string)

zk-1  ←──────── TLS member communication ────────→  zk-2 / zk-3

Healthy production result: 1 leader + 2 followers; any 2 can form quorum.
```

Read this section first, then follow the deployment steps in order. “30 minutes” means enough time to understand the model and safety rules; it does not include certificate issuance, firewall approval, or a production change window.

| Layer | Role in the reference architecture | Daily operational concern |
| --- | --- | --- |
| Applications | Connect to all three secure client endpoints; never pin traffic to the leader. | Session stability, authentication failures, and application-visible latency. |
| ZooKeeper ensemble | One leader coordinates writes; two followers replicate and vote. | One leader, two followers, quorum health, request backlog, and follower convergence. |
| Persistent storage | `dataDir` stores snapshots; a separate `dataLogDir` stores transaction logs. | Capacity, inodes, fsync latency, purge policy, and recoverable snapshots. |
| Network and identity | Firewalls isolate client/quorum ports; TLS/mTLS and ACLs control trust and access. | Certificate expiry, SAN correctness, denied access, and unintended listeners. |
| Service and observability | systemd supervises each JVM; logs and JMX metrics expose symptoms. | Restart loops, JVM health, alert coverage, and ownership of response actions. |

### Newcomer vocabulary

| Term | Meaning for this guide |
| --- | --- |
| Ensemble | The three ZooKeeper servers acting as one service. |
| znode | A small record in ZooKeeper's tree, similar in shape to a file path; applications use it for coordination data. |
| Session and watch | A client session is its live connection; a watch lets the client learn that a znode changed. |
| `myid` | The unique number that tells each server whether it is `server.1`, `server.2`, or `server.3`. |
| `zxid` | A monotonically increasing change number; matching or converging values indicate members are catching up. |
| Snapshot / transaction log | Persistent copies of data / the ordered change log needed to recover it. |
| TLS / SAN | TLS encrypts and authenticates traffic; the certificate SAN must name the host or IP clients actually use. |
| CIDR | A compact way to describe an approved network range in a firewall rule. |
| JMX / Prometheus | JMX is Java's metrics interface; Prometheus is one optional system that collects those metrics and alerts. |

## Reference Architecture and Safety Boundary

At the end, `zk-1`, `zk-2`, and `zk-3` run one leader and two followers. Clients use the secure client port on all three hosts. A single member may be restarted; never deliberately stop or change two members at once.

| Item | Value | Exposure |
| --- | --- | --- |
| Secure client port | `2281` | Approved application CIDRs only |
| Quorum port | `2888` | ZooKeeper members only |
| Leader-election port | `3888` | ZooKeeper members only |
| AdminServer port | disabled in the baseline | none |
| Plain client port | disabled | none |

ZooKeeper stays available only while a majority can communicate. Three members tolerate one failed member; four members still tolerate only one, so adding a fourth member does not improve failure tolerance. Put members in independent failure domains, with independent power and network paths where possible. The transaction log needs its own device, and ZooKeeper must not swap. These are operational requirements, not optional tuning. See the [Apache Administrator's Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperAdmin.html).

Do not use this guide to recover a damaged data directory. For one failed member after disk-full transaction-log corruption, use the separate [recovery runbook](../../runbooks/disk-full-transaction-log-recovery/README.md) only after proving the other two members are healthy. If quorum is lost, stop routine changes and use the approved disaster-recovery process.

## 1. Prepare Hosts and Release Material — understand before running

**What you are doing:** preparing three independent servers and two persistent storage locations per server. **Why:** a shared failure domain or one busy disk can remove quorum or delay durable writes. **Success looks like:** each host has its own identity, and the snapshot and transaction-log paths are different mounted devices.

Prepare three Ubuntu 24.04 LTS VMs named `zk-1.example.internal`, `zk-2.example.internal`, and `zk-3.example.internal`. Ensure forward DNS for these certificate names, synchronized clocks, a current JDK, and firewall rules from the table above. Do not depend on reverse DNS for TLS identity, and do not co-locate ZooKeeper with a busy database, broker, or application workload.

On every host, install prerequisites, create the unprivileged account, and create distinct snapshot and log directories on separate mounted devices. Replace the version and release URL only through an approved release change; verify the Apache SHA-512 checksum before extracting it.

```bash
export ZK_VERSION=3.9.5
export ZK_HOME="/opt/apache-zookeeper-${ZK_VERSION}"
export ZK_USER=zookeeper
export ZK_GROUP=zookeeper

sudo apt-get update
sudo apt-get install --yes openjdk-17-jre-headless curl ca-certificates
sudo groupadd --system "$ZK_GROUP"
sudo useradd --system --gid "$ZK_GROUP" --home-dir /nonexistent --shell /usr/sbin/nologin "$ZK_USER"
sudo install -d -o "$ZK_USER" -g "$ZK_GROUP" -m 0750 \
  /etc/zookeeper /var/lib/zookeeper /var/log/zookeeper /srv/zookeeper-txn /etc/zookeeper/tls
```

Download and verify the exact Apache binary distribution with its published SHA-512 checksum, then extract it into the fixed `/opt` location owned by root. This example uses the official Apache download directory; an approved internal artifact repository may replace it only when it preserves the exact version and checksum.

```bash
export ZK_RELEASE_URL="https://downloads.apache.org/zookeeper/zookeeper-${ZK_VERSION}"
curl --fail --location --remote-name \
  "$ZK_RELEASE_URL/apache-zookeeper-${ZK_VERSION}-bin.tar.gz"
curl --fail --location --remote-name \
  "$ZK_RELEASE_URL/apache-zookeeper-${ZK_VERSION}-bin.tar.gz.sha512"
expected_sha512=$(awk '{print $1}' "apache-zookeeper-${ZK_VERSION}-bin.tar.gz.sha512")
actual_sha512=$(sha512sum "apache-zookeeper-${ZK_VERSION}-bin.tar.gz" | awk '{print $1}')
test "$actual_sha512" = "$expected_sha512" || { echo 'SHA-512 verification failed'; exit 1; }
sudo tar -xzf "apache-zookeeper-${ZK_VERSION}-bin.tar.gz" -C /opt
sudo ln -sfn "/opt/apache-zookeeper-${ZK_VERSION}-bin" "$ZK_HOME"
sudo chown -R root:root "/opt/apache-zookeeper-${ZK_VERSION}-bin"
sudo chmod -R go-w "/opt/apache-zookeeper-${ZK_VERSION}-bin"
```

Before continuing, record `hostname -f`, `timedatectl status`, `java -version`, `findmnt /var/lib/zookeeper /srv/zookeeper-txn`, and `df -hT` as sanitized deployment evidence. The data and transaction-log files must survive a process restart; the two directories must not resolve to the same backing device.

## 2. Configure the Ensemble and TLS — understand before running

**What you are doing:** giving all three servers the same membership list, while assigning each one a different `myid`. **Why:** every member must know who may vote, and TLS protects both application-to-ZooKeeper and member-to-member traffic. **Success looks like:** certificates match the host names, configuration is identical except for `myid`, and no plaintext client port exists.

Issue one server certificate per host, one administrator client certificate, and one host-local health-check client certificate per member from your existing CA. Each server certificate must include the host's FQDN and IP address, as applicable, in its Subject Alternative Name. This guide uses mutual TLS (mTLS): the server verifies client certificates, and clients verify server certificates. Store the server materials and each host-local health-check PKCS12 keystore/truststore in `/etc/zookeeper/tls/`, owned by `zookeeper` and mode `0640`; keep the administrator client certificate only on its controlled administrator host. Store every keystore/truststore password in a separate mode-`0640` password file, not in `zoo.cfg`, a shell history, or this repository.

Create `/etc/zookeeper/zoo.cfg` with the same ensemble lines on every host. The first block is common; replace only `server.id` in `myid` below. The passwords and certificate filenames are examples of paths, not credentials. Read the configuration in five groups: timing and disk paths; client entry point; client TLS; quorum TLS; then retention, diagnostics, and membership.

```properties
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper
dataLogDir=/srv/zookeeper-txn
secureClientPort=2281
serverCnxnFactory=org.apache.zookeeper.server.NettyServerCnxnFactory
ssl.keyStore.location=/etc/zookeeper/tls/server.p12
ssl.keyStore.passwordPath=/etc/zookeeper/tls/keystore-password
ssl.keyStore.type=PKCS12
ssl.trustStore.location=/etc/zookeeper/tls/truststore.p12
ssl.trustStore.passwordPath=/etc/zookeeper/tls/truststore-password
ssl.trustStore.type=PKCS12
ssl.hostnameVerification=true
ssl.allowReverseDnsLookup=false
ssl.clientAuth=need

sslQuorum=true
portUnification=false
ssl.quorum.keyStore.location=/etc/zookeeper/tls/server.p12
ssl.quorum.keyStore.passwordPath=/etc/zookeeper/tls/keystore-password
ssl.quorum.keyStore.type=PKCS12
ssl.quorum.trustStore.location=/etc/zookeeper/tls/truststore.p12
ssl.quorum.trustStore.passwordPath=/etc/zookeeper/tls/truststore-password
ssl.quorum.trustStore.type=PKCS12
ssl.quorum.hostnameVerification=true
ssl.quorum.allowReverseDnsLookup=false
ssl.quorum.clientAuth=need

autopurge.snapRetainCount=5
autopurge.purgeInterval=24
4lw.commands.whitelist=srvr,stat,ruok
server.1=zk-1.example.internal:2888:3888
server.2=zk-2.example.internal:2888:3888
server.3=zk-3.example.internal:2888:3888
```

`secureClientPort` replaces plaintext `clientPort`; do not add `clientPort` for convenience. `4lw.commands.whitelist` is deliberately minimal. The daily-operation baseline disables AdminServer, so there is no always-on HTTP management endpoint. ZooKeeper 3.5.3 and later require explicit 4LW allowlisting. TLS hostname verification must remain enabled, reverse-DNS fallback must remain disabled, and quorum client authentication is explicitly required, so certificates need correct SAN values. Configuration options are defined in the [Administrator's Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperAdmin.html).

Initialize the member on its matching host with the release-provided initializer. This is only for creating this brand-new ensemble: it creates the required `version-2` directories, writes the matching `myid`, and creates the `initialize` marker that ZooKeeper consumes on first start. Never run it, especially with `--force`, while repairing an existing member.

```bash
# Run one matching command per host, once, before its first start.
sudo -u zookeeper /opt/apache-zookeeper-3.9.5/bin/zkServer-initialize.sh \
  --configfile=/etc/zookeeper/zoo.cfg --myid=1  # zk-1 only
# ... --myid=2  # zk-2 only
# ... --myid=3  # zk-3 only
```

## 3. Run Under systemd — understand before running

**What you are doing:** letting systemd supervise ZooKeeper as an unprivileged service. **Why:** a failed JVM should be restarted predictably, but a missing data path must stop startup rather than create an empty service. **Success looks like:** systemd reports `active`, then the ensemble elects one leader after enough members start.

Create `/etc/systemd/system/zookeeper.service` on every member. The pre-start checks refuse to start with missing paths or an unexpectedly empty existing database; they reduce the risk of serving from a typoed data directory.

```ini
[Unit]
Description=Apache ZooKeeper
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=zookeeper
Group=zookeeper
Environment=ZOO_DATADIR_AUTOCREATE_DISABLE=1
Environment=ZOO_LOG_DIR=/var/log/zookeeper
Environment="SERVER_JVMFLAGS=-Dzookeeper.db.autocreate=false -Dzookeeper.serializeLastProcessedZxid.enabled=true -Dzookeeper.admin.enableServer=false -Dzookeeper.leader.closeSocketAsync=true -Dzookeeper.learner.closeSocketAsync=true"
ExecStartPre=/usr/bin/test -f /etc/zookeeper/zoo.cfg
ExecStartPre=/usr/bin/test -f /var/lib/zookeeper/myid
ExecStartPre=/usr/bin/test -d /srv/zookeeper-txn
ExecStart=/opt/apache-zookeeper-3.9.5/bin/zkServer.sh start-foreground /etc/zookeeper/zoo.cfg
Restart=on-failure
RestartSec=5
TimeoutStopSec=60
LimitNOFILE=65536
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

The pinned Apache ZooKeeper 3.9.5 binary distribution accepts `start-foreground /etc/zookeeper/zoo.cfg`; retain this invocation if you retain the pinned version. Because the foreground mode has no `zkServer.sh` PID file, systemd stops the JVM it supervises directly; do not add `zkServer.sh stop` as `ExecStop`. Treat a ZooKeeper version change as a separate, tested production change.

Start one member at a time, then inspect its journal before starting the next. A lone first member may remain `LOOKING` until it has a quorum; that is expected. Never use `systemctl restart zookeeper` across all hosts.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now zookeeper
sudo systemctl status zookeeper --no-pager
sudo journalctl -u zookeeper -b --no-pager | tail -n 100
```

## 4. Environment Acceptance Example

**What you are doing:** proving the client path, znode authorization, and quorum state. **Why:** a running process or open port alone does not prove that ZooKeeper can coordinate safely. **Success looks like:** a TLS client can perform only its approved test operations, and the three servers report one leader plus two followers.

Use the secure client configuration and a non-sensitive test path. Never test against an application's production znode without the application owner's authorization. mTLS identifies a client at the TLS connection, but it does not grant znode permissions by itself: each application's root znode needs an ACL matching its approved x509 X500 principal and minimum required permissions. Do not use `world:anyone` or `OPEN_ACL_UNSAFE` in production.

On the controlled administrator host, create `$HOME/.config/zookeeper/client-tls.env` with mode `0600`, owned by the approved administrator account. Keep this client-only file outside the server-owned `/etc/zookeeper` directory. It contains paths only, not a password; do not commit it. Replace the example paths with the administrator certificate material approved for this one-off deployment check.

```bash
install -d -m 0700 "$HOME/.config/zookeeper"
install -m 0600 /dev/null "$HOME/.config/zookeeper/client-tls.env"
${EDITOR:-vi} "$HOME/.config/zookeeper/client-tls.env"
```

```bash
# Contents of $HOME/.config/zookeeper/client-tls.env
export CLIENT_JVMFLAGS='-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty \
  -Dzookeeper.client.secure=true \
  -Dzookeeper.ssl.keyStore.location=/secure/path/admin-client.p12 \
  -Dzookeeper.ssl.keyStore.passwordPath=/secure/path/admin-client-keystore-password \
  -Dzookeeper.ssl.keyStore.type=PKCS12 \
  -Dzookeeper.ssl.trustStore.location=/secure/path/client-truststore.p12 \
  -Dzookeeper.ssl.trustStore.passwordPath=/secure/path/client-truststore-password \
  -Dzookeeper.ssl.trustStore.type=PKCS12'
```

Load the file in the current shell, then start the CLI:

```bash
. "$HOME/.config/zookeeper/client-tls.env"
/opt/apache-zookeeper-3.9.5/bin/zkCli.sh -server \
  'zk-1.example.internal:2281,zk-2.example.internal:2281,zk-3.example.internal:2281'
```

Before creating an application root path, record the application's approved X500 principal and permissions. The following administrator-only test grants permissions to the identity authenticated on this mTLS connection. ZooKeeper stores the resulting ACL under that client's `x509` principal. Application owners must use a separate root path and their own minimal permissions, never this administrator ACL.

```text
create /operations-guide-test "ok" auth::cdrwa
get /operations-guide-test
getAcl /operations-guide-test
quit
```

`getAcl` must display the expected `x509` principal and must not display `world:anyone`. Before deleting the test znode, reconnect in an approved isolated test with a second trusted certificate whose principal is not in this ACL and confirm `get /operations-guide-test` returns `NoAuth`. Do not use an application certificate for this negative test. Reconnect as the administrator, delete `/operations-guide-test`, then quit. This proves both TLS client authentication and znode authorization.

### Prepare recovery-root authorization before an incident

The snapshot and restore APIs require a dedicated recovery administrator to have `ALL` permission on `/`. Decide and approve that root ACL before production use; ACLs on child znodes do not grant this root permission. First record `getAcl /`. Then apply the exact approved root ACL through the normal access-control change process and verify it with `getAcl /` plus a `NoAuth` test using a separate trusted certificate. Do not copy the illustrative test ACL above into `/`: `setAcl /` replaces the root ACL list and can affect clients that need root access.

On each server, use TLS-aware `status` with that host's health-check client certificate. `ruok=imok` proves a bound, non-error process; it does not prove quorum. `zkServer.sh status` reports only the local role, so run it on all three members. Accept the deployment only when exactly one reports `leader`, two report `follower`, and the authorized TLS client test above succeeds.

```bash
sudo -u zookeeper env CLIENT_JVMFLAGS='-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty \
  -Dzookeeper.client.secure=true \
  -Dzookeeper.ssl.keyStore.location=/etc/zookeeper/tls/health-client.p12 \
  -Dzookeeper.ssl.keyStore.passwordPath=/etc/zookeeper/tls/health-client-keystore-password \
  -Dzookeeper.ssl.keyStore.type=PKCS12 \
  -Dzookeeper.ssl.trustStore.location=/etc/zookeeper/tls/truststore.p12 \
  -Dzookeeper.ssl.trustStore.passwordPath=/etc/zookeeper/tls/truststore-password \
  -Dzookeeper.ssl.trustStore.type=PKCS12' \
  /opt/apache-zookeeper-3.9.5/bin/zkServer.sh status /etc/zookeeper/zoo.cfg
```

For a TLS-only port, use `zkServer.sh status` with the same client TLS JVM settings; do not send plaintext probes to `2281`. Deeper request, latency, and data-size evidence belongs to the metrics path configured after first acceptance. ZooKeeper documents TLS-specific status invocation in its [tools guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperTools.html).

## 5. Operate, Monitor, and Change Safely — after first acceptance

### Daily checks and alerts

#### Why Prometheus?

Prometheus is not required to run ZooKeeper. ZooKeeper exposes JVM and server information through JMX; the Prometheus JMX Exporter is one way to convert that information into a standard `/metrics` endpoint for central collection, alerting, and historical trend analysis.

```text
ZooKeeper JVM → JMX → Prometheus JMX Exporter → Prometheus → Alerting
```

This guide uses the Java agent because it avoids exposing remote JMX/RMI. If your organization already uses Datadog, Zabbix, Elastic, or a cloud monitoring agent, replace only the exporter and collection step; the ZooKeeper ensemble, TLS, and systemd deployment remain unchanged.

Deploy the Prometheus JMX Exporter Java agent rather than remote JMX/RMI. Download the pinned upstream release, verify its published SHA-256 checksum before installation, and store it outside the writable ZooKeeper paths. An approved internal artifact repository may replace the URL only when it preserves this exact version and checksum:

```bash
export JMX_EXPORTER_VERSION=1.6.0
export JMX_EXPORTER_RELEASE_URL="https://github.com/prometheus/jmx_exporter/releases/download/${JMX_EXPORTER_VERSION}"
curl --fail --location --remote-name \
  "$JMX_EXPORTER_RELEASE_URL/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar"
curl --fail --location --remote-name \
  "$JMX_EXPORTER_RELEASE_URL/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar.sha256"
sha256sum --check "jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar.sha256"
sudo install -d -o root -g root -m 0755 /opt/jmx-exporter
sudo install -o root -g root -m 0644 \
  "jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar" \
  "/opt/jmx-exporter/jmx_prometheus_javaagent-${JMX_EXPORTER_VERSION}.jar"
```

Create `/etc/zookeeper/jmx-exporter.yaml` with this minimal reviewed rule set, then replace the existing `SERVER_JVMFLAGS` line in the systemd unit with the following combined line. Run `sudo systemctl daemon-reload`, then perform the one-member rolling restart procedure below. Preserve every existing JVM safeguard, including database validation, disabled AdminServer, and asynchronous quorum TLS socket closure; replacing the line with the Java agent alone would remove production safeguards. Binding to `127.0.0.1` keeps port `9404` private; use a local Prometheus agent or an approved local forwarder to scrape it.

```yaml
lowercaseOutputName: true
lowercaseOutputLabelNames: true
rules:
  - pattern: ".*"
```

```ini
Environment="SERVER_JVMFLAGS=-Dzookeeper.db.autocreate=false -Dzookeeper.serializeLastProcessedZxid.enabled=true -Dzookeeper.admin.enableServer=false -Dzookeeper.leader.closeSocketAsync=true -Dzookeeper.learner.closeSocketAsync=true -javaagent:/opt/jmx-exporter/jmx_prometheus_javaagent-1.6.0.jar=127.0.0.1:9404:/etc/zookeeper/jmx-exporter.yaml"
```

Verify `curl --fail http://127.0.0.1:9404/metrics` after each member restarts. Alert on: no leader or fewer than three healthy members, a follower not converging, request backlog, slow fsync warnings, JVM restart loops, disk/inode at 70% warning and 85% critical, snapshot/log growth, and certificate expiry within your organization's renewal window. The Java agent is the exporter’s recommended mode and its explicit host/port form binds to the chosen host; see the [JMX Exporter guide](https://prometheus.github.io/jmx_exporter/deployment/java-agent/). ZooKeeper itself exposes JMX and supports `zkServer.sh status` and diagnostic commands for monitoring.

At least daily, review:

```bash
sudo systemctl is-active zookeeper
sudo journalctl -u zookeeper --since '24 hours ago' --no-pager | grep -Ei \
  'error|exception|fsync|out of memory|unable|partial' || true
df -h /var/lib/zookeeper /srv/zookeeper-txn
df -i /var/lib/zookeeper /srv/zookeeper-txn
```

`autopurge.*` prevents unbounded old snapshot and transaction-log accumulation, but it does not replace capacity alerting or backup. Retain at least three snapshots; tune retention only after measuring recovery and storage needs. Apache describes automatic purge and data-file behavior in the [Administrator's Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperAdmin.html).

### Rolling restart or configuration change

**What you are doing:** changing one member while the other two preserve quorum. **Stop immediately** if the pre-check does not show one leader and two followers, or if the restarted member fails to rejoin. Do not proceed to a second member.

1. Freeze unrelated changes and confirm all three members are healthy.
2. Change only one member. For `zoo.cfg`, restart that member. For a systemd unit or drop-in, run `sudo systemctl daemon-reload` on that member before restarting it.
3. Wait for it to return as leader or follower, then run the TLS-aware role check on all three members.
4. Continue to the next member only after acceptance succeeds; otherwise stop and roll back that one member's change.

```bash
sudo systemctl restart zookeeper
sudo journalctl -u zookeeper -n 100 --no-pager
sudo -u zookeeper env CLIENT_JVMFLAGS='-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty \
  -Dzookeeper.client.secure=true \
  -Dzookeeper.ssl.keyStore.location=/etc/zookeeper/tls/health-client.p12 \
  -Dzookeeper.ssl.keyStore.passwordPath=/etc/zookeeper/tls/health-client-keystore-password \
  -Dzookeeper.ssl.keyStore.type=PKCS12 \
  -Dzookeeper.ssl.trustStore.location=/etc/zookeeper/tls/truststore.p12 \
  -Dzookeeper.ssl.trustStore.passwordPath=/etc/zookeeper/tls/truststore-password \
  -Dzookeeper.ssl.trustStore.type=PKCS12' \
  /opt/apache-zookeeper-3.9.5/bin/zkServer.sh status /etc/zookeeper/zoo.cfg
```

Do not use this procedure for a ZooKeeper version upgrade, quorum-TLS enablement, dynamic reconfiguration, a member-list change, client-port change, or certificate-CA replacement. Plan and validate each as a separate controlled change. The official guide specifically documents staged TLS rollout constraints.

### Backup and disaster recovery

**What you are doing:** distinguishing a normal single-member resync from data recovery. A restarted healthy member normally catches up automatically; a damaged data directory or lost quorum is an incident, not a routine restart.

A healthy ensemble normally resynchronizes one restarted member; do not copy another member's `myid` or data directory. Preserve and escalate on corruption. The existing [disk-full recovery runbook](../../runbooks/disk-full-transaction-log-recovery/README.md) covers the single-member case.

For complete quorum loss, block client traffic, use an approved and recently tested snapshot, and restore every member from the same snapshot under the dedicated [quorum-loss snapshot-restore runbook](../../runbooks/quorum-loss-snapshot-restore/README.md). This baseline keeps AdminServer disabled; the runbook defines the temporary, loopback-only HTTPS/mTLS management path. Snapshot/restore requires root-path authorization; never expose the endpoint publicly or paste its credentials into commands or logs. Test the complete recovery procedure in an isolated environment before relying on it. See the [Snapshot and Restore Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperSnapshotAndRestore.html).

## Production Readiness Checklist for Adopting Teams

Use this checklist when adapting the reference architecture to a real environment. Checked boxes are evidence collected by the adopting team; their presence in this guide is not a claim that this repository ran those tests.

- [ ] All three members run as the `zookeeper` user through systemd.
- [ ] The three members occupy independent failure domains and their firewall rules match the port matrix.
- [ ] Snapshot and transaction-log directories are on different devices, have inode/capacity alerts, and `autopurge` is active.
- [ ] Client and quorum traffic use TLS with valid SANs and hostname verification enabled.
- [ ] Every application has an approved znode-root ACL matrix; the separate recovery administrator has approved `ALL` permission on `/`; `getAcl` and `NoAuth` negative tests prove x509 authorization.
- [ ] Exactly one leader and two followers are observed; a TLS client has completed authorized test znode operations.
- [ ] Monitoring, log retention, certificate renewal ownership, snapshot retention, an isolated quorum-loss recovery rehearsal, and the recovery Runbooks are assigned to an operational owner.
- [ ] A single-member rolling restart was rehearsed in a maintenance-approved environment and returned to healthy quorum.
