#!/bin/zsh

set -euo pipefail

script_dir="${0:A:h}"
destination_dir="${HOME}/Library/Application Support/com.mitchellh.ghostty"
destination_path="${destination_dir}/config.ghostty"
backup_suffix="$(date +%Y%m%d-%H%M%S).$$"

mkdir -p "${destination_dir}"

if [[ -e "${destination_path}" ]]; then
    cp -p "${destination_path}" "${destination_path}.backup-${backup_suffix}"
fi

install -m 0644 "${script_dir}/config.ghostty" "${destination_path}"

print "Installed personal Ghostty configuration in ${destination_dir}"
