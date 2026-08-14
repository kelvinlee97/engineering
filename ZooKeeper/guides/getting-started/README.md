# ZooKeeper Beginner Tutorial

Chinese version: [README_ZH.md](README_ZH.md)

ZooKeeper is a distributed coordination service. Applications use it to keep a small amount of shared coordination state: for example, electing one leader, recording which workers are available, or notifying clients that a setting changed.

It is not a general database, message queue, object store, or a place for large files and secrets.

## When to use it

Use ZooKeeper when several application instances must agree on a small piece of state.

- Leader election: one active scheduler, controller, or worker.
- Service coordination: workers register with ephemeral znodes, which ZooKeeper deletes when their session ends.
- Configuration notification: clients are notified when a small setting changes.

Do not use it for application records, event streams, large payloads, or credentials. Use a database, a message system, object storage, or a secret manager for those jobs.

## Five terms to know

| Term | Meaning |
| --- | --- |
| Ensemble | ZooKeeper servers working together as one service. |
| Quorum | A majority of ensemble members. A three-member ensemble needs two members to agree. |
| znode | A small node in ZooKeeper's tree, similar to a path such as `/apps/api`. |
| Session | A client's live connection to ZooKeeper. |
| Watch | A one-time notification that tells a client a znode changed. The client registers another watch if it still needs updates. |

In an ensemble, one server is the leader and the others keep copies of the same coordination data. Clients may connect to any available member. For a first local experiment, one server is enough; it does not provide high availability.

## Try the CLI locally

This example assumes a local standalone server is already configured: `conf/zoo.cfg` exists, its `dataDir` exists, and it uses `clientPort=2181`. It deliberately does not describe installation or production configuration. From the extracted ZooKeeper directory, start the local server and connect with the bundled client:

```bash
bin/zkServer.sh start
bin/zkCli.sh -server 127.0.0.1:2181
```

At the `zk:` prompt, create a temporary znode, read it, list its parent, change it, and remove it:

```text
create /demo "hello"
get /demo
ls /
set /demo "hello again"
get /demo
delete /demo
quit
```

`create` makes a znode, `get` reads its value, `ls` lists child znodes, `set` changes a value, and `delete` removes an empty znode. If `/demo` already exists, either delete it first or choose another temporary path.

Stop the local server when finished:

```bash
bin/zkServer.sh stop
```

## What to learn next

Applications normally use a ZooKeeper client library rather than manually issuing CLI commands. Before using it in an application, learn how sessions, ephemeral znodes, sequential znodes, watches, and ACLs affect that client's design.

For production, use a separately reviewed deployment design. It must cover ensemble size, network access, authentication and ACLs, data durability, monitoring, backup, and recovery; this beginner tutorial does not prescribe those choices.

- [Apache ZooKeeper documentation](https://zookeeper.apache.org/doc/current/)
- [Apache ZooKeeper Getting Started Guide](https://zookeeper.apache.org/doc/current/zookeeperStarted.html)
- [Apache ZooKeeper Programmer's Guide](https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html)
- [Apache ZooKeeper Administrator's Guide](https://zookeeper.apache.org/doc/current/zookeeperAdmin.html)
