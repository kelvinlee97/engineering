# ZooKeeper Quorum 丢失快照恢复 Runbook

English version: [README.md](README.md)

当三成员 ZooKeeper ensemble 失去 quorum、不能再接受更新时，才使用此事故专用 Runbook。它不适用于普通重启、单成员损坏或磁盘满 follower 修复；后者应使用[单成员磁盘满恢复手册](../disk-full-transaction-log-recovery/README_ZH.md)。

## 安全边界

此流程会破坏成员当前的本地数据库状态，并可能丢失所选 snapshot 之后的写入。在执行第 4 节前，必须获得 incident commander、ZooKeeper owner、应用 owner 和 security owner 批准。若健康多数派可能仍存在、snapshot 来源未知，或未验证根 znode ACL，则不得继续。

日常 systemd 服务会禁用 AdminServer。本 Runbook 仅临时以 `127.0.0.1:8443` 启用它，强制 HTTPS 并要求 client certificate。只能通过获批 SSH tunnel 访问；不得为恢复 endpoint 添加防火墙规则或公网监听。

## 前置条件与输入

- [ ] 已记录事故时间、受影响 ensemble、成员主机名、已配置 `dataDir` 和 `dataLogDir`。
- [ ] 已在获批 load-balancer、防火墙或应用层阻断 client traffic；应用已停止或进入 safe mode。
- [ ] 没有任意两台成员报告健康的 leader/follower quorum；若有两台健康，停止并改用单成员恢复。
- [ ] 受控存储中有一份已批准 snapshot 及其 SHA-512 checksum，且已确认是正确的恢复点。
- [ ] 管理员 x509 client certificate 对 `/` 拥有已批准的 `ALL` 权限，且已在事故前通过 `getAcl /` 和独立证书的 `NoAuth` 测试证明；获批 secret 机制可提供用于 HTTPS mTLS 的独立 control-host PEM certificate/key 和 CA file。
- [ ] 服务配置显式启用 `-Dzookeeper.serializeLastProcessedZxid.enabled=true`；禁用此前置条件时，restore 与 snapshot 都会失败。
- [ ] 已在隔离环境中针对该 ZooKeeper 版本与配置演练恢复流程。

在 control host 记录固定、非敏感变量。以下占位符不是凭据：

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

在变更任何成员前验证所选 snapshot；不匹配则停止。

```bash
expected_sha512=$(awk '{print $1}' "$SNAPSHOT_SHA512")
actual_sha512=$(sha512sum "$SNAPSHOT" | awk '{print $1}')
test "$actual_sha512" = "$expected_sha512" || {
  echo 'Snapshot checksum verification failed'; exit 1;
}
```

## 1. 确认 Quorum 丢失并保全证据

在三台主机采集 `systemctl status zookeeper`、最近 200 行 journal、`df -hT`、`df -i` 与 `findmnt /var/lib/zookeeper /srv/zookeeper-txn`。在每台成员执行生产指南中的 TLS-aware `zkServer.sh status`。不得把 `ruok` 当作 quorum 证据。

将证据和 snapshot checksum 附到事故记录。不得删除、重新初始化或复制其他成员的 `myid`、`version-2` 或 transaction-log data。

## 2. 临时启用本地恢复 AdminServer

一次只处理一个成员。创建 `/etc/systemd/system/zookeeper.service.d/90-disaster-recovery.conf`，内容如下；它只在事故期间替换日常 `SERVER_JVMFLAGS`。server 现有的 `ssl.quorum.*` keystore/truststore 设置会提供 HTTPS material，且 truststore 必须信任恢复管理员证书。

```ini
[Service]
Environment="SERVER_JVMFLAGS=-Dzookeeper.db.autocreate=false -Dzookeeper.serializeLastProcessedZxid.enabled=true -Dzookeeper.admin.enableServer=true -Dzookeeper.admin.serverAddress=127.0.0.1 -Dzookeeper.admin.serverPort=8443 -Dzookeeper.admin.forceHttps=true -Dzookeeper.admin.needClientAuth=true"
```

reload systemd 并只重启当前准备的成员。即使进程仍在运行，也必须重启：`systemctl start` 不会应用新的 JVM flags。此时 client traffic 已被阻断。确认 journal 显示 AdminServer 绑定 `127.0.0.1:8443`；若显示其他地址，继续前必须停止并移除 drop-in。

```bash
sudo install -d -m 0755 /etc/systemd/system/zookeeper.service.d
sudoedit /etc/systemd/system/zookeeper.service.d/90-disaster-recovery.conf
sudo systemctl daemon-reload
sudo systemctl restart zookeeper
sudo journalctl -u zookeeper -n 100 --no-pager
```

从 control host 建立保留 server FQDN 的 tunnel，以便 TLS hostname verification：

```bash
ssh -N -L 8443:127.0.0.1:8443 zookeeper-admin@zk-1.example.internal
```

在第二个 control-host shell 通过 mTLS 使用 tunnel。`--resolve` 让 TLS name 匹配 server certificate，而 TCP 连接仍保持在本地 tunnel：

```bash
curl --fail --silent --show-error \
  --cacert "$DR_CA_CERT_PEM" \
  --cert "$DR_CLIENT_CERT_PEM" --key "$DR_CLIENT_KEY_PEM" \
  --resolve "zk-1.example.internal:${DR_ADMIN_PORT}:127.0.0.1" \
  "https://zk-1.example.internal:${DR_ADMIN_PORT}/commands/leader"
```

请求只能经 tunnel 成功；不带 client certificate 的请求必须失败。任一条件不成立时停止并联系 security owner。

## 3. 从同一 Snapshot 恢复每个成员

在 incident commander 指挥下逐成员执行。恢复成员前先停止它，并把两份 `version-2` 目录保留为带时间戳的同级目录。不得删除这些保留目录；它们是回退与取证证据。由于服务保持启用 database-existence validation，必须仅在完成保全后、且 client traffic 仍被阻断时创建一次性 `initialize` marker。它让这个有意清空的成员在恢复获批 snapshot 前暂时能够投票；ZooKeeper 会在启动时消费该 marker。替换下方路径前必须确认配置的实际路径。

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

本地 HTTPS AdminServer 通过 tunnel 可用后，将*同一份已验证 snapshot*发送给该成员。恢复管理员证书必须对 `/` 拥有 `ALL` 权限。将成功 response 的 `last_zxid` 记录到事故记录；任何非 2xx response 都是停止条件。

```bash
curl --fail --silent --show-error \
  --cacert "$DR_CA_CERT_PEM" \
  --cert "$DR_CLIENT_CERT_PEM" --key "$DR_CLIENT_KEY_PEM" \
  --resolve "zk-1.example.internal:${DR_ADMIN_PORT}:127.0.0.1" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary "@$SNAPSHOT" \
  "https://zk-1.example.internal:${DR_ADMIN_PORT}/commands/restore"
```

立即将已恢复的内存数据库持久化到该成员的新 data directory。response headers 必须包含 `last_zxid`；记录它，并确认它与 restore response 一致，因为 client traffic 仍被阻断。

```bash
curl --fail --silent --show-error --output /dev/null --dump-header - \
  --cacert "$DR_CA_CERT_PEM" \
  --cert "$DR_CLIENT_CERT_PEM" --key "$DR_CLIENT_KEY_PEM" \
  --resolve "zk-1.example.internal:${DR_ADMIN_PORT}:127.0.0.1" \
  "https://zk-1.example.internal:${DR_ADMIN_PORT}/commands/snapshot?streaming=false"
```

等待 restore 与 snapshot 的 journal evidence 后才能处理下一台成员。对 `zk-2` 和 `zk-3` 重复 tunnel、保全、一次性 marker、restore 与持久化流程，只替换 FQDN。成员间不得混用 snapshot，也不得并行运行成员。

## 4. 重建 Quorum 并关闭恢复接口

三台成员都从同一 snapshot 恢复并持久化后，不得为了重建 quorum 而重启它们：这些成员已经在运行。保持 client traffic 阻断并等待选举。对每台成员使用生产指南的 TLS-aware status command。若无法形成恰好一台 leader、两台 follower，停止并携带 restore response 与 journal 升级处理；不得把重试 restore 或重启节点当作试验。

只有 quorum 检查成功后，才在每台成员移除事故专用 drop-in 并逐台重启。每次重启后，等待它重新加入为 leader 或 follower 才能继续。仅当恰好一台报告 `leader`、两台报告 `follower`、每台成员已记录的 restore 与本地 snapshot `last_zxid` 相符，且应用 owner 已批准 ACL 与依赖检查时，才能接受恢复。

在每台成员移除事故专用 drop-in、reload systemd，并逐台重启，使日常服务再次包含 `-Dzookeeper.admin.enableServer=false`。重新开放 client traffic 前，确认没有 listener 占用 `8443`。

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

最后执行每个应用已批准的 `getAcl` 与 authorized-operation checks。逐步重新开放 client traffic，观察应用错误与 ZooKeeper metrics；保留 pre-restore directories 与事故证据，直至 incident commander 关闭事故。

## 参考

- [Apache Snapshot and Restore Guide](https://zookeeper.apache.org/doc/current/zookeeperSnapshotAndRestore.html)
- [Apache Administrator's Guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html)
- [生产部署指南](../../guides/production-deployment/README_ZH.md)
