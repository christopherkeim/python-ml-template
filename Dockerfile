# syntax=docker/dockerfile:1


###############################################################
# Set up all our environment variables
###############################################################

FROM python:3.10-buster

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # Poetry Version
    POETRY_VERSION=1.5.1 \
    # Set the location that Poetry will install to
    POETRY_HOME="/opt/poetry" \
    # Configure Poetry to create virtual envs in project, '.venv'
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # Non-interactive for automation
    POETRY_NO_INTERACTION=1 \
    # Append project's directory to PYTHONPATH (allows module imports)
    PYTHONPATH="${PYTHONPATH}:/app/src"

# Prepend Poetry to path
ENV PATH="$POETRY_HOME/bin:$PATH"

###############################################################
# Install system dependencies 
###############################################################

RUN apt-get update && apt-get -y install --no-install-recommends \
    curl \
    make \
    gcc \
    pciutils

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

# Create a directory /app/
WORKDIR /app/

# Copy project pyproject.toml and poetry.lock here to ensure they'll be cached.
COPY ./pyproject.toml .

# Install runtime dependencies with Poetry - uses $POETRY_VIRTUALENVS_IN_PROJECT and
# $POETRY_NO_INTERACTION 
RUN poetry install --no-root

###############################################################
# Install application and define entry point 
###############################################################

# Project files (`/app/src/`, `/app/api/`)
COPY ./src/ src/
COPY ./api/ api/

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "uvicorn", "api.server:app", "--host", "0.0.0.0"]
