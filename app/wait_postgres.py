#!/usr/bin/env python3

import logging
from time import sleep

import psycopg2


while True:
    try:
        with psycopg2.connect(host='catalog-sql', user='app', dbname='catalog') as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM table6 LIMIT 0')
        break
    except (psycopg2.OperationalError, psycopg2.errors.UndefinedTable):
        logging.info('Postgres is not available yet')
        sleep(1)

logging.warning('POSTGRES IS AVAILABLE')
