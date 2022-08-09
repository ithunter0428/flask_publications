# Flask Project

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Create database

Create a .env file based on .env.example file:

```bash
APP_SETTINGS=config.DevelopmentConfig
DATABASE_URL=postgresql://postgres:password@localhost:5432/publications
```

To create the database, run these commands:

```bash
flask db init
flask db migrate
flask db upgrade
```

## Usage

### Unit tests

```bash
python -m pytest tests/
```

### Run API server

```bash
flask run
```

## Documentation for API Endpoints

All URIs are relative to *http://127.0.0.1:5000/api*

You can see in *https://127.0.0.1/5000/api/doc*