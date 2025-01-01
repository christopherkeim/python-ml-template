# syntax=docker/dockerfile:1


################################################################################
# Base: add non-root user, common environment variables, and system dependencies
# for runtime
################################################################################

FROM python:3.10-buster AS base

RUN groupadd -r appuser && useradd -r -g appuser appuser

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


################################################################################
# Builder: Install build tooling / dependencies and Python dependencies
################################################################################

FROM base AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry Version
    POETRY_VERSION=1.5.1 \
    # Set the location that Poetry will install to
    POETRY_HOME="/opt/poetry" \
    # Configure Poetry to create virtual envs in project, '.venv'
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # Non-interactive
    POETRY_NO_INTERACTION=1 \
    # Cache directory for installs
    POETRY_CACHE_DIR=/tmp/poetry_cache 

RUN apt-get update && apt-get -y install --no-install-recommends \
    curl \
    make \
    gcc \
    pciutils

# For virutal environment copy
WORKDIR /app/

# Copy project pyproject.toml
COPY ./pyproject.toml .

# Runtime dependencies 
RUN pip install poetry && \
    poetry install --no-root && rm -rf ${POETRY_CACHE_DIR}


###############################################################
# Prod: install application into production runtime image
###############################################################

FROM base AS prod

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app/

# Project files (e.g. `/app/src/`, `/app/api/`)
COPY ./src/ src/

EXPOSE 8000

USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
