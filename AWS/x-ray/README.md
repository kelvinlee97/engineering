# AWS X-Ray - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS X-Ray collects data about requests your application serves and provides tools to view, filter, and analyze that data. It shows the full request path through your front end, microservices, databases, and downstream AWS APIs, helping you identify bottlenecks, latency spikes, and errors.

## Key concepts

- **Segments and subsegments**: units of trace data describing work done by a service (or a call within it).
- **Traces**: a complete request path composed of segments/subsegments across services.
- **Service map**: a visual graph of services and calls with latency and error data.
- **Sampling**: control how many requests are traced to manage cost; default rules plus custom rules.
- **Instrumentation**: X-Ray SDKs (Java, Python, Node.js, Go, .NET, Ruby) send segment documents to the X-Ray daemon, which batches and uploads them over UDP.
- **Integrated services**: Lambda, API Gateway, ECS/EKS, EC2, Elastic Beanstalk, and more send trace data automatically with minimal configuration.
- **Trace header**: `X-Amzn-Trace-Id` propagates the trace context between services.

## Common operations (AWS CLI)

```bash
# Get the service graph (recent trace data)
aws xray get-service-graph --start-time 1784332800 --end-time 1784419200

# Summaries and traces
aws xray get-trace-summaries --start-time 1784332800 --end-time 1784419200 \
  --filter-expression 'service("checkout") { fault = true }'
aws xray batch-get-traces --trace-ids <trace-id>

# Groups
aws xray create-group --group-name errors --filter-expression 'fault = true'
aws xray get-groups
```

## Best practices

- Instrument at service boundaries: HTTP clients, AWS SDK calls, and database queries get subsegments automatically with the SDKs.
- Run the X-Ray daemon on EC2/on-premises (it is included on Lambda and Elastic Beanstalk platforms).
- Set sampling rules so high-traffic services trace a representative sample without breaking the budget.
- Use the trace header for propagation across services; keep IDs in your application logs for correlation.
- Store traces you care about longer by exporting to S3; trace data is retained for 30 days by default.
- Review the service map regularly for latency and error hotspots.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No traces visible | Check SDK instrumentation, daemon status, and IAM permissions for the X-Ray service. |
| Missing downstream calls | Verify SDK version and that HTTP/AWS SDK clients are instrumented. |
| Cost too high | Reduce sampling rate or add sampling rules for lower-value endpoints. |
| Trace context lost | Confirm the trace header is propagated across services (proxies/Lambda). |
| Service map gaps | Check which services are instrumented and their Regions. |

## Limits

Trace retention (30 days), segments per trace, and API request rates have quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS X-Ray?](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)
- [AWS X-Ray quotas](https://docs.aws.amazon.com/general/latest/gr/xray.html)
- [AWS X-Ray pricing](https://aws.amazon.com/xray/pricing/)
- [AWS CLI: xray commands](https://docs.aws.amazon.com/cli/latest/reference/xray/)
