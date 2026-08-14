# Modern BFF Architecture Assessment for Beginners

Chinese version: [README_ZH.md](README_ZH.md)

This guide helps an operator assess a common web path without assuming facts about a particular production environment:

```text
Browser -> edge gateway -> Node.js BFF -> OpenResty/Lua or downstream services
```

The pattern is **not obsolete**. A BFF still provides browser-specific authorization, request adaptation, and aggregation. Nginx/OpenResty remains useful at the edge for TLS, routing, rate limiting, and carefully bounded Lua extensions. What can become outdated is the operating model: manually managed hosts, mutable releases, process-local state, shared long-lived credentials, and no usable evidence during an incident.

## Start with evidence, not a migration

Do not infer topology from one host or one process list. Before selecting a platform, record the owner-approved answers below. An unknown is a discovery item, not evidence that a capability is missing.

| Area | Evidence to collect | Why it changes the decision |
| --- | --- | --- |
| Request path | DNS/LB/gateway owner, routes, timeouts, authentication boundary | Prevents moving the wrong layer or bypassing a control. |
| Runtime | Node version, PM2/systemd setup, worker count, shutdown behavior, resource use | Shows whether the BFF is safely stateless and restartable. |
| Delivery | Artifact source, lockfile, image/signature policy, rollback time and success record | Determines whether release risk, rather than hosting, is the urgent issue. |
| Reliability | Traffic, latency, errors, dependency failures, RTO/RPO, incident history | Establishes whether scale and availability needs justify a platform change. |
| Security | Identity, secret delivery, network policy, audit trail, dependency ownership | Finds long-lived credentials and unowned exposure first. |

Capture measurements over a representative period, including normal load and a release. Never copy real hostnames, ports, tokens, customer data, or internal routes into a public document.

## What to keep and what to improve

| Component or practice | Assessment | Modern direction |
| --- | --- | --- |
| Node.js BFF | Still valid when it has a clear browser-facing contract. | Make workers stateless; define ownership, timeouts, error mapping, and an API compatibility policy. |
| PM2 cluster on a VM | Valid for a small, stable service with a capable host owner. | Retain only with non-root execution, immutable releases, graceful termination, automated rollback, and measured capacity. |
| OpenResty/Lua | Still valid for gateway policy and request processing close to the edge. | Keep Lua modules small, tested, observable, and versioned; do not use it as an unbounded replacement for application services. |
| Manual SSH release | Operationally weak, not a platform. | Build once in CI, promote the same immutable artifact, and record a tested rollback. |
| Static credentials in files | High-risk operational debt. | Prefer a platform or workload identity and short-lived credentials; keep secrets separate from source and images. |
| Logs without correlation | Insufficient for multi-hop diagnosis. | Emit structured logs, metrics, and traces with one request correlation ID. |

PM2 cluster mode can remain a reasonable intermediate step, but its graceful reload depends on the application reacting correctly to termination signals. It is not a substitute for an availability design or a deployment control plane. See the [PM2 cluster documentation](https://pm2.keymetrics.io/docs/usage/cluster-mode/).

## Choose the smallest platform that satisfies the evidence

| Option | Choose it when | Do not choose it merely because |
| --- | --- | --- |
| VM + systemd/PM2 | One or few stable services, predictable traffic, a clear host owner, and automated releases/rollback are already feasible. | Containers or Kubernetes are fashionable. |
| Managed container service | The BFF is stateless, needs repeatable images, simple autoscaling, and the team does not need to operate Kubernetes primitives. | It is assumed to provide application SLOs, API security, or dependency resilience automatically. |
| Kubernetes | Multiple independently released services/teams/environments need standard workload policy, routing, and scaling, and there is a staffed platform ownership model. | There are only a few services or no one can operate cluster upgrades, networking, and incidents. |

For Kubernetes, Gateway API provides a role-oriented model for infrastructure, gateway, and route owners. It is a useful target where those roles and controls are real; it is not a requirement for a single BFF. See the [Kubernetes Gateway API documentation](https://kubernetes.io/docs/concepts/services-networking/gateway/).

## Reference architecture: a modern, incremental target

This is a target model, **not a claim about an existing system**.

```text
Internet
  -> CDN/WAF and managed load balancer
  -> gateway policy (Gateway API or managed equivalent)
  -> stateless Node.js BFF replicas
  -> OpenResty/Lua gateway functions and approved downstream services
  -> managed data and identity services

Every hop -> correlated logs, metrics, traces, and release metadata
CI -> tested immutable artifact -> progressive release -> monitored rollback
```

- Keep the BFF browser-focused. It authenticates and adapts client requests; it must not become a hidden catch-all for unrelated domain logic.
- Move only independently deployable, stateless BFF workloads to containers first. Stateful services require a separate data, backup, and recovery design.
- Retain OpenResty where it provides a proven gateway function. Migrate or rewrite Lua only when tests, ownership, release safety, or scale evidence demands it.
- Use readiness to decide when a replica may receive traffic, startup probes for slow initialization, and liveness only for a fault that a restart can fix. Incorrect liveness probes can create restart loops. See [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes).
- Give each workload an identity and obtain short-lived credentials through the approved platform. SPIFFE is one interoperable workload-identity standard; adoption is optional and must fit the organization's identity system. See the [SPIFFE overview](https://spiffe.io/docs/latest/spiffe-about/overview/).
- Instrument BFFs with OpenTelemetry-compatible traces and metrics; JavaScript traces and metrics are stable, while log support should be checked against the current project status. See [OpenTelemetry JavaScript](https://opentelemetry.io/docs/languages/js/).

## Minimum operating contract before any move

The following contract should exist on the current platform before it is moved. It makes a future move safer and also improves a VM deployment today.

| Contract | Minimum behavior |
| --- | --- |
| Health | Separate liveness from readiness. Readiness becomes unhealthy before a terminating instance receives new work. |
| Shutdown | On `SIGTERM`/`SIGINT`, stop accepting new requests, allow bounded in-flight work, close approved clients, then exit non-zero if the deadline is exceeded. |
| State | No session, upload, job, or authoritative business state is held only in worker memory. |
| Dependencies | Explicit connect/read/write timeouts; retries only for safe, bounded, idempotent operations; dependency failures are visible. |
| Observability | A correlation ID crosses gateway, BFF, and downstream calls; logs are structured and redacted; RED metrics and release version are queryable. |
| Delivery | One immutable artifact, checked dependencies, pre-deploy verification, progressive exposure, a defined rollback owner, and a tested rollback path. |

## Decision gates for an eventual migration

Do not start a platform migration until the service owner can answer the previous sections and all gates below pass.

1. A representative request path and dependency map are approved.
2. The BFF passes a controlled restart without user-visible data loss or unsafe duplicate side effects.
3. A release can be traced from source revision to artifact to running version and rolled back within the agreed recovery objective.
4. Baseline error rate, latency, resource use, and dependency behavior exist; success thresholds for the new platform are written before a canary.
5. Network, identity, secret rotation, logging retention, on-call ownership, and incident escalation are approved for the target platform.

If these gates are not met, improve the current platform first. That is a modernization outcome, not a failure to adopt Kubernetes.

## Related guides

- [Node.js / Express BFF production deployment](../express-bff-production-deployment/README.md)
- [Nginx and OpenResty operations](../../../Nginx/README.md)
- [Kubernetes operations](../../../Kubernetes/README.md)
