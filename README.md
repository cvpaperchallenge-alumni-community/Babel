# Babel

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-blue)](https://github.com/python/mypy)

## Project Organization

```
    ├── .github/               <- GitHub settings.
    │
    ├── data/                  <- Datasets.
    │
    ├── environments/          <- Environment-specific configurations.
    │
    ├── models/                <- Pretrained and serialized models.
    │
    ├── notebooks/             <- Jupyter notebooks.
    │
    ├── outputs/               <- Outputs.
    │
    ├── src/                   <- Python Source code.
    │
    ├── tests/                 <- Test code.
    │
    ├── .dockerignore
    ├── .gitignore
    ├── LICENSE
    ├── Makefile               <- Commands for task automation.
    ├── poetry.lock            <- Auto-generated lock file (do not edit manually).
    ├── poetry.toml            <- Poetry configuration.
    ├── pyproject.toml         <- Main project configuration file.
    └── README.md              <- Top-level README for developers.
```

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://github.com/docker/compose)
