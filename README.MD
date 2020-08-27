# Coin Monitor API

## Setup

#### Poetry
Poetry is used for virtual environments / dependency management.
Install it here: https://python-poetry.org/docs/

##### Install dependencies
```shell script
poetry install
```

##### Activate virtual env
```shell script
poetry shell
```

##### Install pre-commit checks
```shell script
pre-commit install
```

## Routes
- `GET /coinList/`: Gets a list of coins
- `GET /marketCap/`: Params: coin_id, date (YYYY/MM/DD), currency

## Scaling
#### Caching
JSON responses are cached per view for one hour, to minimize load on CoinGecko
`/marketCap` views are cached according to combination of query parameters to ensure maximum accuracy
and cache hit rate.

#### Sessions
The CoinGecko client uses Sessions to reuse TCP connections, reducing load on CoinGecko


## Security
- HTTPS (including forced redirect if not in debug mode)
- Input validation of GET parameters
- Validation of downstream data (CoinGecko) using pydantic models
