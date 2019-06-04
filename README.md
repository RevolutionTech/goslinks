# Goslinks
#### URL shortener for teams

[![Build Status](https://travis-ci.com/RevolutionTech/goslinks.svg?branch=master)](https://travis-ci.com/RevolutionTech/goslinks)
[![codecov](https://codecov.io/gh/RevolutionTech/goslinks/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/goslinks)

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

Deployments are done using `zappa`. First, you will need to decrypt the `zappa_settings.json.enc` to `zappa_settings.json`:

    openssl aes-256-cbc -k $DECRYPT_PASSWORD -in zappa_settings.json.enc -out zappa_settings.json -d

where `$DECRYPT_PASSWORD` contains the key that the settings were encrypted with. Then, use `zappa` to deploy to the production environment:

    poetry run zappa deploy

Once deployed, you will need to set environment variables on the generated Lambda, since `.env` is excluded from the package.

If any changes to `zappa_settings.json` are made, the file should be re-encrypted before being committed. The following bash functions may be helpful for encrypting/decrypting:

    function encrypt_openssl () { openssl aes-256-cbc -k $DECRYPT_PASSWORD -in "$1" -out "$1".enc; }
    function decrypt_openssl () { openssl aes-256-cbc -k $DECRYPT_PASSWORD -in "$1".enc -out "$1" -d; }
