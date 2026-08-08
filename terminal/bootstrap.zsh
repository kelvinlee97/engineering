#!/bin/zsh

set -euo pipefail

readonly RELEASE_TAG="v1.0.0"
readonly ARCHIVE_URL="https://github.com/kelvinlee97/engineering/archive/refs/tags/${RELEASE_TAG}.tar.gz"
temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/engineering-terminal-bootstrap.XXXXXX")"

cleanup() {
    [[ -n "${temporary_dir:-}" && -d "${temporary_dir}" && "${temporary_dir}" == *engineering-terminal-bootstrap.* ]] || return 1
    rm -rf -- "${temporary_dir}"
}
trap cleanup EXIT

print -- "Downloading engineering terminal ${RELEASE_TAG}..."
/usr/bin/curl --fail --show-error --location "${ARCHIVE_URL}" --output "${temporary_dir}/release.tar.gz"
/usr/bin/tar -xzf "${temporary_dir}/release.tar.gz" -C "${temporary_dir}"

release_root="${temporary_dir}/engineering-${RELEASE_TAG#v}"
[[ -x "${release_root}/terminal/install.zsh" ]] || {
    print -u2 -- "Release archive does not contain terminal/install.zsh"
    exit 1
}

"${release_root}/terminal/install.zsh" "$@"
