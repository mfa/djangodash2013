from django.db import models
from django.contrib.auth.models import User

VERIFIED_CHOICES = (
    ('uv', 'unverified'),
    ('fv', 'fingerprint verified'),
    ('sv', 'shared secret verified')
)


class JabberConversation(models.Model):

    from_jid = models.ForeignKey(User, related_name='conversations')
    to_jid = models.CharField(max_length=300)
    verified = models.CharField(choices=VERIFIED_CHOICES, max_length=2)


class JabberRoster(models.Model):

    account = models.ForeignKey(User, related_name='roster_items')
    jid = models.CharField(max_length=300)

    @property
    def highest_resource(self):
        x = self.presences.all().order_by('-priority')
        if x:
            return x[0]
        return None


class JabberPresence(models.Model):
    jid = models.ForeignKey(JabberRoster, related_name='presences')

    resource = models.CharField(max_length=300)
    priority = models.IntegerField(default=0)

    show = models.CharField(max_length=300, default='unavailable')
    status = models.CharField(max_length=300, default='')
