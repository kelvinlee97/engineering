# AWS Well-Architected Framework - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

The AWS Well-Architected Framework is a set of best practices for designing and operating reliable, secure, efficient, and cost-effective workloads in the cloud. The AWS Well-Architected Tool (AWS WA Tool) provides a consistent process to document decisions, answer review questions, and get recommendations for improvement across the six pillars.

## Key concepts

- **Six pillars**:
  1. **Operational excellence**: run and monitor systems, and continuously improve processes.
  2. **Security**: protect data, systems, and assets; apply identity, detective, and infrastructure protection.
  3. **Reliability**: recover from failures, scale, and meet demand; design for availability and durability.
  4. **Performance efficiency**: use computing resources efficiently to meet requirements.
  5. **Cost optimization**: avoid unnecessary cost and maximize value.
  6. **Sustainability**: minimize environmental impacts of cloud workloads.
- **AWS WA Tool**: document a workload, answer pillar questions with evidence, and receive high/medium risk improvement plans.
- **Lenses**: AWS-provided lenses (for example, serverless, SaaS, HPC) and custom lenses you define for your own best practices.
- **Review process**: regular workload reviews across the lifecycle, with improvements tracked in the tool.
- **Integrations**: Trusted Advisor and Service Catalog AppRegistry help gather the information needed to answer review questions.

## Common operations (AWS CLI)

```bash
# Create a workload and run a review
aws wellarchitected create-workload --client-request-token demo \
  --workload-name prod-workload --environment PRODUCTION \
  --review-owner owner@example.com --lenses "arn:aws:wellarchitected::aws:lens/wellarchitected"
aws wellarchitected list-workloads
aws wellarchitected get-workload --workload-id <workload-id>

# Add an answer and get improvement plan
aws wellarchitected update-answer --workload-id <workload-id> \
  --lens-alias wellarchitected --question-id reliability \
  --selected-choices <choice-id>
aws wellarchitected get-lens-review --workload-id <workload-id> \
  --lens-alias wellarchitected
```

## Best practices

- Run a Well-Architected review at design time and at meaningful milestones (new major features, scaling events).
- Attach evidence (architecture diagrams, dashboards, runbooks) to answers so decisions are documented.
- Prioritize high-risk items; turn recommendations into tracked improvement tasks with owners.
- Combine pillars with the Well-Architected Tool's improvement plan and review regularly.
- Use appropriate lenses for your workload type (serverless, SaaS, etc.) and custom lenses for internal governance.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Workload not visible | Confirm the AWS account/Region and IAM permissions (`wellarchitected:*`). |
| Answers not saving | Check the workload/lens IDs and that choices are valid for the question. |
| No improvement plan | Answer all applicable questions; the plan is generated from answered risks. |
| Custom lens missing | Publish/share the custom lens and grant access to the workload owners. |

## Limits

Workloads and custom lenses per account have quotas. See the AWS Well-Architected Tool endpoints and quotas page and Service Quotas console for current values.

## Official references

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Well-Architected Tool user guide](https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html)
- [AWS Well-Architected Tool pricing](https://aws.amazon.com/well-architected-tool/pricing/)
- [AWS CLI: wellarchitected commands](https://docs.aws.amazon.com/cli/latest/reference/wellarchitected/)
