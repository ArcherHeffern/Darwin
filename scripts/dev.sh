#!/usr/bin/env bash
set -euo pipefail 

rm db || true

export DEBUG=1
fastapi dev application.py