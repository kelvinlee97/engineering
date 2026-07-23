#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
destination_dir="${HOME}/.codex"
backup_suffix="$(date +%Y%m%d-%H%M%S).$$"
files=(AGENTS.md ENGINEERING_PHILOSOPHY.md)

mkdir -p "${destination_dir}"

for file_name in "${files[@]}"; do
    source_path="${script_dir}/${file_name}"
    destination_path="${destination_dir}/${file_name}"

    if [[ -e "${destination_path}" ]]; then
        cp -p "${destination_path}" "${destination_path}.backup-${backup_suffix}"
    fi

    install -m 0644 "${source_path}" "${destination_path}"
done

print "Installed personal Codex configuration in ${destination_dir}"
