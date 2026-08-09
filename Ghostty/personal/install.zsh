#!/bin/zsh

set -euo pipefail

readonly script_dir="${0:A:h}"
readonly managed_dir="${HOME}/.config/engineering-ghostty-personal"
readonly managed_zsh="${managed_dir}/init.zsh"
readonly zshrc_path="${HOME}/.zshrc"
readonly ghostty_dir="${HOME}/Library/Application Support/com.mitchellh.ghostty"
readonly ghostty_path="${ghostty_dir}/config.ghostty"
readonly block_begin='# BEGIN engineering-ghostty-personal'
readonly block_end='# END engineering-ghostty-personal'

skip_packages=false
zshrc_existed=false
[[ -e "${zshrc_path}" || -L "${zshrc_path}" ]] && zshrc_existed=true
for argument in "$@"; do
    case "${argument}" in
        --skip-packages) skip_packages=true ;;
        --help|-h)
            print -- 'Usage: install.zsh [--skip-packages]'
            exit 0
            ;;
        *)
            print -u2 -- "Unknown option: ${argument}"
            exit 64
            ;;
    esac
done

[[ "$(uname -s)" == Darwin ]] || {
    print -u2 -- 'This installer supports macOS only.'
    exit 69
}

timestamp="$(date +%Y%m%d-%H%M%S).$$"

backup_path() {
    local target="$1"
    [[ -e "${target}" || -L "${target}" ]] || return 0
    /bin/cp -pP "${target}" "${target}.backup-${timestamp}"
    print -- "Backed up ${target}"
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

validate_zshrc_block() {
    [[ -f "${zshrc_path}" ]] || return 0
    local begin_count end_count existing_block expected_block
    begin_count="$(/usr/bin/grep -Fxc "${block_begin}" "${zshrc_path}" || true)"
    end_count="$(/usr/bin/grep -Fxc "${block_end}" "${zshrc_path}" || true)"
    if [[ "${begin_count}" != "${end_count}" || "${begin_count}" -gt 1 ]]; then
        print -u2 -- "Refusing to modify ${zshrc_path}: installer markers are unbalanced or duplicated."
        exit 65
    fi
    if [[ "${begin_count}" == 1 ]]; then
        existing_block="$(/usr/bin/awk -v begin="${block_begin}" -v end="${block_end}" '
            $0 == begin { inside = 1 }
            inside { print }
            $0 == end { exit }
        ' "${zshrc_path}")"
        expected_block="${block_begin}"$'\n''source "$HOME/.config/engineering-ghostty-personal/init.zsh"'$'\n'"${block_end}"
        [[ "${existing_block}" == "${expected_block}" ]] || {
            print -u2 -- "Refusing to modify ${zshrc_path}: the existing installer block is not recognized."
            exit 65
        }
    fi
}

validate_zshrc_block

if [[ "${skip_packages}" != true ]]; then
    if ! brew_path="$(find_brew)"; then
        print -- 'Installing Homebrew...'
        /bin/bash -c "$(/usr/bin/curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        brew_path="$(find_brew)" || {
            print -u2 -- 'Homebrew installation finished, but brew was not found.'
            exit 1
        }
    fi

    print -- 'Installing Ghostty, Nerd Font, and command-line tools...'
    "${brew_path}" update
    if "${brew_path}" list --cask ghostty >/dev/null 2>&1; then
        print -- 'Ghostty is already managed by Homebrew.'
    elif [[ -d /Applications/Ghostty.app ]]; then
        print -- 'Ghostty already exists in /Applications; keeping the existing application.'
    else
        "${brew_path}" install --cask ghostty
    fi
    "${brew_path}" install --cask font-jetbrains-mono-nerd-font
    "${brew_path}" install \
        ripgrep fd zoxide tmux fzf eza bat starship glow gh jq tree \
        zsh-autosuggestions zsh-syntax-highlighting
else
    brew_path="$(find_brew 2>/dev/null || true)"
fi

brew_prefix=""
[[ -z "${brew_path:-}" ]] || brew_prefix="${brew_path:h:h}"

/bin/mkdir -p "${managed_dir}" "${ghostty_dir}"

if [[ -f "${script_dir}/config.ghostty" ]]; then
    ghostty_source="${script_dir}/config.ghostty"
else
    ghostty_source="${managed_dir}/config.ghostty"
    /bin/zsh -c 'print -r -- "$1" > "$2"' _ '# Font
font-family = JetBrainsMono Nerd Font
font-size = 12
font-thicken = true
font-thicken-strength = 100

# Appearance
theme = Catppuccin Mocha
window-padding-x = 12
window-padding-y = 12
window-padding-balance = true

# Behavior
macos-titlebar-style = tabs
confirm-close-surface = false
quit-after-last-window-closed = true
cursor-style = bar
cursor-style-blink = true
mouse-hide-while-typing = true
scrollback-limit = 10000000

# Split navigation and creation
keybind = ctrl+shift+h=goto_split:left
keybind = ctrl+shift+l=goto_split:right
keybind = ctrl+shift+j=goto_split:bottom
keybind = ctrl+shift+k=goto_split:top
keybind = ctrl+shift+d=new_split:right
keybind = ctrl+shift+minus=new_split:down
keybind = shift+enter=text:\x1b\r

shell-integration = zsh
shell-integration-features = cursor,sudo,title,path,ssh-env,ssh-terminfo
macos-option-as-alt = left' "${ghostty_source}"
fi

if [[ ! -f "${ghostty_path}" ]] || ! /usr/bin/cmp -s "${ghostty_source}" "${ghostty_path}"; then
    backup_path "${ghostty_path}"
    /usr/bin/install -m 0644 "${ghostty_source}" "${ghostty_path}"
fi

if [[ -f "${managed_zsh}" ]]; then
    backup_path "${managed_zsh}"
fi

{
    print -- '# Generated by engineering Ghostty personal installer.'
    if [[ -n "${brew_prefix}" ]]; then
        print -r -- "eval \"\$(${brew_prefix}/bin/brew shellenv)\""
    fi
    print -r -- 'export STARSHIP_CONFIG="$HOME/.config/starship.toml"'
    print -r -- 'if [[ -o interactive ]]; then'
    print -r -- '  command -v zoxide >/dev/null && eval "$(zoxide init zsh)"'
    print -r -- '  command -v fzf >/dev/null && source <(fzf --zsh)'
    print -r -- '  [[ -f "${HOMEBREW_PREFIX:-}/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]] && source "${HOMEBREW_PREFIX}/share/zsh-autosuggestions/zsh-autosuggestions.zsh"'
    print -r -- '  command -v starship >/dev/null && eval "$(starship init zsh)"'
    print -r -- '  [[ -f "${HOMEBREW_PREFIX:-}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]] && source "${HOMEBREW_PREFIX}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"'
    print -r -- 'fi'
    print -r -- 'alias ll="eza -lah --git"'
    print -r -- 'alias preview="bat --style=numbers,changes"'
} > "${managed_zsh}"
/bin/chmod 0644 "${managed_zsh}"
/bin/zsh -n "${managed_zsh}"

touch "${zshrc_path}"
if ! /usr/bin/grep -Fqx "${block_begin}" "${zshrc_path}"; then
    [[ "${zshrc_existed}" != true ]] || backup_path "${zshrc_path}"
    {
        [[ ! -s "${zshrc_path}" ]] || print
        print -- "${block_begin}"
        print -- 'source "$HOME/.config/engineering-ghostty-personal/init.zsh"'
        print -- "${block_end}"
    } >> "${zshrc_path}"
fi

if [[ -x /Applications/Ghostty.app/Contents/MacOS/ghostty ]]; then
    /Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config --config-file="${ghostty_path}"
fi

print
print -- 'Installation complete. Open a new Ghostty window to use the environment.'
print -- 'Installed commands: rg fd zoxide tmux fzf eza bat starship glow gh jq tree'
print -- 'Useful first commands: z <directory>, rg <text>, fd <name>, tmux, ll'
