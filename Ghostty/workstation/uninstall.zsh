#!/bin/zsh

set -euo pipefail

readonly managed_dir="${HOME}/.config/engineering-terminal"
readonly zshrc_path="${HOME}/.zshrc"
readonly block_begin='# BEGIN engineering-terminal'
readonly block_end='# END engineering-terminal'

validate_zshrc_block() {
    [[ -f "${zshrc_path}" ]] || return 0

    local begin_count end_count existing_block expected_block
    begin_count="$(/usr/bin/grep -Fxc "${block_begin}" "${zshrc_path}" || true)"
    end_count="$(/usr/bin/grep -Fxc "${block_end}" "${zshrc_path}" || true)"
    if [[ "${begin_count}" != "${end_count}" || "${begin_count}" -gt 1 ]]; then
        print -u2 -- "Refusing to uninstall: managed markers are unbalanced or duplicated."
        exit 65
    fi
    if [[ "${begin_count}" == 1 ]]; then
        existing_block="$(/usr/bin/sed -n '/^# BEGIN engineering-terminal$/,/^# END engineering-terminal$/p' "${zshrc_path}")"
        expected_block="${block_begin}"$'\n''source "$HOME/.config/engineering-terminal/zsh/init.zsh"'$'\n'"${block_end}"
        if [[ "${existing_block}" != "${expected_block}" ]]; then
            print -u2 -- "Refusing to uninstall: the managed block is not recognized."
            exit 65
        fi
    fi
}

validate_zshrc_block

if [[ -f "${zshrc_path}" ]] && /usr/bin/grep -Fqx "${block_begin}" "${zshrc_path}"; then
    temporary_file="$(mktemp "${TMPDIR:-/tmp}/engineering-zshrc.XXXXXX")"
    /usr/bin/sed '/^# BEGIN engineering-terminal$/,/^# END engineering-terminal$/d' "${zshrc_path}" > "${temporary_file}"
    /bin/cp "${temporary_file}" "${zshrc_path}"
    /bin/rm -- "${temporary_file}"
fi

remove_managed_symlink() {
    local target="$1"
    local expected_target="$2"
    if [[ -L "${target}" && "$(readlink "${target}")" == "${expected_target}" ]]; then
        /bin/rm -f -- "${target}"
    fi
}

remove_managed_symlink "${HOME}/.config/ghostty/config" "${managed_dir}/ghostty/config"
remove_managed_symlink "${HOME}/.tmux.conf" "${managed_dir}/tmux.conf"
remove_managed_symlink "${HOME}/.local/bin/terminal-doctor" "${managed_dir}/bin/doctor.zsh"
remove_managed_symlink "${HOME}/.local/bin/terminal-uninstall" "${managed_dir}/bin/uninstall.zsh"

print -- "Managed links and the zsh initialization block were removed."
print -- "Managed configuration remains in ${managed_dir}."
print -- 'Homebrew packages were intentionally not removed.'
