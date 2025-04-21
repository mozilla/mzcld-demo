FROM python:3.12.10-slim@sha256:85824326bc4ae27a1abb5bc0dd9e08847aa5fe73d8afb593b1b45b7cb4180f57 AS app_base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.14@sha256:3362a526af7eca2fcd8604e6a07e873fb6e4286d8837cb753503558ce1213664 /uv /uvx /bin/

# Set environment variables
ENV PYTHONUNBUFFERED=True
ENV UV_COMPILE_BYTECODE=1
ENV APP_HOME=/app

# Set working directory
WORKDIR $APP_HOME

RUN groupadd --gid 10001 app \
  && useradd -m -g app --uid 10001 -s /usr/sbin/nologin app

# Copy local code to the container image
COPY . $APP_HOME

# Install maxmind db and app dependencies. Clean up build tools after
RUN apt-get update && \
    apt-get install --yes build-essential && \
    uv sync --frozen --no-cache --no-dev --no-managed-python && \
    apt-get remove --yes build-essential && \
    apt-get -q --yes autoremove && \
    apt-get clean && \
    rm -rf /root/.cache

RUN chown -R app:app $APP_HOME

# Set the PATH environment variable
ENV PATH="$APP_HOME/.venv/bin:$PATH"

# Now create the final context that runs the web api
FROM app_base AS web_api

EXPOSE 8000

USER app

ENTRYPOINT ["uv", "run", "--no-project", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
