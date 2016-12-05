# Cajero ATM (sockets TCP y cifrado AES)

Proyecto Final de Arquitecturas Cliente Servidor de la Facultad de Ingeniería UNAM

## SCRIPTS
* Para correr el servidor desde linea de comandos se puede realizar de la siguiente forma:

    ```
    $ python servidorATM.py [ip] [puerto] [llave]
    ```

* Para correr el cliente desde linea de comandos se puede realizar de la siguiente forma:

    ```
    $ python clienteATM.py [ip] [puerto] [llave]
    ```
* Para probar los códigos es necesario el modulo **pycrypto** instalado, se puede
     instalar de manera sencilla con la siguiente línea:

    ```
    $ pip install pycrypto
    ```
* O buscar el instalador de esta [lista](http://www.voidspace.org.uk/python/modules.shtml#pycrypto),(Nota: solo para Python 2.6, 2.7 y 3.3)

* Instalación para Python 3.5 mediante [wheels](https://github.com/sfbahr/PyCrypto-Wheels)

* **NOTA:** Asegurarse de tener los [compiladores](http://www.microsoft.com/en-us/download/details.aspx?id=44266) para C++ si se ejecuta en Windows 