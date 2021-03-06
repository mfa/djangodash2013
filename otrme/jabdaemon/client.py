import json
import logging

from sleekxmpp import ClientXMPP

from events.pgnotify import pg_notify
from otrbackend.magic import OTRContextManager, OTRContext
from django.utils.timezone import now
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from jabber.models import JabberRoster, JabberPresence


class XMPPOTRContext(OTRContext):

    def __init__(self, user, other, xmpp_client):
        super(XMPPOTRContext, self).__init__(user, other)
        self.xmpp_client = xmpp_client

    def inject(self, msg, appdata=None):
        # This method send some message from account to the target peer
        logging.getLogger().debug('Call inject; %s => %s; %s',
                                  self.user, self.peer, msg)
        self.xmpp_client.send_message(mto=self.peer, mbody=msg)

    def start_otr(self):
        inv_msg = self.sendMessage(self.getPolicy('ALLOW_V2'), '')
        self.inject(inv_msg)


class XMPPOTRContextManager(OTRContextManager):

    def __init__(self, xmpp_client):
        super(XMPPOTRContextManager, self).__init__(unicode(xmpp_client.jid))
        self.xmpp_client = xmpp_client

    def context_to(self, other):
        if other not in self.contexts:
            # No context already for other than create a new context
            self.contexts[other] = XMPPOTRContext(self.account, other,
                                                  self.xmpp_client)
        return self.contexts[other]


class OTRMeClient(ClientXMPP):

    def __init__(self, jid, password):
        self.django_user = User.objects.get(username=jid)

        super(OTRMeClient, self).__init__(jid, password)
        self.resource = 'OTRMe'

        self.otr = XMPPOTRContextManager(self)

        self.register_plugin('xep_0054')  # vCard support

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.changed_status)
        self.add_event_handler("roster_update", self.roster_update)

    def session_start(self, event):
        # Request roster
        self.get_roster(block=True)

        self.send_presence(pshow="chat", pstatus="Using OTRMe!", ppriority=20)

    def message(self, msg):
        plain_msg, was_encrypted = self.otr.incoming({
            'from': unicode(msg['from']),
            'type': unicode(msg['type']),
            'body': unicode(msg['body']).encode('utf8')
        })

        context = self.otr.context_to(unicode(msg['from']))
        if msg['type'] in ('chat', 'normal'):
            if was_encrypted:
                message_text = plain_msg[0]
            else:
                message_text = plain_msg

            if message_text is None:
                return

            event_payload = {
                # for now, until we know how to get the name
                'name': msg['from'].bare,
                'jid': msg['from'].bare,
                'resource': msg['from'].resource,
                'message': strip_tags(message_text),
                'time':  now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                'otr_state': context.state
            }
            pg_notify(
                'events/%s' % unicode(self.boundjid.bare),
                ["message", json.dumps(event_payload)]
            )

    def changed_status(self, presence):
        print "-" * 80
        print presence

        if presence['type'] == 'unavailable':
            show = 'unavailable'
        elif presence['show'] == '':
            show = 'available'
        else:
            show = presence['show']

        if show != 'unavailable':
            status = presence['status']
        else:
            status = ''

        roster_item = self.django_user.roster_items.get_or_create(
            jid=presence['from'].bare,
        )[0]

        _presence, created = JabberPresence.objects.get_or_create(
            jid=roster_item,
            resource=presence['from'].resource,
            priority=presence['priority']
        )

        _presence.show = show
        _presence.status = status
        _presence.save()

        # Check was the presence update of the highest resource for this
        # roster item than notify frontend about status change
        highest_resource = roster_item.highest_resource

        print highest_resource.pk
        print _presence.pk

        if highest_resource.pk == _presence.pk:
            pg_notify(
                'events/%s' % unicode(self.boundjid.bare),
                ["status_changed", json.dumps({
                    'jid': presence['from'].bare,
                    'show': show,
                    'status': presence['status']
                })]
            )

        print "-" * 80

    def roster_update(self, event):
        roster = self.client_roster

        JabberRoster.objects.filter(account=self.django_user) \
                            .exclude(jid__in=roster.keys()).delete()

        current_jids = self.django_user.roster_items.all() \
                                       .values_list('jid', flat=True)

        for jid in self.client_roster:
            if jid not in current_jids:
                self.django_user.roster_items.create(jid=jid)

        pg_notify(
            'events/%s' % unicode(self.boundjid.bare),
            ["roster_updated", "{}"]
        )
