from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class OTRMeClient(ClientXMPP):

    def __init__(self, jid, password):
        super(OTRMeClient, self).__init__(jid, password)
        self.resource = 'OTRMe'

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("changed_status", self.changed_status)

    def session_start(self, event):
        self.send_presence(pshow="chat", pstatus="Using OTRMe!", ppriority=20)
        # roster = self.get_roster()
        # print roster

    def message(self, msg):
        print msg

        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()

    def changed_status(self, presence):
        print presence['from']
        print presence.get_type()
