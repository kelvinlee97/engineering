# Personal Codex Configuration

This directory is the canonical, version-controlled source for the owner's personal Codex rules.

## Contents

- `AGENTS.md` contains cross-project behavioral guidelines.
- `ENGINEERING_PHILOSOPHY.md` contains the owner's engineering principles.
- `install.zsh` installs both files into `~/.codex/`.

The copies under `~/.codex/` are runtime files. Update the files in this directory first, commit the change, and then run the installer.

## Install on a new computer

From this directory, run:

```zsh
./install.zsh
```

If either destination file already exists, the installer creates a timestamped backup beside it before installing the repository version.

Start a new Codex task after installation so the new user-level instructions are loaded.

## Security boundary

Only portable, personally owned rules belong here. Do not add:

- credentials, tokens, or login state;
- Codex conversations, logs, or caches;
- employer or client source code;
- confidential internal information;
- machine-specific absolute paths.

Follow applicable employer policies before moving personal configuration from a company-owned computer.
