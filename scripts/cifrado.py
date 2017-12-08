from Crypto.Cipher import AES

#Este es el vector de inicialización, debe ser el mismo para cifrar y descifrar
iv="IVV's12345667890"

def encrypt(key,message,iv):
	'''Función para cifrar con una llave de 16, 32 o 64 bytes'''
	encryptionSuite=AES.new(key, AES.MODE_CFB, iv)
	encryptedMessage=encryptionSuite.encrypt(message)
	return encryptedMessage

def decrypt(key,encryptedMessage,iv):
	'''Función para decifrar con una llave de 16, 32 o 64 bytes'''
	decryptionSuite=AES.new(key, AES.MODE_CFB, iv)
	decryptedMessage=decryptionSuite.decrypt(encryptedMessage)
	return decryptedMessage.decode("UTF-8")

if __name__ == '__main__':
	#Esta parte es para probar el modulo de cifrado, no se ejecuta cuando lo importa otro modulo
	encryptionSuite=AES.new('Esta es la llave', AES.MODE_CFB, 'Este es un IV456')
	cipherText=encryptionSuite.encrypt("Mensaje bien prro de cifrar.")
	print(cipherText)

	decryption_suite=AES.new('Esta es la llave', AES.MODE_CFB, 'Este es un IV456')
	plainText=decryption_suite.decrypt(cipherText)
	print(plainText.decode("UTF-8"))
