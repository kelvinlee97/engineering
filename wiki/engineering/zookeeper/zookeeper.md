---
type: Service
title: ZooKeeper
description: What Apache ZooKeeper is, how its ensemble and quorum work, and how to deploy it in production.
tags:
- zookeeper
- distributed-systems
aliases:
- engineering/zookeeper/production-deployment
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
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Apache ZooKeeper is a coordination service that a cluster of servers (an ensemble) keeps consistent by majority vote. This page covers the terms and quorum arithmetic, what ZooKeeper is and is not good for, and how to deploy a three-member ensemble in production. Recovery runbooks are on [ZooKeeper recovery](zookeeper-recovery.md).

## What ZooKeeper is

Apache ZooKeeper is a distributed coordination service. Applications use it to keep a small amount of shared coordination state, such as which instance is leader, which workers are available, or that a setting changed. It is not a general database, message queue, object store, or a place for large files and secrets.[^zookeeper-getting-started]

### Terms

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

### Quorum arithmetic

One member is the leader, which orders writes; the others are followers that replicate and vote.[^zookeeper-getting-started] With three members, two form a quorum, so one member can be restarted safely but two cannot. Four members still tolerate only one failure, so a fourth member adds no failure tolerance. Members belong in independent failure domains, the transaction log needs its own device, and ZooKeeper must not swap.[^zookeeper-production-guide]

### Good and bad uses

| Use it for | Do not use it for |
| --- | --- |
| Leader election (one active scheduler, controller, or worker) | Application records |
| Service coordination with ephemeral znodes, deleted when a session ends | Event streams |
| Notifying clients that a small setting changed | Large payloads or credentials |

As listed in the tutorial. A single local server is fine for experiments but gives no high availability; applications normally use a client library rather than the CLI.[^zookeeper-getting-started]

## Production deployment

A reference build of a three-member [ZooKeeper](#what-zookeeper-is) 3.9.5 ensemble on Ubuntu 24.04 LTS. The healthy result is one leader and two followers.[^zookeeper-production-guide]

### Ports

| Port | Purpose | Exposure |
| --- | --- | --- |
| `2281` | Secure client port | Approved application CIDRs only |
| `2888` | Quorum | Members only |
| `3888` | Leader election | Members only |
| AdminServer | Disabled in the baseline | None |
| Plain client port | Disabled | None |

As specified in the guide.[^zookeeper-production-guide]

### Build steps

1. **Hosts.** Three VMs with forward DNS for the certificate names, synchronized clocks, a JDK, and firewall rules as above; `dataDir` (snapshots) and `dataLogDir` (transaction logs) on different mounted devices; no busy database or broker on the same host. Verify the Apache release's SHA-512 checksum before extracting.
2. **Configuration.** An identical `zoo.cfg` on every host except `myid`, with `secureClientPort=2281` instead of a plaintext `clientPort`, TLS hostname verification on and reverse-DNS fallback off for both client and quorum traffic, `ssl.clientAuth=need`, `autopurge.snapRetainCount=5`, `autopurge.purgeInterval=24`, and a minimal four-letter-word allowlist (`srvr,stat,ruok`). Passwords live in separate files, not in `zoo.cfg`.
3. **Initialize once.** `zkServer-initialize.sh` per host with its `--myid`, only for a brand-new ensemble; never during a repair, especially with `--force`.
4. **systemd.** Pre-start checks refuse to start without the config, `myid`, or log directory; `zookeeper.db.autocreate=false` stops a typoed path from serving an empty database. Start one member at a time; a lone member may stay `LOOKING` until quorum forms.
5. **Acceptance.** A TLS client creates a test znode with an ACL for its own x509 principal, `getAcl` shows no `world:anyone`, and a second certificate gets `NoAuth`. `zkServer.sh status` on all three shows exactly one `leader` and two `follower`.

mTLS identifies a client but does not grant znode permissions; each application root needs its own ACL, and the recovery administrator needs an approved `ALL` ACL on `/` before any incident.[^zookeeper-production-guide]

### Operating it

- Metrics through the Prometheus JMX Exporter Java agent (version 1.6.0 in the guide, checksum-verified) bound to `127.0.0.1:9404`, keeping all existing JVM safeguards in the same flags line.
- Alert on no leader or fewer than three healthy members, a non-converging follower, request backlog, slow fsync, JVM restart loops, disk or inodes at 70% (warning) and 85% (critical), and certificate expiry.
- **Rolling change:** confirm one leader and two followers, change one member, wait for it to rejoin, check all three, and only then continue; stop and roll back that member otherwise. Not for version upgrades, TLS enablement, membership or client-port changes, or CA replacement.[^zookeeper-production-guide]

## Related

- [ZooKeeper single-member recovery](zookeeper-recovery.md#recovering-a-single-member)
- [ZooKeeper quorum-loss restore](zookeeper-recovery.md#restoring-after-quorum-loss)
- [Safe change procedure](../operations/incident-operations.md#safe-change-procedure)

[^zookeeper-getting-started]: [ZooKeeper Beginner Tutorial](../../sources/zookeeper-getting-started.md), [original](https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/getting-started/README.md)
[^zookeeper-production-guide]: [ZooKeeper Production Deployment Guide for DevOps Beginners](../../sources/zookeeper-production-guide.md), [original](https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/production-deployment/README.md)
