# 10 类常见 Node.js / Express BFF 事故 Runbook

English version: [README.md](README.md)

本通用 Runbook 用于由 PM2 cluster 托管的 Express BFF。占位符只能在获授权环境中替换。修改进程、release、路由、凭据或下游目标前必须保留证据。重启可能暂时恢复服务，但不能证明根因。

## 目录

- [安全边界与第一批证据](#安全边界与第一批证据)
- [判断流程](#判断流程)
- [10 类事故](#10-类事故)
- [恢复验收](#恢复验收)

## 安全边界与第一批证据

记录影响范围、受影响路径/用户、首次失败时间、环境、release ID、近期变更、当前 `current` 指向和负责人。不得记录 Token、含个人数据的 request body、完整环境文件、私有 URL 或完整进程参数。

先收集只读证据：

```bash
sudo -iu <app-user> pm2 status
sudo -iu <app-user> pm2 describe <app-name>
sudo -iu <app-user> pm2 logs <app-name> --lines 200 --nostream
readlink -f /srv/<app-name>/current
curl --fail --max-time 5 http://127.0.0.1:<private-port>/healthz
sudo ss -lntp '( sport = :<private-port> )'
df -h /srv/<app-name> /var/log; df -i /srv/<app-name> /var/log; free -h
```

不要一开始执行 `pm2 restart`、`pm2 reload`、`pm2 delete`、`pm2 flush`，不要修改下游 URL 或删除 release。应先找出第一层失败点。

## 判断流程

```text
用户请求失败
  |
  +-- 到达网关？ -------- 否 --> DNS/LB/TLS/网关负责人
  |
  +-- 网关可达 BFF /healthz？-- 否 --> PM2、端口、release、主机
  |
  +-- BFF 接收请求？ ---- 否 --> 路由、授权、配置、应用日志
  |
  +-- BFF 可达下游？ ---- 否 --> DNS/网络/下游负责人
  |
  +-- 资源健康？ -------- 否 --> 容量/保留策略/批准的缓解动作
  |
  +-- 刚发布过？ -------- 是 --> 比较版本并使用批准回滚
```

## 10 类事故

### 1. 请求没有到达 BFF

检查网关 access/error log、DNS/LB/TLS 健康、网关 upstream 地址与 BFF `healthz`。网关和 BFF 分主机时，只从批准的诊断位置测试。BFF 日志没有请求意味着故障在网关或之前，并不自动是 Node.js。

**恢复：**使用网关/DNS/LB 负责人的批准流程；不要重启 BFF 修复外部路由。**验证：**已批准请求到达 BFF，网关/BFF 状态码恢复。

### 2. PM2 daemon 或开机恢复缺失

检查 `pm2 status`、`pm2 ping`、服务账户 home，以及批准 `pm2 startup` 创建的 OS 启动单元。Node 升级后检查二进制路径；PM2 启动集成可能仍指向旧 runtime。

**恢复：**仅通过审查过的 PM2 输出命令重建启动集成，再执行 `pm2 save`。**验证：**在受控重启/窗口中，PM2 与已保存应用自动恢复并通过 `healthz`。

### 3. 进程崩溃或反复重启

用 `pm2 describe` 查看重启计数和退出信息；将 `pm2 logs` 与 release ID、host journal 关联。任何重启前先检查未捕获异常、模块缺失、无效配置和依赖错误。

**恢复：**不满足验收的新 release 应回滚；其他错误特征升级给应用/依赖负责人。**验证：**重启计数稳定、预期 Worker online、代表性请求成功。

### 4. 端口冲突、绑定地址错误或健康检查失败

对比 ecosystem 的 `PORT`/绑定地址与 `ss -lntp`、loopback health、网关 upstream。`EADDRINUSE` 表示端口被其他进程占用；即使 health 成功，外网绑定也可能是安全缺陷。

**恢复：**仅经批准停止或重配已确认冲突进程，恢复批准的私有 listener。**验证：**只有预期 listener、私有健康检查成功、没有公网直接访问。

### 5. Node 版本、制品、lockfile 或依赖不匹配

记录 `node --version`、`npm --version`、release ID、`package.json`/lockfile 是否存在，以及失败 release 的 `npm ci` 输出。不要运行 `npm install`、编辑 lockfile 或在主机随机安装包。

**恢复：**以批准的 Node LTS 补丁版本和 `npm ci` 部署已测试制品；否则将 `current` 指回已知正常 release。**验证：**版本、依赖安装、应用语法/启动、health 均成功。

### 6. 环境变量、密钥交付或权限失败

检查键名、环境文件属主/模式、服务账户读取权限和脱敏后的应用错误。不得打印敏感值，也不能将环境文件复制到工单。Node `--env-file` 在预期文件缺失时会失败。

**恢复：**只修正已批准密钥引用、键名或文件权限；怀疑泄露时轮换凭据。**验证：**应用启动、批准依赖认证成功、日志中没有值。

### 7. 网关 `502` 或 `504`

检查 BFF loopback `healthz`、网关能否连接正确私有 listener、网关 error log、BFF log 和上游延迟。`502` 常意味着连接/上游响应失败；`504` 必须先证明耗时在哪一层。

**恢复：**修复第一失败层：网关路由、BFF 进程/listener 或下游依赖。不要只加大所有 timeout。**验证：**网关 health、一个已批准端到端请求和错误率恢复。

### 8. 下游 DNS、连接、超时、HTTP 或响应适配失败

区分 BFF 是否收到请求、下游 DNS、TCP/TLS 连接、下游 HTTP 状态和 BFF 响应解析。系统若有 correlation ID，只保留脱敏 ID/时间。下游 `4xx/5xx` 不是 BFF 损坏的证明。

**恢复：**使用下游负责人批准的动作；若发布引入请求适配错误，回滚 BFF release。**验证：**分别验证依赖健康、BFF 路由和浏览器可见结果。

### 9. 内存增长或 OOM

检查 PM2 内存/重启历史、主机内存、kernel OOM 证据、流量/release 关联和磁盘空间。PM2 内存重启是缓解，不是内存泄露诊断。

受控诊断 release 可让 Node 在 fatal error、uncaught exception 或批准信号时写诊断报告。报告放入受限目录并使用 `--report-exclude-env`；它可能含运行时敏感信息。heap snapshot 消耗内存和磁盘，必须先获容量批准。

**恢复：**按批准流程将不健康容量移出流量或回滚；不要盲目提高 heap limit。**验证：**约定观察期内内存稳定且容量健康。

### 10. CPU/event-loop 延迟、磁盘/inode 或日志压力

检查 CPU/load、每 Worker 利用率、可用的 event-loop 指标、`df -h`、`df -i`、日志增长和近期流量/release。区分 CPU 饱和、I/O wait 和磁盘/inode 耗尽。

**恢复：**使用批准的扩容、限流、release 回滚或保留/轮转策略。没有确认目标和保留要求前，不要删除活动日志或数据。**验证：**资源余量、日志、health、延迟和错误率稳定。

## 恢复验收

仅当适用证据显示以下项目均满足，才可关闭事故：

- [ ] 已把第一失败层、已完成缓解动作与假设分开记录。
- [ ] PM2 处于预期稳定 Worker 状态，没有无法解释的重启循环。
- [ ] 私有 BFF health、网关路由和代表性获授权流程均成功。
- [ ] 依赖健康、错误、延迟、容量和 release 标识满足约定观察标准。
- [ ] 回滚、密钥暴露、监控缺口或后续工作均有负责人；脱敏证据已存入获授权事故系统。

## 官方资料

- [Node.js diagnostic reports](https://nodejs.org/api/report.html)
- [Node.js process signals](https://nodejs.org/api/process.html)
- [PM2 process management](https://pm2.keymetrics.io/docs/usage/process-management/)
- [PM2 restart strategy](https://pm2.keymetrics.io/docs/usage/restart-strategies/)
- [Nginx proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
