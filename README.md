# Goslinks
#### URL shortener for teams

## Deprecated

This project is no longer being maintained by the owner. Consider switching your team over to [GoLinks](https://www.golinks.io/).

---

![CI](https://github.com/RevolutionTech/goslinks/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/RevolutionTech/goslinks/branch/main/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/goslinks)

## Setup

### Prerequisites

Goslinks uses [DynamoDB](https://aws.amazon.com/dynamodb/) and requires Amazon's [downloadable version](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) for local development.

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Goslinks uses [python-dotenv](https://github.com/theskumar/python-dotenv) to read environment variables in from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://flask.pocoo.org/docs/latest/config/#SECRET_KEY).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run flask migrate
