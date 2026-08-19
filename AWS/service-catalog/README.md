# AWS Service Catalog - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Service Catalog lets organizations create and manage catalogs of approved IT services, from single resources (AMI-based servers, databases, software) to complete multi-tier application architectures. Administrators assemble portfolios with constraints and access control; end users discover and self-service provision only the approved products.

## Key concepts

- **Product**: an IT service that users can provision; products are built from CloudFormation templates (or Terraform open source) and can have multiple versions.
- **Portfolio**: a collection of products plus constraints (launch, template, stack-set, notification constraints) and resource tags; access to portfolios is granted via IAM users/groups/roles.
- **Provisioned product**: an instance of a product launched by a user; supports update and termination.
- **Self-service discovery**: end users browse the products and portfolios they have access to and launch them without direct access to the underlying AWS services.
- **Version control and reuse**: one product can be added to many portfolios; updating the product version propagates to all portfolios that reference it.
- **Service actions and budgets**: run predefined operations on provisioned products and attach budget constraints.

## Common operations (AWS CLI)

```bash
# Product and portfolio
aws servicecatalog create-product --name web-app --owner platform \
  --product-type CLOUD_FORMATION_TEMPLATE \
  --provisioning-artifact-parameters file://artifact.json
aws servicecatalog create-portfolio --display-name Platform --provider-name eng

# Associate and constrain
aws servicecatalog associate-product-with-portfolio \
  --product-id <product-id> --portfolio-id <portfolio-id>
aws servicecatalog create-constraint \
  --portfolio-id <portfolio-id> --product-id <product-id> \
  --type LAUNCH --parameters file://launch-constraint.json

# Provision and manage
aws servicecatalog provision-product --product-id <product-id> \
  --provisioning-artifact-id <artifact-id> \
  --provisioned-product-name web-01 \
  --provisioning-parameters file://params.json
aws servicecatalog list-provisioned-products
aws servicecatalog terminate-provisioned-product --provisioned-product-id <pp-id>
```

## Best practices

- Treat products as versioned artifacts: test a new version in a lower environment before making it available in production portfolios.
- Enforce governance with launch constraints (instance type limits, IAM role), template constraints, and stack-set constraints for multi-account rollout.
- Grant portfolios to groups/roles instead of individuals; use tag options for consistent resource tagging.
- Use budgets to alert on provisioned product spend.
- Review the catalog periodically: retire unused products and versions, and audit provisioned products.
- Integrate with Control Tower Account Factory and Organizations for governed account-level provisioning.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| User cannot see a product | Check portfolio association, IAM access to the portfolio, and product version availability. |
| Provisioning fails | Review CloudFormation stack events, launch constraint role permissions, and parameter validation. |
| Update not applied | Confirm the new provisioning artifact is associated and the provisioned product was updated. |
| Constraint not enforced | Verify the constraint is attached to the right portfolio/product combination. |
| Cannot terminate | Some products require a termination constraint/role; check IAM and stack state. |

## Limits

Products, portfolios, constraints, and provisioned products per account have quotas. See the AWS Service Catalog endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Service Catalog?](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html)
- [AWS Service Catalog quotas](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/limits.html)
- [AWS Service Catalog pricing](https://aws.amazon.com/servicecatalog/pricing/)
- [AWS CLI: servicecatalog commands](https://docs.aws.amazon.com/cli/latest/reference/servicecatalog/)
