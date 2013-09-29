from django.conf import settings
from django.contrib.auth.models import User, check_password
from events.pgnotify import pg_notify

from sleekxmpp import ClientXMPP
import logging

class JabberAuthCheckClient(ClientXMPP):

    def __init__(self, jid, password):
        self.authenticated = False
        super(JabberAuthCheckClient, self).__init__(jid, password)

        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("session_start", self.session_start)

    def failed_auth(self, data):
        self.authenticated = False
        self.disconnect()

    def session_start(self, event):
        self.authenticated = True
        self.disconnect()


class JabberAuthBackend(object):
    """
    Authenticate against remote Jabber server.
    """

    def authenticate(self, username=None, password=None):
        logging.basicConfig(level=logging.DEBUG)

        if '@' not in username:
            return None

        client = JabberAuthCheckClient(username, password)
        if client.connect(reattempt=False):
            client.process(block=True)
            if client.authenticated:
                # Yes authenticated!

                # create user
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username,
                                password='WeDontSavePasswords!')
                    user.save()

                # and login on backgroud daemon
                event_payload = {
                    'type': 'connect',
                    'jid': username,
                    'password': password,
                }
                pg_notify(
                    'jab-control',
                    event_payload
                )

                return user
            else:
                # Auth at jabber server failed
                return None
        else:
            # Connection to jabber server failed
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
