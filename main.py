from logging import log
from os import close
from slixmpp import jid
from getpass import getpass
from cliente import *
from ssl import OP_NO_RENEGOTIATION

#Inicio del codigo, aqui se hara el loop del main

def user_online(event): 
    xmpp.start()
    print("-------Inicio-------", xmpp.boundjid.bare)

    while True: 
        print("/////////////////////////////")
        print("1. Usuarios")
        print("2. Agregar contactos")
        print("3. Informacion de contacto")
        print("4. MD")
        print("5. Mensaje grupal")
        print("6. Establecer mensaje de presencia")
        print("7. Enviar/recibir notificaciones")
        print("8. Enviar/recibir archivos")
        print("9. Cerrar sesion")
        print("10. Eliminar la cuenta")

        des = input("¿Que quieres hacer? : ")

        
