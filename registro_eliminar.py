import asyncio
import slixmpp
import xmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 



# Creacion de usuario
def createUser(jid, password):
		print(' ')
		print('Ingresa el usuario con el que te deseas registrar ')
		new_user = input('username@alumchat.fun:  ')
		new_password = input('password:  ')
		user = new_user
		password = new_password
		jid = xmpp.JID(user)
		cli = xmpp.Client(jid.getDomain(), debug=[])
		cli.connect()
		if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
				return True
		else:
				return False

# Login para el usuario



# Clase para eliminacion de un usuario
class Eliminar(slixmpp.ClientXMPP):

    def __init__(self, jid, password, show, status):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.show = show
        self.stat = status
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence(self.show, self.stat)
        self.get_roster()
        self.delete_account()
        

    def delete_account(self):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("Tu cuenta ha sido elimada \n")
            self.disconnect()
        except IqError as e:
            print("No se que paso, pero no se pudo realizar", e)
        except IqTimeout:
            print("Time Up, no se puede establecer conexion. ")
        except Exception as e:
            print(e)  