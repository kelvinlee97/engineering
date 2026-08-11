#!/bin/zsh

set -euo pipefail

readonly script_dir="${0:A:h}"
readonly managed_dir="${HOME}/.config/engineering-terminal"
readonly ghostty_path="${HOME}/.config/ghostty/config"
readonly zshrc_path="${HOME}/.zshrc"
readonly local_bin_dir="${HOME}/.local/bin"
readonly homebrew_install_commit="24173182915f24bdd52a22fd073e421953b2a252"
readonly homebrew_install_url="https://raw.githubusercontent.com/Homebrew/install/${homebrew_install_commit}/install.sh"
readonly homebrew_install_sha256="12479a24be3f5307eecac7cde670fad7118640f031229e964f544b1367b52a41"
readonly block_begin='# BEGIN engineering-terminal'
readonly block_end='# END engineering-terminal'

skip_packages=false
skip_system_checks=false

usage() {
    print -- "Usage: ./install.zsh [--skip-packages] [--skip-system-checks]"
}

for argument in "$@"; do
    case "${argument}" in
        --skip-packages) skip_packages=true ;;
        --skip-system-checks) skip_system_checks=true ;;
        --help|-h) usage; exit 0 ;;
        *) print -u2 -- "Unknown option: ${argument}"; usage >&2; exit 64 ;;
    esac
done

/bin/zsh -n "${script_dir}/config/zsh/init.zsh" "${script_dir}/config/zsh/aliases.zsh"

validate_zshrc_block() {
    [[ -f "${zshrc_path}" ]] || return 0

    local begin_count end_count existing_block expected_block
    begin_count="$(/usr/bin/grep -Fxc "${block_begin}" "${zshrc_path}" || true)"
    end_count="$(/usr/bin/grep -Fxc "${block_end}" "${zshrc_path}" || true)"
    if [[ "${begin_count}" != "${end_count}" || "${begin_count}" -gt 1 ]]; then
        print -u2 -- "Refusing to modify ${zshrc_path}: managed markers are unbalanced or duplicated."
        exit 65
    fi
    if [[ "${begin_count}" == 1 ]]; then
        existing_block="$(/usr/bin/sed -n '/^# BEGIN engineering-terminal$/,/^# END engineering-terminal$/p' "${zshrc_path}")"
        expected_block="${block_begin}"$'\n''source "$HOME/.config/engineering-terminal/zsh/init.zsh"'$'\n'"${block_end}"
        if [[ "${existing_block}" != "${expected_block}" ]]; then
            print -u2 -- "Refusing to modify ${zshrc_path}: the managed block is not recognized."
            exit 65
        fi
    fi
}

validate_zshrc_block

install_managed_file() {
    local source="$1"
    local destination="$2"
    /bin/mkdir -p "${destination:h}"
    /usr/bin/install -m 0644 "${source}" "${destination}"
}

install_managed_executable() {
    local source="$1"
    local destination="$2"
    /bin/mkdir -p "${destination:h}"
    /usr/bin/install -m 0755 "${source}" "${destination}"
}

install_managed_symlink() {
    local source="$1"
    local destination="$2"
    /bin/mkdir -p "${destination:h}"
    if [[ -L "${destination}" && "$(readlink "${destination}")" == "${source}" ]]; then
        return 0
    fi
    /bin/rm -f -- "${destination}"
    /bin/ln -s "${source}" "${destination}"
}

find_brew() {
    if [[ -x /opt/homebrew/bin/brew ]]; then
        print -- /opt/homebrew/bin/brew
    elif [[ -x /usr/local/bin/brew ]]; then
        print -- /usr/local/bin/brew
    else
        return 1
    fi
}

if [[ "${skip_system_checks}" != true ]]; then
    [[ "$(uname -s)" == Darwin ]] || {
        print -u2 -- 'This installer supports macOS only.'
        exit 69
    }
    if ! /usr/bin/xcode-select -p >/dev/null 2>&1; then
        print -- 'Apple Command Line Tools are required. Complete the macOS prompt, then run this installer again.'
        /usr/bin/xcode-select --install || true
        exit 2
    fi
fi

if [[ "${skip_packages}" != true ]]; then
    if ! brew_path="$(find_brew)"; then
        temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/engineering-homebrew-install.XXXXXX")"
        cleanup_homebrew_installer() {
            [[ -n "${temporary_dir:-}" && -d "${temporary_dir}" && "${temporary_dir}" == *engineering-homebrew-install.* ]] || return 1
            /bin/rm -rf -- "${temporary_dir}"
        }
        trap cleanup_homebrew_installer EXIT
        print -- "Downloading the official Homebrew installer pinned to ${homebrew_install_commit}..."
        /usr/bin/curl --fail --show-error --location "${homebrew_install_url}" --output "${temporary_dir}/install.sh"
        print -- "${homebrew_install_sha256}  ${temporary_dir}/install.sh" | /usr/bin/shasum -a 256 --check
        /bin/bash "${temporary_dir}/install.sh"
        cleanup_homebrew_installer
        trap - EXIT
        brew_path="$(find_brew)" || {
            print -u2 -- 'Homebrew installation finished, but brew was not found.'
            exit 1
        }
    fi
    HOMEBREW_NO_INSTALL_CLEANUP=1 "${brew_path}" bundle --file "${script_dir}/Brewfile"
fi

brew_path="$(find_brew 2>/dev/null || true)"
brew_prefix=""
if [[ -n "${brew_path}" ]]; then
    brew_prefix="${brew_path:h:h}"
fi

brew_tool() {
    local tool_name="$1"
    [[ -n "${brew_prefix}" && -x "${brew_prefix}/bin/${tool_name}" ]] || return 1
    print -- "${brew_prefix}/bin/${tool_name}"
}

# Validate tool-specific source configuration before changing user configuration.
if [[ -x /Applications/Ghostty.app/Contents/MacOS/ghostty ]]; then
    /Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config --config-file="${script_dir}/config/ghostty/config"
fi
if tmux_path="$(brew_tool tmux 2>/dev/null)"; then
    validation_socket="engineering-terminal-validate-$$"
    "${tmux_path}" -L "${validation_socket}" -f "${script_dir}/config/tmux.conf" new-session -d
    "${tmux_path}" -L "${validation_socket}" kill-server
fi
if starship_path="$(brew_tool starship 2>/dev/null)"; then
    STARSHIP_CONFIG="${script_dir}/config/starship.toml" TERM=xterm-ghostty "${starship_path}" prompt >/dev/null
fi

install_managed_file "${script_dir}/config/ghostty/config" "${managed_dir}/ghostty/config"
install_managed_file "${script_dir}/config/starship.toml" "${managed_dir}/starship.toml"
install_managed_file "${script_dir}/config/tmux.conf" "${managed_dir}/tmux.conf"
install_managed_file "${script_dir}/config/zsh/init.zsh" "${managed_dir}/zsh/init.zsh"
install_managed_file "${script_dir}/config/zsh/aliases.zsh" "${managed_dir}/zsh/aliases.zsh"
install_managed_executable "${script_dir}/doctor.zsh" "${managed_dir}/bin/doctor.zsh"
install_managed_executable "${script_dir}/uninstall.zsh" "${managed_dir}/bin/uninstall.zsh"

/bin/mkdir -p "${managed_dir}/zsh/generated"
homebrew_integration_path="${managed_dir}/zsh/generated/homebrew.zsh"
if [[ -n "${brew_prefix}" ]]; then
    {
        print -r -- "export ENGINEERING_HOMEBREW_PREFIX=\"${brew_prefix}\""
        print -r -- 'path=("$ENGINEERING_HOMEBREW_PREFIX/bin" $path)'
        print -r -- 'fpath=("$ENGINEERING_HOMEBREW_PREFIX/share/zsh/site-functions" $fpath)'
    } > "${homebrew_integration_path}"
else
    : > "${homebrew_integration_path}"
fi
/bin/chmod 0644 "${homebrew_integration_path}"

for integration_name in fzf starship zoxide; do
    integration_path="${managed_dir}/zsh/generated/${integration_name}.zsh"
    case "${integration_name}" in
        fzf)
            if tool_path="$(brew_tool fzf 2>/dev/null)"; then "${tool_path}" --zsh > "${integration_path}"; else : > "${integration_path}"; fi
            ;;
        starship)
            if tool_path="$(brew_tool starship 2>/dev/null)"; then "${tool_path}" init zsh > "${integration_path}"; else : > "${integration_path}"; fi
            ;;
        zoxide)
            if tool_path="$(brew_tool zoxide 2>/dev/null)"; then "${tool_path}" init zsh > "${integration_path}"; else : > "${integration_path}"; fi
            ;;
    esac
    /bin/chmod 0644 "${integration_path}"
done

install_managed_symlink "${managed_dir}/ghostty/config" "${ghostty_path}"
install_managed_symlink "${managed_dir}/tmux.conf" "${HOME}/.tmux.conf"
install_managed_symlink "${managed_dir}/bin/doctor.zsh" "${local_bin_dir}/terminal-doctor"
install_managed_symlink "${managed_dir}/bin/uninstall.zsh" "${local_bin_dir}/terminal-uninstall"

touch "${zshrc_path}"
if ! /usr/bin/grep -Fqx "${block_begin}" "${zshrc_path}"; then
    {
        [[ ! -s "${zshrc_path}" ]] || print
        print -- "${block_begin}"
        print -- 'source "$HOME/.config/engineering-terminal/zsh/init.zsh"'
        print -- "${block_end}"
    } >> "${zshrc_path}"
fi

{
    print -- "source=${script_dir}"
    print -- "managed_dir=${managed_dir}"
    print -- "ghostty_config=${ghostty_path}"
    print -- "zshrc=${zshrc_path}"
} > "${managed_dir}/install-manifest.txt"

/bin/zsh -n "${managed_dir}/zsh/init.zsh" "${managed_dir}/zsh/aliases.zsh"
if [[ -x /Applications/Ghostty.app/Contents/MacOS/ghostty ]]; then
    /Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
fi

print -- 'Engineering terminal configuration installed.'
print -- "Run ${local_bin_dir}/terminal-doctor to verify the environment."
print -- 'Then open Ghostty and confirm the font, prompt, tabs, and splits.'
