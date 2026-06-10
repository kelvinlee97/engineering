#!/bin/bash

# Status line script mimicking Oh My Zsh agnoster theme
# Shows: current directory > git branch > model > effort

# Read JSON input from stdin
input=$(cat)

# Extract relevant information from JSON
cwd=$(echo "$input" | jq -r '.cwd // .workspace.current_dir // empty')
if [ -z "$cwd" ]; then
    cwd=$(pwd)
fi

# Get model info from JSON input
model_name=$(echo "$input" | jq -r '.model.id // "unknown"')

# Get effort from settings.json (reasoningEffort field)
# Possible values: low, medium, high, xhigh
settings_file="$HOME/.codebuddy/settings.json"
if [ -f "$settings_file" ]; then
    effort=$(jq -r '.reasoningEffort // "xhigh"' "$settings_file")
else
    effort="xhigh"
fi

# Powerline symbols (using Unicode characters)
sep=""
sep_thin=""
git_branch=""

# Build the status line
# Section 1: current directory
# Shorten home directory to ~
short_cwd="${cwd/#$HOME/\~}"
printf " %s " "$short_cwd"

# Section 2: git branch (if in a git repo)
if git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --short HEAD 2>/dev/null)

    if [ -n "$branch" ]; then
        printf " %s %s " "$sep_thin" "$git_branch $branch"
    fi
fi

# Section 3: model
printf " %s %s " "$sep_thin" "$model_name"

# Section 4: effort
printf " %s %s " "$sep_thin" "$effort"

# Section 5: context usage bar (if available)
ctx_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$ctx_pct" ]; then
    # Build 10-char progress bar with awk (portable, no color)
    bar_data=$(echo "$ctx_pct" | awk '{
        n = int($1 / 10); if (n > 10) n = 10; if (n < 0) n = 0;
        bar = ""; for (i = 1; i <= n; i++) bar = bar "█";
        empty = ""; for (i = 1; i <= 10 - n; i++) empty = empty "░";
        printf "%s|%s", bar, empty;
    }')
    bar=$(echo "$bar_data" | cut -d'|' -f1)
    empty=$(echo "$bar_data" | cut -d'|' -f2)
    printf " %s %s%s %s%%" "$sep_thin" "$bar" "$empty" "$ctx_pct"
fi

# Add the final separator
printf " %s" "$sep"

echo
