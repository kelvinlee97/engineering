#!/bin/zsh

set -euo pipefail

readonly managed_dir="${HOME}/.config/engineering-terminal"
readonly zshrc_path="${HOME}/.zshrc"
readonly block_begin='# BEGIN engineering-terminal'
readonly block_end='# END engineering-terminal'
timestamp="$(date +%Y%m%d-%H%M%S).$$"

if [[ -f "${zshrc_path}" ]]; then
    begin_count="$(/usr/bin/grep -Fxc "${block_begin}" "${zshrc_path}" || true)"
    end_count="$(/usr/bin/grep -Fxc "${block_end}" "${zshrc_path}" || true)"
    if [[ "${begin_count}" != "${end_count}" || "${begin_count}" -gt 1 ]]; then
        print -u2 -- "Refusing to uninstall: ${zshrc_path} has unbalanced or duplicated managed markers."
        exit 65
    fi
fi

remove_managed_symlink() {
    local target="$1"
    local expected_prefix="$2"
    if [[ -L "${target}" && "$(readlink "${target}")" == ${expected_prefix}* ]]; then
        /bin/rm -- "${target}"
    fi
}

remove_managed_symlink "${HOME}/.config/ghostty/config" "${managed_dir}/"
remove_managed_symlink "${HOME}/.tmux.conf" "${managed_dir}/"
remove_managed_symlink "${HOME}/.local/bin/terminal-doctor" "${managed_dir}/"
remove_managed_symlink "${HOME}/.local/bin/terminal-uninstall" "${managed_dir}/"

if [[ -f "${zshrc_path}" ]] && /usr/bin/grep -Fqx "${block_begin}" "${zshrc_path}"; then
    /bin/cp -p "${zshrc_path}" "${zshrc_path}.backup-${timestamp}"
    temporary_file="$(mktemp "${TMPDIR:-/tmp}/engineering-zshrc.XXXXXX")"
    /usr/bin/awk -v begin="${block_begin}" -v end="${block_end}" '
        $0 == begin { managed = 1; next }
        $0 == end { managed = 0; next }
        !managed { print }
    ' "${zshrc_path}" > "${temporary_file}"
    /bin/cp "${temporary_file}" "${zshrc_path}"
    /bin/rm -- "${temporary_file}"
fi

print -- "Managed links and the zsh initialization block were removed."
print -- "Configuration and backups remain in ${managed_dir} and beside their original files."
print -- 'Homebrew packages were intentionally not removed.'
