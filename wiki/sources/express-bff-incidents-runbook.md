---
type: Source Summary
title: Express BFF incidents runbook (summary)
description: Summary of the legacy runbook covering ten common incidents for an Express BFF supervised by PM2 cluster mode.
tags: [nodejs, bff, runbook]
sources:
  - id: express-bff-incidents-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/runbooks/common-express-bff-incidents/README.md
    title: "Node.js / Express BFF: Ten Common Incidents Runbook"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A runbook in this repository, `Nodejs/runbooks/common-express-bff-incidents/README.md`, covering ten common incidents for an Express BFF under PM2 cluster mode. It stresses that a restart can restore service temporarily without proving the root cause.[^express-bff-incidents-runbook]

## Takeaways

- A failing request crosses a fixed chain of hops; find the first broken one before touching any control.[^express-bff-incidents-runbook] See [Layered troubleshooting](../engineering/operations/layered-troubleshooting.md).
- Each incident has checks, a recovery, and a verification step.[^express-bff-incidents-runbook] See [Express BFF incidents](../engineering/web-serving/express-bff-incidents.md).

[^express-bff-incidents-runbook]: Node.js / Express BFF: Ten Common Incidents Runbook
