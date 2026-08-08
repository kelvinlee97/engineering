#!/bin/zsh

set -euo pipefail

readonly RELEASE_TAG="v1.0.0"
readonly RELEASE_ASSET="engineering-terminal-v1.0.0.tar.gz"
readonly ARCHIVE_URL="https://github.com/kelvinlee97/engineering/releases/download/${RELEASE_TAG}/${RELEASE_ASSET}"
readonly ARCHIVE_SHA256="54759443266da35a51fe4aecc273acd0cd21bf81517859fbab18058c0ef32edd"
temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/engineering-terminal-bootstrap.XXXXXX")"

cleanup() {
    [[ -n "${temporary_dir:-}" && -d "${temporary_dir}" && "${temporary_dir}" == *engineering-terminal-bootstrap.* ]] || return 1
    rm -rf -- "${temporary_dir}"
}
trap cleanup EXIT

print -- "Downloading engineering terminal ${RELEASE_TAG}..."
/usr/bin/curl --fail --show-error --location "${ARCHIVE_URL}" --output "${temporary_dir}/release.tar.gz"
/usr/bin/printf '%s  %s\n' "${ARCHIVE_SHA256}" "${temporary_dir}/release.tar.gz" | /usr/bin/shasum -a 256 --check
/usr/bin/tar -xzf "${temporary_dir}/release.tar.gz" -C "${temporary_dir}"

release_root="${temporary_dir}/engineering-terminal-${RELEASE_TAG}"
[[ -x "${release_root}/install.zsh" ]] || {
    print -u2 -- "Release archive does not contain install.zsh"
    exit 1
}

"${release_root}/install.zsh" "$@"
