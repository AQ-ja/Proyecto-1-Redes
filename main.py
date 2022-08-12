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

        if des == "1":
            print ("'============ Empieza el shat ============= ")
            username = input("Ingrese el usuario: " )
            user_pass = getpass("Ingrese la contraseña del usuario: ", username)
            xmpp = Cliente( jid= username, password = user_pass )

        elif des == "2":
            print ("Gracias por usar el shat ")
            break
        elif des == "3":
            print ("Gracias por usar el shat ")
            break
        elif des == "4":
            print ("Gracias por usar el shat ")
            break
        elif des == "5":
            print ("Gracias por usar el shat ")
            break
        elif des == "6":
            print ("Gracias por usar el shat ")
            break
        elif des == "7":
            print ("Gracias por usar el shat ")
            break
        elif des == "8":
            print ("Gracias por usar el shat ")
            break
        elif des == "9":
            print ("Gracias por usar el shat ")
            break
        elif des == "10":
            print ("Gracias por usar el shat ")
            break
        else:
           print('Opcion no listada')
        
