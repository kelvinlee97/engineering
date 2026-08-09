# Validation Record

Date: 2026-08-09
Status: existing-device verified; local release gates passed; external publication, signed tag, and fresh-device verification remain open

## Environment

- macOS 26.5.2 (25F84), Apple Silicon `arm64`
- Ghostty 1.3.1
- Starship 1.26.0
- tmux 3.7b
- fzf 0.74.2
- fd 10.4.2
- ripgrep 15.2.0
- eza 0.23.5
- bat 0.26.1
- Glow 2.1.2
- zoxide 0.10.0
- Git 2.55.0
- GitHub CLI 2.97.0

## Passed evidence

- Isolated HOME installation with spaces in its path
- Existing `.zshrc` and Ghostty backup preservation
- Second-run idempotency
- Managed-link and bounded-zsh-block uninstall
- Rejection of malformed managed markers before modification
- Rejection of invalid source zsh configuration before target creation
- Ghostty, Starship, tmux, and zsh source validation
- Twenty-five `terminal-doctor` checks
- Real fd, ripgrep, eza, bat, Glow, fzf, zoxide, and tmux scenarios
- Working-tree and precise full-history credential-pattern scans
- Real Ghostty screenshot with visible-content and metadata review
- Final release diff review across 25 files with no precise credential-format match
- Release payload generated from commit `ef2e246`; SHA-256 `54759443266da35a51fe4aecc273acd0cd21bf81517859fbab18058c0ef32edd`
- Bootstrap pinned to commit `c037a2a209f40a1c22711c8ba1f8931c5baeb2b0`; bootstrap SHA-256 `e8f01661e79f11ca29667904193dd6e20e99fce7bea0e547e3499d7ea12105e0`
- Homebrew installer pinned to commit `24173182915f24bdd52a22fd073e421953b2a252` with SHA-256 verification

Historical broad scans matched only non-functional teaching placeholders such as `ghp_your_new_github_token`, `sk-your-openai-key-here`, and a private-key block whose body is `...`. No value matching the precise credential formats survived validation.

## Open release gates

- `v1.0.0` does not exist locally or remotely.
- No Git signing identity is configured; a signed tag cannot yet be produced. GitHub API confirmation of an SSH signing key requires the `admin:ssh_signing_key` scope, which is not granted to the current CLI session.
- ShellCheck 0.11.0 does not support zsh; `zsh -n`, behavior tests, and manual review are the available evidence.
- A fresh personal MacBook Air has not run the released tag.
- Push, tag creation, and GitHub Release require human approval.
