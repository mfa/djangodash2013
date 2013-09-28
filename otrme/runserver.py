#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otrme.settings.local")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    server = WSGIServer(('0.0.0.0', 8000), application)
    server.serve_forever()
