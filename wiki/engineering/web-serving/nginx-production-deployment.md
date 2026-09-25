---
type: Playbook
title: Nginx production deployment
description: Deploy Nginx on one Ubuntu 24.04 VM to serve static files and reverse-proxy a loopback application, with Certbot HTTPS and layer-by-layer checks.
tags: [nginx, deployment, runbook]
sources:
  - id: nginx-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nginx/guides/nginx-production-deployment/README.md
    title: Nginx Production Deployment and Operations for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A baseline for running Nginx alone on one Ubuntu 24.04 LTS VM: static files, a [reverse proxy](reverse-proxy-gateway.md) to an application on `127.0.0.1:3000`, and HTTPS through Certbot webroot.[^nginx-production-guide]

## Steps

1. **Prepare the host.** Confirm the domain resolves to the VM, the firewall allows TCP 80/443, time is correct, and no server owns either port (`ss -lntp`). Install `nginx`, `curl`, `ca-certificates`, and `certbot`.[^nginx-production-guide]
2. **Configure.** Back up `/etc/nginx`, remove the default site, create a site with an ACME challenge location, a `/healthz` location returning `200`, and a `location /` that proxies to the application with `proxy_connect_timeout 5s` and `proxy_read_timeout 60s`. For a static-only site use `try_files` instead of the proxy.[^nginx-production-guide]
3. **Enable.** Link the site, run `nginx -t`, enable the service, and reload. Always run `nginx -t` before a reload.[^nginx-production-guide]
4. **Add HTTPS.** Prove HTTP health publicly (ACME needs public DNS and port 80), issue the certificate with `certbot certonly --webroot`, then add an HTTP-to-HTTPS redirect server that keeps the challenge location, and an HTTPS server with `ssl_protocols TLSv1.2 TLSv1.3`. Confirm `certbot renew --dry-run`.[^nginx-production-guide]
5. **Verify each layer.** Service state, effective config (`nginx -T`), loopback health, the upstream's own health path, HTTPS via `curl --resolve`, and the journal. An open port is not an acceptance test.[^nginx-production-guide]

Never copy `privkey.pem` into an application directory or repository.[^nginx-production-guide]

## Troubleshooting by symptom

| Symptom | First checks | Do not |
| --- | --- | --- |
| `nginx -t` fails | Reported file and line, `nginx -T` | Reload anyway |
| Port 80/443 bind failure | `ss` port check | Run Nginx and OpenResty together |
| `502` / `504` | Loopback upstream, app logs, error log, timeouts | Raise timeouts before finding the failing layer |
| `403` | `namei -l` on the web root, ownership | `chmod -R 777` |
| `404` | Effective config, `root`, location, URI | Change many locations at once |
| `413` | Whether large uploads are really required; a reviewed `client_max_body_size` | Remove limits blindly |
| ACME failure | DNS, port 80, challenge path, Certbot logs | Share keys or disable TLS checks |

As described in the guide.[^nginx-production-guide]

## Monitoring

If `nginx -V` shows `http_stub_status_module`, expose `stub_status` on a loopback-only listener; it is not an authenticated admin API. Watch availability, status codes, latency, connections, restarts, disk and inodes, certificate expiry, and upstream errors.[^nginx-production-guide]

## Related

- [Safe change procedure](../operations/safe-change-procedure.md)
- [OpenResty production deployment](openresty-production-deployment.md)
- Source: [Nginx production deployment guide](../../sources/nginx-production-guide.md)

[^nginx-production-guide]: Nginx Production Deployment and Operations for Beginners
