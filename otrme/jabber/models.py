from django.db import models

# Create your models here.

class JabberUser(models.Model):
    username = models.CharField(max_length=256)
    domainname = models.CharField(max_length=256)

    @property
    def jid(self):
        return "%s@%s" % (self.username, self.domainname)

    def __unicode__(self):
        return self.jid
