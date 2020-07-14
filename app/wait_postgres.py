#!/usr/bin/env python3

import psycopg2
from time import sleep


while True:
    try:
        with psycopg2.connect(host='catalog-sql', user='app', dbname='catalog') as con:
            with con.cursor() as cur:
                cur.execute('SELECT * FROM table6 LIMIT 0')
        break
    except psycopg2.OperationalError:
        sleep(1)
        pass

print('POSTGRES IS AVAILABLE')
