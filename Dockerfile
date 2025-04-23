FROM python:3.12.10-slim@sha256:85824326bc4ae27a1abb5bc0dd9e08847aa5fe73d8afb593b1b45b7cb4180f57 AS app_base

# Set up user and group
ARG groupid=10001
ARG userid=10001

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.14@sha256:3362a526af7eca2fcd8604e6a07e873fb6e4286d8837cb753503558ce1213664 /uv /uvx /bin/

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV UV_COMPILE_BYTECODE=1
ENV APP_HOME=/app

# Set working directory
WORKDIR $APP_HOME

RUN groupadd --gid $groupid app \
  && useradd -m -g app --uid $userid -s /usr/sbin/nologin app

# Install dependencies as root
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-managed-python --no-install-project

# Copy local code to the container image
COPY --chown=app:app . $APP_HOME

# Set the PATH environment variable
ENV PATH="$APP_HOME/.venv/bin:$PATH"

# Now create the final context that runs the web api
FROM app_base AS web_api

EXPOSE 8000

USER app

ENTRYPOINT ["/app/script/entrypoint.sh"]
CMD ["web"]
