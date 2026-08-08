# Security and Publishing

This public repository contains rebuild instructions, never private machine state.

## Release blockers

A release is blocked by:

- any confirmed credential, private key, cloud configuration, company information, or private machine path;
- any Critical or High security finding;
- an unresolved Medium finding without an explicit documented acceptance decision;
- an installer path that can delete outside a validated temporary or managed target;
- an unpinned stable remote-execution URL;
- a failed backup, idempotency, uninstall, or configuration-validation test.

## Review order

1. Run `./test/run.zsh`.
2. Parse every shell file with `zsh -n` and review static-analysis findings.
3. Scan the working tree and complete Git history for secrets and sensitive filenames.
4. Inspect image pixels, visible terminal text, and metadata.
5. Review dependency sources, Homebrew names, the pinned Homebrew commit, and release URLs.
6. Complete the repository security scan and record its report and coverage gaps.
7. Inspect the final Git diff before committing.
8. Create a signed, immutable version tag only after human approval.

## Data that must never be published

- API tokens, passwords, private keys, certificates, `.env` files, or shell history
- AWS profiles, account identifiers, kubeconfig, cluster names, SSH targets, or internal domains
- employer/client code, logs, tickets, hostnames, paths, or screenshots
- personal Git signing keys or GitHub authentication state

## Release evidence

Record the commit SHA, signed tag, validation date, tested macOS version, hardware architecture, tool versions, test results, scan coverage, and accepted limitations. Existing-device testing must not be relabeled as fresh-device testing.
