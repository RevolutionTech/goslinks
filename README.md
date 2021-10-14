# Goslinks
#### URL shortener for teams

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

### Deployment

Goslinks is deployed as a `zappa` app on AWS Lambda. To modify the deployment settings, first you will need to decrypt `zappa_settings.json`:

    DECRYPT_PASSWORD=abc123 poetry run inv openssl.decrypt zappa_settings.json

where `DECRYPT_PASSWORD` is assigned to the key that the settings were encrypted with.

Then, generate a Docker container and run the container to execute zappa commands, such as `zappa update`:

    poetry run inv deploy

Once deployed, you will need to set environment variables on the generated Lambda. See `Config` for environment variables used in production. Once completed, the assigned URL should be running Goslinks.

If any changes to `zappa_settings.json` are made, the file should be re-encrypted before being committed. You can use the `openssl` invoke tasks to do this.
