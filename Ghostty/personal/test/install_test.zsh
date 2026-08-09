#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
project_dir="${script_dir:h}"
test_home="$(mktemp -d)"
remote_test_home="$(mktemp -d)"

cleanup() {
    [[ -n "${test_home:-}" && -d "${test_home}" ]] && rm -rf -- "${test_home}"
    [[ -n "${remote_test_home:-}" && -d "${remote_test_home}" ]] && rm -rf -- "${remote_test_home}"
}
trap cleanup EXIT

destination_dir="${test_home}/Library/Application Support/com.mitchellh.ghostty"
mkdir -p "${destination_dir}"
print 'existing configuration' > "${destination_dir}/config.ghostty"

HOME="${test_home}" "${project_dir}/install.zsh" --skip-packages

cmp "${project_dir}/config.ghostty" "${destination_dir}/config.ghostty"
[[ -f "${test_home}/.config/engineering-ghostty-personal/init.zsh" ]]
/bin/zsh -n "${test_home}/.config/engineering-ghostty-personal/init.zsh"
grep -Fqx '# BEGIN engineering-ghostty-personal' "${test_home}/.zshrc"
grep -Fqx 'source "$HOME/.config/engineering-ghostty-personal/init.zsh"' "${test_home}/.zshrc"

backup_files=("${destination_dir}"/config.ghostty.backup-*(N))
(( ${#backup_files} == 1 ))
grep -q '^existing configuration$' "${backup_files[1]}"

HOME="${test_home}" "${project_dir}/install.zsh" --skip-packages
[[ "$(grep -Fc '# BEGIN engineering-ghostty-personal' "${test_home}/.zshrc")" == 1 ]]
backup_files=("${destination_dir}"/config.ghostty.backup-*(N))
(( ${#backup_files} == 1 ))

(
    cd /tmp
    HOME="${remote_test_home}" /bin/zsh -s -- --skip-packages < "${project_dir}/install.zsh"
)
[[ -f "${remote_test_home}/Library/Application Support/com.mitchellh.ghostty/config.ghostty" ]]
[[ -f "${remote_test_home}/.config/engineering-ghostty-personal/init.zsh" ]]
grep -Fqx '# BEGIN engineering-ghostty-personal' "${remote_test_home}/.zshrc"
/bin/zsh -n "${remote_test_home}/.config/engineering-ghostty-personal/init.zsh"

print 'Ghostty installer test passed'
