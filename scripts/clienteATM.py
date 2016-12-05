import sys,socket
from cifrado import encrypt,decrypt,iv

def startClient(ip,port,key,iv):
	'''Esta función inicializa el cliente TCP para conectarse con el servidor en la ip:puerto indicado, además
	   de que cifra con AES los mensajes utilizando la llave key.'''
	try:
		s=socket.socket()
		s.connect((ip,port))
		print("Cliente ATM "+socket.gethostname()+" conexión exitosa.")  
		while True:  
			mensaje=input("> ")
			if mensaje=="SALIR":
				print("Finalizando ejecución...") 
				s.send(encrypt(key,mensaje,iv)) 
				break 
			elif mensaje=="":
				#Evitar mandar un mensaje vacio, en TCP se interpreta como un peer disconect
				continue
			else:
				s.send(encrypt(key,mensaje,iv)) 
			recibido=decrypt(key,s.recv(1024),iv)
			if recibido=="":
				print("Sesión finalizada....")
				break
			else:
				print("# "+recibido)   
	except socket.error as se:
		print("Imposible conectar con el servidor\n Motivo: %s\n Finalizando ejecución..." % se)
		sys.exit(1)
	except ValueError as ve:
		print("Error con la llave, para el cifrado AES la llave debe ser de  16, 24, o 32 bytes.\n",ve)
		sys.exit(1)
	finally:
		print("Cerrando la conexión....")
		s.close()

if __name__ == '__main__':
	#Esta parte solo se ejecuta cuando se manda a ejecutar directamente el modulo desde línea de comandos
	if len(sys.argv)<4:
		print("El uso del cliente es el siguente:\n $python clienteATM.py [ip] [puerto] [llave]\n Nota: Recuerda que la llave debe de ser minimo de 16 bytes.")
	else:
		startClient(sys.argv[1],int(sys.argv[2]),sys.argv[3],iv)