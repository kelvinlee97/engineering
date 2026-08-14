# Node.js / Express BFF: Ten Common Incidents Runbook

Chinese version: [README_ZH.md](README_ZH.md)

Use this generic runbook for an Express BFF supervised by PM2 cluster mode. Replace placeholders only in an authorized environment. Preserve evidence before changing processes, releases, routes, credentials, or downstream targets. A restart can restore service temporarily; it does not prove the root cause.

## Contents

- [Safety boundary and first evidence](#safety-boundary-and-first-evidence)
- [Decision flow](#decision-flow)
- [Ten incidents](#ten-incidents)
- [Recovery acceptance](#recovery-acceptance)

## Safety boundary and first evidence

Record impact, affected paths/users, first failure time, environment, release ID, recent changes, current `current` target, and owner. Do not record tokens, request bodies containing personal data, full environment files, private URLs, or full process arguments.

Start with read-only evidence:

```bash
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 describe <app-name>
sudo -iu <app-user> pm2 logs <app-name> --lines 200 --nostream
readlink -f /srv/<app-name>/current
curl --fail --max-time 5 http://127.0.0.1:<private-port>/healthz
sudo ss -lntp '( sport = :<private-port> )'
df -h /srv/<app-name> /var/log; df -i /srv/<app-name> /var/log; free -h
```

Never start by running `pm2 restart`, `pm2 reload`, `pm2 delete`, `pm2 flush`, changing a downstream URL, or deleting a release. First locate the first failing layer.

## Decision flow

```text
User request fails
  |
  +-- Reached the gateway? ---- no --> DNS/LB/TLS/gateway owner
  |
  +-- Gateway can reach BFF /healthz? -- no --> PM2, port, release, host
  |
  +-- BFF accepts request? ---- no --> route, auth, configuration, app logs
  |
  +-- BFF reaches downstream? -- no --> DNS/network/downstream owner
  |
  +-- Resources healthy? ------ no --> capacity/retention/approved mitigation
  |
  +-- Recent release? --------- yes -> compare and use approved rollback
```

## Ten incidents

### 1. Request does not reach the BFF

Check gateway access/error logs, DNS/LB/TLS health, the gateway upstream address, and BFF `healthz`. If gateway and BFF are separate hosts, test only from an approved diagnostic location. A missing request in BFF logs means the fault is at or before the gateway, not automatically Node.js.

**Recover:** use the gateway/DNS/LB owner's approved path; do not restart BFF to repair an external route. **Verify:** an approved request reaches BFF and gateway/BFF status codes return to normal.

### 2. PM2 daemon or boot restoration is missing

Check `pm2 status`, `pm2 ping`, the service-account home directory, and the OS startup unit created by the approved `pm2 startup` procedure. Confirm Node binary paths after any Node upgrade; PM2 startup integration can point to an obsolete runtime.

**Recover:** rebuild startup integration only through the reviewed PM2 output command, then `pm2 save`. **Verify:** in a controlled reboot/window, PM2 and the saved application return, then pass `healthz`.

### 3. Process crashes or restart loop

Use `pm2 describe` for restart count and exit data, then correlate `pm2 logs` with the release ID and host journal. Check uncaught exceptions, missing modules, invalid configuration, and dependency errors before any restart.

**Recover:** roll back a release that fails agreed checks; otherwise escalate the error signature to the application/dependency owner. **Verify:** restart count stabilizes, all intended workers are online, and a representative request succeeds.

### 4. Port conflict, wrong bind address, or failed health check

Compare the ecosystem `PORT`/bind address with `ss -lntp`, `curl` loopback health, and gateway upstream. `EADDRINUSE` means another process owns the port; an external bind may be a security defect even if health passes.

**Recover:** stop or reconfigure only the confirmed conflicting process under approval; restore the approved private listener. **Verify:** one intended listener, private health success, and no public direct access.

### 5. Node version, artifact, lockfile, or dependency mismatch

Record `node --version`, `npm --version`, release ID, `package.json`/lockfile presence, and `npm ci` output from the failed release. Do not run `npm install`, edit lockfiles, or install random packages on the host.

**Recover:** deploy the tested artifact with the approved Node LTS patch and `npm ci`; otherwise return `current` to the known-good release. **Verify:** expected version, dependency install, application syntax/start, and health all pass.

### 6. Environment variable, secret delivery, or permission failure

Check key names, environment-file owner/mode, service-account read access, and redacted application errors. Do not print secret values or copy the environment file to tickets. Node's `--env-file` fails when its expected file is missing.

**Recover:** correct only the approved secret reference, key name, or file permission; rotate credentials when exposure is suspected. **Verify:** application starts, approved dependency authentication works, and no value appears in logs.

### 7. Gateway `502` or `504`

Check whether BFF loopback `healthz` works, whether the gateway can reach the correct private listener, gateway error logs, BFF logs, and upstream latency. `502` commonly signals connection/upstream response failure; `504` requires evidence of where time was spent.

**Recover:** fix the first failed layer: gateway route, BFF process/listener, or downstream dependency. Do not simply increase all timeouts. **Verify:** gateway health plus one approved end-to-end request and error-rate recovery.

### 8. Downstream DNS, connection, timeout, HTTP, or response-adaptation failure

Distinguish BFF request receipt, downstream DNS resolution, TCP/TLS connection, downstream HTTP status, and BFF response parsing. Preserve a redacted correlation ID/time if the system has one. A downstream `4xx/5xx` is not proof that BFF is broken.

**Recover:** use the downstream owner's approved remediation or roll back the BFF release when request adaptation introduced the fault. **Verify:** dependency health, BFF route, and browser-visible result separately.

### 9. Memory growth or OOM

Check PM2 memory/restart history, host memory, kernel OOM evidence, traffic/release correlation, and disk capacity before capturing diagnostics. A PM2 memory restart is mitigation, not memory-leak diagnosis.

For a controlled diagnostic release, Node can write reports on fatal errors, uncaught exceptions, or an approved signal. Keep reports in a restricted directory and use `--report-exclude-env`; reports can contain runtime-sensitive information. Heap snapshots consume memory and disk, so enable them only with capacity approval.

**Recover:** remove unhealthy capacity from traffic or roll back under approval; do not raise heap limits blindly. **Verify:** memory stabilizes during the agreed observation period and capacity remains healthy.

### 10. CPU/event-loop delay, disk/inode, or log pressure

Check CPU/load, per-worker utilization, event-loop metrics when available, `df -h`, `df -i`, log growth, and recent traffic/release changes. Separate CPU saturation from I/O wait and disk/inode exhaustion.

**Recover:** use approved capacity, rate limiting, release rollback, or retention/rotation policy. Do not delete active logs or data without confirming the target and retention requirement. **Verify:** resource headroom, logging, health, latency, and error rate remain stable.

## Recovery acceptance

Close an incident only when applicable evidence shows:

- [ ] The first failing layer and completed mitigation are documented separately from hypotheses.
- [ ] PM2 has the intended stable worker state; no unexplained restart loop remains.
- [ ] Private BFF health, gateway route, and representative authorized flow pass.
- [ ] Dependency health, errors, latency, capacity, and release identity meet the agreed observation criteria.
- [ ] Any rollback, secret exposure, monitoring gap, or follow-up has an owner; redacted evidence is stored in the authorized incident system.

## Official references

- [Node.js diagnostic reports](https://nodejs.org/api/report.html)
- [Node.js process signals](https://nodejs.org/api/process.html)
- [PM2 process management](https://pm2.keymetrics.io/docs/usage/process-management/)
- [PM2 restart strategy](https://pm2.keymetrics.io/docs/usage/restart-strategies/)
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
