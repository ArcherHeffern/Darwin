#!/usr/bin/env bash

set -euo pipefail

mvn -Dtest="$1" surefire:test