# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from events.pgnotify import pg_notify
from django.contrib.auth.views import logout as authlogout


class MainView(TemplateView):
    template_name = "layout.html"


def logout(request, *args, **kwargs):
    event_payload = {
        'type': 'disconnect',
        'jid': request.user.username,
    }
    pg_notify(
        'jab-control',
        event_payload
    )
    return authlogout(request, *args, **kwargs)
