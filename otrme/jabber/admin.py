from django.contrib import admin
from .models import JabberConversation, JabberRoster, JabberPresence

admin.site.register(JabberConversation)
admin.site.register(JabberRoster)
admin.site.register(JabberPresence)
