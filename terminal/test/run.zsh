#!/bin/zsh

set -euo pipefail

test_dir="${0:A:h}"

for test_file in "${test_dir}"/*_test.zsh; do
    /bin/zsh "${test_file}"
done
