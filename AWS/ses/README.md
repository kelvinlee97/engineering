# Amazon SES - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Simple Email Service (Amazon SES) is a scalable email platform for sending transactional email (order confirmations, password resets), marketing email (offers, newsletters), and for receiving email. You can send through the SES API, the SMTP interface, or AWS SDKs, and receive email into S3, SNS, or Lambda. You pay per email sent and received.

## Key concepts

- **Email identity**: a verified domain or email address that you are authorized to send from; DKIM and SPF/DMARC are configured for the domain.
- **Easy DKIM**: SES manages DKIM signing for your domain (especially simple when DNS is in Route 53); required for production sending.
- **Configuration sets**: group sending settings and event destinations (CloudWatch, Amazon Data Firehose, SNS, EventBridge, Pinpoint) for tracking bounces, complaints, deliveries, and opens/clicks.
- **Suppression and reputation**: SES tracks bounce and complaint rates, applies sending limits, and lets you manage a suppression list.
- **Receiving**: incoming email routes to S3 (optionally KMS-encrypted), SNS, or Lambda through receipt rules in a rule set.
- **SMTP interface**: send from applications or tools that support SMTP, using SES SMTP credentials (separate from IAM).
- **Sending limits**: daily message quota and maximum send rate per second, adjustable through the SES console/API based on reputation.

## Common operations (AWS CLI)

```bash
# Verify an identity (domain)
aws sesv2 create-email-identity --identity-name example.com
aws sesv2 get-email-identity --email-identity-name example.com

# Send an email
aws sesv2 send-email \
  --from-email-address no-reply@example.com \
  --destination '{"ToAddresses":["user@example.com"]}' \
  --content '{"Simple":{"Subject":{"Data":"Hello"},"Body":{"Text":{"Data":"Test from SES"}}}}'

# Configuration set and event destination
aws sesv2 create-configuration-set --configuration-set-name prod
aws sesv2 create-configuration-set-event-destination \
  --configuration-set-name prod --event-destination-name cloudwatch \
  --event-destination '{"Enabled":true,"MatchingEventTypes":["BOUNCE","COMPLAINT"],"CloudWatchDestination":{"DimensionConfigurations":[]}}'

# Sending statistics and quotas
aws sesv2 get-account
aws sesv2 get-send-quota

# Receive email (rule set with S3 action)
aws sesv2 create-receipt-rule-set --rule-set-name default
aws sesv2 create-receipt-rule --rule-set-name default \
  --rule file://rule.json
```

## Best practices

- Verify and configure Easy DKIM (and SPF/DMARC) for all sending domains; never send from unverified identities.
- Warm up new sending identities gradually and keep bounce/complaint rates low; act on feedback notifications.
- Use configuration sets for every workload and alert on bounce/complaint spikes.
- Store suppression lists and honor unsubscribe requests to protect reputation and comply with email regulations.
- Separate transactional and marketing streams with distinct identities/configuration sets.
- Protect SES credentials (SMTP or API) with IAM least privilege and monitor API calls with CloudTrail.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Sending from unverified identity | Verify the domain/email identity and complete DKIM setup; wait for propagation. |
| Daily quota exceeded | Check `get-send-quota`; request a limit increase after demonstrating low complaint/bounce rates. |
| Emails landing in spam | Verify DKIM/SPF/DMARC, warm up the identity, and review content and sending patterns. |
| Bounce/complaint events missing | Confirm the configuration set is attached and the event destination is configured correctly. |
| Inbound email not delivered | Check receipt rule set order, S3/SNS/Lambda action permissions, and spam filtering behavior. |

## Limits

Daily sending quota, maximum send rate, message size, and identities per account have limits; SES adjusts quotas based on reputation. See the SES service quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon SES?](https://docs.aws.amazon.com/ses/latest/dg/Welcome.html)
- [Amazon SES service quotas](https://docs.aws.amazon.com/ses/latest/dg/quotas.html)
- [Amazon SES pricing](https://aws.amazon.com/ses/pricing/)
- [AWS CLI: sesv2 commands](https://docs.aws.amazon.com/cli/latest/reference/sesv2/)
