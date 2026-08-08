# Troubleshooting

## Apple Command Line Tools are missing

Complete the macOS installer prompt, then rerun `./install.zsh`. The script exits instead of continuing with a partial toolchain.

## Homebrew finished but `brew` is not found

Open a new system Terminal and follow Homebrew's printed shell-environment instructions. Then rerun the installer. The scripts check both `/opt/homebrew` and `/usr/local` without assuming the CPU architecture.

## Existing Oh My Zsh configuration

The installer preserves it and adds the managed block at the end of `.zshrc`. If two prompts or duplicated suggestions appear, inspect the timestamped `.zshrc` backup and remove old theme/plugin initialization manually only after confirming it is personal rather than employer-managed configuration.

## Ghostty does not show the expected configuration

Run:

```zsh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
readlink ~/.config/ghostty/config
```

Fully quit and reopen Ghostty after validation.

## Icons render as boxes

Confirm `font-jetbrains-mono-nerd-font` is installed, then fully restart Ghostty. Font rendering remains a visual check and is not proven by `terminal-doctor` alone.

## Restore previous files

Run `terminal-uninstall`, inspect timestamped `.backup-*` files beside the original targets, and restore only the specific file required. Homebrew packages are preserved deliberately.
