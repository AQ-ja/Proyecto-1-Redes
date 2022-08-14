import asyncio
import slixmpp
import time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass


"""fhhghfghgfhfghfgh  
Referenicas: 
https://slixmpp.readthedocs.io/en/latest/
https://slixmpp.readthedocs.io/en/latest/getting_started/sendlogout.html
https://lab.louiz.org/poezio/slixmpp/-/blob/master/examples/register_account.py



"""



class Msg_group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        self.room = room
        self.msg = msg

    async def start(self, event):
        await self.get_roster()
        self.send_presence()

        self.send_message(
            mto=self.room,
            mbody=self.msg,
            mtype='groupchat',
            mfrom=self.boundjid.full
        )
        print('SI SE ENVIOOOOOOOOOOOOOOOOO') 