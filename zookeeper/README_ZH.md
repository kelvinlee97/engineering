# ZooKeeper 磁盘满恢复手册

English version: [README.md](README.md)

本手册用于处理 ZooKeeper 单个节点因磁盘写满、导致本地事务日志不完整且无法启动的场景。命令采用 Apache [Getting Started Guide](https://zookeeper.apache.org/doc/r3.8.6/zookeeperStarted.html) 的二进制发行包布局：从 `<apache-zookeeper-home>` 运行，官方示例配置文件为 `conf/zoo.cfg`，其中 `dataDir=/var/lib/zookeeper`、`clientPort=2181`。只有在确认生效配置和恢复权限后，才能替换主机值。

## 安全边界

典型错误：

```text
Last transaction was partial.
Unable to load database on disk
java.io.EOFException
```

释放磁盘空间只能消除写入阻塞，不能修复已经截断的 transaction log。不要反复执行 `zkServer.sh restart`。

只有在以下条件都满足时才继续：仅一个节点故障、其他节点可组成健康 quorum、已确认实际 `dataDir` 和可选 `dataLogDir`、故障节点已停止，且磁盘/inode 足以容纳备份和重新同步的数据。若 quorum 不健康、数据新鲜度不确定或需要重建多个节点，应停止并升级处理。

## 确认故障和健康 quorum

从解压后的 Apache ZooKeeper 发行包根目录开始，仅在本地填入当前事故的主机值，不得提交真实值：

```bash
cd <apache-zookeeper-home>
export ZK_CLIENT_PORT=2181
export HEALTHY_HOSTS='<healthy-host-1> <healthy-host-2>'
export FAILED_HOST='<failed-host>'
export DATA_DIR=/var/lib/zookeeper
```

检查容量和启动日志：

```bash
df -h "$DATA_DIR"
df -i "$DATA_DIR"
grep -iE 'error|exception|partial|unable|snapshot|transaction' \
  '<configured-zookeeper-log-file>'
```

处理数据前，确认故障节点已停止：

```bash
ps -ef | grep '[Q]uorumPeerMain'
ss -lntp | grep ":$ZK_CLIENT_PORT"
```

两条命令都不能显示 ZooKeeper 进程或监听端口。然后检查健康节点：

使用 Four Letter Words 前，确认 `srvr` 以及需要时的 `ruok` 已列入 `4lw.commands.whitelist`，且目标是明文 client port。ZooKeeper 3.5.3 及以后要求显式白名单这些命令。不得为了临时探测在事故中放宽白名单。若仅启用了 TLS client port，应按照 [ZooKeeper tools guide](https://zookeeper.apache.org/doc/current/zookeeperTools.html) 使用已配置的 TLS client settings 运行 `bin/zkServer.sh status`，而不是使用 `nc`。

```bash
for host in $HEALTHY_HOSTS; do
  echo "===== $host ====="
  echo ruok | nc -w 5 "$host" "$ZK_CLIENT_PORT"
  echo srvr | nc -w 10 "$host" "$ZK_CLIENT_PORT" \
    | grep -E 'Zxid:|Mode:|Node count:|Outstanding:'
done
```

预期是一台 leader、一台 follower、`Outstanding: 0`，以及相同或快速趋同的 `Zxid` 和 `Node count`。在已白名单 `ruok` 的情况下，`imok` 只能说明进程运行且已绑定 client port，不能证明已加入 quorum。若 `srvr` 不可用，应改为本机执行 `bin/zkServer.sh status`，不要在恢复中修改白名单。

## 保留损坏数据并重同步一个节点

从生效配置读取路径，不能根据日志猜测：

```bash
grep -nE '^[[:space:]]*(dataDir|dataLogDir|server\.)[[:space:]]*=' conf/zoo.cfg
cat "$DATA_DIR/myid"
```

停止 ZooKeeper 后，再确认进程和端口已消失：

```bash
bin/zkServer.sh stop
ps -ef | grep '[Q]uorumPeerMain'
ss -lntp | grep ":$ZK_CLIENT_PORT"
```

移动而不是删除损坏的 `version-2`，保持 `myid` 完全不变：

```bash
backup_dir="$DATA_DIR/version-2.corrupt.$(date +%Y%m%d-%H%M%S)"
test ! -e "$backup_dir" || { echo "Backup target exists: $backup_dir"; exit 1; }
mv "$DATA_DIR/version-2" "$backup_dir"
ls -ld "$DATA_DIR"/version-2* "$DATA_DIR/myid"
cat "$DATA_DIR/myid"
```

如果 `dataLogDir` 是独立目录，也要单独移动其 `version-2`；如果与 `dataDir` 相同，只移动一次。不要手动创建新的 `version-2`。

```bash
bin/zkServer.sh start
```

启动后检查控制台输出或已配置的 ZooKeeper 日志。成功恢复通常会显示发现 leader，并执行 DIFF、SNAP、TRUNC 或 snapshot 同步；最终成为 follower，且不再出现原先的 EOF 错误。Apache 文档说明日志默认输出到控制台，并可由日志配置写入文件，因此不应假设某个特定发行包的日志路径。

## 验收与下游服务验证

先验证本机和整个 ensemble：

```bash
bin/zkServer.sh status
echo ruok | nc -w 5 "$FAILED_HOST" "$ZK_CLIENT_PORT"

for host in $HEALTHY_HOSTS "$FAILED_HOST"; do
  echo "===== $host ====="
  echo srvr | nc -w 10 "$host" "$ZK_CLIENT_PORT" \
    | grep -E 'Zxid:|Mode:|Node count:|Outstanding:'
done
```

验收标准：一台 leader、两台 follower、`Outstanding: 0`、相同的 `Node count`，以及相同或快速趋同的 `Zxid`。

ZooKeeper 恢复不等于它是应用故障的唯一根因。对已获授权的下游服务原始请求进行连续验证，只保留脱敏后的状态码和耗时：

```bash
for i in $(seq 1 20); do
  curl -sS --connect-timeout 3 --max-time 20 \
    -o "/tmp/dependent-service-${i}.out" \
    -w 'http=%{http_code} total=%{time_total}s\n' \
    '<dependent-service-url>'
  sleep 2
done
```

如果仍有失败，应先检查应用日志和下游依赖，再决定是否重启服务。

## 禁止操作与后续工作

- 未确认健康 quorum 和实际数据目录前，不要重建节点。
- 不要同时清空两个或多个节点的 `version-2`。
- 不要删除损坏数据、覆盖 `myid`，或复制其他节点的 `myid`。
- 不要用 `chmod 777` 等宽泛权限变更作为恢复手段。
- 节点重新加入后，不要立即删除备份。

根据 [Apache ZooKeeper Administrator's Guide](https://zookeeper.apache.org/doc/r3.7.0/zookeeperAdmin.html)，`dataDir` 保存 snapshot；若未配置 `dataLogDir`，它也保存 transaction log；`myid` 用于标识服务器。恢复后只记录脱敏证据：错误特征、quorum 检查、备份位置类别而非真实路径、恢复时间和下游服务验证结果。补充磁盘与 inode 告警，复核 snapshot/log 保留策略；版本升级应作为独立、受控的变更处理。
