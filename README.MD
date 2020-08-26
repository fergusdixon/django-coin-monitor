# Coin Monitor API

## Setup

### Poetry
Poetry is used for virtual environments / dependency management.
Install it here: https://python-poetry.org/docs/

##### Install dependencies
```bash
poetry install
```

##### Activate virtual env
```bash
poetry shell
```

##### Install pre-commit checks
```
pre-commit install
```

## Caching
Response are cached for 1 hour to reduce strain on the 3rd party API
