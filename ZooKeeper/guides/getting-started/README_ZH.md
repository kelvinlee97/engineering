# ZooKeeper 新手教程

English version: [README.md](README.md)

ZooKeeper 是一个分布式协调服务。应用通过它保存少量共享的协调状态，例如选出一台 leader、记录哪些 worker 可用，或在小型配置变更时通知客户端。

它不是通用数据库、消息队列、对象存储，也不应用来保存大文件或密码等敏感信息。

## 何时使用

当多个应用实例需要就一小段状态达成一致时，可以使用 ZooKeeper。

- Leader 选举：只允许一个 scheduler、controller 或 worker 处于活动状态。
- 服务协调：worker 使用 ephemeral znode 注册；session 结束时，ZooKeeper 会删除该临时节点。
- 配置通知：小型配置变更时通知客户端。

不要用它保存业务记录、事件流、大型 payload 或凭据。这些场景应使用数据库、消息系统、对象存储或密钥管理服务。

## 五个核心概念

| 术语 | 含义 |
| --- | --- |
| Ensemble | 多台 ZooKeeper server 作为一个服务协同工作。 |
| Quorum | ensemble 中的多数成员。三成员 ensemble 至少需要两台达成一致。 |
| znode | ZooKeeper 树中的小节点，类似 `/apps/api` 这样的路径。 |
| Session | 客户端与 ZooKeeper 之间的活动连接。 |
| Watch | znode 变化时的一次性通知；如仍需更新，客户端需要重新注册 watch。 |

在一个 ensemble 中，一台 server 是 leader，其他 server 保存相同协调数据的副本。客户端可连接任一可用成员。首次本地练习时，一台 server 已足够，但它不提供高可用。

## 在本地试用 CLI

本示例假设本机单机 server 已完成配置：存在 `conf/zoo.cfg`，其中的 `dataDir` 已存在，且使用 `clientPort=2181`。它刻意不讲安装或生产配置。在解压后的 ZooKeeper 目录中启动本地 server，并使用自带客户端连接：

```bash
bin/zkServer.sh start
bin/zkCli.sh -server 127.0.0.1:2181
```

在 `zk:` 提示符下，创建临时 znode、读取它、列出父节点、修改它并删除它：

```text
create /demo "hello"
get /demo
ls /
set /demo "hello again"
get /demo
delete /demo
quit
```

`create` 创建 znode，`get` 读取值，`ls` 列出子 znode，`set` 修改值，`delete` 删除空 znode。若 `/demo` 已存在，可先删除它，或换用其他临时路径。

完成后停止本地 server：

```bash
bin/zkServer.sh stop
```

## 下一步学习什么

应用通常通过 ZooKeeper client library，而不是手动输入 CLI 命令。在将它用于应用前，应了解 session、ephemeral znode、sequential znode、watch 与 ACL 如何影响 client 设计。

生产环境应使用单独评审过的部署设计，其中必须覆盖 ensemble 规模、网络访问、认证与 ACL、数据持久性、监控、备份和恢复；本新手教程不规定这些选择。

- [Apache ZooKeeper 官方文档](https://zookeeper.apache.org/doc/current/)
- [Apache ZooKeeper Getting Started Guide](https://zookeeper.apache.org/doc/current/zookeeperStarted.html)
- [Apache ZooKeeper Programmer's Guide](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html)
- [Apache ZooKeeper Administrator's Guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html)
