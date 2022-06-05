#!/bin/sh
#python /Users/nancy506/Projects/DE projects/douban_bookTop250_scraper/douban/backend/scraper.py
export FLASK_APP=./douban/index.py
export FLASK_ENV=development
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0 --no-debugger --no-reload