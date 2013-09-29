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

        to_jid = self.request.user.roster_items.filter(
            jid=self.kwargs.get('to')
        )[:1]

        if not to_jid:
            raise Exception("JID not in roster!")

        presence = to_jid[0].presences.all().order_by('-resource')[0]
        to_jid_str = "%s/%s" % (to_jid[0].jid, presence.resource)

        event_payload = {
            'type': 'message',
            'jid': self.request.POST.get('jid'),
            'to_jid': to_jid_str,
            'message': self.request.POST.get('message'),
        }
        pg_notify(
            'jab-control',
            event_payload
        )

        return HttpResponse(json.dumps({'success': True}))

class JabberSetFocusView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        print args
        # Jarus
        # something with jab-control and kwargs,get(who) I guess
        return HttpResponse("")
