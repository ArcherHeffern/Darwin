#!/usr/bin/env bash
set -euo pipefail 

rm db || true
fastapi dev application.py