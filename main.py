from ast import arg
import asyncio
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.util.stringprep_profiles import create
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


#importar las clases y funciones:
from cliente import *
from grupo_ycosas import *
from lista_contactos import *
from registro_eliminar import *

if __name__ == '__main__':
    parser = ArgumentParser(description=Client.__doc__)

    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    parser.add_argument("-s", "--show", dest="show",
                        help="show to use")
    parser.add_argument("-t", "--status", dest="status",
                        help="status to use")
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    args = parser.parse_args()

    posible_status = {
        "1": "chat",
        "2": "away",
        "3": "dnd",
        "4": "xa",
    }

    print(""" <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<>
        Bienvenido, acabas de entrar al chat, que deseas hacer?
        1. Crear una cuenta
        2. Ingresar a tu cuenta
        <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<> 
    """)
    opci = input("Ingresa el numero de opcion que desea: ")
    
    if opci == '1' or opci == '2':
        if args.jid is None:
            args.jid = input("Ingrese su nombre de usuario: ")
        if args.password is None:
            args.password = input("Ingrese su contraseña: ")
        args.show = '1'
        args.status = ''
        print("has ingresado exitosamente")
    
    if opci == '1':
        if createUser(args.jid, args.password):
            print("Acabas de crear tu cuenta, deseas ingresar?")
        else:
            print("Algo salio mal :( ")
    
    if opci == '2' or opci.lower() == 'y':
        dentro = True 
        while dentro: 
            print("<>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<>")
            print("---------- OPCIONES DE USUARIO ----------")
            print("1. Mostrar contactos ")
            print("2. Agregar a un contacto ")
            print("3. Mostrar informacion de un contacto")
            print("4. DM ")
            print("5. Conversacion grupal")
            print("6. Definir mensaje de presencia")
            print("7. Enviar/recibir notificaciones")
            print("8. Enviar/recibir archivos")
            print("-----------------------------------------")
            print("<>-<> <>-<> <>-<> <>-<> <>-<> <>-<> <>-<>")
            opti2 = input("Selecciona la opcion que desees... ")
            

            if opti2 == '1':
                cliente = Rooster(args.jid, args.password)
                cliente.register_plugin('xep_0030')  # Service Discovery
                cliente.register_plugin('xep_0199')  # XMPP Pin
                print("Empieza pero, terminara?...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")


            if opti2 == '2':
                print('Agregando nuevo contacto')
                name = input('Ingrese el nombre: ')
                cliente = AddFriend(args.jid, args.password, name)
                cliente.register_plugin('xep_0030')  # Service Discovery
                cliente.register_plugin('xep_0199')  # XMPP Ping
                cliente.register_plugin('xep_0077')  # In-Band Registration
                cliente.register_plugin('xep_0100')
                print("Empieza pero, terminara?...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")

            if opti2 == '3':
                contact = input('Ingrese el nombre del contacto: ')
                cliente = GetInfo(args.jid, args.password, contact)
                print("Empieza pero, terminara?...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")


            if opti2 == '4':
                recipient = input("Ingresa el user al que le quieres enviar el mensaje: ") 
                message = input("Ingresa el mensaje... ")
                meg = Client(args.jid, args.password, recipient, message, posible_status[args.show], args.status)
                meg.register_plugin('xep_0030') # Service Discovery
                meg.register_plugin('xep_0199') # XMPP Ping
                print("Empieza pero, terminara?...")
                meg.connect()
                meg.process(forever=False)
                print("Se envia el mensaje")

            if opti2 == '5':
                room = input("Ingresa el nombre del room... ") 
                nick = input("¿Que nick deseas usar? ")
                if '@conference.alumchat.fun' in room:
                    cliente = Chatgrupo(args.jid, args.password, room, nick)
                    cliente.register_plugin('xep_0030') # Service Discovery
                    cliente.register_plugin('xep_0199') # XMPP Ping
                    cliente.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                    print("Empieza pero, terminara?...")
                    cliente.connect()
                    cliente.process(forever=False)
                    print("Ejecucion completa")
                    

            if opti2 == '6':
                m_presencia = input("Ingresa el mensaje... ")
                cliente = Rooster(args.jid, args.password, message=m_presencia)
                cliente.register_plugin('xep_0030') # Service Discovery
                cliente.register_plugin('xep_0199') # XMPP Ping
                print("Empieza pero, terminara?...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")

            if opti2 == '7':
                print("Funcion de notificaciones disponible para la siguiente actualizacion :) ")

            if opti2 == '8':
                print("Seguimos trabajando en esta funcion")
