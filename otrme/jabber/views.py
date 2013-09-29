import json

from django.views.generic import ListView
from django.http import HttpResponse

from .mixins import LoginRequiredMixin
from .models import JabberRoster


class JabberRosterView(LoginRequiredMixin, ListView):
    model = JabberRoster

    def get_queryset(self):
        return self.model.objects.filter(account=self.request.user)

    def get(self, request, *args, **kwargs):
        data = {}
        for element in self.get_queryset():
            data[element.jid] = {}
            for key in ('jid', 'show', 'status'):
                data[element.jid][key] = element.__dict__.get(key)
        return HttpResponse(json.dumps(data))
