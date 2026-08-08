#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
project_dir="${script_dir:h}"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/engineering-terminal-test.XXXXXX")"

cleanup() {
    [[ -n "${test_root:-}" && -d "${test_root}" && "${test_root}" == *engineering-terminal-test.* ]] || return 1
    rm -rf -- "${test_root}"
}
trap cleanup EXIT

fail() {
    print -u2 -- "FAIL: $1"
    exit 1
}

assert_file() {
    [[ -f "$1" ]] || fail "expected file: $1"
}

assert_symlink_to() {
    [[ -L "$1" ]] || fail "expected symlink: $1"
    [[ "$(readlink "$1")" == "$2" ]] || fail "unexpected target for $1"
}

test_home="${test_root}/Home With Spaces"
mkdir -p "${test_home}/.config/ghostty"
print -- 'existing ghostty config' > "${test_home}/.config/ghostty/config"
print -- 'export EXISTING_SETTING=yes' > "${test_home}/.zshrc"

HOME="${test_home}" "${project_dir}/install.zsh" --skip-packages --skip-system-checks

managed_dir="${test_home}/.config/engineering-terminal"
assert_file "${managed_dir}/ghostty/config"
assert_file "${managed_dir}/starship.toml"
assert_file "${managed_dir}/tmux.conf"
assert_file "${managed_dir}/zsh/init.zsh"
assert_file "${managed_dir}/zsh/generated/homebrew.zsh"
assert_file "${managed_dir}/zsh/generated/fzf.zsh"
assert_file "${managed_dir}/zsh/generated/starship.zsh"
assert_file "${managed_dir}/zsh/generated/zoxide.zsh"
assert_file "${managed_dir}/install-manifest.txt"
assert_symlink_to "${test_home}/.config/ghostty/config" "${managed_dir}/ghostty/config"
assert_symlink_to "${test_home}/.local/bin/terminal-doctor" "${managed_dir}/bin/doctor.zsh"
assert_symlink_to "${test_home}/.local/bin/terminal-uninstall" "${managed_dir}/bin/uninstall.zsh"
[[ -x "${managed_dir}/bin/doctor.zsh" ]] || fail 'managed doctor is not executable'
[[ -x "${managed_dir}/bin/uninstall.zsh" ]] || fail 'managed uninstaller is not executable'
[[ "$(grep -Ec '^export ENGINEERING_HOMEBREW_PREFIX=' "${managed_dir}/zsh/generated/homebrew.zsh" || true)" -le 1 ]] || fail 'more than one Homebrew prefix was configured'
grep -q '^export EXISTING_SETTING=yes$' "${test_home}/.zshrc" || fail 'existing zshrc content was lost'
[[ "$(grep -c '^# BEGIN engineering-terminal$' "${test_home}/.zshrc")" == 1 ]] || fail 'managed zsh block missing'
backup_count="$(find "${test_home}/.config/ghostty" -maxdepth 1 -name 'config.backup-*' | wc -l | tr -d ' ')"
[[ "${backup_count}" == 1 ]] || fail 'existing Ghostty config was not backed up exactly once'

HOME="${test_home}" "${project_dir}/install.zsh" --skip-packages --skip-system-checks
[[ "$(grep -c '^# BEGIN engineering-terminal$' "${test_home}/.zshrc")" == 1 ]] || fail 'second install duplicated zsh block'
backup_count="$(find "${test_home}/.config/ghostty" -maxdepth 1 -name 'config.backup-*' | wc -l | tr -d ' ')"
[[ "${backup_count}" == 1 ]] || fail 'second install backed up its own managed symlink'

HOME="${test_home}" "${project_dir}/uninstall.zsh"
[[ ! -L "${test_home}/.config/ghostty/config" ]] || fail 'Ghostty managed symlink was not removed'
[[ ! -L "${test_home}/.local/bin/terminal-doctor" ]] || fail 'doctor managed symlink was not removed'
[[ ! -L "${test_home}/.local/bin/terminal-uninstall" ]] || fail 'uninstaller managed symlink was not removed'
[[ -d "${managed_dir}" ]] || fail 'uninstall should preserve managed files for recovery'
[[ "$(grep -c '^# BEGIN engineering-terminal$' "${test_home}/.zshrc" || true)" == 0 ]] || fail 'managed zsh block was not removed'
grep -q '^export EXISTING_SETTING=yes$' "${test_home}/.zshrc" || fail 'uninstall removed existing zshrc content'

malformed_home="${test_root}/Malformed Home"
mkdir -p "${malformed_home}"
{
    print -- 'export KEEP_BEFORE=yes'
    print -- '# BEGIN engineering-terminal'
    print -- 'export KEEP_AFTER=yes'
} > "${malformed_home}/.zshrc"
set +e
HOME="${malformed_home}" "${project_dir}/install.zsh" --skip-packages --skip-system-checks >/dev/null 2>&1
malformed_status=$?
set -e
[[ "${malformed_status}" != 0 ]] || fail 'installer accepted an unbalanced managed zsh block'
grep -q '^export KEEP_AFTER=yes$' "${malformed_home}/.zshrc" || fail 'malformed zshrc content was damaged'
mkdir -p "${malformed_home}/.config/engineering-terminal/bin" "${malformed_home}/.local/bin"
print -- '#!/bin/zsh' > "${malformed_home}/.config/engineering-terminal/bin/doctor.zsh"
ln -s "${malformed_home}/.config/engineering-terminal/bin/doctor.zsh" "${malformed_home}/.local/bin/terminal-doctor"
set +e
HOME="${malformed_home}" "${project_dir}/uninstall.zsh" >/dev/null 2>&1
malformed_uninstall_status=$?
set -e
[[ "${malformed_uninstall_status}" != 0 ]] || fail 'uninstaller accepted an unbalanced managed zsh block'
[[ -L "${malformed_home}/.local/bin/terminal-doctor" ]] || fail 'uninstaller made partial changes before rejecting malformed zshrc'

invalid_project="${test_root}/invalid-project"
/bin/cp -R "${project_dir}" "${invalid_project}"
print -- 'if broken syntax' >> "${invalid_project}/config/zsh/init.zsh"
invalid_home="${test_root}/Invalid Config Home"
mkdir -p "${invalid_home}"
set +e
HOME="${invalid_home}" "${invalid_project}/install.zsh" --skip-packages --skip-system-checks >/dev/null 2>&1
invalid_status=$?
set -e
[[ "${invalid_status}" != 0 ]] || fail 'installer accepted invalid source configuration'
[[ ! -e "${invalid_home}/.config/engineering-terminal" ]] || fail 'invalid source configuration changed the target home'

print -- 'install and uninstall tests passed'
