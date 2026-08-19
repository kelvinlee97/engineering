# AWS Elastic Beanstalk - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Elastic Beanstalk 是一项托管服务，用于在 EC2、S3、负载均衡器等常见 AWS 资源上部署和扩展 Web 应用程序与后台进程。你上传代码，Elastic Beanstalk 负责容量供给、负载均衡、扩展、健康监控和更新，同时你仍可控制底层资源。

## 核心概念

- **Application**：版本和环境的逻辑容器。
- **Environment**：某个应用版本的一次运行部署。
  - **Web server 环境**：在负载均衡器后面处理 HTTP/HTTPS 请求。
  - **Worker 环境**：通过从 SQS 队列拉取消息运行后台任务。
- **Platform**：运行时栈，包括 Go、Java（Corretto、Tomcat）、.NET（Linux）、Node.js、PHP、Python、Ruby 和 Docker（单容器与多容器）；平台会维护你选择的运行时版本。
- **Configuration**：实例、扩展、负载均衡、更新和健康相关的环境设置；可保存配置并复用。
- **部署策略**：all-at-once、rolling、rolling with additional batch、immutable、流量拆分（canary），以及通过环境 CNAME 交换实现蓝绿部署。
- **Health**：增强健康报告提供实例级健康和原因；环境健康页面聚合结果。

## 常用操作（CLI）

```bash
# 初始化项目目录并创建环境
eb init my-app --platform python-3.11 --region us-east-1
eb create my-app-prod --instance-type t3.small

# 部署新版本
eb deploy my-app-prod

# 状态、打开站点和查看日志
eb status my-app-prod
eb open my-app-prod
eb logs my-app-prod

# 更新配置和终止
eb config my-app-prod
eb terminate my-app-prod
```

## 最佳实践

- 为不同阶段（dev、staging、prod）使用独立环境，保持应用版本不可变。
- 环境变量在配置中设置而不是硬编码；敏感值使用 Secrets Manager。
- 根据预期负载配置扩展策略和告警；路由流量前验证健康检查。
- 生产环境使用 immutable 或流量拆分部署以避免停机。
- 固定平台版本，先在低环境测试升级再应用到生产。
- Worker 环境的任务要幂等，并针对 SQS 重试和死信队列设计。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 环境 `Degraded`/`Severe` | 打开环境健康页面，检查实例级原因和最近事件。 |
| 部署失败 | 查看构建/应用日志（`eb logs`），确认制品对当前平台有效。 |
| 实例不健康 | 核对安全组、健康检查路径，确认应用绑定在预期端口。 |
| Worker 任务未处理 | 检查 SQS 队列、worker 环境扩展和应用错误日志。 |
| 变更未生效 | 确认 `eb config` 保存/部署周期完成，且环境不在更新中。 |

## 配额

Elastic Beanstalk 本身无额外费用；你只为它供给的底层 AWS 资源付费。应用数、环境数和平台版本可用性受服务配额和平台生命周期约束。以 Elastic Beanstalk 平台文档和 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Elastic Beanstalk？- 开发者指南](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
- [AWS Elastic Beanstalk 平台](https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html)
- [AWS Elastic Beanstalk 配额](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/limits.html)
- [AWS Elastic Beanstalk 定价](https://aws.amazon.com/elasticbeanstalk/pricing/)
- [AWS CLI：elasticbeanstalk 命令](https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/)
