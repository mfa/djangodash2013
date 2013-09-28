# -*- coding: utf-8 -*-
from django_sse.views import BaseSseView
from pgnotify import pg_listen
import json

class PGEventsView(BaseSseView):
    def dispatch(self, request, *args, **kwargs):
        # EventSource /events/ should work for all logged in users,
        # so we should be able to get this from request.user
        # alternatives welcome
        self.pg_channel = request.user.username
        super(self, PGEventsView).dispatch(request, *args, **kwargs)

    def handle_message(self, message):
        # this can be overridden for alternative behavior
        # must return a tuple (sse_channel, message)
        # where message should be json for the frontend
        # and channel should be a channel that has an attached
        # EventSource listener on the client side
        message = json.loads(message)
        return message[0], message[1]

    def iterator(self):
        for message in pg_listen(self.pg_channel):
            message = self.handle_message(message)
            self.sse.add_message(message[0], message[1])
