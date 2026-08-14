# DevOps 新手 OpenResty 生产部署与运维指南

English version: [README.md](README.md)

本指南在一台 Ubuntu 24.04 LTS VM 上部署**仅 OpenResty**。OpenResty 是集成 LuaJIT 和 Lua 模块的 Nginx Web 平台。它提供 Lua 健康检查、反向代理 `127.0.0.1:3000` 的应用，并使用 Certbot webroot 获取 HTTPS。所有 `<example>` 值必须通过已批准的变更流程替换。

## 目录

- [明确选择 OpenResty](#明确选择-openresty)
- [准备与安装](#准备与安装)
- [配置站点和 Lua 健康检查](#配置站点和-lua-健康检查)
- [启用 HTTPS](#启用-https)
- [验证与日常运维](#验证与日常运维)
- [按层排障](#按层排障)
- [验收清单](#验收清单)

## 明确选择 OpenResty

```text
客户端 -> OpenResty :443 -> Lua /healthz
                          -> 应用 127.0.0.1:3000
```

仅当 Nginx 网关确实需要经审查的 Lua 行为（例如这里的小型健康检查）时选择 OpenResty；基本静态站点与反向代理使用普通 Nginx 即可。OpenResty 是本机 Nginx Web 服务进程的替代品，不是运行中的 Ubuntu `nginx` 服务的插件。两者会争用 `80/443`，绝不可同时运行。

`content_by_lua_file` 在 OpenResty 的事件驱动请求路径中执行 Lua。未经过审查的应用设计，不要加入阻塞 shell 命令、阻塞文件 I/O、无限循环、凭据或临时网络调用。

## 准备与安装

确认 DNS、TCP `80/443` 的已批准入站规则、时间同步、CPU 架构和端口所有权。官方 x86_64 包要求 CPU 支持 SSE 4.2。

```bash
sudo ss -lntp '( sport = :80 or sport = :443 )'
hostname -f
timedatectl status
getent hosts <domain>
dpkg --print-architecture
```

如果 Ubuntu Nginx 已安装，只有在确认它未承载所需站点且变更窗口获批准后才停止并禁用：

```bash
sudo systemctl disable --now nginx
```

安装 OpenResty 官方仓库。本段命令适用于 Ubuntu 24.04 amd64；arm64 必须使用 OpenResty 官方 arm64 仓库 URL。

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

包的默认前缀为 `/usr/local/openresty/`；使用 `openresty` 命令，不要使用可能指向另一个二进制的裸 `nginx` 命令。

## 配置站点和 Lua 健康检查

备份生效配置。创建 `/etc/openresty/lua/health.lua`，属主为 `root:root`、模式 `0644`：

```bash
sudo tee /etc/openresty/lua/health.lua >/dev/null <<'EOF'
ngx.status = ngx.HTTP_OK
ngx.header.content_type = "text/plain"
ngx.say("ok")
EOF
sudo chown root:root /etc/openresty/lua/health.lua
sudo chmod 0644 /etc/openresty/lua/health.lua
```

创建 `/etc/openresty/conf.d/<site>.conf`：

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

主配置必须在 `http {}` 内加载这个站点目录。编辑前先检查；仅当没有等价行时才增加 include。

```bash
sudo cp -a /usr/local/openresty/nginx/conf /usr/local/openresty/nginx/conf.backup.$(date +%Y%m%d-%H%M%S)
sudo grep -n 'conf.d' /usr/local/openresty/nginx/conf/nginx.conf
# 如有需要，在 http {} 内加入：include /etc/openresty/conf.d/*.conf;
sudo openresty -t
sudo systemctl enable --now openresty
sudo systemctl reload openresty
```

站点与 Lua 文件应分离；不要在 vendor `nginx.conf` 做无关修改。

## 启用 HTTPS

先证明公网 HTTP 健康检查可用，再签发证书：

```bash
curl --fail http://<domain>/healthz
sudo certbot certonly --webroot -w /var/www/<site> -d <domain> \
  --email <operations-email> --agree-tos --no-eff-email
```

把 `80` 端口 server 替换为跳转 server，并追加下方 HTTPS server。必须在 HTTP 上保留 ACME location 用于续期。

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

绝不可把 `privkey.pem` 复制到应用目录或仓库。

## 验证与日常运维

分别检查服务、Lua、上游和 TLS：

```bash
sudo systemctl is-active openresty
sudo openresty -T | less
curl --fail http://127.0.0.1/healthz
curl --fail http://127.0.0.1:3000/<approved-health-path>
curl --fail --resolve <domain>:443:127.0.0.1 https://<domain>/healthz
sudo journalctl -u openresty -n 100 --no-pager
```

每次变更：备份受影响的一个站点或 Lua 文件、只改一个关注点、执行 `openresty -t`、优雅 `systemctl reload openresty`、测试 health 和一个已批准代理请求、检查日志。不要只为应用配置而 restart。监控可用性、HTTP 状态码、延迟、worker 重启、磁盘/inode、证书到期、Lua 错误和上游失败。

仅当 `openresty -V 2>&1 | grep http_stub_status_module` 成功时才使用基础 `stub_status`，且只能绑定 `127.0.0.1`。它是指标数据，不是公网管理端点。

## 按层排障

| 症状 | 首先检查 | 不要做 |
| --- | --- | --- |
| `openresty -t` 失败 | 报告的文件/行、`sudo openresty -T`、Lua 语法/路径。 | 仍然 reload。 |
| 端口绑定失败 | `sudo ss -lntp '( sport = :80 or sport = :443 )'`。 | 在 OpenResty 旁启动 Ubuntu Nginx。 |
| `/healthz` 返回 `500` | error log、Lua 路径/权限、配置测试。 | 用坏脚本伪造成功。 |
| `502` / `504` | loopback upstream、应用日志、error log。 | 未检查上游就怪 Lua。 |
| ACME 失败 | DNS、`80`、webroot、Certbot 日志。 | 暴露私钥。 |

## 验收清单

- [ ] 已检查 DNS、防火墙、端口所有权、架构和时间。
- [ ] `openresty -t` 成功；OpenResty 已 enable 且 active。
- [ ] Lua `/healthz` 返回 `200`；HTTP 跳转 HTTPS。
- [ ] 上游通过自身健康检查，且一个已批准请求可经 OpenResty 成功。
- [ ] `certbot renew --dry-run` 成功；监控、日志、备份、续期和回滚均有负责人。
- [ ] 没有 Nginx 服务争用端口，且未暴露凭据、公网状态端点或生产数据。

## 官方资料

- [OpenResty Linux packages](https://openresty.org/en/linux-packages.html)
- [OpenResty deb packages](https://openresty.org/en/deb-packages.html)
- [OpenResty Lua Nginx module](https://openresty.org/en/lua-nginx-module.html)
- [Nginx control](https://nginx.org/en/docs/control.html)
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
- [Certbot webroot](https://eff-certbot.readthedocs.io/en/stable/using.html)
