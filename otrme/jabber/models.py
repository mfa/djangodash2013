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
