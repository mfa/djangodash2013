OTRMe - Jabber OTR Web Client
=============================

About
-----

Login using your jabber-account and password.
(And yes we don't have https (yet) :( - so create a new account on a jabber server for testing).

Our minimal webclient is using `OTR <http://otr.cypherpunks.ca/>`_ if available on the other side to encrypt the connection.


Technology
----------

 * Django (obviously)
 * sleekxmpp (for jabber)
 * pure-python-otr (for otr)
 * PostgreSQL (Database and push (sse, NOTIFY))
 * gevent (parallize all things)
 * Bootstrap
 * Angular.js (Frontend stuff)


Installation and usage
----------------------

::

  mkvirtualenv otrme
  workon otrme

  git clone git@github.com:mfa/djangodash2013.git otrme
  cd otrme

  pip install -r requirements.txt

  # change local.py
  # syncdb
  
  # for jabber daemon
  python manage.py run_jabdaemon

  # runserver (gevent based for SSE)
  python runserver.py

