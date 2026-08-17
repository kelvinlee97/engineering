# DevOps 新手 ZooKeeper 生产部署与运维指南

English version: [README.md](README.md)

本指南展示 Ubuntu 24.04 LTS 上三成员 Apache ZooKeeper 3.9.5 生产环境应有的样子。它是一套参考架构与日常运维指南，不代表本仓库已经部署或认证某个真实环境。文中命令用于展示一套前后一致的实现；采用时应通过自己的设计评审和变更流程调整示例域名、地址、CIDR、证书路径、容量与保留值。

## 先读这里：30 分钟建立心智模型

ZooKeeper 是一个小型、高可用的分布式协调服务。应用用它来对共享事实达成一致，例如哪一个服务实例是 leader、哪些成员仍存活，或当前配置是什么。它不是通用数据库、消息队列，也不适合存放大型应用数据。

本指南部署的是生产 **ensemble（集群）**：三台 ZooKeeper server 保存同一份协调数据。一台是 **leader**，负责协调变更；另外两台是 **follower**，保存副本并参与投票。**quorum（多数派）** 是能够互相通信的多数节点：三台中只要两台即可。因此一次重启一台是安全的，同时停两台则不是。

```text
应用 ── TLS ──> zk-1、zk-2、zk-3  （client connection string）

zk-1  ←──────── TLS 成员间通信 ────────→  zk-2 / zk-3

健康生产结果：1 台 leader + 2 台 follower；任意 2 台可形成 quorum。
```

先读完本节，再按顺序执行部署步骤。“30 分钟”指理解模型和安全规则所需时间，不包括申请证书、防火墙审批或生产变更窗口。

| 层级 | 在参考架构中的职责 | 日常运维关注点 |
| --- | --- | --- |
| 应用 | 连接全部三个安全客户端端点；不得把流量固定到 leader。 | Session 稳定性、认证失败和应用可见延迟。 |
| ZooKeeper ensemble | 一台 leader 协调写入，两台 follower 复制并投票。 | 一主两从、quorum 健康、请求积压和 follower 收敛。 |
| 持久化存储 | `dataDir` 保存 snapshot，独立的 `dataLogDir` 保存 transaction log。 | 容量、inode、fsync 延迟、清理策略和可恢复 snapshot。 |
| 网络与身份 | 防火墙隔离 client/quorum 端口；TLS/mTLS 与 ACL 控制信任和访问。 | 证书到期、SAN 正确性、拒绝访问和意外 listener。 |
| 服务与可观测性 | systemd 管理各 JVM；日志和 JMX 指标暴露症状。 | 重启循环、JVM 健康、告警覆盖和响应责任人。 |

### 新手术语卡片

| 术语 | 在本指南中的含义 |
| --- | --- |
| Ensemble（集群） | 三台 ZooKeeper server 作为一个服务协同工作。 |
| znode | ZooKeeper 树中的小型记录，形状类似文件路径；应用用它保存协调数据。 |
| Session / watch | Session 是客户端的持续连接；watch 让客户端知道某个 znode 已发生变化。 |
| `myid` | 每台 server 的唯一编号，用于确认自己是 `server.1`、`server.2` 或 `server.3`。 |
| `zxid` | 单调递增的变更编号；数值一致或趋同表示成员正在同步。 |
| Snapshot / transaction log | 数据的持久化副本 / 按顺序记录的变更日志，恢复时需要它们。 |
| TLS / SAN | TLS 负责加密和验证身份；证书 SAN 必须包含客户端实际使用的主机名或 IP。 |
| CIDR | 防火墙规则中表示获准网络范围的简写。 |
| JMX / Prometheus | JMX 是 Java 的指标接口；Prometheus 是可选的指标采集与告警系统。 |

## 参考架构与安全边界

完成后，`zk-1`、`zk-2`、`zk-3` 组成一台 leader 和两台 follower；客户端通过三个节点的安全 client port 连接。一次只允许重启或变更一个成员，绝不可同时停止或变更两个成员。

| 项目 | 值 | 暴露范围 |
| --- | --- | --- |
| 安全 client port | `2281` | 仅获批准的应用 CIDR |
| Quorum port | `2888` | 仅 ZooKeeper 成员 |
| Leader election port | `3888` | 仅 ZooKeeper 成员 |
| AdminServer port | 基线中禁用 | 无 |
| 明文 client port | 禁用 | 无 |

ZooKeeper 只有在多数节点互相通信时才可用。三节点可容忍一台故障；四节点仍然只能容忍一台，因此增加第四个节点不会提升容错能力。成员应放在独立故障域，并尽可能使用独立电源和网络路径。transaction log 必须使用独立设备，ZooKeeper 不得发生 swap；这些是运维前提，不是可选调优。参见 [Apache Administrator's Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperAdmin.html)。

本指南不能用于恢复损坏的数据目录。单个成员因磁盘满导致 transaction log 损坏时，必须先证明另两个成员健康，再使用独立的[磁盘满恢复手册](../../runbooks/disk-full-transaction-log-recovery/README_ZH.md)。如果失去 quorum，应停止常规变更，转入已批准的灾难恢复流程。

## 1. 准备主机与发布包：理解后再执行

**你在做什么：** 准备三台相互独立的服务器，并为每台准备两个持久化存储位置。**为什么：** 共用故障域或繁忙的单块磁盘可能使 quorum 丢失，或拖慢持久化写入。**成功时应看到：** 每台主机有独立身份，snapshot 与 transaction-log 路径位于不同挂载设备。

准备三台 Ubuntu 24.04 LTS VM：`zk-1.example.internal`、`zk-2.example.internal`、`zk-3.example.internal`。确认这些证书名称的正向 DNS、时间同步、当前 JDK，以及符合上表的防火墙规则。不要依赖反向 DNS 作为 TLS identity，也不要把 ZooKeeper 与繁忙的数据库、broker 或应用工作负载共置。

每台主机都安装前置软件、创建非特权账户，并在不同挂载设备上创建 snapshot 与 transaction-log 目录。版本与发布地址只能通过已批准的发布变更替换；解压前必须使用 Apache 发布的 SHA-512 校验值验证发行包。

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

下载并使用其发布的 SHA-512 校验值验证精确的 Apache 二进制发行包，再解压至固定的 `/opt` 位置并由 root 所有。下面示例使用 Apache 官方下载目录；已批准的内部制品库可替代它，但必须保留完全相同的版本与 checksum。

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

继续前，以脱敏方式记录 `hostname -f`、`timedatectl status`、`java -version`、`findmnt /var/lib/zookeeper /srv/zookeeper-txn` 和 `df -hT`。数据目录和 transaction-log 目录必须跨进程重启保留，且不能落在相同底层设备。

## 2. 配置 Ensemble 与 TLS：理解后再执行

**你在做什么：** 让三台 server 使用相同成员列表，同时给每台分配不同 `myid`。**为什么：** 每个成员都必须知道谁能投票；TLS 同时保护应用到 ZooKeeper、以及 ZooKeeper 成员之间的通信。**成功时应看到：** 证书匹配主机名，除了 `myid` 外配置一致，且不存在明文 client port。

通过现有组织 CA 为每台主机签发一张 server certificate、为管理员签发一张 client certificate，并为每台成员签发一张仅本机使用的 health-check client certificate。每张 server certificate 必须在 Subject Alternative Name 中包含相应 FQDN 和适用的 IP。本指南使用 mutual TLS（mTLS）：server 验证 client certificate，client 验证 server certificate。将 server material 与每台本机 health-check PKCS12 keystore/truststore 放入 `/etc/zookeeper/tls/`，所有者设为 `zookeeper`、权限为 `0640`；管理员 client certificate 只保留在受控管理员主机。每个 keystore/truststore password 应放在单独的 `0640` password file 中，不能写入 `zoo.cfg`、shell history 或此仓库。

在每台主机创建相同的 `/etc/zookeeper/zoo.cfg`。下面是通用配置；仅在下文 `myid` 中替换各自 ID。密码和证书文件名只是路径示例，并非凭据。可将配置分成五组阅读：时间和磁盘路径、client 入口、client TLS、quorum TLS、以及保留策略/诊断/成员列表。

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

`secureClientPort` 取代明文 `clientPort`；不要为了方便再添加 `clientPort`。`4lw.commands.whitelist` 有意保持最小。日常运维基线会禁用 AdminServer，因此不存在常驻 HTTP 管理端点。ZooKeeper 3.5.3 以后需显式允许 4LW；TLS 主机名验证必须保持开启、反向 DNS fallback 必须保持禁用，并且 quorum client authentication 被显式设为必需，因此证书 SAN 必须正确。配置含义参见 [Administrator's Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperAdmin.html)。

在对应主机使用发行包自带初始化脚本创建成员。该步骤仅用于创建全新的 ensemble：它会创建所需 `version-2` 目录、写入对应的 `myid`，并创建供 ZooKeeper 首次启动消费的 `initialize` marker。修复已有成员时绝不能运行它，尤其不能使用 `--force`。

```bash
# 每台主机在首次启动前只执行与自身匹配的一条，且只执行一次。
sudo -u zookeeper /opt/apache-zookeeper-3.9.5/bin/zkServer-initialize.sh \
  --configfile=/etc/zookeeper/zoo.cfg --myid=1  # 仅 zk-1
# ... --myid=2  # 仅 zk-2
# ... --myid=3  # 仅 zk-3
```

## 3. 使用 systemd 运行：理解后再执行

**你在做什么：** 让 systemd 以非特权服务账户监管 ZooKeeper。**为什么：** JVM 故障后应可预测地重启，但数据路径缺失时必须阻止启动，不能默默创建一个空服务。**成功时应看到：** systemd 显示 `active`；足够成员启动后，集群选出一台 leader。

在每个成员创建 `/etc/systemd/system/zookeeper.service`。启动前检查会拒绝缺失路径或意外空数据库启动，从而降低因写错数据目录而提供空数据的风险。

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

固定的 Apache ZooKeeper 3.9.5 二进制发行包支持 `start-foreground /etc/zookeeper/zoo.cfg`；只要仍使用该固定版本就应保留此调用方式。foreground 模式不会创建 `zkServer.sh` 所需的 PID file，因此由 systemd 直接停止其监管的 JVM；不要把 `zkServer.sh stop` 添加为 `ExecStop`。ZooKeeper 版本变更必须作为独立、经测试的生产变更。

每次只启动一个成员，并在启动下一台之前查看 journal。第一台单独启动时可能保持 `LOOKING`，直到获得 quorum；这属于预期。绝不能在所有主机同时运行 `systemctl restart zookeeper`。

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now zookeeper
sudo systemctl status zookeeper --no-pager
sudo journalctl -u zookeeper -b --no-pager | tail -n 100
```

## 4. 环境验收示例

**你在做什么：** 同时证明 client 路径、znode 授权与 quorum 状态。**为什么：** 进程运行或端口开放，不能单独证明 ZooKeeper 能安全协调。**成功时应看到：** TLS client 只能完成已批准的测试操作，三个 server 显示一台 leader 加两台 follower。

使用安全 client configuration 和无敏感性的测试路径。未经应用所有者授权，不得对应用生产 znode 进行测试。mTLS 在 TLS 连接上识别 client，但不会自动授予 znode 权限：每个应用的根 znode 都必须有与已批准 x509 X500 principal 及最小权限相匹配的 ACL。生产环境禁止使用 `world:anyone` 或 `OPEN_ACL_UNSAFE`。

在受控管理员主机创建 `$HOME/.config/zookeeper/client-tls.env`，权限为 `0600`，所有者为获批管理员账户。此 client-only 文件必须位于 server 所有的 `/etc/zookeeper` 目录之外。文件只保存路径、不保存 password，且不得提交。将示例路径替换为仅用于本次部署检查的已批准管理员证书材料。

```bash
install -d -m 0700 "$HOME/.config/zookeeper"
install -m 0600 /dev/null "$HOME/.config/zookeeper/client-tls.env"
${EDITOR:-vi} "$HOME/.config/zookeeper/client-tls.env"
```

```bash
# $HOME/.config/zookeeper/client-tls.env 的内容
export CLIENT_JVMFLAGS='-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty \
  -Dzookeeper.client.secure=true \
  -Dzookeeper.ssl.keyStore.location=/secure/path/admin-client.p12 \
  -Dzookeeper.ssl.keyStore.passwordPath=/secure/path/admin-client-keystore-password \
  -Dzookeeper.ssl.keyStore.type=PKCS12 \
  -Dzookeeper.ssl.trustStore.location=/secure/path/client-truststore.p12 \
  -Dzookeeper.ssl.trustStore.passwordPath=/secure/path/client-truststore-password \
  -Dzookeeper.ssl.trustStore.type=PKCS12'
```

在当前 shell 加载文件，再启动 CLI：

```bash
. "$HOME/.config/zookeeper/client-tls.env"
/opt/apache-zookeeper-3.9.5/bin/zkCli.sh -server \
  'zk-1.example.internal:2281,zk-2.example.internal:2281,zk-3.example.internal:2281'
```

创建应用根路径前，记录应用已批准的 X500 principal 与权限。以下管理员专用测试会把权限授予当前 mTLS 连接中已认证的身份；ZooKeeper 会将结果 ACL 保存为该 client 的 `x509` principal。应用所有者必须使用独立根路径和自己的最小权限，不能使用此管理员 ACL。

```text
create /operations-guide-test "ok" auth::cdrwa
get /operations-guide-test
getAcl /operations-guide-test
quit
```

`getAcl` 必须显示预期的 `x509` principal，且不得显示 `world:anyone`。删除测试 znode 前，在已批准的隔离测试中，使用第二张已受信但 principal 不在 ACL 中的证书重新连接，并确认 `get /operations-guide-test` 返回 `NoAuth`。不得使用应用证书执行此反向测试。再以管理员身份重新连接，删除 `/operations-guide-test` 后退出。这样才能同时证明 TLS client authentication 与 znode authorization。

### 在事故前准备 recovery-root authorization

Snapshot 和 restore API 要求专用 recovery administrator 对 `/` 拥有 `ALL` 权限。必须在生产使用前决定并批准该 root ACL；子 znode 上的 ACL 不会授予此 root 权限。先记录 `getAcl /`。然后通过正常 access-control 变更流程应用已批准的精确 root ACL，并用 `getAcl /` 和另一张受信任证书的 `NoAuth` 测试验证。不得把上方示例测试 ACL 复制到 `/`：`setAcl /` 会替换 root ACL 列表，并可能影响需要访问 root 的 client。

每台服务器上使用支持 TLS 的 `status`，并使用该主机的 health-check client certificate。`ruok=imok` 只能证明进程已绑定端口且没有错误，不能证明 quorum。`zkServer.sh status` 只输出本机角色，因此必须在三台成员上都运行。仅当恰好一台显示 `leader`、两台显示 `follower`，并且上文已授权 TLS client 测试成功时，才能接受本次部署。

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

TLS-only port 应以相同 client TLS JVM 设置运行 `zkServer.sh status`；不得向 `2281` 发送明文探测流量。更深入的请求、延迟和数据规模证据属于首次验收后配置的 metrics 路径。ZooKeeper 对 TLS 场景的 status 用法见 [tools guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperTools.html)。

## 5. 安全运维、监控与变更：首次验收后再做

### 日常检查与告警

#### 为什么选择 Prometheus？

运行 ZooKeeper 不依赖 Prometheus。ZooKeeper 通过 JMX 暴露 JVM 与 server 信息；Prometheus JMX Exporter 只是把这些信息转换为标准 `/metrics` endpoint 的一种方式，从而支持集中采集、告警和历史趋势分析。

```text
ZooKeeper JVM → JMX → Prometheus JMX Exporter → Prometheus → Alerting
```

本指南采用 Java agent，因为它避免暴露 remote JMX/RMI。如果组织已经使用 Datadog、Zabbix、Elastic 或云监控 agent，只需替换 exporter 与采集环节；ZooKeeper ensemble、TLS 和 systemd 部署均不受影响。

使用 Prometheus JMX Exporter Java agent，而不是远程 JMX/RMI。下载固定的上游 release，在安装前验证其已发布的 SHA-256 checksum，并把它放在 ZooKeeper 不可写的路径之外。只有在内部 artifact repository 保留精确版本和 checksum 时，才可替换该 URL：

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

创建 `/etc/zookeeper/jmx-exporter.yaml`，使用以下经过审阅的最小 rule set；随后将 systemd unit 中现有的 `SERVER_JVMFLAGS` 行替换为下面合并后的行。执行 `sudo systemctl daemon-reload`，再按照下文单成员滚动重启流程执行。必须保留现有全部 JVM 安全设置，包括数据库验证、禁用 AdminServer 和 quorum TLS socket 异步关闭；若只替换成 Java agent，会移除生产保护。绑定到 `127.0.0.1` 可让 `9404` 保持私有；请通过本地 Prometheus agent 或获批准的本地转发器采集。

```yaml
lowercaseOutputName: true
lowercaseOutputLabelNames: true
rules:
  - pattern: ".*"
```

```ini
Environment="SERVER_JVMFLAGS=-Dzookeeper.db.autocreate=false -Dzookeeper.serializeLastProcessedZxid.enabled=true -Dzookeeper.admin.enableServer=false -Dzookeeper.leader.closeSocketAsync=true -Dzookeeper.learner.closeSocketAsync=true -javaagent:/opt/jmx-exporter/jmx_prometheus_javaagent-1.6.0.jar=127.0.0.1:9404:/etc/zookeeper/jmx-exporter.yaml"
```

每个成员重启后，执行 `curl --fail http://127.0.0.1:9404/metrics` 验证。应对以下情况告警：没有 leader 或健康成员少于三台、follower 未收敛、请求积压、fsync 变慢、JVM 重启循环、磁盘/inode 70% 告警和 85% 严重、snapshot/log 增长、以及证书在组织续期窗口内即将到期。Java agent 是 exporter 推荐模式；显式 host/port 形式会绑定到指定主机，见 [JMX Exporter guide](https://prometheus.github.io/jmx_exporter/deployment/java-agent/)。ZooKeeper 本身支持 JMX、`zkServer.sh status` 和诊断命令。

每天至少检查：

```bash
sudo systemctl is-active zookeeper
sudo journalctl -u zookeeper --since '24 hours ago' --no-pager | grep -Ei \
  'error|exception|fsync|out of memory|unable|partial' || true
df -h /var/lib/zookeeper /srv/zookeeper-txn
df -i /var/lib/zookeeper /srv/zookeeper-txn
```

`autopurge.*` 可防止旧 snapshot 和 transaction log 无限制累积，但不能替代容量告警或备份。至少保留三份 snapshot；只可在测量恢复需求和存储需求后调整保留数。Apache 在 [Administrator's Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperAdmin.html) 说明自动清理和数据文件行为。

### 滚动重启或配置变更

**你在做什么：** 在另两台维持 quorum 时只变更一台成员。若前置检查未显示一台 leader、两台 follower，或重启成员未重新加入，应立刻停止；不得继续处理第二台成员。

1. 冻结无关变更，确认三个成员全部健康。
2. 只变更一个成员。若修改 `zoo.cfg`，重启该成员；若修改 systemd unit 或 drop-in，先在该成员执行 `sudo systemctl daemon-reload`，再重启。
3. 等待该成员恢复为 leader 或 follower，再在三台成员上运行支持 TLS 的角色检查。
4. 仅在验收成功后继续下一台；否则停止并回滚这一台的变更。

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

不得将 ZooKeeper 版本升级、quorum TLS 启用、动态重配置、成员列表变更、client port 变更或证书 CA 替换纳入此流程。每项都必须独立计划和验证；官方指南对 TLS 的分阶段上线有明确约束。

### 备份与灾难恢复

**你在做什么：** 区分正常单成员重新同步和数据恢复。健康成员重启后通常会自动追上；数据目录损坏或失去 quorum 属于事故，不是常规重启。

健康 ensemble 通常会让单个重启成员自动同步；不要复制其他成员的 `myid` 或数据目录。发现损坏时保留现场并升级处理。[磁盘满恢复手册](../../runbooks/disk-full-transaction-log-recovery/README_ZH.md) 仅覆盖单成员场景。

如果整个 ensemble 失去 quorum，应阻断 client traffic，使用已经验证且近期生成的 snapshot，并按独立的 [quorum 丢失快照恢复 Runbook](../../runbooks/quorum-loss-snapshot-restore/README_ZH.md) 让所有成员从同一 snapshot 恢复。本基线会禁用 AdminServer；该 Runbook 定义临时、仅 loopback 的 HTTPS/mTLS 管理路径。snapshot/restore 需要 root-path 授权；绝不公开该端点，也不得把凭据粘贴到命令或日志中。在依赖它前，必须先在隔离环境完成完整恢复演练。见 [Snapshot and Restore Guide](https://zookeeper.apache.org/doc/r3.9.5/zookeeperSnapshotAndRestore.html)。

## 采用团队的生产就绪检查表

将这套参考架构应用到真实环境时使用本检查表。勾选项应由采用团队收集证据；它们出现在本文中，并不表示本仓库已经执行这些测试。

- [ ] 三个成员均以 `zookeeper` 用户通过 systemd 运行。
- [ ] 三成员位于独立故障域，防火墙规则符合端口矩阵。
- [ ] Snapshot 与 transaction-log 目录位于不同设备，具备 inode/容量告警，且启用了 `autopurge`。
- [ ] Client 与 quorum traffic 均使用 TLS、有效 SAN 和开启的主机名验证。
- [ ] 每个应用都有已批准的 znode-root ACL 矩阵；独立的 recovery administrator 对 `/` 拥有已批准的 `ALL` 权限；`getAcl` 与 `NoAuth` 反向测试证明 x509 授权有效。
- [ ] 已观察到一台 leader、两台 follower；TLS client 已完成已授权测试 znode 操作。
- [ ] 监控、日志保留、证书续期责任、snapshot 保留、隔离 quorum 丢失恢复演练和恢复 Runbook 均已有运维负责人。
- [ ] 已在获批准维护环境演练单成员滚动重启，并恢复为健康 quorum。
