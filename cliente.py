import logging
from multiprocessing.connection import Client
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
class registro(slixmpp.ClientXMPP):
    def __init__(self, jid, passw):
        slixmpp.ClientXMPP.__init__(self, jid, passw)

        self.add_event_handler('register', self.register)
        self.add_event_handler('disconnected', self.got_diss)
        self.register_plugin('xep_0030') #Service Discovery
        self.register_plugin('xep_0004') #Data forms
        self.register_plugin('xep_0066') #Out-of-band Data
        self.register_plugin('xep_0199') #XMPP Ping
        self.register_plugin('xep_0077') #In-band Registration
        self.register_plugin('xep_0045') #Multi user chat
        self['xep_0077'].force_registration = True

        #Para desconectarse 
        def dissco(self, event):
            print("Te desconectaste")

        #Para un nuevo usuario y contraseña 
        def registro(self, event):
            resp = self.Iq()
            resp['type'] = 'set'
            resp['register']['username'] = self.boundjid.user
            resp['register']['password'] = self.password

            try:
                resp.send()
                print("Entrada exitosa")
            except IqError:
                print("Ocurrio un error en el registro")
            except IqTimeout:
                print("Tiempo agotado")
            
            self.disconnect()


class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid 
        self.password = password
        self.add_event_handler('disconnected', self.got_diss)
        self.add_event_handler('failed_auth', self.failed)
        self.add_event_handler('error', self.handle_error)
        self.add_event_handler('presence_subscribed', self.new_subscribed)
        self.add_event_handler('message', self.message)
        self.add_event_handler('got_offline', self.handle_offline)
        self.add_event_handler('got_online', self.handle_online)
        self.register_plugin('xep_0004') #Data Forms
        self.register_plugin('xep_0030') #Service Discovery
        self.register_plugin('xep_0045') #Multi user chat
        self.register_plugin('xep_0047') #In-band Bytestreams
        self.register_plugin('xep_0050') #Ad-Hoc Commands
        self.register_plugin('xep_0066') #Out of Band Data
        self.register_plugin('xep_0077') #In-band Registration
        self.register_plugin('xep_0085') #Chat State Notifications
        self.register_plugin('xep_0092') #Software version
        self.register_plugin('xep_0199') #Xmpp ping
        self.register_plugin('xep_0231') #Bits of Binary
        self['xep_0077'].force_registration = True

#Funcion para enviar mensajes 
    def mensaje(self, msg):
        sender = str(msg['from'])
        jid = sender.split('/')[0]
        username = jid.split('@')[0]

        if msg['type'] in ('chat', 'normal'): print('Has recibido un mensaje de: '+username+'... el mensaje es ' +msg['body'])

        elif msg['type'] in ('groupchat', 'normal'):
            nick = sender.split('/')[1]
            if jid != self.jid:
                print('Nuevo mensaje del grupo: ' +nick+' de: '+jid+' que dice: '+msg['body'])
    
#Manejo de errores 
    def handle_error(self, event):
        print("Se encontro un error")
        self.disconnect()

#Cuando se vaya la conexion del usuario 
    def handler_offline(self, presence):
        print(str(presence['from']).split('/')[0] + ' got disconected')

#Cuando un usuario se conecta
    def handle_online(self, presence):
        print(str(presence['from']).split('/')[0] + ' got conected')

#Cuando la autentificacion falla 
    def handle_online(self, event):
        print('Usuario o contraseña incorrecta')

    def start (self):
        self.send_presence()
        self.get_roster()
    
    def got_diss(self, event):
        print('Se desconecto')

    def new_subscribed(self, presence):
       print(presence.get_from()+' tienes un nuevo nuevo amigo!')

    #-------------------------------------------------------------------------
    def set_presence(self, show, status):
        self.send_presence(show, status)
        self.get_roster()
        time.sleep(3)

    #-------------------------------------------------------------------------
    def delete(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full 
        resp['register']['remove'] = True

        try: 
            print("La cuenta", self.boundjid.bare, "ha sido eliminada")

        except IqError as err: 
            print("Ocurrio un error eliminando la cuenta")
            self.disconnect()
        except IqTimeout:
            print("Se ha agotado el tiempo")
            self.disconnect()

    
#Agregar un nuevo amigo 
    def add_friend(self, JID):
        self.send_presence_subscription(pto=JID, ptype='subscribe', pfrom= self.boundjid.bare)
        self.get_roster()
        time.sleep(3)

#Mensaje privado 

class MsgPriv(slixmpp.ClientXMPP):
    def __init__(self, jid, password, uname, msg):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.uname = uname
        self.msg = msg

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('presence_subscribed', self.new_subscribed)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.uname,
                          mbody=self.msg,
                          mtype='chat')
        
        print("Tu mensaje ha sido enviado exitosamente")
        