# Amazon Lex - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Lex V2 is a service for building conversational interfaces (chatbots) using voice and text. It provides natural language understanding (NLU) and automatic speech recognition (ASR), so developers can build, test, and publish bots that understand user intent and fulfill tasks, without deep learning expertise. You pay only for the text or speech requests made.

## Key concepts

- **Bot**: the conversational application; you define the conversation flow in the console or via APIs.
- **Intent**: what the user wants to do (for example, BookAppointment); intents have sample utterances and slots.
- **Slot and slot type**: a variable the bot collects (for example, date, city); slot types can be built-in or custom.
- **Fulfillment**: Lambda functions (or conditional branching) that complete the user's request.
- **Conditional branching**: control conversation flow without writing Lambda code (for bots created after August 17, 2022).
- **Assisted NLU**: LLM-powered intent classification and slot resolution within your configured intents/slots.
- **Multi-Region replication (MRR)**: deploy bots across Regions for availability and disaster recovery.
- **Channels**: publish to web apps, mobile, Facebook Messenger, Slack, Teams, WhatsApp, and more.
- **Integration**: works with Lambda, CloudWatch, and AWS services such as Connect Customer, Comprehend, and Kendra.

## Common operations (AWS CLI)

```bash
# Create a bot, intent, and slot type
aws lexv2-models create-bot --bot-name support-bot \
  --role-arn arn:aws:iam::123456789012:role/lex-role --data-privacy '{"childDirected":false}' \
  --idle-session-ttl-in-seconds 300 --bot-locale-settings '{}'
aws lexv2-models create-intent --bot-id <bot-id> --bot-version DRAFT \
  --locale-id en_US --intent-name BookAppointment \
  --sample-utterances file://utterances.json
aws lexv2-models create-slot-type --bot-id <bot-id> --bot-version DRAFT \
  --locale-id en_US --slot-type-name City --value-selection-setting file://slots.json

# Build and test
aws lexv2-models build-bot-locale --bot-id <bot-id> --bot-version DRAFT --locale-id en_US
aws lexv2-runtime recognize-text --bot-id <bot-id> --bot-alias-id <alias-id> \
  --locale-id en_US --text "Book an appointment"
```

## Best practices

- Start with a few high-value intents and sample utterances; iterate based on conversation logs.
- Use slots with validation and Lambda fulfillment for business logic; use conditional branching for simple flows.
- Monitor bot analytics and CloudWatch logs for fallback/confusion; improve utterances and add edge cases.
- Publish bot versions and aliases; use MRR for multi-Region deployments.
- Secure fulfillment with least-privilege Lambda roles; sanitize user input.
- Combine with Connect Customer for agent escalation and Comprehend for sentiment analysis.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Intent not recognized | Add more sample utterances and check the locale; review conversation logs. |
| Slot not collected | Validate slot prompting/message configuration and slot types. |
| Fulfillment fails | Check the Lambda function, IAM permissions, and timeout settings. |
| Bot not responding in channel | Verify the alias/version deployed to the channel and channel credentials. |
| High fallback rate | Review analytics, improve utterances, and use assisted NLU features. |

## Limits

Bots, intents, slots, versions, and API request rates per account have quotas. See the Amazon Lex endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Lex V2?](https://docs.aws.amazon.com/lexv2/latest/dg/what-is.html)
- [Amazon Lex endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/lex.html)
- [Amazon Lex pricing](https://aws.amazon.com/lex/pricing/)
- [AWS CLI: lexv2-models and lexv2-runtime commands](https://docs.aws.amazon.com/cli/latest/reference/lexv2-models/)
