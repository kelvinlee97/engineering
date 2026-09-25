---
type: Pattern
title: Incident closure criteria
description: Close an incident only when written acceptance evidence shows each affected layer is healthy, and the record separates evidence, actions, and hypotheses.
tags: [operations, incident]
sources:
  - id: k8s-ip-eni-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Kubernetes/runbooks/insufficient-ip-or-eni/README.md
    title: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: express-bff-incidents-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/runbooks/common-express-bff-incidents/README.md
    title: "Node.js / Express BFF: Ten Common Incidents Runbook"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: zookeeper-disk-full-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/runbooks/disk-full-transaction-log-recovery/README.md
    title: ZooKeeper Disk-Full Recovery Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: zookeeper-quorum-loss-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/runbooks/quorum-loss-snapshot-restore/README.md
    title: ZooKeeper Quorum-Loss Snapshot Restore Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:00:00Z }
status: draft
---
An incident is closed against explicit acceptance evidence, not because the alert stopped. Both incident runbooks in this wiki end with such a list.

## What the lists have in common

- **Every affected layer is shown healthy.** For Kubernetes: nodes `Ready`, a usable same-zone subnet, ENI/IP capacity no longer exhausted, a new Pod that schedules and gets an IP, DaemonSets at `DESIRED = CURRENT = READY`, and no new `InsufficientIPOrENI` events during the observation period.[^k8s-ip-eni-runbook] For the BFF: stable PM2 workers, private health, the gateway route, and a representative authorized flow.[^express-bff-incidents-runbook]
- **Recovery of a dependency is not proof it was the only cause.** After rebuilding a ZooKeeper member, the runbook repeats the original dependent-service request rather than assuming the application is fixed.[^zookeeper-disk-full-runbook] After a quorum-loss restore, closure also needs matching `last_zxid` values on every member and application owners' approval of their ACL and dependency checks.[^zookeeper-quorum-loss-runbook]
- **An agreed observation period.** Health must hold over time, not at one moment.[^k8s-ip-eni-runbook][^express-bff-incidents-runbook]
- **The record separates facts from guesses.** Observed evidence, completed actions, and pending validation are kept apart; the first failing layer and the mitigation are recorded separately from hypotheses.[^k8s-ip-eni-runbook][^express-bff-incidents-runbook]
- **Sanitized records.** Environment identifiers, raw logs, and screenshots stay in the authorized incident system; follow-ups get an owner.[^k8s-ip-eni-runbook][^express-bff-incidents-runbook]

## Related

- Source: [ZooKeeper quorum-loss snapshot restore runbook](../../sources/zookeeper-quorum-loss-runbook.md)
- Source: [ZooKeeper disk-full recovery runbook](../../sources/zookeeper-disk-full-runbook.md)
- [Layered troubleshooting](layered-troubleshooting.md)
- Source: [Kubernetes IP or ENI exhaustion runbook](../../sources/k8s-ip-eni-runbook.md)
- Source: [Express BFF incidents runbook](../../sources/express-bff-incidents-runbook.md)

[^k8s-ip-eni-runbook]: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
[^express-bff-incidents-runbook]: Node.js / Express BFF: Ten Common Incidents Runbook
[^zookeeper-disk-full-runbook]: ZooKeeper Disk-Full Recovery Runbook
[^zookeeper-quorum-loss-runbook]: ZooKeeper Quorum-Loss Snapshot Restore Runbook
