# -*- coding: utf-8 -*-
import psycopg2.extensions
import select # <= Jarus?

from django.db import connection

def pg_listen(channel):
    crs = connection.cursor()
    pg_con = connection.connection
    pg_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    crs.execute('LISTEN %s;' % channel);
 
    while True:
        if select.select([pg_con], [], [], 5) == ([], [], []):
            continue # Timeout
        else:
            pg_con.poll()
            while pg_con.notifies:
                yield pg_con.notifies.pop()

def pg_notify(channel, payload=None):
    # usage for later:
    # channel: the unique user identifier for some connected user
    # payload: json list with 2 elements, first is the sse event, second
    #          is a pk of a jabber.models.JabberMessage object
    # example:
    # pg_notify('testchannel', '["test", "123"]')
    crs = connection.cursor()
    connection.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    if payload is None:
        crs.execute('NOTIFY {};'.format(channel));
    else:
        crs.execute('NOTIFY {}, %s;'.format(channel), [payload]);
