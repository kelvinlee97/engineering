# AWS CodeDeploy - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS CodeDeploy 自动化向 EC2 实例、本地服务器、Lambda 函数和 Amazon ECS 服务的应用部署。你将应用与 AppSpec 文件打包；CodeDeploy 负责发布修订、跟踪健康状态，出错时可停止并回滚。它支持就地（in-place）和蓝绿（blue/green）两种部署策略。

## 核心概念

- **计算平台**：EC2/本地、AWS Lambda 和 Amazon ECS。
- **应用与部署组**：应用是部署组的集合；部署组定义目标实例（标签、ASG）或 Lambda/ECS 服务配置。
- **修订（Revision）**：应用包加 AppSpec 文件；存放在 S3 或 GitHub。
- **AppSpec**：定义生命周期事件钩子（BeforeInstall、AfterInstall、ApplicationStart、ValidateService 等）及各平台部署行为的 YAML/JSON 文件。
- **部署类型**：
  - **就地部署**（仅 EC2/本地）：实例分批更新并跟踪健康。
  - **蓝绿部署**：新实例/Lambda 版本/ECS 任务集按 canary、linear 或 all-at-once 配置接收流量。
- **CodeDeploy 代理**：安装在 EC2/本地实例上，轮询并执行部署。
- **部署配置**：控制部署速度和部署期间必须保持健康的最小实例数。

## 常用操作（AWS CLI）

```bash
# 创建应用、部署组并推送修订
aws codedeploy create-application --application-name web-app \
  --compute-platform Server
aws codedeploy create-deployment-group --application-name web-app \
  --deployment-group-name prod --service-role-arn arn:aws:iam::123456789012:role/codedeploy-role \
  --ec2-tag-filters Key=env,Type=KEY_AND_VALUE,Value=prod
aws deploy push --application-name web-app --s3-location s3://deploy-bucket/web-app.zip \
  --source .

# 启动并监控部署
aws deploy create-deployment --application-name web-app \
  --deployment-group-name prod \
  --s3-location bucket=deploy-bucket,key=web-app.zip,bundleType=zip
aws deploy get-deployment --deployment-id <deployment-id>

# 回滚
aws deploy stop-deployment --deployment-id <deployment-id> --auto-rollback-enabled
```

## 最佳实践

- 小而频繁地部署；关键工作负载使用蓝绿部署降低风险、支持快速回滚。
- 定义健康检查和验证钩子（ValidateService），让不健康部署自动回滚。
- 为 CodeDeploy 代理和服务使用 IAM 角色；修订包在 S3 加密。
- 部署配置作为代码管理（CodePipeline + CodeDeploy），先在 staging 测试。
- 监控部署事件和告警；对 Failed/Stopped 部署告警。
- Lambda/ECS 选择 canary/linear 流量切换，验证指标后再全量发布。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 实例部署失败 | 检查 CodeDeploy 代理日志（`/var/log/aws/codedeploy-agent`）、IAM 实例角色和 S3 修订访问。 |
| 钩子未运行 | 核对 AppSpec 文件路径、权限和脚本退出码（非零会失败）。 |
| 部署卡住 | 检查部署配置（最小健康实例数）、负载均衡摘除和代理连通性。 |
| 未触发回滚 | 确认自动回滚设置及告警/验证条件。 |
| ECS/Lambda 流量未切换 | 核对目标组/监听器配置和流量切换设置。 |

## 配额

每账户应用、部署组、并发部署和修订大小有限制。以 AWS CodeDeploy 配额页面和 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS CodeDeploy？- 用户指南](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html)
- [AWS CodeDeploy 配额](https://docs.aws.amazon.com/codedeploy/latest/userguide/limits.html)
- [AWS CodeDeploy 定价](https://aws.amazon.com/codedeploy/pricing/)
- [AWS CLI：codedeploy 命令](https://docs.aws.amazon.com/cli/latest/reference/codedeploy/)
