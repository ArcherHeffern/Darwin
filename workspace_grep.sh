#!/usr/bin/env bash

set -euo pipefail

fd -t d --max-depth=1 '^\d' workspace \
    --exec sh -c 'printf "Processing: %s\n" "$0"; grep -rin --include='*.java' "$1" "$0"; printf "\n\n"' {} "$1"
