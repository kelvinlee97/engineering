# Nginx Production Deployment and Operations for Beginners

Chinese version: [README_ZH.md](README_ZH.md)

Deploy **Nginx only** on one Ubuntu 24.04 LTS VM. It serves static files, reverse-proxies an application on `127.0.0.1:3000`, and obtains HTTPS certificates through Certbot webroot. Replace `<domain>`, `<site>`, `<operations-email>`, and `<approved-health-path>` through your change process. This is a deployable baseline, not evidence that any particular server has been deployed.

## Contents

- [Build and safety boundary](#build-and-safety-boundary)
- [Prepare the host](#prepare-the-host)
- [Install and configure](#install-and-configure)
- [Add HTTPS](#add-https)
- [Verify the service](#verify-the-service)
- [Operate and change safely](#operate-and-change-safely)
- [Troubleshoot by layer](#troubleshoot-by-layer)
- [Acceptance checklist](#acceptance-checklist)

## Build and safety boundary

```text
Client -> Nginx :443 -> application 127.0.0.1:3000
                    -> static files /var/www/<site>/
```

Nginx's master process reads and validates configuration; worker processes serve requests. A `server` is a virtual host, a `location` matches a request path, and `proxy_pass` forwards a request to the upstream application. Do not install or run OpenResty on this host: both products use ports `80` and `443`.

## Prepare the host

Before changing anything, confirm that `<domain>` resolves to this VM, the approved firewall allows TCP `80`/`443`, system time is correct, and no server owns either port.

```bash
sudo ss -lntp '( sport = :80 or sport = :443 )'
hostname -f
timedatectl status
getent hosts <domain>
sudo apt-get update
sudo apt-get install --yes nginx curl ca-certificates certbot
sudo install -d -o root -g root -m 0755 /var/www/<site>/.well-known/acme-challenge
sudo tee /var/www/<site>/index.html >/dev/null <<'EOF'
<!doctype html><title>It works</title><h1>Nginx is working</h1>
EOF
```

Certbot obtains and renews certificates in this guide; it does not alter Nginx configuration. Use an organization-approved certificate source instead if public ACME issuance is not permitted.

## Install and configure

Back up the active configuration. A new Ubuntu server includes a default site; disable it before enabling the site below.

```bash
sudo cp -a /etc/nginx /etc/nginx.backup.$(date +%Y%m%d-%H%M%S)
sudo rm -f /etc/nginx/sites-enabled/default
```

Create `/etc/nginx/sites-available/<site>`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name <domain>;
    root /var/www/<site>;
    index index.html;

    location ^~ /.well-known/acme-challenge/ { try_files $uri =404; }
    location = /healthz {
        access_log off;
        add_header Content-Type text/plain;
        return 200 "ok\n";
    }
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

For a static-only site, use `try_files $uri $uri/ =404;` instead of the final proxy location. Do not point at an upstream that does not exist.

```bash
sudo ln -s ../sites-available/<site> /etc/nginx/sites-enabled/<site>
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
sudo systemctl status nginx --no-pager
```

Always run `nginx -t` before reload. A successful reload validates the new configuration then gracefully replaces workers; it is safer than a routine restart.

## Add HTTPS

First prove that HTTP works publicly. The ACME challenge requires public DNS and TCP port `80`.

```bash
curl --fail http://<domain>/healthz
sudo certbot certonly --webroot -w /var/www/<site> -d <domain> \
  --email <operations-email> --agree-tos --no-eff-email
```

Replace the HTTP server with the following redirect server plus HTTPS server. Keep the challenge location on HTTP for renewal. Never copy `privkey.pem` to an application directory or repository.

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
    root /var/www/<site>;
    location = /healthz { access_log off; add_header Content-Type text/plain; return 200 "ok\n"; }
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
sudo nginx -t && sudo systemctl reload nginx
curl --fail --location http://<domain>/healthz
curl --fail https://<domain>/healthz
sudo certbot renew --dry-run
```

## Verify the service

An open port is not an application acceptance test. Prove each layer:

```bash
sudo systemctl is-active nginx
sudo nginx -T | less
curl --fail http://127.0.0.1/healthz
curl --fail http://127.0.0.1:3000/<approved-health-path>
curl --fail --resolve <domain>:443:127.0.0.1 https://<domain>/healthz
sudo journalctl -u nginx -n 100 --no-pager
```

The upstream check is not required for an intentionally static site. For a proxy, it distinguishes an application failure from a Nginx failure.

## Operate and change safely

| Need | Command | Rule |
| --- | --- | --- |
| Service state | `sudo systemctl status nginx --no-pager` | `active` does not prove routes work. |
| Recent errors | `sudo journalctl -u nginx -n 100 --no-pager` | Also review the configured error log. |
| Configuration test | `sudo nginx -t` | Required before reload. |
| Apply valid config | `sudo systemctl reload nginx` | Avoid routine restarts. |
| Capacity | `df -h; df -i; free -h` | Alert before exhaustion. |

For each change: record intent, back up the file, make one small edit, test, reload, verify `/healthz` and an approved application request, then inspect logs. If testing fails, restore the backup and test it before reloading.

For basic connection metrics, first confirm `nginx -V 2>&1 | grep http_stub_status_module`. Then bind status to loopback only:

```nginx
server {
    listen 127.0.0.1:8080;
    location = /basic_status { stub_status; access_log off; }
}
```

Verify with `curl --fail http://127.0.0.1:8080/basic_status`. Monitor availability, status-code rate, latency, active connections, restarts, disk/inodes, certificate expiry, and upstream errors. `stub_status` is not an authenticated admin API.

## Troubleshoot by layer

| Symptom | First checks | Do not do |
| --- | --- | --- |
| `nginx -t` fails | Read its file/line and inspect `sudo nginx -T`. | Reload or restart anyway. |
| `bind() ... 80/443 failed` | `ss` port check; stop only the confirmed service through approval. | Run Nginx and OpenResty together. |
| `502` / `504` | Loopback upstream, application logs, Nginx error log, timeout values. | Increase timeouts before finding the failing layer. |
| `403` | `namei -l /var/www/<site>` and file ownership. | `chmod -R 777`. |
| `404` | Effective config, `root`, location, requested URI. | Change many locations at once. |
| `413` | Confirm valid upload requirement; set reviewed `client_max_body_size`. | Remove limits blindly. |
| ACME failure | DNS, port `80`, challenge path, Certbot logs. | Share keys or disable TLS checks. |

## Acceptance checklist

- [ ] DNS, firewall, port ownership, and time synchronization were checked.
- [ ] `nginx -t` passes; Nginx is enabled and active.
- [ ] HTTP redirects to HTTPS and `https://<domain>/healthz` returns `200`.
- [ ] A proxy upstream passes its own approved health check and an approved request works through Nginx.
- [ ] `certbot renew --dry-run` succeeds; monitoring, log retention, backups, renewal, and rollback have an owner.
- [ ] No private key, credential, real internal address, or public status endpoint is exposed.

## Official references

- [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Nginx control](https://nginx.org/en/docs/control.html)
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [Nginx HTTPS servers](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Nginx stub status](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)
- [Certbot webroot](https://eff-certbot.readthedocs.io/en/stable/using.html)
