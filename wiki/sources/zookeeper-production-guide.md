---
type: Source Summary
title: ZooKeeper production deployment guide (summary)
description: Summary of the legacy reference guide for a three-member ZooKeeper 3.9.5 ensemble on Ubuntu 24.04 with TLS, systemd, and monitoring.
tags: [zookeeper, deployment]
sources:
  - id: zookeeper-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/production-deployment/README.md
    title: ZooKeeper Production Deployment Guide for DevOps Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
A guide in this repository, `ZooKeeper/guides/production-deployment/README.md`, describing a three-member Apache ZooKeeper 3.9.5 ensemble on Ubuntu 24.04 LTS with mutual TLS, systemd, JMX metrics, and safe changes. It is a reference architecture, not evidence that a live environment was deployed or certified.[^zookeeper-production-guide]

## Takeaways

- Three members tolerate one failure; four still tolerate only one. See [ZooKeeper](../engineering/zookeeper/zookeeper.md#what-zookeeper-is).
- Change one member at a time and stop if the ensemble is not one leader plus two followers.[^zookeeper-production-guide] See [ZooKeeper production deployment](../engineering/zookeeper/zookeeper.md#production-deployment).

[^zookeeper-production-guide]: ZooKeeper Production Deployment Guide for DevOps Beginners, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/production-deployment/README.md)
