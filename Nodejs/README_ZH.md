# Node.js / Express BFF 运维文档

English version: [README.md](README.md)

本模块提供面向初级运维的 Node.js Express BFF 与 PM2 cluster 运维指南。通用生产模型为：外部 Nginx 或 OpenResty 网关把流量转发到私有 Node.js BFF，BFF 再调用已批准的下游 HTTP 服务。

该模型刻意保持通用：不描述任何雇主的端口、Worker 数、下游服务、发布工具或入口拓扑。

## 指南

| 指南 | 说明 |
| --- | --- |
| [初级运维生产部署指南](guides/express-bff-production-deployment/README_ZH.md) | 使用非 root 账户、PM2、可回滚发布、健康检查与可选网关集成部署 Express BFF。 |
| [现代 BFF 架构评估](guides/modern-bff-architecture-assessment/README_ZH.md) | 判断 VM/PM2 BFF 是否需要现代化，并按实际需求选择平台，而非把 Kubernetes 当作必选项。 |

## Runbook

| Runbook | 说明 |
| --- | --- |
| [10 类常见 Node.js / Express BFF 事故](runbooks/common-express-bff-incidents/README_ZH.md) | 按证据优先原则排查网关、PM2、运行时、依赖、资源与发布故障。 |
