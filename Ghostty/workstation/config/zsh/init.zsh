export STARSHIP_CONFIG="$HOME/.config/engineering-terminal/starship.toml"

if [[ -f "$HOME/.config/engineering-terminal/private.zsh" ]]; then
    source "$HOME/.config/engineering-terminal/private.zsh"
fi

source "$HOME/.config/engineering-terminal/zsh/generated/homebrew.zsh"

source "$HOME/.config/engineering-terminal/zsh/aliases.zsh"

if [[ -o interactive ]]; then
    source "$HOME/.config/engineering-terminal/zsh/generated/fzf.zsh"
    source "$HOME/.config/engineering-terminal/zsh/generated/zoxide.zsh"
    source "$HOME/.config/engineering-terminal/zsh/generated/starship.zsh"

    [[ -f "${ENGINEERING_HOMEBREW_PREFIX:-}/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]] && source "${ENGINEERING_HOMEBREW_PREFIX}/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
    [[ -f "${ENGINEERING_HOMEBREW_PREFIX:-}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]] && source "${ENGINEERING_HOMEBREW_PREFIX}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

unset ENGINEERING_HOMEBREW_PREFIX
