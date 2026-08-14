# ZooKeeper 生产部署基线

English version: [README.md](README.md)

本文是相邻事故 Runbook 的部署与验证基线，不替代特定版本的设计评审、容量测试或灾难恢复演练。

## Ensemble 与存储

- 使用部署在独立主机上的奇数成员 ensemble；三成员 ensemble 只能容忍一个成员失效。
- 每个成员保留一致的 `server.<id>=host:quorum-port:election-port` 成员列表，并保持 `myid` 唯一。
- 配置 `dataDir`；若另设 `dataLogDir`，将事务日志放在独立设备上。事故前记录两个实际配置路径。
- 通过服务管理器运行服务；配置、证书位置与 secret 均不进入本仓库。

Apache [管理员指南](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html) 说明了集群部署、多数派要求、`myid`、`dataDir` 与 `dataLogDir`。

## TLS-aware 状态检查

启用客户端 TLS 时，在每个成员上使用该成员获准的服务配置运行发行版自带状态命令：

```bash
cd <apache-zookeeper-home>
bin/zkServer.sh status
```

不得在 TLS-only 客户端端口上以明文 Four Letter Word 探针替代它。确认服务账号可读取所配置的 trust material，但不要输出证书路径、密码、私钥或连接字符串。状态检查失败是排查信号，不是削弱 TLS 或 ACL 设置的许可。

## 运维边界

- 投产前在隔离环境演练单成员重启与故障转移。
- 默认禁用或仅本地绑定 AdminServer；不得公开恢复接口。
- 使用与版本匹配的 Apache TLS 与运维文档，并在事故中只保留已脱敏证据。

## 相关 Runbook

- [Quorum-loss snapshot restore](../../runbooks/quorum-loss-snapshot-restore/README_ZH.md)
- [磁盘满事务日志恢复](../../runbooks/disk-full-transaction-log-recovery/README_ZH.md)
