[![CI](https://github.com/christopherkeim/python-ml-template/actions/workflows/cicd.yaml/badge.svg)](https://github.com/christopherkeim/python-ml-template/actions/workflows/cicd.yaml)
![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)
![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

# Python Machine Learning Template

This is a template repository for Python-based Machine Learning web APIs.

This repository is optimized for cloud-native container based deployments.

## Quick Start 🐍 🚀 ✨

```bash
# Clone repository
git clone https://github.com/christopherkeim/python-template.git

cd python-ml-template

# Setup system dependencies
make setup

# Install Python dependencies
make install

# Run the dev server
make dev
```

## Getting Started

This repository is a GitHub Template that you can use to create a new repository for Python-based machine learning web APIs. It comes pre-configured to use Python3.10 with Poetry 1.5.1 as a package manager.

To get started you can:

1. Click the `Use this template` button at the top right of the page. This will let you create a new repository set up with all of the resources in this template.

2. You can also directly clone this repository:

```bash
git clone https://github.com/christopherkeim/python-template.git
```

## Setup

**Note: for the moment I've targeted Ubuntu 20.04/22.04 development environments for automated setup.**

1. Once you have local copy of this repository in your development environment, navigate into this directory and run the `setup.sh` script:

```bash
cd python-ml-template
make setup
```

This will install Poetry 1.5.1 and Python3.10 into your development environment.

## Package Management

2. You can configure any dependencies you'd like using the `pyproject.toml` file:

```toml
[tool.poetry.dependencies]
python = ">=3.10, <3.11"

# DevOps
click = "^8.1.8"
pydantic-settings = "^2.7.0"

# Web
httpx = "^0.28.1"
pydantic = "^2.3.0"
fastapi = "^0.115.6"
uvicorn = "^0.34.0"
slowapi = "^0.1.9"

# Data Science
pandas = "^2.2.3"
numpy = "^2.2.1"
scikit-learn = "^1.6.0"
matplotlib = "^3.10.0"
seaborn = "^0.13.2"
jupyter = "^1.1.1"

# MLOps
wandb = "^0.15.10"
```

## Package Installation

3. Once you're happy with your defined dependencies, you can run `make install` (or `poetry install` directly) to install the Python dependencies for your project into a virtual environment (pre-configured to be placed in your project's directory):

```bash
make install
```

4. This will create a `poetry.lock` file defining exactly what dependencies you're using in development and testing. It's recommended that you check this file into version control so others can recreate this on their machines 💻 and in production 🚀.

## Containerization 🐋

**Resource**: [OWASP Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

By default most systems will run a container as root if a user is not set in the build stage (i.e. with an `USER` directive in the `Dockerfile`) or at runtime (with `--user <username>`).

The Dockerfile included in this repository adds a user `appuser` and switches to that user before running the entry point.

Additionally the Makefile `run` command includes a `--cap-drop all` to drop all Linux kernel capabilities from the container. Required capabilities can be added to this command as needed with `--cap-add <CAPABILITY>`. A list of Linux kernel capabilities and their descriptions for Docker can be found in the [Docker docs](https://docs.docker.com/engine/containers/run/#runtime-privilege-and-linux-capabilities:~:text=Linux%20capability%20options). 

5. To build the container:

```bash
make build
```

6. To run the container:

```bash
make run
```

7. And to do both sequentially:

```bash
make prod
```

## Continuous Integration

You'll want to edit the `README.md` and replace the CI badge with a hook for your specific repository's GitHub Actions CI workflow.

## Continuous Delivery

You can also add a deploy target by editing your `Makefile` or the `cicd.yaml` GitHub Actions workflow file.

## Why Poetry?

As I'm learning more about DevOps and the joys of dependency management in Python projects, I've noticed that Software Engineering and MLOps minded folks tend to like Poetry. There's a few reasons I think Poetry is a solid choice for setting your code up to survive across different environments at the level of dependency management:

1. It allows you to express what primary dependencies you believe your application will work with using the `pyproject.toml` file, and allow for upgrade paths down the road

2. Unlike `pip`, the `poetry.lock` file lets you define exactly what dependencies you're using in development and testing. This means your Python dependency structure can be exactly replicated on other machines, every time.

3. Poetry has very convenient virtual environment management (which we've configured here to be placed within your project directory)
