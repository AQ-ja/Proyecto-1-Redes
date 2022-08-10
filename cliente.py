import logging
import threading
import slixmpp
import base64
import time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

"""
Referenicas: 
https://slixmpp.readthedocs.io/en/latest/
https://slixmpp.readthedocs.io/en/latest/getting_started/sendlogout.html
https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/register_account.py



"""

# Primera prueba de la clase de registro
class registroserver(slixmpp.ClientXMPP):
    def __init__(self, jid, passw):
        slixmpp.ClientXMPP.__init__(self, jid, passw)

        self.add_event_handler('register', self.register)
        self.add_event_handler('disconnected', self.got_diss)


