#!/bin/zsh

set -u

failures=0

check() {
    local label="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        printf '%-28s PASS\n' "${label}"
    else
        printf '%-28s FAIL\n' "${label}"
        failures=$((failures + 1))
    fi
}

path_has() {
    command -v "$1" >/dev/null 2>&1 || [[ -x "/opt/homebrew/bin/$1" ]] || [[ -x "/usr/local/bin/$1" ]]
}

ghostty_has_font() {
    /Applications/Ghostty.app/Contents/MacOS/ghostty +list-fonts 2>/dev/null | /usr/bin/grep -Fq 'JetBrainsMono Nerd Font'
}

symlink_points_to() {
    [[ -L "$1" && "$(readlink "$1")" == "$2" ]]
}

check 'macOS' test "$(uname -s)" = Darwin
check 'Apple Command Line Tools' /usr/bin/xcode-select -p
check 'Homebrew' path_has brew
check 'Ghostty' test -x /Applications/Ghostty.app/Contents/MacOS/ghostty
check 'JetBrainsMono Nerd Font' ghostty_has_font
check 'zsh' path_has zsh
for command_name in starship tmux fzf fd rg eza bat glow zoxide git gh; do
    check "${command_name}" path_has "${command_name}"
done
check 'Managed configuration' test -f "${HOME}/.config/engineering-terminal/install-manifest.txt"
check 'Ghostty config link' symlink_points_to "${HOME}/.config/ghostty/config" "${HOME}/.config/engineering-terminal/ghostty/config"
check 'tmux config link' symlink_points_to "${HOME}/.tmux.conf" "${HOME}/.config/engineering-terminal/tmux.conf"
check 'zsh integration' /usr/bin/grep -Fqx '# BEGIN engineering-terminal' "${HOME}/.zshrc"
check 'fzf zsh integration' test -s "${HOME}/.config/engineering-terminal/zsh/generated/fzf.zsh"
check 'Starship zsh integration' test -s "${HOME}/.config/engineering-terminal/zsh/generated/starship.zsh"
check 'zoxide zsh integration' test -s "${HOME}/.config/engineering-terminal/zsh/generated/zoxide.zsh"

if [[ -x /Applications/Ghostty.app/Contents/MacOS/ghostty ]]; then
    check 'Ghostty config validation' /Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
fi

if (( failures > 0 )); then
    print -u2 -- "${failures} check(s) failed. See terminal/README.md troubleshooting guidance."
    exit 1
fi

print -- 'All automated checks passed. Font rendering and interactive shortcuts still require a visual check in Ghostty.'
