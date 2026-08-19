# AWS CodeArtifact - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS CodeArtifact is a managed artifact repository service for storing and sharing software packages. It works with popular package managers (npm, yarn, pip, twine, Maven, Gradle, NuGet), supports private packages and external connections to public repositories, and has no limits on the number or total size of packages you store.

## Key concepts

- **Domain**: the top-level container that groups repositories and provides organizational boundaries and policy; use one production domain with one or more repositories.
- **Repository**: a polyglot collection of packages (any supported package type); repositories are members of exactly one domain.
- **Upstream repository**: makes packages from one repository available to another repository in the same domain, including packages fetched via external connections.
- **External connection**: links a repository to a public repository (npmjs.com, Maven Central, PyPI, NuGet Gallery); packages are fetched and stored on demand.
- **Authentication**: users authenticate with authorization tokens created from AWS credentials; packages cannot be made publicly available.
- **Package managers**: npm/yarn/pip/twine/Maven/Gradle/NuGet publish and consume from repository endpoint URLs.

## Common operations (AWS CLI)

```bash
# Create domain and repository
aws codeartifact create-domain --domain my-org
aws codeartifact create-repository --domain my-org --repository shared

# Get an auth token (for package manager config)
aws codeartifact get-authorization-token --domain my-org \
  --domain-owner 123456789012 --query authorizationToken --output text

# Publish a package (npm example)
npm publish --registry https://my-org-123456789012.d.codeartifact.us-east-1.amazonaws.com/npm/shared/

# Manage packages
aws codeartifact list-packages --domain my-org --repository shared
aws codeartifact list-package-versions --domain my-org --repository shared \
  --package my-pkg --format npm
aws codeartifact delete-package --domain my-org --repository shared \
  --format npm --package my-pkg
```

## Best practices

- Use one production domain per organization and separate repositories per team/project.
- Connect repositories to public sources as upstreams so builds never depend on a single internet source; control which versions flow in.
- Use resource policies on domains to control cross-account access; apply least-privilege IAM.
- Rotate authorization tokens automatically in CI/CD; never commit tokens.
- Enable external connection caching and monitor package versions; remove unneeded versions.
- Log package activity with CloudTrail for audit.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Package manager auth failed | Get a fresh authorization token and verify the repository endpoint/region. |
| Cannot publish | Check IAM permissions (`codeartifact:PublishPackageVersion`) and repository policies. |
| Upstream package missing | Verify the upstream repository configuration and external connection status. |
| npm/yarn cache stale | Clear the local package manager cache or bump the version. |
| Cross-account access denied | Confirm the domain resource policy grants the consuming account and the token uses the correct domain owner. |

## Limits

Domains and repositories per account, upstream repositories per repository, and API request rates have quotas. See the AWS CodeArtifact quotas page and Service Quotas console for current values.

## Official references

- [What is AWS CodeArtifact?](https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html)
- [AWS CodeArtifact quotas](https://docs.aws.amazon.com/codeartifact/latest/ug/service-limits.html)
- [AWS CodeArtifact pricing](https://aws.amazon.com/codeartifact/pricing/)
- [AWS CLI: codeartifact commands](https://docs.aws.amazon.com/cli/latest/reference/codeartifact/)
