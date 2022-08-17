import asyncio
import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Rooster(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show1, status, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.show = show
        self.show1 = show1
        self.stat = status
        self.message = message
        self.my_user = jid

    async def start(self, event):
        self.send_presence(self.show1, self.stat)
        await self.get_roster()

        my_contacts = []
        try:
            self.get_roster()
        except IqError as e:
            print("Algo salio mal", e, "\n")
        except IqTimeout:
            print("Time UP")
        
        self.presences.wait(3)

        # Traer a mis contactos 
        
        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                show = 'Conectado'
                status = answer = ''
                conexions = self.client_roster.presence(user)
                username = str(user).split("@")[0]
                if conexions.items():
                    for answer, pres in conexions.items():
                        if pres['show']:
                            show = pres['show']
                        if pres['status']:
                            status = pres['status']
                else:
                    show = 'Desconectado'
                    
                my_contacts.append([
                    user,
                    status,
                    username,
                    show
                ])
                self.contacts = my_contacts

        if(self.show):
            # Mostrar todos mis usuarios

            if(not self.user):
                if len(my_contacts) == 1:
                    print('Aun no tienes contactos.')
                else:
                    print('\nContactos:\n')
                    for contact in my_contacts:
                        if contact[0] != self.my_user:
                            print('**** JID >> ' + str(contact[0])  + '\n**** Nombre de usuario >> ' + str(contact[2]) + '\n**** Estado >> ' + str(contact[1]) + '\n**** Disponibilidad >> ' + str(contact[3]) + "\n\n")
            else:
                # Mostrar un usuario especifico

                flag = True
                for contact in my_contacts:
                    if(contact[0] == self.user):
                        print('**** JID >> ' + str(contact[0]) + '\n**** Nombre de usuario >> ' + str(contact[2]) + '\n**** Estado >> ' + str(contact[1]) + '\n**** Disponibilidad >> ' + str(contact[3]) + "\n\n")
                        flag = False
                if flag:
                    print("\nNO hay match para la busqueda \n")
        else:
            for JID in self.contacts:
                self.presenceRoster(JID[0], self.message)

        self.disconnect()

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


class AddRoster(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show, status, to=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to
        self.show = show
        self.stat = status

    async def start(self, event):
        self.send_presence(self.show, self.stat)
        await self.get_roster()

        # Agregar contactos 
        
        try:
            if self.to is not None:
                self.send_presence_subscription(pto = self.to) 
        except IqTimeout:
            print("Time UP") 
        self.disconnect()
        

