# Amazon Forecast - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Forecast 是全托管时间序列预测服务，使用统计算法和机器学习算法根据历史数据预测未来值，无需 ML 经验。注意：Amazon Forecast 已不再向新客户开放；现有客户可以继续正常使用。

## 核心概念

- **时间序列预测**：基于历史序列预测未来数据点（需求、流量、容量、财务指标）。
- **数据集**：通过控制台、API、CLI 或 SDK 导入时间序列数据（以及相关条目/用户元数据）。
- **Predictor**：由数据集训练出的预测模型；Forecast 自动完成算法选择和训练。
- **预测生成**：为你定义的时间范围生成预测；用回测评估准确率。
- **功能**：自动化 ML、先进算法、缺失值处理，以及内置的特征工程数据集（例如节假日）。
- **用途**：零售需求规划、供应链、资源规划、运营规划（Web 流量、服务器容量）。

## 常用操作（AWS CLI）

```bash
# 创建数据集组、导入数据并创建 predictor
aws forecast create-dataset-group --dataset-group-name retail \
  --domain RETAIL --dataset-arns <dataset-arn>
aws forecast create-dataset-import-job --dataset-arn <dataset-arn> \
  --dataset-import-job-name initial \
  --data-source '{"S3Config":{"Path":"s3://bucket/data","RoleArn":"arn:aws:iam::123456789012:role/forecast-role"}}'
aws forecast create-auto-predictor --predictor-name demand \
  --forecast-horizon 30 --data-config file://data.json

# 生成并获取预测
aws forecast create-forecast --forecast-name demand-30 \
  --predictor-arn <predictor-arn>
aws forecast describe-forecast --forecast-arn <forecast-arn>
```

## 最佳实践

- 准备干净、规则的时间序列数据（时间戳、条目 ID、目标值），有可用元数据时提供相关时间序列。
- 用 AutoPredictor 自动选择算法；生产前用回测验证准确率。
- 预测范围匹配规划周期（例如 30 或 90 天）。
- 有意识地处理缺失值；Forecast 提供多种填充方法。
- 预测结果存 S3/Redshift 供下游规划系统使用。
- 现有客户：跟踪服务状态；启动新预测项目时规划替代方案。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 数据集导入失败 | 检查 CSV 格式、S3 权限和数据集 schema。 |
| Predictor 训练失败 | 核对数据频率、条目数限制和预测范围设置。 |
| 预测准确率差 | 补充相关时间序列数据、清理离群值，并用回测指标评估。 |
| 新账户无法开通 | Forecast 已对新客户关闭；使用文档化替代方案。 |
| 成本高于预期 | Forecast 按生成的预测、存储和训练小时收费；审查用量。 |

## 配额

每账户数据集、predictor 和预测数量及数据集大小有限制；服务仅限现有客户开通。以 Amazon Forecast 端点和配额页面为准。

## 官方参考

- [什么是 Amazon Forecast？- 开发者指南](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html)
- [Amazon Forecast 端点和配额](https://docs.aws.amazon.com/general/latest/gr/forecast.html)
- [Amazon Forecast 定价](https://aws.amazon.com/forecast/pricing/)
- [AWS CLI：forecast 命令](https://docs.aws.amazon.com/cli/latest/reference/forecast/)
