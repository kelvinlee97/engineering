# Nginx 与 OpenResty 运维文档

English version: [README.md](README.md)

本模块提供面向初级运维的 Ubuntu 24.04 LTS Nginx 与 OpenResty 生产部署、运维指南。两者是独立的服务选择：OpenResty 是集成 LuaJIT 与 Lua 模块的 Nginx 发行版，并不是要与系统 Nginx 同时运行的插件。

不要在同一台主机同时按两份指南运行它们；两者都会监听 TCP `80` 和 `443`。

如需使用 PM2 管理 Node.js BFF 上游，请参阅 [Node.js / Express BFF 运维文档](../Nodejs/README_ZH.md)。

## 指南

| 指南 | 说明 |
| --- | --- |
| [Nginx 生产部署](guides/nginx-production-deployment/README_ZH.md) | 使用 systemd 与 HTTPS 提供静态站点和本机应用反向代理。 |
| [OpenResty 生产部署](guides/openresty-production-deployment/README_ZH.md) | 使用 systemd 与 HTTPS 提供 Lua 健康检查和本机应用反向代理。 |
