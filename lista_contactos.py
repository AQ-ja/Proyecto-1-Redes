import asyncio
import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 



class Rooster(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        print('Contactos: \n')
        contactos = []
        roster = self.client_roster
        for contact in roster:
            contactos.append(contact)

        
        for contact in contactos:
            print(contact)


    # Enviar mensaje de presencia a mis amigos

    def presenceRoster(self, to, body):
        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body
        try:
            message.send()
        except IqError as e:
            print("Algo salio mal", e, "\n")
        except IqTimeout:
            print("Time UP")


class AddFriend(slixmpp.ClientXMPP):
    def __init__(self, jid, password, name):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.name = name
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_presence(pto=self.name, pstatus=None,
                           ptype='subscribe', pfrom=self.jid)
        self.disconnect()

class GetInfo(slixmpp.ClientXMPP):
    def __init__(self, jid, password, contact):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.contact = contact
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0054')
        contactos = []
        roster = self.client_roster
        for jid in roster:
            contactos.append(jid)
        if self.contact in contactos:
            for x in range(0, 10):
                print("")
            print("El contacto existe")
            print("Mostrando información del contacto: " + self.contact)
            print(roster[self.contact])
            for x in range(0, 2):
                print("")
        else:
            print("El contacto no existe")

        self.disconnect()