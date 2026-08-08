#!/bin/zsh

set -euo pipefail

project_dir="${0:A:h:h}"
repository_dir="${project_dir:h}"

fail() {
    print -u2 -- "FAIL: $1"
    exit 1
}

dangerous_pattern='curl[^|]*\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)|wget[^|]*\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)|chmod[[:space:]]+777|eval[[:space:]]|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+clean[[:space:]]+-'
secret_pattern='AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{30,}'
private_pattern='/Users/[^ <]+|J07VTMVXWL|~/\.aws|~/\.kube'

if rg -n "${dangerous_pattern}" "${project_dir}" -g '!**/test/security_test.zsh'; then
    fail 'dangerous shell pattern found'
fi
if rg -n "${secret_pattern}" "${project_dir}" -g '!**/test/security_test.zsh'; then
    fail 'credential-like value found'
fi
if rg -n "${private_pattern}" "${project_dir}" -g '!**/test/security_test.zsh'; then
    fail 'private machine or cloud path found'
fi
if find "${project_dir}" -type f | /usr/bin/grep -Ei '(^|/)(\.env($|\.)|id_(rsa|ed25519)|.*\.pem$|.*\.key$|credentials$|kubeconfig$|known_hosts$)'; then
    fail 'sensitive filename found'
fi
if rg -n 'command -v brew|engineering_brew_prefixes|\(/opt/homebrew /usr/local\)' "${project_dir}" -g '!**/test/security_test.zsh'; then
    fail 'multiple or PATH-selected Homebrew installations are not allowed'
fi
grep -Fq 'homebrew_install_sha256=' "${project_dir}/install.zsh" || fail 'Homebrew installer checksum is missing'
grep -Fq '/usr/bin/shasum -a 256 --check' "${project_dir}/install.zsh" || fail 'Homebrew installer checksum is not verified'

if git -C "${repository_dir}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git -C "${repository_dir}" diff --check
fi
print -- 'security regression checks passed'
