---
type: Service
title: ZooKeeper
description: A distributed coordination service that keeps a small, consistently replicated tree of data for leader election, membership, and configuration notification.
tags: [zookeeper, distributed-systems]
sources:
  - id: zookeeper-getting-started
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/getting-started/README.md
    title: ZooKeeper Beginner Tutorial
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: zookeeper-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/production-deployment/README.md
    title: ZooKeeper Production Deployment Guide for DevOps Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
Apache ZooKeeper is a distributed coordination service. Applications use it to keep a small amount of shared coordination state, such as which instance is leader, which workers are available, or that a setting changed.[^zookeeper-getting-started] It is not a general database, message queue, object store, or a place for large files and secrets.[^zookeeper-getting-started]

## Terms

| Term | Meaning |
| --- | --- |
| Ensemble | ZooKeeper servers working together as one service |
| Quorum | A majority of members that can communicate |
| znode | A small node in ZooKeeper's tree, shaped like a path such as `/apps/api` |
| Session | A client's live connection |
| Watch | A one-time notification that a znode changed; the client registers again if it still needs updates |
| `myid` | The number telling each server whether it is `server.1`, `server.2`, or `server.3` |
| `zxid` | A monotonically increasing change number; converging values mean members are catching up |

As defined in the tutorial and production guide.[^zookeeper-getting-started][^zookeeper-production-guide]

## Quorum arithmetic

One member is the leader, which orders writes; the others are followers that replicate and vote.[^zookeeper-getting-started] With three members, two form a quorum, so one member can be restarted safely but two cannot.[^zookeeper-production-guide] Four members still tolerate only one failure, so a fourth member adds no failure tolerance. Members belong in independent failure domains, the transaction log needs its own device, and ZooKeeper must not swap.[^zookeeper-production-guide]

## Good and bad uses

| Use it for | Do not use it for |
| --- | --- |
| Leader election (one active scheduler, controller, or worker) | Application records |
| Service coordination with ephemeral znodes, deleted when a session ends | Event streams |
| Notifying clients that a small setting changed | Large payloads or credentials |

As listed in the tutorial.[^zookeeper-getting-started] A single local server is fine for experiments but gives no high availability; applications normally use a client library rather than the CLI.[^zookeeper-getting-started]

## Related

- [ZooKeeper production deployment](production-deployment.md)
- [ZooKeeper single-member recovery](single-member-recovery.md)
- [ZooKeeper quorum-loss restore](quorum-loss-restore.md)
- Source: [ZooKeeper beginner tutorial](../../sources/zookeeper-getting-started.md)
- Source: [ZooKeeper production deployment guide](../../sources/zookeeper-production-guide.md)

[^zookeeper-getting-started]: ZooKeeper Beginner Tutorial
[^zookeeper-production-guide]: ZooKeeper Production Deployment Guide for DevOps Beginners
