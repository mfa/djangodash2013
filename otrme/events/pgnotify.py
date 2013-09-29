# -*- coding: utf-8 -*-
import psycopg2.extensions
import select

import json

import psycopg2

from django.conf import settings


connection = psycopg2.connect(database=settings
                              .DATABASES.get('default', {}).get('NAME'),
                              user=settings
                              .DATABASES.get('default', {}).get('USER'),
                              password=settings
                              .DATABASES.get('default', {}).get('PASSWORD'),
                              host=settings
                              .DATABASES.get('default', {}).get('HOST'),
                              port=settings
                              .DATABASES.get('default', {}).get('PORT'))
connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)


def pg_listen(channel):
    crs = connection.cursor()
    crs.execute('LISTEN "%s";' % channel)

    while True:
        if select.select([connection], [], [], 5) == ([], [], []):
            continue  # Timeout
        else:
            connection.poll()
            while connection.notifies:
                yield connection.notifies.pop()


def pg_notify(channel, payload=None):
    # usage for later:
    # channel: the unique user identifier for some connected user
    # payload: json list with 2 elements, first is the sse event, second
    #          is a pk of a jabber.models.JabberMessage object
    # example:
    # pg_notify('testchannel', '["test", "123"]')
    crs = connection.cursor()
    if payload is None:
        crs.execute('NOTIFY "{}";'.format(channel))
    else:
        crs.execute('NOTIFY "{}", %s;'.format(channel), [json.dumps(payload)])
