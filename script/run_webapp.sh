#!/bin/bash

# Usage: script/run_webapp.sh [--dev]
#
# Runs the webapp service.
#
# Use the "--dev" argument to run the webapp in a docker container for
# local development.
#
# Note: This should be called from inside the Docker container.

set -euxo pipefail


if [ "${1:-}" == "--dev" ]; then
    echo "******************************************************************"
    echo "Running webapp in local dev environment."
    echo "Connect with your browser using: http://localhost:8000/ "
    echo "******************************************************************"
    exec uv run --no-project fastapi run

else
    exec uv run --no-project uvicorn app.main:app --host 0.0.0.0
fi
