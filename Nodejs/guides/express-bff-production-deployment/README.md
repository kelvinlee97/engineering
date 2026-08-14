# Node.js / Express BFF Production Deployment for Beginners

Chinese version: [README_ZH.md](README_ZH.md)

This guide deploys a generic Express BFF on a Linux VM. PM2 runs multiple Node.js workers as an unprivileged account; an optional, separately operated Nginx or OpenResty gateway proxies public traffic. Replace every `<placeholder>` through approved change control. It is a repeatable baseline, not evidence that any production service uses these paths, ports, or worker counts.

## Contents

- [Mental model and boundaries](#mental-model-and-boundaries)
- [Prepare the release host](#prepare-the-release-host)
- [Create an application that can be operated](#create-an-application-that-can-be-operated)
- [Deploy and supervise with PM2](#deploy-and-supervise-with-pm2)
- [Release, verify, and roll back](#release-verify-and-roll-back)
- [Gateway integration and daily operations](#gateway-integration-and-daily-operations)
- [Acceptance checklist](#acceptance-checklist)

## Mental model and boundaries

```text
Browser -> external Nginx/OpenResty -> Express BFF (PM2 cluster)
                                      -> approved downstream HTTP service
```

Node.js runs JavaScript outside the browser. Express is a web framework. A BFF is a backend used by a browser-facing application: it can enforce session/authorization rules, adapt requests, and call downstream services. It is not OpenResty, Nginx, or the downstream API.

PM2 cluster workers share one private listener. Cluster mode needs stateless workers: do not keep sessions, uploads, or authoritative data in a worker's local memory. Use an approved shared service for such state. A gateway may be on another host; do not infer co-location from this guide.

## Prepare the release host

Use a supported Node.js LTS **exact patch version** selected and recorded in the release change. Production must not use an EOL or Current-only line. Install Node through the organization's approved package source; verify the actual binaries after installation.

```bash
node --version
npm --version
command -v node
command -v npm
```

Create a dedicated service account and release layout. The account may read its application and restricted environment file, but must not have root access.

```bash
sudo groupadd --system <app-group>
sudo useradd --system --gid <app-group> --home-dir /srv/<app-name> --create-home \
  --shell /bin/bash <app-user>
sudo install -d -o <app-user> -g <app-group> -m 0750 \
  /srv/<app-name>/releases /srv/<app-name>/shared /srv/<app-name>/shared/logs \
  /etc/<app-name>
sudo install -o root -g <app-group> -m 0640 /dev/null /etc/<app-name>/production.env
```

The system account password remains locked; do not authorize direct SSH login. Put secret values only in the approved secret-delivery mechanism or `/etc/<app-name>/production.env`; never commit them. The file is a `KEY=value` environment file, not JavaScript. Record only its owner, permissions, and required key names in a change ticket.

## Create an application that can be operated

Developers normally provide a tested release artifact with `package.json` and `package-lock.json`. `npm ci` requires both files to agree and does not rewrite them, so it is the deployment install command. Do not run `npm install` on the server to “fix” a release.

The minimal application contract is a private `GET /healthz` endpoint and graceful exit. This teaching example has no authentication or business routes; real BFF authorization belongs to application code and review.

```js
// app.js
const express = require('express');
const app = express();
app.get('/healthz', (_req, res) => res.status(200).type('text').send('ok\n'));
const server = app.listen(process.env.PORT, '127.0.0.1');

function stop(signal) {
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), Number(process.env.SHUTDOWN_TIMEOUT_MS || 30000));
}
process.on('SIGINT', () => stop('SIGINT'));
process.on('SIGTERM', () => stop('SIGTERM'));
```

Use one ecosystem file per application release configuration. Values below are safe examples, not capacity recommendations. Choose `instances`, memory limit, and timeouts from approved load tests and host capacity.

```js
// ecosystem.config.cjs
module.exports = {
  apps: [{
    name: '<app-name>',
    script: './app.js',
    cwd: '/srv/<app-name>/current',
    instances: 2,
    exec_mode: 'cluster',
    env: { NODE_ENV: 'production', PORT: '3000' },
    node_args: '--env-file=/etc/<app-name>/production.env',
    min_uptime: '10s',
    max_restarts: 5,
    restart_delay: 5000,
    listen_timeout: 10000,
    kill_timeout: 30000,
    max_memory_restart: '512M',
    watch: false,
    time: true,
    out_file: '/srv/<app-name>/shared/logs/out.log',
    error_file: '/srv/<app-name>/shared/logs/error.log',
    merge_logs: true
  }]
};
```

`NODE_ENV=production` prevents development-style Express error responses. PM2 sends `SIGINT` first during its normal reload/stop flow, so the application must close listeners and approved dependencies before `kill_timeout`. Do not use PM2 `watch` on a production release directory.

## Deploy and supervise with PM2

Obtain the artifact through the approved pipeline, verify its release identifier/checksum as required, and create a new immutable release directory. Do not overwrite `current` before the new release has passed its local checks.

```bash
sudo -u <app-user> install -d -m 0750 /srv/<app-name>/releases/<release-id>
sudo -u <app-user> tar -xzf <approved-artifact>.tar.gz -C /srv/<app-name>/releases/<release-id>
sudo -u <app-user> sh -c 'cd /srv/<app-name>/releases/<release-id> && npm ci --omit=dev'
sudo -u <app-user> sh -c 'cd /srv/<app-name>/releases/<release-id> && npm run test --if-present'
sudo -u <app-user> sh -c 'cd /srv/<app-name>/releases/<release-id> && node --check app.js'
```

Review the approved artifact's actual start file before replacing `app.js`. Do not assume that `package.json` `main` is its production entry point.

Install the approved PM2 version for `<app-user>`, then create its OS startup integration once. Run `pm2 startup` as the service account and execute only the specific privileged command PM2 prints; finally save the known process list. Repeat startup setup when the Node binary location changes.

```bash
sudo -iu <app-user> npm install --global pm2@<approved-pm2-version>
sudo -iu <app-user> pm2 startup
# Run the exact sudo command printed by the preceding command after review.
sudo -iu <app-user> pm2 save
```

## Release, verify, and roll back

Take a read-only baseline first:

```bash
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 describe <app-name>
readlink -f /srv/<app-name>/current
curl --fail http://127.0.0.1:3000/healthz
```

After local artifact checks pass, atomically move `current` to the new release, then start or reload the ecosystem. `reload` is for cluster-mode applications; PM2 can fall back to a restart when workers never become ready, so watch status, logs, and real requests.

```bash
sudo -u <app-user> ln -sfn /srv/<app-name>/releases/<release-id> /srv/<app-name>/current
# First deployment only:
sudo -iu <app-user> pm2 start /srv/<app-name>/current/ecosystem.config.cjs --only <app-name>
# Existing cluster application:
sudo -iu <app-user> pm2 reload /srv/<app-name>/current/ecosystem.config.cjs --only <app-name>
sudo -iu <app-user> pm2 save
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 logs <app-name> --lines 100 --nostream
curl --fail http://127.0.0.1:3000/healthz
```

Only after the private health check, gateway request, representative approved user flow, error rate, and release identity meet the change criteria may the release continue. If they fail, stop expansion, preserve logs, repoint `current` to `<known-good-release-id>`, reload, and repeat the same validation. Never delete the known-good release during the observation window.

## Gateway integration and daily operations

The BFF listens on `127.0.0.1:3000` only in this single-host example. In an external-gateway architecture, replace it with the approved private interface and network policy; never expose an unauthenticated development listener directly to the Internet.

Use the existing [Nginx guide](../../../Nginx/guides/nginx-production-deployment/README.md) or [OpenResty guide](../../../Nginx/guides/openresty-production-deployment/README.md) to configure the gateway. The gateway's upstream must match the BFF listener. Preserve `Host`, `X-Forwarded-For`, and `X-Forwarded-Proto`; trust these headers only when traffic is constrained to an approved gateway.

Daily read-only checks:

```bash
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 logs <app-name> --lines 100 --nostream
curl --fail http://127.0.0.1:3000/healthz
df -h /srv/<app-name> /var/log
df -i /srv/<app-name> /var/log
free -h
```

Monitor request success/latency, gateway `5xx`, BFF `5xx`, worker restarts, memory, CPU, event-loop delay if the application exposes it, downstream failures, disk/inodes, log growth, and release version. Do not set SLO or memory thresholds from this document; use service ownership and measured behavior.

## Acceptance checklist

- [ ] Node is a supported LTS exact patch version; PM2 is an approved version owned by `<app-user>`.
- [ ] Release uses `npm ci`, a committed lockfile, non-root ownership, and a restricted environment file.
- [ ] PM2 cluster workers are stateless, `watch` is disabled, and startup recovery has been tested after a controlled reboot.
- [ ] Private `/healthz`, approved gateway path, representative flow, logs, errors, and deployed release identity were validated.
- [ ] A known-good release and an approved rollback owner remain available.
- [ ] No credentials, real internal addresses, client data, or full process arguments were published.

## Official references

- [Node.js supported releases](https://nodejs.org/en/about/previous-releases)
- [Node.js environment files](https://nodejs.org/api/cli.html)
- [Node.js signals](https://nodejs.org/api/process.html)
- [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/)
- [PM2 cluster mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/)
- [PM2 ecosystem file](https://pm2.keymetrics.io/docs/usage/application-declaration/)
- [PM2 startup](https://pm2.keymetrics.io/docs/usage/startup/)
- [Express production reliability](https://expressjs.com/en/advanced/best-practice-performance/)
