import json
import logging

from django.core.management.base import BaseCommand

from jabdaemon.client import OTRMeClient
from events.pgnotify import pg_listen


class Command(BaseCommand):
    args = ''
    help = 'Start the JabDaemon'

    def handle(self, *args, **options):
        self.logger = logging.getLogger('jabdaemon')
        logging.basicConfig(level=logging.DEBUG)

        self.clients = {}

        for event in pg_listen('jab-control'):
            if not event.payload:
                self.logger.error("Notify event doesn't contains payload")
                continue

            try:
                event = json.loads(event.payload)
            except Exception:
                self.logger.exception("Error while parsing event json")
                continue

            if event.get('type') == 'shutdown':
                self.logger.info("JabDaemon goes down!")
                break

            try:
                self.process_event(event)
            except Exception:
                self.logger.exception("Error while processing")

        for client in self.clients.values():
            client.disconnect()

    def process_event(self, event):
        if event.get('type') == 'connect':
            jid = event['jid']
            password = event['password']

            if jid in self.clients:
                self.logger.debug("JID %s is already connected", jid)
                return

            self.logger.debug("Create client for %s", jid)
            self.clients[jid] = OTRMeClient(jid, password)
            self.clients[jid].connect()
            self.clients[jid].process(block=False)

        elif event.get('type') == 'disconnect':
            jid = event['jid']

            if jid not in self.clients:
                self.logger.debug("JID %s wasn't connected", jid)
                return

            self.logger.debug("Close client for %s", jid)
            self.clients[jid].disconnect()
        elif event.get('type') == 'message':
            jid = event['jid']
            if 'to_jid' not in event:
                self.logger.error("to_jid missing in event")
                return
            if 'message' not in event:
                self.logger.error("messae missing in event")
                return
            if jid not in self.clients:
                self.logger.debug("JID %s is not connected", jid)
                return
            conversation_context = self.clients[jid].otr.context_to(event['to_jid'])
            conversation_context.inject(event['message'])
            self.logger.debug("Sent message from %s to %s",
                              event['to_jid'], event['jid'])
        else:
            self.logger.error("Unknown event: %s", event)
