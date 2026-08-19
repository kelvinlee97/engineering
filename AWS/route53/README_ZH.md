# Amazon Route 53 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Route 53 是高可用、可扩展的域名系统（DNS）Web 服务，三大功能：域名注册、DNS 路由、健康检查。

## 核心概念

- **托管区域（Hosted zone）**：公有（面向互联网）和私有（VPC 内）的 DNS 记录容器。
- **记录类型**：A、AAAA、CNAME、MX、TXT、NS、SOA，以及 alias 记录。
- **Alias 记录**：把域名指向 AWS 资源（ELB、CloudFront、S3），免费且无 TTL 问题。
- **路由策略**：simple、weighted、latency、failover、geolocation、geoproximity、multivalue。
- **健康检查**：验证资源可达性，与 failover 路由配合。
- **DNSSEC**：对区域签名，防止 DNS 欺骗。
- **VPC Resolver / DNS Firewall**：私有 DNS 解析和出站 DNS 过滤。

## 常用操作（AWS CLI）

```bash
# 托管区域
aws route53 create-hosted-zone --name example.com --caller-reference "$(date +%s)"
aws route53 list-hosted-zones

# 变更记录（批量 JSON）
aws route53 change-resource-record-sets --hosted-zone-id Z0123456789ABCDEF \
  --change-batch file://change-batch.json

cat > change-batch.json <<'EOF'
{
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "www.example.com.",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "my-alb-1234567890.ap-southeast-1.elb.amazonaws.com.",
          "EvaluateTargetHealth": false
        }
      }
    }
  ]
}
EOF

# 健康检查
aws route53 create-health-check --caller-reference "$(date +%s)" \
  --health-check-config Type=HTTPS,ResourcePath=/health,FullyQualifiedDomainName=example.com

# 查看
aws route53 list-resource-record-sets --hosted-zone-id Z0123456789ABCDEF
aws route53 get-change --id /change/C01234567890
```

## 最佳实践

- AWS 资源用 **alias 记录**（免费、自动更新），不要用 CNAME/A。
- **健康检查 + failover 路由**做跨区域高可用。
- 全球流量管理用 weighted/latency/geolocation 策略，先在测试环境验证预期行为。
- 关键区域开启 **DNSSEC**；用 **DNS Firewall** 过滤出站查询。
- 内部 DNS 用**私有托管区域**和 Resolver；在注册商处记录 NS 委派。
- 用 CloudWatch 监控健康检查状态并告警。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| DNS 不解析 | 核对注册商的 NS 委派和记录是否存在；考虑 TTL 缓存。 |
| Failover 不生效 | 检查健康检查状态、评估窗口、failover 记录配置。 |
| Alias 记录报错 | 使用目标服务正确的 hosted zone ID 和完整域名。 |
| VPC 内私有 DNS 不生效 | 开启 `enableDnsHostnames`/`enableDnsSupport`；检查 Resolver 规则和 VPC 关联。 |
| 传播慢 | 变更前降低 TTL；用 `get-change` 跟踪变更批次。 |
| DNSSEC 问题 | 校验密钥签名和注册商处 DS 记录发布。 |

## 配额

默认配额：每账户 500 个托管区域、每区域 10,000 条记录（可调），另有健康检查配额。以 Service Quotas 为准。

## 官方参考

- [什么是 Amazon Route 53？- Route 53 开发者指南](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
- [AWS CLI：route53 命令](https://docs.aws.amazon.com/cli/latest/reference/route53/)
