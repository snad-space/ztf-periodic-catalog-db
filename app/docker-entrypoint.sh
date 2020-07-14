#!/bin/bash

python3 /wait_postgres.py

gunicorn -w4 -b0.0.0.0:80 app:app
