import asyncio
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


#Vemos lo de las nuevas inscripciones al server
def new_subscribed(self, presence):
    print(presence.get_from()+'te agrego como amigo')

#============================================================================
#Para el chat de grupo 

class group(slixmpp.ClientXMPP):
    def __init__(self, jid, password, jid_room, ak_room):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("sesion_iniciada")
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)
        self.room = jid_room
        self.ak = ak_room

        async def start(self, event):
            self.send_presence()
            await self.get_roster()

            try:
                self.plugin['xep_0045'].join_muc(self.room, self.ak)
                print("Acabas de entrar al grupo")
            except IqError:
                print("Ocurrio un error")
            except IqTimeout:
                print("Sin respuesta del server")
            self.disconnect()


class subscribe(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("sesion_iniciada", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to)        
        except IqTimeout:
            print("Timeout") 
        self.disconnect()
                

class GetRooster(slixmpp.ClientXMPP):
    def __init__(self, jid, password, user_search = None):
        slixmpp.ClienteXMPP.__init__(self, jid, password)
        self.roster = {}
        self.user_search = user_search

        self.add_event_handler('sesion_iniciada', self.start)
        self.add_event_handler('changed_status', self.wait_for_presences)
        self.add_event_handler('desconnected', self.got_diss)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')

        self.received = set()
        self.precense_received = asyncio.Event()

    def got_diss(self, event):
        print('Se ha desconectado')
        quit()

    async def start(self, event):
        try:
            await self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Timeout del server')
        self.send_presence()

        print('Esperando actualizaciones...')
        await asyncio.sleep(5)

        print('El roster de %s es:' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                status = ''
                show = ''
                sub = ''
                name = ''
                sub = self.client_roster[jid]['subscription']
                conexion = self.client_roster.presence(jid)
                name = self.client_roster[jid]['name']
                for answer, pres in conexion.items():
                    if pres['show']:
                        show = pres['show']
                    if pres['status']:
                        status = pres['status']
                self.roster[jid] = User(jid, show, status, sub, name)


        if(not self.u_search):
            if len(self.roster) == 0:
                print('No hay usuarios agregados')
            else:
                for key in self.roster.keys():
                    friend = self.roster[key]
                    print('- Jid: '+friend.jid+' Username:'+friend.username+' Show:'+friend.show+' Status:'+friend.status+' Subscription:'+friend.subscription)

 
        else:
            if self.u_search in self.roster.keys():
                user = self.roster[self.u_search]
                print('- Jid: '+user.jid+' Username:'+user.username+' Show:'+user.show+' Status:'+user.status+' Subscription:'+user.subscription)
            else:
                print('Usuario no encontrado')
        

        await asyncio.sleep(5)
        self.disconnect()

    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()


#para comodidad xd
# ------------------------
class User():
    def __init__(self, jid, show, status, subscription, username):
        self.jid = jid
        self.show = show
        self.status = status
        self.subscription = subscription
        self.username = username

class SendFile(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.receiver = receiver    
        self.file = open(filename, 'rb')
        self.domain = domain
        
    
        self.add_event_handler("sesion_iniciada", self.start)
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0071')
        self.register_plugin('xep_0128')
        self.register_plugin('xep_0363')

    
    async def start(self, event):
        try:
    
            proxy = await self['xep_0363'].handshake(self.receiver)
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)
            proxy.transport.write_eof()
    
        except (IqError, IqTimeout) as e:
            print("Error detectado")
        else:
            print("Si se logro hacer el envio")
        finally:
    
    
            self.file.close()
    
            self.disconnect()



# ===============================================================
# Para la parte de los grupos, que sigan las funciones :)
# ===============================================================

class create_gruop(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('sesion_iniciada', self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()

        status = 'open'
        self.plugin['xep_0045'].join_muc(
            self.room,
            self.alias,
            pstatus = status, 
            pfrom = self.boundjid.full
        )

        await self.plugin['xep_0045'].set_affiliation(self.room, jid = self.boundjid.full, affiliation = 'owner')
        print("Se acaba crear el grupo")
        self.disconnect()
        quit()

class unirse_grupo(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        self.room = room
        self.alias = alias

    async def start(self, start):
        await self.get_roster()
        self.send_presence()
        status = 'open'
        self.plugin['xep_0045'].join_muc(
            self.room,
            self.alias,
            pstatus=status,
            pfrom=self.boundjid.full
        )
        self.disconnect()
        quit()


class salir_grupo(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, alias):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045')
        self.register_plugin('xep_0096')
        self.room = room
        self.alias = alias

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        print('AQUI')
        await self.plugin['xep_0045'].leave_muc(self.room, self.alias)
        print('AQUI')
        self.disconnect()
        quit()        


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