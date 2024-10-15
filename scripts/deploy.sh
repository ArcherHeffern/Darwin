#!/usr/bin/env bash

# Currently running into a bug where it crashes when creating a new database
gunicorn application:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000