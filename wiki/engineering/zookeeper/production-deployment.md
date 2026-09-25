---
type: Playbook
title: ZooKeeper production deployment
description: Build and operate a three-member ZooKeeper 3.9.5 ensemble with mutual TLS, systemd, JMX metrics, and one-member-at-a-time changes.
tags: [zookeeper, deployment, tls, runbook]
sources:
  - id: zookeeper-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/production-deployment/README.md
    title: ZooKeeper Production Deployment Guide for DevOps Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
A reference build of a three-member [ZooKeeper](zookeeper.md) 3.9.5 ensemble on Ubuntu 24.04 LTS. The healthy result is one leader and two followers.[^zookeeper-production-guide]

## Ports

| Port | Purpose | Exposure |
| --- | --- | --- |
| `2281` | Secure client port | Approved application CIDRs only |
| `2888` | Quorum | Members only |
| `3888` | Leader election | Members only |
| AdminServer | Disabled in the baseline | None |
| Plain client port | Disabled | None |

As specified in the guide.[^zookeeper-production-guide]

## Build steps

1. **Hosts.** Three VMs with forward DNS for the certificate names, synchronized clocks, a JDK, and firewall rules as above; `dataDir` (snapshots) and `dataLogDir` (transaction logs) on different mounted devices; no busy database or broker on the same host. Verify the Apache release's SHA-512 checksum before extracting.[^zookeeper-production-guide]
2. **Configuration.** An identical `zoo.cfg` on every host except `myid`, with `secureClientPort=2281` instead of a plaintext `clientPort`, TLS hostname verification on and reverse-DNS fallback off for both client and quorum traffic, `ssl.clientAuth=need`, `autopurge.snapRetainCount=5`, `autopurge.purgeInterval=24`, and a minimal four-letter-word allowlist (`srvr,stat,ruok`). Passwords live in separate files, not in `zoo.cfg`.[^zookeeper-production-guide]
3. **Initialize once.** `zkServer-initialize.sh` per host with its `--myid`, only for a brand-new ensemble; never during a repair, especially with `--force`.[^zookeeper-production-guide]
4. **systemd.** Pre-start checks refuse to start without the config, `myid`, or log directory; `zookeeper.db.autocreate=false` stops a typoed path from serving an empty database. Start one member at a time; a lone member may stay `LOOKING` until quorum forms.[^zookeeper-production-guide]
5. **Acceptance.** A TLS client creates a test znode with an ACL for its own x509 principal, `getAcl` shows no `world:anyone`, and a second certificate gets `NoAuth`. `zkServer.sh status` on all three shows exactly one `leader` and two `follower`.[^zookeeper-production-guide]

mTLS identifies a client but does not grant znode permissions; each application root needs its own ACL, and the recovery administrator needs an approved `ALL` ACL on `/` before any incident.[^zookeeper-production-guide]

## Operating it

- Metrics through the Prometheus JMX Exporter Java agent (version 1.6.0 in the guide, checksum-verified) bound to `127.0.0.1:9404`, keeping all existing JVM safeguards in the same flags line.[^zookeeper-production-guide]
- Alert on no leader or fewer than three healthy members, a non-converging follower, request backlog, slow fsync, JVM restart loops, disk or inodes at 70% (warning) and 85% (critical), and certificate expiry.[^zookeeper-production-guide]
- **Rolling change:** confirm one leader and two followers, change one member, wait for it to rejoin, check all three, and only then continue; stop and roll back that member otherwise. Not for version upgrades, TLS enablement, membership or client-port changes, or CA replacement.[^zookeeper-production-guide]

## Related

- [Safe change procedure](../operations/safe-change-procedure.md)
- [ZooKeeper single-member recovery](single-member-recovery.md)
- Source: [ZooKeeper production deployment guide](../../sources/zookeeper-production-guide.md)

[^zookeeper-production-guide]: ZooKeeper Production Deployment Guide for DevOps Beginners
