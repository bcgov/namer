# Namer #
![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

Rapid Name Search

## Dependencies ##

- python (>=3.6)
- node (>=8.2.1)

## Installation ##

### Files ###

Namer requires certain csv files in order to work. It expects these files to be in the `files` directory.
The following files are expected:

* corp-name-data.csv
* corporate_phrase.csv
* descriptive_phrase.csv
* blacklist_phrase.txt
* greylist_phrase.txt

_Note: Please ensure that these files are encoded in either ASCII or UTF-8, and uses LF line endings._

### Docker ###

1. `docker build . -t namer`
2. `docker run --rm -it -p 5000:5000 namer`
3. Visit the URL mentioned after "Serving corporate names on "

### Manual ###

For Namer to work, both the front-end and back-end must be started.

**NPM (Front End)**

1. `cd namer/static/js/app`
2. `npm install`
3. `npm run build`

**Python (Back End)**

1. Change to root repository folder (`cd ../../../..`)
2. `pip install -r requirements.txt`
3. `python namer/wsgi.py`
4. Visit the server on the specified port (5000)

## Tests ##

The tests depend on:

- pytest>=3.2.0
- pytest-cov>=2.5.1
- coverage>=4.4.1

To test the library simply use:

    pytest

_Note:_ Tests are To Be Determined
