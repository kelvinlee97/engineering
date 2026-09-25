---
type: Source Summary
title: Kubernetes IP or ENI exhaustion runbook (summary)
description: Summary of the legacy runbook for Pods stuck Pending on ENI or IP capacity in an ENI-based Kubernetes network.
tags: [kubernetes, runbook]
sources:
  - id: k8s-ip-eni-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Kubernetes/runbooks/insufficient-ip-or-eni/README.md
    title: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A runbook in this repository, `Kubernetes/runbooks/insufficient-ip-or-eni/README.md`, for Pods that stay `Pending` with ENI or IP scheduling events. It uses Tencent Kubernetes Engine (TKE) VPC-CNI as its worked example, with every environment value as a placeholder.[^k8s-ip-eni-runbook]

## Takeaways

- A `Pending` Pod is a broken link in a chain (node health, Pod-subnet IPs, node ENI/IP allocatable, IPAM and admission components); find the link before changing anything.[^k8s-ip-eni-runbook] See [IP or ENI exhaustion runbook](../engineering/kubernetes/ip-eni-exhaustion.md).
- Remediate in dependency order and restart workloads only when needed.[^k8s-ip-eni-runbook] See [Safe change procedure](../engineering/operations/safe-change-procedure.md).
- Close the incident only against explicit acceptance criteria.[^k8s-ip-eni-runbook] See [Incident closure criteria](../engineering/operations/incident-closure-criteria.md).

[^k8s-ip-eni-runbook]: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
