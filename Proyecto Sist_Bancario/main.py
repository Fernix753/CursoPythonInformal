import pandas as pd
import random as rd
import sys
import time
from time import sleep
import os.path
from os import path

# Formato de datos
# data = {
#     0: {'CBU':'9876543210123456', 'Nombre': 'Juan', 'Apellido': 'Pérez', 'PIN': 1234, 'SALDO (PESOS)': 1.0, 'SALDO (USD)': 0.0},
#     1: {'CBU':'9876543210123457', 'Nombre': 'Rodrigo', 'Apellido': 'Saez', 'PIN': 1122, 'SALDO (PESOS)': 50.0, 'SALDO (USD)': 0.0}
#     entero,    string de 16 numeros,         String,                String,      entero,                flotante         flotante
# }
# Formato para agregar datos al diccionario
# data[2]={'CBU':'9876543210123222', 'Nombre': 'Pedro', 'Apellido': 'Nuñez', 'PIN': 1322, 'SALDO (PESOS)': 25.0, 'SALDO (USD)': 0.0}

espaciador = "\n"*25
respuestas = ["SI", "NO"] #Respuesta 0 - Afirmación \\ Respuesta 1 - Negación
acciones = ["0", #Mostrar lista de clientes.
            "1", #Mostrar info de un cliente en especificio
            "2", #Agregar un cliente a la base de datos.
            "3", #Eliminar un cliente de la base de datos.
            "H", #Mostrar ayuda
            "Z"] #Salir del programa
error_0     = "Hubo un error inesperado. No se completo la ultima tarea."
error_1     = "Al parecer los datos ya estaban cargados."
error_2     = "Al parecer no se ha cargardo correctamente la base datos."
error_3     = "Al parecer alguno de los datos es invalido."
error_4     = "Hubo un error al intentar guardar la base de datos."
error_5     = "Al parecer el cliente que intentas crear ya existe en la base de datos."
error_6     = f"No se encontró el documento en el directorio actual ¿Deseas crear una base de datos nueva? [{respuestas[0]}/{respuestas[1]}]"
error_7     = "Al parecer el usuario que ingresaste no existe en la base de datos."

def check_string(nombre):               #Verifica que una cadena de texto no tenga espacios o numeros.
    aux = True
    if isinstance(nombre, int): return False #Si es un entero, retorna False.
    for x in nombre:
        if x.isnumeric() or x.isspace(): #Si encuentra un número o un espacio, retorna False
            aux = False
            break
    return aux
def check_16digit(valor):               #Verifica si es un valor numerico de 16 digitos, y que es un string.
    if isinstance(valor, int):          #Si es un entero, prueba convertirlo.
        return check_16digit(str(valor)) 
    if valor.isnumeric() and len(str(valor))==16: #Checkea si es numerico y de 16 digitos
        return True
    else:
        return False
def check_pin(valor):                   #Verifica si el valor es entero y contiene 4 digitos.
    if isinstance(valor, int) and len(str(valor))==4:
        return True
    else:
        return False

class Database():
    data = None
    dbcheck = False
    last_error = None
    _file = "./bsna_topoland.xlsx"
    _sheet= "BANCO TOPOLAND"

    def data_reset(self):               #Resetea la base de datos (Sólo se usa para cuando no se encuentra la DB y se crea otra desde 0)
        self.data = {}
        self.dbcheck = True
        self.save()

    def load(self):                     #Carga en un diccionario un dataframe extraido de un excel.
        if self.data==None:
            if path.exists(self._file):
                self.data = pd.read_excel(self._file,sheet_name=self._sheet, index_col=0)
                self.data = self.data.to_dict('index')
                self.dbcheck = True
                self.last_error = True
                return True
            else:
                self.last_error = error_6
                return False
        else:
            self.last_error = error_1
            return False
    def save(self):                     #Guarda en un excel un dataframe a partir de la variable data.
        if self.data!=None:
            self.data = pd.DataFrame.from_dict(self.data , orient='index')
            try:
                self.data.to_excel(self._file,sheet_name=self._sheet)
            except PermissionError:
                self.last_error = error_4
                return False
            else:
                self.data = self.data.to_dict('index')
                self.last_error = True
                return True
        else:
            self.last_error = error_2
            return False
    def check_exists(self, nombre,      #Verifica (ineficientemente, posible mejora) si ya existe esa combinación de Nombre y apellido en la database.
        apellido, idget=None ):         #Si se pasa un True en el parametro IDGET, retorna el ID de existir
        rtn = False
        var1= None 
        for x in self.data:
            if self.data[x]['Nombre'] == nombre and self.data[x]['Apellido'] == apellido:
                rtn = True
                var1 = x
                break
        if idget != True:
            return rtn
        elif rtn == True:
            return var1
        else:
            return rtn
    def generar_cbu(self):              #Genera un número de 16 digitos (que no exista) y lo devuelve como un string.
        __set = set()
        if self.dbcheck == True:
            if len(self.data.keys()) > 0:
                for x in self.data:
                    __set.add(self.data[x]['CBU'])
            __cbu = rd.randrange(1000000000000000, 9999999999999999)
            while __cbu in __set:
                __cbu = rd.randrange(1000000000000000, 9999999999999999)
            return str(__cbu)
        else:
            return False
    def create_client(self, cliente,    #Verifica que no exista, que todos los parametros sean válidos y si todo está correcto, lo guarda en mi diccionario/database.
        nombre, apellido, pin):
        if self.dbcheck == True:
            if cliente.name_set(nombre) and cliente.sname_set(apellido) and cliente.cbu_set(self.generar_cbu()) and cliente.pin_set(pin) and cliente.saldo_ars_set(0.0) and cliente.saldo_usd_set(0.0):
                if not self.check_exists(nombre, apellido):
                    aux = max(self.data.keys())+1 if len(self.data.keys()) > 0 else 0
                    self.data[aux] = {
                        'CBU': cliente.cbu_get(),
                        'Nombre': cliente.name_get().capitalize(),
                        'Apellido': cliente.sname_get().capitalize(),
                        'PIN': cliente.pin_get(),
                        'SALDO (PESOS)': cliente.saldo_ars_get(),
                        'SALDO (USD)': cliente.saldo_usd_get()
                    }
                    self.load_client(cliente, aux)
                    return self.save()
                else:
                    cliente.reset()
                    self.last_error = error_5
                    return False
            else:
                cliente.reset()
                self.last_error = error_3
                return False
        else:
            cliente.reset()
            self.last_error = error_2
            return False
    def load_client(self, cliente, id): #Carga la info del cliente (desde el diccionario), a la clase de cliente.
        if (cliente.name_set(       self.data[id]['Nombre']         ) and
            cliente.sname_set(      self.data[id]['Apellido']       ) and
            cliente.cbu_set(        self.data[id]['CBU']            ) and
            cliente.pin_set(        self.data[id]['PIN']            ) and
            cliente.saldo_ars_set(  self.data[id]['SALDO (PESOS)']  ) and
            cliente.saldo_usd_set(  self.data[id]['SALDO (USD)']   )):
            return cliente
        else:
            return False
    def del_client(self, id):           #Eliminar cliente, lo borra del diccionario, y se guarda intenta guardar el cambio
        try: 
            del self.data[id]
        except:
            aux = error_0
        else:
            aux = True
            self.save()
        return aux
    def print_clients(self):            #Recorre el diccionario e imprime los nombres de los clientes.
        cont = 0
        for x in self.data: 
            print(f"-Cliente {x}: {self.data[x]['Nombre']} {self.data[x]['Apellido']}")
            cont += 1
            if cont == 10:
                print(f"Estos son los primeros {cont} clientes de la base de datos.")
                break

class Cliente():
    name    = None
    sname   = None
    cbu     = None
    pin     = None
    saldo_ars= None
    saldo_usd= None

    def reset(self):
        self.name = None
        self.sname = None
        self.cbu = None
        self.pin = None
        self.saldo_ars = None
        self.saldo_usd = None

    def print_data(self):
        return print(f"""
     DATOS DEL CLIENTE:
      Nombre: {self.name}
      Apellido: {self.sname}
      CBU: {self.cbu}
      Saldo (AR$): {self.saldo_ars}
      Saldo (U$D): {self.saldo_usd}""")

    def name_set(self, v):#La 'v' es de value xd
        if check_string(v):
            self.name=v
            return True
        else:
            return False
    def sname_set(self, v):
        if check_string(v):
            self.sname=v
            return True
        else:
            return False
    def cbu_set(self, v):
        if check_16digit(v):
            self.cbu=v
            return True
        else:
            return False
    def pin_set(self, v):
        if check_pin(v):
            self.pin=v
            return True
        else:
            return False
    def saldo_ars_set(self, v):
        if isinstance(v, float):
            self.saldo_ars=v
            return True
        elif isinstance(v, int):
            self.saldo_ars=float(v)
            return True
        else:
            return False
    def saldo_usd_set(self, v):
        if isinstance(v, float):
            self.saldo_usd=v
            return True
        elif isinstance(v, int):
            self.saldo_usd=float(v)
            return True
        else:
            return False

    def name_get(self):
        return self.name
    def sname_get(self):
        return self.sname
    def cbu_get(self):
        return self.cbu
    def pin_get(self):
        return self.pin
    def saldo_ars_get(self):
        return self.saldo_ars
    def saldo_usd_get(self):
        return self.saldo_usd

def print_opciones():                   #Funcion que retorna print con las opciones disponibles.
    return print(
    f"""
    Opción >>  {acciones[0]}  << - Mostrar lista de clientes.
    Opción >>  {acciones[1]}  << - Ver información de un cliente.
    Opción >>  {acciones[2]}  << - Crear un cliente nuevo.
    Opción >>  {acciones[3]}  << - Eliminar un cliente.
    Opción >>  {acciones[5]}  << - Salir del programa.""")

def var_continuar():                    #Funcion para settear una variable común.
    aux = input (f"\nCómo quieres continuar? Ingresa otra acción de la lista, ingresa '{acciones[4]}' para mostrar una ayuda, o '{acciones[5]}' para salir del programa.\n")
    return str(aux).strip().upper()

def main(cliente, db):                  #Main
    print(espaciador)
    print(f"Bienvenido al sistema bancario")
    input("Cargando base de datos. Presiona enter para continuar.")
    for i in range(96):                 #No sé que hace todo esto pero me gusto.
        sys.stdout.write('\r')
        sys.stdout.write("[%-10s] %d%%" % ('='*i, 1*i))
        sys.stdout.flush()
        sleep(0.02)

    db.load()                           #Intento de carga del documento.

    if not db.dbcheck:                  #Si no se pudo cargar el excel, pregunta si desea crear una base de datos nueva.
        if db.last_error == error_6:
            print("\n"+error_6)
            aux = input()
            aux = aux.upper().strip()
            while aux not in respuestas:
                print("Tu respuesta no concuerda con la pregunta, intenta nuevamente.")
                print(error_6)
                aux = input()
                aux = aux.upper().strip()
            if aux == respuestas[0]:
                db.data_reset()
            elif aux == respuestas[1]:
                print("\nSin conexión con la base de datos no se pueden administrar los clientes, el programa se cerrará. Presiona enter para continuar.")
                input()
                return exit()
        else:
            print("\n" + error_4, "El programa se cerrará. Presiona enter para continuar.")
            input()
            return exit()
    print(espaciador)
    print(f"\nAdministración de clientes")
    print("A continuación se muestran las opciones para el manejo de datos de la clientela.")
    print_opciones()
    aux = input()                       #Input auxiliar
    while type(db.data) != None:
        aux = str(aux).strip().upper()
        while aux not in acciones:      #Si el input no es una opción válida, se pregunta nuevamente.
            print(f"La accion ingresada {aux} no está en la lista, prueba nuevamente o ingresa '{acciones[4]}' para mostrar una ayuda")
            aux = input()
            aux = str(aux).strip().upper()
        if acciones[0] == aux:          #Mostrar lista de clientes.
            print(espaciador)
            print("La lista de clientes registrados en nuestra base de datos es la siguiente:")
            db.print_clients()
            aux = var_continuar()
        elif acciones[1] == aux:        #Mostrar info de un cliente en especificio
            print(espaciador)
            print("Buscador de clientes. Complete los campos aqui abajo:")
            nombre = input("\nIngresa el nombre del cliente: ")
            apellido = input("Ingresa el apellido del cliente: ")
            nombre, apellido = nombre.capitalize(), apellido.capitalize()
            if db.check_exists(nombre, apellido):
                cliente_act = db.load_client(cliente, (db.check_exists(nombre, apellido, True)))
                cliente_act.print_data()
                aux = var_continuar()
            else:
                print(error_7, "\n")
                aux = var_continuar()
        elif acciones[2] == aux:        #Agregar un cliente a la base de datos.
            print(espaciador)
            print("Creador de registros para clientes. Complete los campos aqui abajo:")
            nombre = input("\nIngresa el nombre: ")
            apellido = input("Ingresa el apellido: ")
            pin = input("Ingresa el nuevo pin: ")
            pin = pin
            while not check_pin(pin):
                if pin.isnumeric() and len(str(pin))==4:
                    pin = int(pin)
                else:
                    pin = input("El pin ingresado no es válido, ingresa 4 números: ")
            nombre, apellido = nombre.capitalize(), apellido.capitalize()
            aux = db.create_client(cliente,nombre,apellido,pin)
            if aux == True:
                print(f"Cliente creado con éxito, se le asigno el siguiente número de cuenta:{cliente.cbu_get()}")
            else:
                print(db.last_error)
            aux = var_continuar()
        elif acciones[3] == aux:        #Eliminar un cliente de la base de datos.
            aux_opciones = ["ID", "NOMBRE"]
            print("Decidiste eliminar un cliente, usa con cuidado esta herramienta.")
            print(f"Quieres eliminar un cliente por su nombre o por su ID ? [{aux_opciones[0]}/{aux_opciones[1]}]")
            aux1 = input()
            aux1 = aux1.upper().strip()
            if aux1 == aux_opciones[0]:
                print(espaciador)
                print("Eliminar registros de cliente por ID:")
                db.print_clients()
                id = input("\nIngresa el ID del cliente: ")
                while not isinstance(id, int):
                    if id.isnumeric():
                        id = int(id)
                    else:
                        id = input("El ID ingresado no es válido, prueba nuevamente: ")
                db.load_client(cliente, id)
                if db.del_client(id):
                    print(f"Se eliminaron los registros del cliente: {cliente.name_get()} {cliente.sname_get()}")
                    db.save()
                    cliente.reset()
                    aux = var_continuar()
                else:
                    print(aux)
                    aux = var_continuar()
            elif aux1 == aux_opciones[1]:
                print(espaciador)
                print("Eliminar registros de cliente por Nombre. Complete los campos aqui abajo:")
                nombre = input("\nIngresa el nombre del cliente: ")
                apellido = input("Ingresa el apellido del cliente: ")
                nombre, apellido = nombre.capitalize(), apellido.capitalize()
                if db.check_exists(nombre, apellido):
                    aux = db.del_client((db.check_exists(nombre, apellido, True)))
                    if aux == True:
                        print(f"Se eliminaron los registros del cliente: {nombre} {apellido}")
                    else:
                        print(aux)
                    aux = var_continuar()
                else:
                    print(error_7)
                    aux = var_continuar()
            print(f"Introduciste {aux1}, eso no es una opción válida, prueba nuevamente.")
        elif acciones[4] == aux:        #Mostrar ayuda
            print("A continuación se muestran las opciones para el manejo de datos de la clientela.")
            print_opciones()
            aux = var_continuar()
        elif acciones[5] == aux:        #Salir del programa
            print(espaciador)
            print("\nElejiste cerrar el administrador de clientes. Gracias por trabajar con nosotros.")
            input()
            db.save()
            return exit()

cliente = Cliente()                     #Objeto de cliente
db = Database()                         #Base de datos
main(cliente, db)                       #Llamado a la función main