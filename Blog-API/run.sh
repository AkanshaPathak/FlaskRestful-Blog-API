#!/bin/bash

set -e

gunicorn -b 127.0.0.1:8001 app:app --reload --threads 2 --workers 4 -t 300 -k gevent
