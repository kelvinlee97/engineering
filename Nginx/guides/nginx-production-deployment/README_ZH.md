# DevOps 新手 Nginx 生产部署与运维指南

English version: [README.md](README.md)

本指南在一台 Ubuntu 24.04 LTS VM 上部署**仅 Nginx**。它提供静态文件、反向代理监听在 `127.0.0.1:3000` 的应用，并通过 Certbot webroot 获取 HTTPS 证书。必须通过已批准的变更流程替换 `<domain>`、`<site>`、`<operations-email>` 与 `<approved-health-path>`；本文不是任何真实服务器已经部署的证据。

## 目录

- [目标与安全边界](#目标与安全边界)
- [准备主机](#准备主机)
- [安装与配置](#安装与配置)
- [启用 HTTPS](#启用-https)
- [验证服务](#验证服务)
- [日常运维与安全变更](#日常运维与安全变更)
- [按层排障](#按层排障)
- [验收清单](#验收清单)

## 目标与安全边界

```text
客户端 -> Nginx :443 -> 应用 127.0.0.1:3000
                     -> 静态文件 /var/www/<site>/
```

Nginx master 进程读取、验证配置并管理 worker；worker 处理请求。`server` 是虚拟主机，`location` 匹配请求路径，`proxy_pass` 把请求转发给上游应用。不要在该主机安装或运行 OpenResty：两者都会占用 `80`、`443`。

## 准备主机

操作前，确认 `<domain>` 已解析到该 VM、已批准的防火墙允许 TCP `80/443`、系统时间正确，且没有其他服务监听这些端口。

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

此处 Certbot 仅签发和续期证书，不会自动修改 Nginx 配置。若不允许公网 ACME 签发，应改用组织批准的证书来源。

## 安装与配置

先备份生效配置。新的 Ubuntu 主机含默认站点；启用下列站点前先禁用它。

```bash
sudo cp -a /etc/nginx /etc/nginx.backup.$(date +%Y%m%d-%H%M%S)
sudo rm -f /etc/nginx/sites-enabled/default
```

创建 `/etc/nginx/sites-available/<site>`：

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

纯静态站点应以 `try_files $uri $uri/ =404;` 取代最后的代理 location；不要指向不存在的上游。

```bash
sudo ln -s ../sites-available/<site> /etc/nginx/sites-enabled/<site>
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
sudo systemctl status nginx --no-pager
```

每次 reload 前必须执行 `nginx -t`。成功 reload 会验证新配置并优雅替换 worker，比常规 restart 安全。

## 启用 HTTPS

先证明公网 HTTP 可用。ACME challenge 需要公网 DNS 与 TCP `80`。

```bash
curl --fail http://<domain>/healthz
sudo certbot certonly --webroot -w /var/www/<site> -d <domain> \
  --email <operations-email> --agree-tos --no-eff-email
```

把 HTTP server 替换为下列跳转 server，并追加 HTTPS server。HTTP 必须保留 challenge location 供续期使用。不得复制 `privkey.pem` 到应用目录或仓库。

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

## 验证服务

端口开放不代表应用可用，应逐层证明：

```bash
sudo systemctl is-active nginx
sudo nginx -T | less
curl --fail http://127.0.0.1/healthz
curl --fail http://127.0.0.1:3000/<approved-health-path>
curl --fail --resolve <domain>:443:127.0.0.1 https://<domain>/healthz
sudo journalctl -u nginx -n 100 --no-pager
```

有意仅提供静态站点时无需上游检查；代理场景下，它能区分应用故障和 Nginx 故障。

## 日常运维与安全变更

| 目标 | 命令 | 规则 |
| --- | --- | --- |
| 服务状态 | `sudo systemctl status nginx --no-pager` | `active` 不代表所有路由正常。 |
| 最近错误 | `sudo journalctl -u nginx -n 100 --no-pager` | 同时检查配置的 error log。 |
| 配置检查 | `sudo nginx -t` | reload 前必做。 |
| 应用有效配置 | `sudo systemctl reload nginx` | 避免常规 restart。 |
| 容量 | `df -h; df -i; free -h` | 耗尽前告警。 |

每次变更：记录目的、备份文件、仅改一小项、测试、reload、验证 `/healthz` 和已批准的应用请求、再检查日志。测试失败时，先恢复备份并测试，再 reload。

若需要基础连接指标，先确认 `nginx -V 2>&1 | grep http_stub_status_module`。随后仅绑定 loopback：

```nginx
server {
    listen 127.0.0.1:8080;
    location = /basic_status { stub_status; access_log off; }
}
```

用 `curl --fail http://127.0.0.1:8080/basic_status` 验证。监控可用性、状态码比例、延迟、活跃连接、重启、磁盘/inode、证书到期和上游错误。`stub_status` 不是带认证的管理 API。

## 按层排障

| 症状 | 首先检查 | 不要做 |
| --- | --- | --- |
| `nginx -t` 失败 | 输出中的文件/行号、`sudo nginx -T`。 | 仍然 reload/restart。 |
| `bind() ... 80/443 failed` | `ss` 端口检查；仅经批准停止已确认服务。 | 同时运行 Nginx 和 OpenResty。 |
| `502` / `504` | loopback upstream、应用日志、Nginx error log、超时值。 | 未定位失败层就加大超时。 |
| `403` | `namei -l /var/www/<site>`、文件属主。 | `chmod -R 777`。 |
| `404` | 生效配置、`root`、location、请求 URI。 | 同时修改多个 location。 |
| `413` | 合法上传需求、经审查的 `client_max_body_size`。 | 盲目移除全部限制。 |
| ACME 失败 | DNS、`80`、challenge 路径、Certbot 日志。 | 分享私钥或关闭 TLS 验证。 |

## 验收清单

- [ ] 已检查 DNS、防火墙、端口所有权和时间同步。
- [ ] `nginx -t` 成功；Nginx 已 enable 且 active。
- [ ] HTTP 跳转 HTTPS，`https://<domain>/healthz` 返回 `200`。
- [ ] 代理上游通过其已批准健康检查，且一个已批准请求可经 Nginx 成功访问。
- [ ] `certbot renew --dry-run` 成功；监控、日志保留、备份、续期和回滚均有负责人。
- [ ] 未暴露私钥、凭据、真实内部地址或公网状态端点。

## 官方资料

- [Nginx Beginner's Guide](https://nginx.org/en/docs/beginners_guide.html)
- [Nginx control](https://nginx.org/en/docs/control.html)
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [Nginx HTTPS servers](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [Nginx stub status](https://nginx.org/en/docs/http/ngx_http_stub_status_module.html)
- [Certbot webroot](https://eff-certbot.readthedocs.io/en/stable/using.html)
