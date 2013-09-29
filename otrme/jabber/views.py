import json

from django.views.generic import ListView, View
from django.http import HttpResponse
from django.http import Http404

from events.pgnotify import pg_notify
from .mixins import LoginRequiredMixin
from .models import JabberRoster


class JabberRosterView(LoginRequiredMixin, ListView):
    model = JabberRoster

    def get_queryset(self):
        return self.model.objects.filter(account=self.request.user)

    def get(self, request, *args, **kwargs):
        data = []
        for element in self.get_queryset():
            e = {}
            for key in ('jid', 'show', 'status'):
                e[key] = element.__dict__.get(key)
            data.append(e)
        return HttpResponse(json.dumps(data))


class JabberSendMessageView(LoginRequiredMixin, View):

    def get_queryset(self):
        return self.model.objects.filter(account=self.request.user)

    def post(self, request, *args, **kwargs):
        if not self.kwargs.get('to'):
            raise Http404

        event_payload = {
            'jid': self.request.POST.get('jid'),
            'to_jid': self.kwargs.get('to'),
            'message': self.request.POST.get('message'),
        }
        pg_notify(
            'jab-control',
            ["message", json.dumps(event_payload)]
        )

        return HttpResponse(json.dumps({'success': True}))
