#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otrme.settings.local")

    from django.core.wsgi import get_wsgi_application

    # Add dj_static middleware to serve statics
    from dj_static import Cling
    application = Cling(get_wsgi_application())

    print "Runserver on 0.0.0.0:8000"
    server = WSGIServer(('0.0.0.0', 8000), application)
    server.serve_forever()
