# -*- coding: utf-8 -*-
import psycopg2.extensions
import select # <= Jarus?

from django.db import connection

def pg_listen(channel):
    crs = connection.cursor()
    pg_con = connection.connection
    pg_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    crs.execute('LISTEN %s;', channel);
 
    while True:
        if select.select([pg_con], [], [], 5) == ([], [], []):
            continue # Timeout
        else:
            pg_con.poll()
            while pg_con.notifies:
                yield pg_con.notifies.pop()

def pg_notify(channel, payload=None):
    crs = connection.cursor()
    connection.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    if payload is None:
        crs.execute('NOTIFY %s;', channel);
    else:
        crs.execute('NOTIFY %s, %s;', channel, payload);
