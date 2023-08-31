# Introduction

How to maintain the change of dimensions in a somewhat historical table for changing dimensions.


# How to run

## Requierements

- [Poetry](https://python-poetry.org/): To handle dependencies.
- psql terminal (or a way to connecto to pg)
  
## Installation

```sh
poetry install
```

## Execution
```sh
docker-compose up -d
```

```
python3 app.py
```

There are several ways to do this, this is just openning a shell and copy pasting scripts (creds are on the python file)
```sh
psql -h 127.0.0.1 -p 5432 -U postgres -W
```

If you copy paste thes scripts by the order you will see how the dimension history table keeps filling up with the correct periods that dimension was valid for.