import sys,socket,re
from cifrado import encrypt,decrypt,iv  

def consult(fileName):
	'''Función que consulta los datos del cliente, regresa un string con el contenido del archivo.'''
	content="No se encontraron los datos del cliente"
	try:
		#contex manager de python 3 se encarga de cerrar el archivo al finalizar el bloque
		with open(fileName, "r") as f:
			content=f.read()
	except IOError as ioe:
		print("Error de E/S Motivo: ",ioe)
	except OSError as ose:
		print("Error de permisos: ",ose)
	return content

def transaction(fileName,mount,transacType):
	'''Función que realiza un deposito o un retiro(si hay suficiente), modifica el archivo del cliente.'''
	try:
		with open(fileName,"r+") as f:
			lines=f.readlines()
			if transacType=="deposit":
				lines[2]=str(float(lines[2])+mount)
			elif transacType=="withdraw" and float(lines[2])>=mount:
				lines[2]=str(float(lines[2])-mount)
			else:
				return "No se pudo realizar la transacción, fondos insuficientes"
			f.seek(0)
			f.truncate()
			f.writelines(lines)
		return "Transacción realizada con éxito"
	except IOError as ioe:
		print("Error de E/S Motivo: ",ioe)
	except OSError as ose:
		print("Error de permisos: ",ose)
	return "No se pudo realizar la transacción"

def startServer(ip,port,key,iv):
	''' Esta función inicializa el servidor TCP para empezar a escuchar en la ip:puerto indicado, además
		de que cifra con AES los mensajes utilizando la llave key. '''
	try:
		s=socket.socket()   
		s.bind((ip,port))  
		s.listen(1)
		print("Servidor ATM "+socket.gethostname()+" en escucha, esperando conexión....")  
		sc,addr=s.accept() 
		print("Se ha conectado un cliente: ",addr) 
		consulted=False
		fileName=key+".dat"
		while True:  
			recibido=sc.recv(1024)
			print("Cifrado: ",recibido)
			recibido=decrypt(key,recibido,iv)  
			if recibido=="SALIR":
				print("Finalizando ejecución...")
				sys.exit(0)
			elif re.match(r'CONSULTA', recibido):
				data="Datos de la cuenta: \n"+consult(fileName)
				print("Consulta a servidor")
				sc.send(encrypt(key,data,iv))
				consulted=True 
			elif re.match(r'^DEPOSITAR \d+(\.\d{1,2})?$',recibido) and consulted:
				mount=float(re.split(r'(\d+\.?\d*)',recibido)[1])
				print("Monto a depositar: ",mount)
				data=transaction(fileName,mount,"deposit")
				sc.send(encrypt(key,data,iv))
			elif re.match(r'^RETIRAR \d+(\.\d{1,2})?$',recibido) and consulted:
				mount=float(re.split(r'(\d+\.?\d*)',recibido)[1])
				print("Monto a retirar: ",mount)
				data=transaction(fileName,mount,"withdraw")
				sc.send(encrypt(key,data,iv))
			else:
				print("Comando incorrecto: ",recibido)
				sc.send(encrypt(key,"\t---COMANDOS DISPONIBLES---\n1. CONSULTA\n2. DEPOSITAR\n3. RETIRAR\n4. SALIR\nNOTA: Debe consultar antes de poder depositar o retirar\n",iv))
			print("Cliente "+socket.gethostname()+":", recibido)
	except socket.error as se:
		print("No fue posible levantar el servidor\n Motivo: %s\n Finalizando ejecución..." % se)
		sys.exit(1)
	except ValueError as ve:
		print("Error con la llave, para el cifrado AES la llave debe ser de  16, 24, o 32 bytes.",ve)
		sys.exit(1)
	finally:
		print("Cerrando la conexión....")
		sc.close()  
		s.close()

if __name__ == '__main__':
	#Esta parte solo se ejecuta cuando se manda a ejecutar directamente el modulo desde línea de comandos
	if len(sys.argv)<4:
		print("El uso del servidor es el siguente:\n $python servidorATM.py [ip] [puerto] [llave]")
	else:
		startServer(sys.argv[1],int(sys.argv[2]),sys.argv[3],iv)