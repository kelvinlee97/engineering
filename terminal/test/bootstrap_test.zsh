#!/bin/zsh

set -euo pipefail

project_dir="${0:A:h:h}"

grep -q '^readonly RELEASE_TAG="v1.0.0"$' "${project_dir}/bootstrap.zsh"
grep -q 'github.com/kelvinlee97/engineering/archive/refs/tags/${RELEASE_TAG}.tar.gz' "${project_dir}/bootstrap.zsh"
grep -q '^brew "glow"$' "${project_dir}/Brewfile"
grep -q 'for command_name in .* glow ' "${project_dir}/doctor.zsh"

if grep -Eq '(refs/heads/main|/main/terminal)' "${project_dir}/bootstrap.zsh"; then
    print -u2 -- 'FAIL: bootstrap must not install from main'
    exit 1
fi

print -- 'bootstrap pinning test passed'
