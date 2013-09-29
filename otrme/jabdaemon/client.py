import json
import logging
from sleekxmpp import ClientXMPP

from events.pgnotify import pg_notify
from otrbackend.magic import OTRContextManager, OTRContext

class XMPPOTRContext(OTRContext):

    def __init__(self, user, other, xmpp_client):
        super(XMPPOTRContext, self).__init__(user, other)
        self.xmpp_client = xmpp_client

    def inject(self, msg, appdata=None):
        # This method send some message from account to the target peer
        logging.getLogger().debug('Call inject; %s => %s; %s',
                                  self.user, self.peer, msg)
        self.xmpp_client.send_message(mto=self.peer, mbody=msg)

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
        super(OTRMeClient, self).__init__(jid, password)
        self.resource = 'OTRMe'

        self.otr = XMPPOTRContextManager(self)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.changed_status)
        self.add_event_handler("roster_update", self.roster_update)

    def session_start(self, event):
        self.send_presence(pshow="chat", pstatus="Using OTRMe!", ppriority=20)
        roster = self.get_roster()

        for jid in self.client_roster:
            print self.client_roster[jid]

            connections = self.client_roster.presence(jid)
            for res, pres in connections.items():
                print res, pres

        print ""
        print roster
        print ""
        print self.client_roster
        print ""

    def message(self, msg):
        plain_msg, was_encrypted = self.otr.incoming({
            'from': unicode(msg['from']),
            'type': unicode(msg['type']),
            'body': unicode(msg['body']).encode('utf8')
        })

        context = self.otr.context_to(unicode(msg['from']))

        if msg['type'] in ('chat', 'normal'):
            event_payload = {
                'name': 'Gentle',
                'jid': unicode(msg['from']),
                'message': unicode(msg['body']),
                'time': '2013-09-09 18:24'
            }
            pg_notify(
                'events/%s' % unicode(msg['from'].bare),
                json.dumps(["message", event_payload])
            )

            if context.state == 0:
                self.otr.outgoing(
                    msg['from'],
                    "Your message was not encrypted. AARRRR!"
                )
            elif context.state == 1:
                self.otr.outgoing(
                    msg['from'],
                    "Your message was encrypted. Great secret plan!"
                )
            elif context.state == 2:
                self.otr.outgoing(
                    msg['from'],
                    "Okay no OTR anymore. Silence now!"
                )
            else:
                self.otr.outgoing(
                    msg['from'],
                    "Something went terrible wrong..."
                )

        print msg
        print was_encrypted
        print plain_msg

    def changed_status(self, presence):
        print presence['from']
        print presence.get_type()

    def roster_update(self, roster):
        print roster

