# OpenResty Production Deployment and Operations for Beginners

Chinese version: [README_ZH.md](README_ZH.md)

Deploy **OpenResty only** on one Ubuntu 24.04 LTS VM. OpenResty is an Nginx-based web platform with LuaJIT and Lua modules. This baseline provides a Lua health endpoint, reverse-proxies an application at `127.0.0.1:3000`, and uses Certbot webroot for HTTPS. Replace every `<example>` value through approved change control.

## Contents

- [Choose OpenResty deliberately](#choose-openresty-deliberately)
- [Prepare and install](#prepare-and-install)
- [Configure the site and Lua health check](#configure-the-site-and-lua-health-check)
- [Add HTTPS](#add-https)
- [Verify and operate](#verify-and-operate)
- [Troubleshoot by layer](#troubleshoot-by-layer)
- [Acceptance checklist](#acceptance-checklist)

## Choose OpenResty deliberately

```text
Client -> OpenResty :443 -> Lua /healthz
                        -> application 127.0.0.1:3000
```

Choose OpenResty only when an Nginx gateway needs reviewed Lua behavior, such as this small health endpoint. Use ordinary Nginx for basic static serving and reverse proxying. OpenResty replaces the Nginx web-server process on this host; it is not an add-on to a running Ubuntu `nginx` service. Do not run both: they compete for `80/443`.

`content_by_lua_file` runs Lua in OpenResty's event-driven request path. Do not add blocking shell commands, blocking file I/O, unbounded loops, secrets, or ad-hoc network calls without a reviewed application design.

## Prepare and install

Confirm DNS, approved ingress for TCP `80/443`, time synchronization, CPU architecture, and port ownership. Official x86_64 packages require SSE 4.2.

```bash
sudo ss -lntp '( sport = :80 or sport = :443 )'
hostname -f
timedatectl status
getent hosts <domain>
dpkg --print-architecture
```

If Ubuntu Nginx is installed, disable it only after confirming it is not serving a required site and a migration window is approved:

```bash
sudo systemctl disable --now nginx
```

Install OpenResty's official package repository. These commands are for Ubuntu 24.04 amd64; arm64 must use OpenResty's arm64 repository URL.

```bash
sudo apt-get update
sudo apt-get install --yes --no-install-recommends wget gnupg ca-certificates lsb-release curl certbot
wget -O - https://openresty.org/package/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/openresty.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/openresty.gpg] https://openresty.org/package/ubuntu $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/openresty.list >/dev/null
sudo apt-get update
sudo apt-get install --yes openresty
openresty -V
sudo install -d -o root -g root -m 0755 /etc/openresty/conf.d /etc/openresty/lua /var/www/<site>/.well-known/acme-challenge
```

The package prefix is `/usr/local/openresty/`; use `openresty`, not a bare `nginx` command that might select a different binary.

## Configure the site and Lua health check

Back up active configuration. Create `/etc/openresty/lua/health.lua`, owned by `root:root` with mode `0644`:

```bash
sudo tee /etc/openresty/lua/health.lua >/dev/null <<'EOF'
ngx.status = ngx.HTTP_OK
ngx.header.content_type = "text/plain"
ngx.say("ok")
EOF
sudo chown root:root /etc/openresty/lua/health.lua
sudo chmod 0644 /etc/openresty/lua/health.lua
```

Create `/etc/openresty/conf.d/<site>.conf`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name <domain>;
    root /var/www/<site>;
    location ^~ /.well-known/acme-challenge/ { try_files $uri =404; }
    location = /healthz { access_log off; content_by_lua_file /etc/openresty/lua/health.lua; }
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
    }
}
```

The main configuration must load the site directory inside `http {}`. Inspect before editing; only add the include when no equivalent line exists.

```bash
sudo cp -a /usr/local/openresty/nginx/conf /usr/local/openresty/nginx/conf.backup.$(date +%Y%m%d-%H%M%S)
sudo grep -n 'conf.d' /usr/local/openresty/nginx/conf/nginx.conf
# Within http {}, when needed: include /etc/openresty/conf.d/*.conf;
sudo openresty -t
sudo systemctl enable --now openresty
sudo systemctl reload openresty
```

Keep site and Lua files separate; do not make unrelated edits to vendor `nginx.conf`.

## Add HTTPS

First prove public HTTP health, then issue the certificate:

```bash
curl --fail http://<domain>/healthz
sudo certbot certonly --webroot -w /var/www/<site> -d <domain> \
  --email <operations-email> --agree-tos --no-eff-email
```

Replace the port-80 server with the redirect server plus this HTTPS server. Retain the ACME location on HTTP for renewal.

```nginx
server {
    listen 80; listen [::]:80; server_name <domain>;
    location ^~ /.well-known/acme-challenge/ { root /var/www/<site>; }
    location / { return 301 https://$host$request_uri; }
}
server {
    listen 443 ssl; listen [::]:443 ssl; server_name <domain>;
    ssl_certificate /etc/letsencrypt/live/<domain>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<domain>/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    location = /healthz { access_log off; content_by_lua_file /etc/openresty/lua/health.lua; }
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
    }
}
```

```bash
sudo openresty -t && sudo systemctl reload openresty
curl --fail --location http://<domain>/healthz
curl --fail https://<domain>/healthz
sudo certbot renew --dry-run
```

Never copy `privkey.pem` into an application directory or repository.

## Verify and operate

Check service, Lua, upstream, and TLS separately:

```bash
sudo systemctl is-active openresty
sudo openresty -T | less
curl --fail http://127.0.0.1/healthz
curl --fail http://127.0.0.1:3000/<approved-health-path>
curl --fail --resolve <domain>:443:127.0.0.1 https://<domain>/healthz
sudo journalctl -u openresty -n 100 --no-pager
```

For each change: back up the affected site or Lua file, change one concern, run `openresty -t`, use graceful `systemctl reload openresty`, test health and an approved proxy request, and inspect logs. Do not restart only to apply configuration. Monitor availability, HTTP status codes, latency, worker restarts, disk/inodes, certificate expiry, Lua errors, and upstream failures.

Use basic `stub_status` only if `openresty -V 2>&1 | grep http_stub_status_module` succeeds, and bind it to `127.0.0.1` only. It is metrics data, not a public admin endpoint.

## Troubleshoot by layer

| Symptom | First checks | Do not do |
| --- | --- | --- |
| `openresty -t` fails | Reported file/line, `sudo openresty -T`, Lua syntax/path. | Reload anyway. |
| Port bind failure | `sudo ss -lntp '( sport = :80 or sport = :443 )'`. | Start Ubuntu Nginx beside OpenResty. |
| `500` on `/healthz` | Error log, Lua path/ownership, configuration test. | Return success from a broken script. |
| `502` / `504` | Loopback upstream, application logs, error log. | Blame Lua before checking upstream. |
| ACME failure | DNS, port `80`, webroot, Certbot logs. | Expose private keys. |

## Acceptance checklist

- [ ] DNS, firewall, port ownership, architecture, and time were checked.
- [ ] `openresty -t` passes; OpenResty is enabled and active.
- [ ] Lua `/healthz` returns `200`; HTTP redirects to HTTPS.
- [ ] The upstream passes its own health check and an approved request succeeds through OpenResty.
- [ ] `certbot renew --dry-run` passes; monitoring, logs, backups, renewal, and rollback have an owner.
- [ ] No Nginx service competes for ports, and no secret, public status endpoint, or production data is exposed.

## Official references

- [OpenResty Linux packages](https://openresty.org/en/linux-packages.html)
- [OpenResty deb packages](https://openresty.org/en/deb-packages.html)
- [OpenResty Lua Nginx module](https://openresty.org/en/lua-nginx-module.html)
- [Nginx control](https://nginx.org/en/docs/control.html)
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [Certbot webroot](https://eff-certbot.readthedocs.io/en/stable/using.html)
