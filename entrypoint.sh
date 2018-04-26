#!/usr/bin/sh

set -ev

python3 manage.py collectstatic --no-input --clear -v 1

gunicorn axbot.wsgi:application --workers=4 --log-level=debug --log-file=- --bind "0.0.0.0:8000"
