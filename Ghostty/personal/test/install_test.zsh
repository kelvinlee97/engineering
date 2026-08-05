#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
project_dir="${script_dir:h}"
test_home="$(mktemp -d)"
trap 'rm -rf -- "${test_home}"' EXIT

destination_dir="${test_home}/Library/Application Support/com.mitchellh.ghostty"
mkdir -p "${destination_dir}"
print 'existing configuration' > "${destination_dir}/config.ghostty"

HOME="${test_home}" "${project_dir}/install.zsh"

cmp "${project_dir}/config.ghostty" "${destination_dir}/config.ghostty"

backup_files=("${destination_dir}"/config.ghostty.backup-*(N))
(( ${#backup_files} == 1 ))
grep -q '^existing configuration$' "${backup_files[1]}"

print 'Ghostty installer test passed'
