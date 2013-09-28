from django.core.management.base import BaseCommand

from jabdaemon.client import OTRMeClient
import logging

class Command(BaseCommand):
    args = ''
    help = 'Start the JabDaemon'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)

        self.stdout.write('Start JabDaemon')
        client = OTRMeClient('otr@jabme.de', '123')
        client.connect()
        client.process(block=True)