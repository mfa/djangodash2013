# -*- coding: utf-8 -*-

# using code from
# https://blog.darmasoft.net/2013/06/30/using-pure-python-otr.html

import potr
import os
import logging
logging.basicConfig(level=logging.DEBUG)
from django.core.cache import cache

log = logging.getLogger()


class OTRContext(potr.context.Context):
    """Context is like a connection/conversation between two persons."""

    def getPolicy(self, key):
        DEFAULT_POLICY_FLAGS = {
            'ALLOW_V1': False,
            'ALLOW_V2': True,
            'REQUIRE_ENCRYPTION': True,
        }
        if key in DEFAULT_POLICY_FLAGS:
            return DEFAULT_POLICY_FLAGS[key]
        else:
            return False

    def inject(self, msg, appdata=None):
        # This method send some message from account to the target peer
        log.debug('Call inject; %s => %s; %s', self.user, self.peer, msg)

    def setState(self, newstate):
        # Hook to catch changes at the state variable to notify user about
        # state changes lik encryption is ready
        log.debug('set State to %s', newstate)
        super(OTRContext, self).setState(newstate)

    def plain_context(self):
        return self.getState() == potr.STATE_PLAINTEXT

    def encrypted_context(self):
        return self.getState() == potr.STATE_ENCRYPTED

    def finished_context(self):
        return self.getState() == potr.STATE_FINISHED


class OTRAccount(potr.context.Account):

    def __init__(self, jid):
        super(OTRAccount, self).__init__(jid, '-', 1024)
        self.key = 'privatekey-%s.key3' % jid

    def loadPrivkey(self):
        x = cache.get(self.key)
        if x:
            return potr.crypt.PK.parsePrivateKey(x)[0]
        return None

    def savePrivkey(self):
        cache.set(self.key, self.getPrivkey().serializePrivateKey())


class OTRContextManager(object):

    def __init__(self, jid):
        # jid = logged in user
        self.account = OTRAccount(jid)
        self.contexts = {}

    def context_to(self, other):
        if other not in self.contexts:
            # No context already for other than create a new context
            self.contexts[other] = OTRContext(self.account, other)
        return self.contexts[other]

    def incoming(self, msg):
        # msg.dict = from, body, type
        logging.getLogger().debug("Incoming message by %s: %s",
                                  self.account, msg)
        otrctx = self.context_to(msg['from'])

        try:
            # attempt to pass the message through
            # *potr.context.Context.receiveMessage*
            # there are a couple of possible cases
            res = otrctx.receiveMessage(msg["body"])
            return res, True
        except potr.context.UnencryptedMessage:
            # potr raises an UnencryptedMessage exception when a message is
            # unencrypted but the context is encrypted
            # this indicates a plaintext message
            # came through a supposedly encrypted
            # channel it is appropriate here to warn your user!
            return msg['body'], False

    def outgoing(self, jid, msg):
        otrctx = self.context_to(jid)
        if otrctx.state == potr.context.STATE_ENCRYPTED:
            logging.getLogger().debug("sending encrypting message")
            # the context state should currently be encrypted,
            # so encrypt outgoing message
            # passing the plain text message into Context.sendMessage will
            # trigger Context.inject with an encrypted message.
            otrctx.sendMessage(0, msg)
        else:
            # the outgoing state is not encrypted, so send it plain text
            logging.getLogger().debug("sending message unencrypted")
            otrctx.inject(msg)


# usage example:
if __name__ == '__main__':
    import types

    bob = MyOtrContextManager('bob')
    bob_account = bob.account

    alice = MyOtrContextManager('alice')
    alice_account = alice.account

    def bob_to_alice(self, msg, appdata=None):
        print "Bob => Alice: %s" % msg
        alice.incoming({
            'from': 'bob',
            'body': msg,
            'type': 'xxx'
        })
    bob.context_to('alice').inject = types.MethodType(bob_to_alice, bob)

    def alice_to_bob(self, msg, appdata=None):
        print "Alice => Bob: %s" % msg
        bob.incoming({
            'from': 'alice',
            'body': msg,
            'type': 'xxx'
        })
    alice.context_to('bob').inject = types.MethodType(alice_to_bob, alice)

    bob.context_to('alice').inject('Hello World!')
    alice.context_to('bob').inject('Hello World!')

    alice_con_bob = alice.context_to('bob')
    inv_msg = alice_con_bob.sendMessage(
        alice_con_bob.getPolicy('ALLOW_V2'), ''
    )
    alice_con_bob.inject(inv_msg)

    alice.outgoing('bob', 'Hello World!')
    bob.outgoing('alice', 'Hello Alice')
