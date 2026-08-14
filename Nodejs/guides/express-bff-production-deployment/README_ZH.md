# DevOps 新手 Node.js / Express BFF 生产部署指南

English version: [README.md](README.md)

本指南在 Linux VM 上部署通用 Express BFF：PM2 cluster 以非特权账户运行多个 Node.js Worker；可选且独立运维的 Nginx 或 OpenResty 网关转发公网流量。所有 `<placeholder>` 必须通过批准的变更流程替换。本文是可复用基线，不证明任何生产服务使用这些路径、端口或 Worker 数。

## 目录

- [心智模型与边界](#心智模型与边界)
- [准备发布主机](#准备发布主机)
- [创建可运维的应用](#创建可运维的应用)
- [使用 PM2 部署与托管](#使用-pm2-部署与托管)
- [发布、验证与回滚](#发布验证与回滚)
- [网关集成与日常运维](#网关集成与日常运维)
- [验收清单](#验收清单)

## 心智模型与边界

```text
浏览器 -> 外部 Nginx/OpenResty -> Express BFF（PM2 cluster）
                                    -> 已批准的下游 HTTP 服务
```

Node.js 在浏览器外运行 JavaScript；Express 是 Web 框架；BFF 是面向浏览器的后端，可处理 Session/授权、请求适配和下游 HTTP 调用。它不等于 OpenResty、Nginx 或下游 API。

PM2 cluster Worker 共享一个私有监听端口，因此必须无状态：不能把 Session、上传或权威业务数据保存在某个 Worker 内存里，应使用已批准的共享服务。网关可能在另一台主机，不能从本文推断是否共置。

## 准备发布主机

选择并在变更单记录受支持 Node.js LTS 的**精确补丁版本**；生产不能使用 EOL 或仅 Current 的版本。通过组织批准的软件源安装 Node，随后确认实际二进制。

```bash
node --version
npm --version
command -v node
command -v npm
```

创建专用服务账户与发布目录。该账户可读取应用与受限环境文件，但没有 root 权限。

```bash
sudo groupadd --system <app-group>
sudo useradd --system --gid <app-group> --home-dir /srv/<app-name> --create-home \
  --shell /bin/bash <app-user>
sudo install -d -o <app-user> -g <app-group> -m 0750 \
  /srv/<app-name>/releases /srv/<app-name>/shared /srv/<app-name>/shared/logs \
  /etc/<app-name>
sudo install -o root -g <app-group> -m 0640 /dev/null /etc/<app-name>/production.env
```

系统账户密码保持锁定，且不得授权直接 SSH 登录。敏感值只进入批准的密钥交付机制或 `/etc/<app-name>/production.env`，绝不可提交。该文件使用 `KEY=value` 格式，不是 JavaScript；变更记录中只写属主、权限和所需键名。

## 创建可运维的应用

开发者通常提供已测试、含 `package.json` 和 `package-lock.json` 的制品。`npm ci` 要求二者匹配且不会改写它们，因此是部署安装命令。不要在服务器运行 `npm install` 来“修复”发布包。

最小应用契约是私有 `GET /healthz` 和优雅退出。以下教学代码没有认证和业务路由；真实 BFF 授权必须由应用代码与评审负责。

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

每个应用使用一个 ecosystem 文件。以下是安全示例，不是容量建议；`instances`、内存阈值和超时必须由批准的压测与主机资源决定。

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
    min_uptime: '10s', max_restarts: 5, restart_delay: 5000,
    listen_timeout: 10000, kill_timeout: 30000,
    max_memory_restart: '512M', watch: false, time: true,
    out_file: '/srv/<app-name>/shared/logs/out.log',
    error_file: '/srv/<app-name>/shared/logs/error.log', merge_logs: true
  }]
};
```

`NODE_ENV=production` 避免 Express 返回开发式错误页面。PM2 正常 reload/stop 时先发送 `SIGINT`，应用必须在 `kill_timeout` 前关闭监听器和已批准依赖。生产 release 目录不能启用 PM2 `watch`。

## 使用 PM2 部署与托管

从批准的流水线取得制品，按要求验证发布标识/校验和，创建新的不可变 release 目录。新版本未通过本地检查前不能覆盖 `current`。

```bash
sudo -u <app-user> install -d -m 0750 /srv/<app-name>/releases/<release-id>
sudo -u <app-user> tar -xzf <approved-artifact>.tar.gz -C /srv/<app-name>/releases/<release-id>
sudo -u <app-user> sh -c 'cd /srv/<app-name>/releases/<release-id> && npm ci --omit=dev'
sudo -u <app-user> sh -c 'cd /srv/<app-name>/releases/<release-id> && npm run test --if-present'
sudo -u <app-user> sh -c 'cd /srv/<app-name>/releases/<release-id> && node --check app.js'
```

替换 `app.js` 前先确认批准制品的真实启动文件；不能假定 `package.json` 的 `main` 就是生产入口。

为 `<app-user>` 安装批准版本 PM2，并仅首次创建 OS 启动集成。以服务账户运行 `pm2 startup`，审查后仅执行它输出的那条特定特权命令；最后保存已知进程清单。Node 二进制路径变更后必须重新设置启动脚本。

```bash
sudo -iu <app-user> npm install --global pm2@<approved-pm2-version>
sudo -iu <app-user> pm2 startup
# 审查后执行上一条命令打印出的精确 sudo 命令。
sudo -iu <app-user> pm2 save
```

## 发布、验证与回滚

先采集只读基线：

```bash
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 describe <app-name>
readlink -f /srv/<app-name>/current
curl --fail http://127.0.0.1:3000/healthz
```

本地制品检查成功后，原子切换 `current` 到新 release，再启动或 reload ecosystem。`reload` 用于 cluster 应用；若 Worker 无法 ready，PM2 可能退化为 restart，因此必须观察状态、日志和真实请求。

```bash
sudo -u <app-user> ln -sfn /srv/<app-name>/releases/<release-id> /srv/<app-name>/current
# 仅首次部署：
sudo -iu <app-user> pm2 start /srv/<app-name>/current/ecosystem.config.cjs --only <app-name>
# 已存在的 cluster 应用：
sudo -iu <app-user> pm2 reload /srv/<app-name>/current/ecosystem.config.cjs --only <app-name>
sudo -iu <app-user> pm2 save
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 logs <app-name> --lines 100 --nostream
curl --fail http://127.0.0.1:3000/healthz
```

只有私有健康检查、网关请求、已批准代表性用户流程、错误率和 release 标识都满足变更标准后，才能继续发布。失败时停止扩大范围、保留日志、将 `current` 指回 `<known-good-release-id>`、reload，并重复相同验证。观察期内不得删除已知正常 release。

## 网关集成与日常运维

本单机例子将 BFF 仅绑定 `127.0.0.1:3000`。外部网关架构应替换为获批准的私有接口与网络策略；不得把未认证的开发监听器直接暴露到 Internet。

配置网关请使用现有 [Nginx 指南](../../../Nginx/guides/nginx-production-deployment/README_ZH.md) 或 [OpenResty 指南](../../../Nginx/guides/openresty-production-deployment/README_ZH.md)。网关 upstream 必须匹配 BFF listener；保留 `Host`、`X-Forwarded-For`、`X-Forwarded-Proto`，且仅在流量来自受批准网关时信任这些 header。

日常只读检查：

```bash
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 logs <app-name> --lines 100 --nostream
curl --fail http://127.0.0.1:3000/healthz
df -h /srv/<app-name> /var/log
df -i /srv/<app-name> /var/log
free -h
```

监控请求成功率/延迟、网关 `5xx`、BFF `5xx`、Worker 重启、内存、CPU、应用可提供的 event-loop delay、下游失败、磁盘/inode、日志增长和 release 版本。SLO、内存阈值不能从本文照抄，应由服务 owner 与实测决定。

## 验收清单

- [ ] Node 是受支持 LTS 的精确补丁版本；PM2 是 `<app-user>` 所有的批准版本。
- [ ] release 使用 `npm ci`、已提交 lockfile、非 root 属主和受限环境文件。
- [ ] PM2 cluster Worker 无状态、`watch` 已关闭，且启动恢复已在受控重启后验证。
- [ ] 已验证私有 `/healthz`、批准网关路径、代表性流程、日志、错误和发布版本。
- [ ] 已知正常 release 和获批准的回滚负责人仍可用。
- [ ] 未公开凭据、真实内部地址、客户数据或完整进程参数。

## 官方资料

- [Node.js supported releases](https://nodejs.org/en/about/previous-releases)
- [Node.js environment files](https://nodejs.org/api/cli.html)
- [Node.js signals](https://nodejs.org/api/process.html)
- [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/)
- [PM2 cluster mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/)
- [PM2 ecosystem file](https://pm2.keymetrics.io/docs/usage/application-declaration/)
- [PM2 startup](https://pm2.keymetrics.io/docs/usage/startup/)
- [Express production reliability](https://expressjs.com/en/advanced/best-practice-performance/)
