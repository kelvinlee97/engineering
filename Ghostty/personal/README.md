# Personal Ghostty Configuration

This directory is the canonical, version-controlled source for the owner's personal Ghostty configuration on macOS.

## Contents

- `config.ghostty` contains the portable terminal configuration.
- `install.zsh` installs it in Ghostty's macOS application-support directory.
- `test/install_test.zsh` verifies installation and backup behavior in an isolated temporary home directory.

## Requirements

- Ghostty 1.3 or later
- JetBrainsMono Nerd Font
- The bundled `Catppuccin Mocha` Ghostty theme
- zsh

## Install on a new Mac

From this directory, run:

```zsh
./install.zsh
```

If a configuration already exists, the installer creates a timestamped backup beside it before installing the repository version. Fully restart Ghostty after installation so settings that only affect new processes are applied.

## Verify

Run the isolated installer test:

```zsh
./test/install_test.zsh
```

After Ghostty is installed, validate the installed configuration:

```zsh
/Applications/Ghostty.app/Contents/MacOS/ghostty +validate-config
```

## Security boundary

Only portable, personally owned settings belong here. Do not add credentials, shell history, company information, machine-specific paths, or confidential data. Follow applicable employer policies before moving personal configuration from a company-owned computer.
