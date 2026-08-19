# Amazon Rekognition - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Rekognition 是基于深度学习的云图像与视频分析服务。通过简单 API，无需 ML 专业知识即可检测 S3 中图片/视频的对象、场景、文本、人脸、名人和不安全内容。该服务适用于 HIPAA，采用按用即付定价。

## 核心概念

- **图像分析**：对象/场景/概念检测、文本检测、不安全内容审核、名人识别、人脸分析、图像属性（质量、颜色、清晰度），以及 Custom Labels 分类器。
- **视频分析**：对象/场景/概念检测、文本检测、人员轨迹（people pathing）、人脸分析、名人识别、不安全内容、视频分段和人脸活体检测。
- **人脸集合（Face collections）**：用于人脸搜索和身份验证的索引容器。
- **Face Liveness**：全托管功能，验证用户真实在场，检测照片、视频、3D 面具和 deepfake 等欺骗攻击。
- **内容审核**：带置信度分数的分层标签，用于过滤用户生成内容；可用 adapters 定制。
- **Custom Labels**：无需 ML 专业知识即可训练领域特定对象（logo、产品、角色）的自定义分类器。
- **PPE 检测**：检测个人防护装备，监控安全合规。
- **集成**：与 S3、Lambda、IAM 集成；无需移动数据即可分析图像/视频。

## 常用操作（AWS CLI）

```bash
# 图像分析
aws rekognition detect-labels --image '{"S3Object":{"Bucket":"bucket","Name":"photo.jpg"}}'
aws rekognition detect-text --image '{"S3Object":{"Bucket":"bucket","Name":"sign.jpg"}}'
aws rekognition detect-moderation-labels --image '{"S3Object":{"Bucket":"bucket","Name":"photo.jpg"}}'

# 人脸操作
aws rekognition create-collection --collection-id users
aws rekognition index-faces --collection-id users \
  --image '{"S3Object":{"Bucket":"bucket","Name":"face.jpg"}}'
aws rekognition search-faces-by-image --collection-id users \
  --image '{"S3Object":{"Bucket":"bucket","Name":"probe.jpg"}}'

# 视频分析（异步，结果发 SNS）
aws rekognition start-label-detection --video '{"S3Object":{"Bucket":"bucket","Name":"clip.mp4"}}' \
  --notification-channel file://sns.json
aws rekognition get-label-detection --job-id <job-id>
```

## 最佳实践

- 媒体存 S3 并设置生命周期策略；用 IAM 限定角色原地分析。
- UGC 平台用带 adapters 的内容审核并设置置信度阈值。
- 身份验证用 Face Liveness 防欺骗；遵守适用隐私法律并按要求获得同意。
- 小众对象用 Custom Labels，而不是依赖通用标签。
- 视频用带 SNS 通知的异步任务并监控任务完成。
- 与 Lambda 和 EventBridge 组合实现自动化管道（审核、编目）。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| S3 图像 API 报错 | 检查桶权限、对象键和区域。 |
| 找不到人脸 | 核对图像质量/方向和人脸尺寸要求。 |
| 视频任务卡住 | 检查 SNS 主题权限和任务状态；必要时重新提交。 |
| Custom Labels 准确率低 | 每个类别增加更多带标签的训练图像。 |
| 审核漏检 | 调整置信度阈值或用样本图像训练 adapters。 |

## 配额

图像大小、每账户人脸集合数、视频时长和 API 请求速率有限制。以 Amazon Rekognition 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Rekognition？- 开发者指南](https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html)
- [Amazon Rekognition 端点和配额](https://docs.aws.amazon.com/general/latest/gr/rekognition.html)
- [Amazon Rekognition 定价](https://aws.amazon.com/rekognition/pricing/)
- [AWS CLI：rekognition 命令](https://docs.aws.amazon.com/cli/latest/reference/rekognition/)
