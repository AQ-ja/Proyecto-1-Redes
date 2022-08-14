from logging import log
from multiprocessing import forkserver
from os import close
from xmpp import *
from slixmpp import jid
from getpass import getpass
from cliente import *
from ssl import OP_NO_RENEGOTIATION
from cliente import *
from registro_eliminar import *

#Inicio del codigo, aqui se hara el loop del main

def user_online(event):
    xmpp.start()
    print("Acabas de entrar al mejor chat del mundo", xmpp.boundjid.bare)

    while True:
        print("-=============--------------==============----------=============----------")
        print("1. Mostrar los usuarios")
        print("2. Agregar contactos")
        print("3. Ver un contacto")
        print("4. Enviar MD")
        print("5. Mandar mensaje grupal")
        print("6. Establecer mensaje de presencia")
        print("7. Enviar o recibir cosas")
        print("8. Cerrar sesion")
        print("9. **** ELIMINAR LA CUENTA **** ")

        opt = input("¿Que quieres hacer?")

        if opt == "1":
            get_my_rooster = GetRooster(xmpp.jid, xmpp.password)
            get_my_rooster.connect()
            get_my_rooster.process(forever=False)

        elif opt == '2':
            print('Agregar un nuevo contacto')
            contact_jid = input('Ingresa el USER: ')
            if '@alumchat.fun' in contact_jid:
                xmpp.add_friend(contact_jid)
                print("Has agregado a un nuevo amigo")
            else: 
                print("No se reconoce el usuario ingresado")

        elif opt == '3':
            user = input("Ingrese el usuario a buscar: ")
            if '@alumchat.fun' in user:
                get_my_rooster = GetRooster(xmpp.jid, xmpp.password, user)
                get_my_rooster.connect()
                get_my_rooster.process(forever=False)
            else: 
                print("No es un input valido")

        elif opt == '4':
            user = input('Ingresa el JID del usuario: ')
            if '@alumchat.fun' in user:
                to_send = input('Escribe el mensaje que quieres enviar: ')
                if to_send:
                    md = MsgPriv(xmpp.jid, xmpp.password, user, to_send)
                    md.connect()
                    md.process(forever=False)
                else:
                    print('No existen mensajes')
            else: 
                print("Input invalido")

        elif opt == '5':
            print("|||||||||||| APARTADO DE GRUPOS |||||||||||| ") 
            print("1. Crear un grupo")
            print("2. Entrar a un grupo")
            print("3. Mensaje general")
            print("4. Salir del grupo")
            print("5. Regreasar")
            opt_grupos = input("Que quieres hacer? ")

            if opt_grupos == '1':
                name = input("Nombre del grupo: ")
                nick = input("Cual es tu nick: ")
                if nick and name and '@conference.' in name:
                    group_create = create_gruop(xmpp.jid, xmpp.password, name, nick)
                    group_create.connect()
                    group_create.process(forever=False)
                else:
                    print("Verifique los datos")
                    continue   

            elif opt_grupos == '2':
                name = input('Room: ')
                nick = input('Nick: ')
                if nick and name and '@conference.' in name:
                    group_join = unirse_grupo(xmpp.jid, xmpp.password, name, nick)
                    group_join.connect()
                    group_join.process(forever=False)
                else:
                    print('Verifique los datos')
                    continue
            
            
            elif opt_grupos == '3':
                name = input("Room: ")
                msg = input("Cual es el mensaje: ")
                if msg and name and '@conference.' in name:
                    send_group = Msg_group(xmpp.jid, xmpp.password, name, msg)
                    send_group.connect()
                    send_group.process(forever=False)
                else:
                    print('Verifique los datos')
                    continue
            
            elif opt_grupos == '4':
                name = input('Room: ')
                nick = input('Nick: ')
                if nick and name and '@conference.' in name:
                    group_exit = salir_grupo(xmpp.jid, xmpp.password, name, nick)
                    group_exit.connect()
                    group_exit.process(forever=False)
                else:
                    print("Verifique los datos")
                    continue
            
            elif opt_grupos == '5':
                pass
            else:
                print('Input no registrado')


        elif opt == "6":
            estados = ["En linea", "AFK", "Ocupado", "Restringido"]
            print("Elige el estado deseado")
            i = 1
            for opt in estados:
                print(str(i)+'. '+opt)
                i += 1
            show_input = input('Ver la opcion: ')
            status = input('Nuevo status ')
            try:
                show = estados[int(show_input)-1]
            except:
                print('No se logro modificar')
                show = 'available'
            xmpp.set_presence(show, status)
            print("Estado Cambiado")


        elif opt == "7":
            user = input('A quien lo deseas enviar? : ')
            file = input('Cual es el archivo: ')
            if file and user and '@' in user:
                send_file = SendFile(xmpp.jid, xmpp.password, user, file, xmpp.boundjid.domain)
                send_file.connect()
                send_file.process(forever=False)

        
        elif opt == "8":
            xmpp.disconnect()
            print(" Se ha cerrado sesion del usuario: " , xmpp.boundjid.bare)
            break

        elif opt == "9":
            xmpp.delete()
            xmpp.disconnect()
            print(" Se ha eliminado el usuario:  " , xmpp.boundjid.bare)
            break

        else:
            print("Opcion no listada.")

while(True):
    print('.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::')
    print('.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::')
    print('1. Deseas iniciar sesion')
    print('2. Deseas crear una cuenta')
    print('3. Deseas salir del chat')
    opci = input("Que quieres hacer?")
    print('.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::')
    print('.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::.:::::')

    if opci == '1':
      print(' ')
      print('You Choose Login')
      username = input('user:  ')
      password = input('password: ')
      xmpp = Login(username, password)
      xmpp.register_plugin('xep_0030') # Service Discovery
      xmpp.register_plugin('xep_0199') # XMPP Ping
      xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
      xmpp.register_plugin('xep_0096') # Jabber Search
      xmpp.connect()
      xmpp.process(forever=False)

    elif opci == '2':
      createUser()

    elif opci == '3':
        print ("Gracias por utilizar este chat! ")
        break

    else:
        print('Opcion no listada.')
