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

xlsx = None
data = None
espaciador = "\n"*25
respuestas = ["SI", "NO"] #Respuesta 0 - Afirmación \\ Respuesta 1 - Negación
acciones = ["0", #Mostrar lista de clientes.
            "1", #Mostrar info de un cliente en especificio
            "2", #Agregar un cliente a la base de datos.
            "3", #Eliminar un cliente de la base de datos.
            "H", #Mostrar ayuda
            "Z"] #Salir del programa

error_0 = "Hubo un error inesperado. No se completo la ultima tarea."
error_1 = "Al parecer los datos ya estaban cargados."
error_2 = "Al parecer no se ha cargardo correctamente la base datos."
error_3 = "Al parecer alguno de los datos es invalido."
error_4 = "Hubo un error al intentar guardar la base de datos."
error_5 = "Al parecer el cliente que intentas crear ya existe en la base de datos."
error_6_0 = "missing_file"
error_6_1 = f"No se encontró el documento en el directorio actual ¿Deseas crear una base de datos nueva? [{respuestas[0]}/{respuestas[1]}]"
error_7 = "Al parecer el usuario que ingresaste no existe en la base de datos."
archivo = "./bna_topoland.xlsx"
hoja_datos = "BANCO TOPOLAND"

def cargar_xlsx(archivo,hoja):          #Carga en un diccionario un dataframe extraido de un excel.
    global data
    if data==None:
        if path.exists(archivo):
            data = pd.read_excel(archivo,sheet_name=hoja, index_col=0)
            data = data.to_dict('index')
            return True, data
        else:
            return False, error_6_0
    else:
        return False, error_1

def guardar_xlsx(archivo,hoja):         #Guarda en un excel un dataframe a partir de la variable data.
    global data
    if data!=None:
        data = pd.DataFrame.from_dict(data , orient='index')
        try:
            data.to_excel(archivo,sheet_name=hoja_datos)
        except PermissionError:
            return False, error_4
        else:
            data = data.to_dict('index')
            return True, True
    else:
        return False, error_2

def print_clientes():                   #Recorre el diccionario e imprime los nombres de los clientes.
    global data
    cont = 0
    for x in data: 
        print(f"-Cliente {x}: {data[x]['Nombre']} {data[x]['Apellido']}")
        cont += 1
        if cont == 10:
            print(f"Estos son los primeros {cont} clientes de la base de datos.")
            break

def check_string(nombre):               #Verifica que una cadena de texto no tenga espacios o numeros.
    aux = 0
    if isinstance(nombre, int): return False #Si es un entero, retorna False.
    for x in nombre:
        if x.isnumeric() or x.isspace(): #Si encuentra un número o un espacio, retorna False
            aux += 1
            break
    aux = True if aux < 1 else False
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

def check_Existe(nombre, apellido, info=None ):     #Verifica (ineficientemente, posible mejora) si ya existe esa combinación de Nombre y apellido en la database.
    global data
    aux = False
    aux1= None 
    for x in data:
        if data[x]['Nombre'] == nombre and data[x]['Apellido'] == apellido:
            aux = True
            aux1 = x
            break
    if info != True:
        return aux
    elif aux == True:
        return aux1
    else:
        return aux

def generar_cbu():                      #Genera un número de 16 digitos (que no exista) y lo devuelve como un string.
    global data, xlsx
    cbu_set = set()
    if xlsx == True:
        if len(data.keys()) > 0:
            for x in data:
                cbu_set.add(data[x]['CBU'])
        cbu = rd.randrange(1000000000000000, 9999999999999999)
        while cbu in cbu_set:
            cbu = rd.randrange(1000000000000000, 9999999999999999)
        return str(cbu)
    else:
        return False

class Cliente():                        #Clase de clientes.
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

    def name_set(self, v): #La 'v' es de value xd
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

def eliminar_cliente(dict_id):          #Eliminar cliente, lo borra del diccionario, y se guarda en el excel el cambio
    global data, archivo, hoja_datos
    try: 
        del data[dict_id]
    except:
        aux = error_0
    else:
        aux = True
        guardar_xlsx(archivo, hoja_datos)
    return aux

def guardar_cliente(class_id):          #Guarda los datos del cliente en mi diccionario/database
    global data, xlsx
    if xlsx == True and data!=None:
        aux = max(data.keys())+1 if len(data.keys()) > 0 else 0
        data[aux] = {'CBU':str(class_id.cbu_get()).capitalize(), 'Nombre': str(class_id.name_get()).capitalize(), 'Apellido': class_id.sname_get(),
                    'PIN': class_id.pin_get(), 'SALDO (PESOS)': class_id.saldo_ars_get(), 'SALDO (USD)': class_id.saldo_usd_get()}
        return guardar_xlsx(archivo,hoja_datos)
    else:
        return False, error_2

def crear_cliente(nombre,apellido,pin): #Verifica que no exista, que todos los parametros sean válidos y si todo está correcto, lo guarda en mi diccionario/database.
    global data, xlsx
    if xlsx == True:
        cliente_act.reset()
        un_cbu = generar_cbu()
        if cliente_act.name_set(nombre) and cliente_act.sname_set(apellido) and cliente_act.cbu_set(un_cbu) and cliente_act.pin_set(pin) and cliente_act.saldo_ars_set(0.0) and cliente_act.saldo_usd_set(0.0):
            if not check_Existe(nombre, apellido):
                aux, aux1 = guardar_cliente(cliente_act)
                if aux == True:
                    return True, un_cbu
                else:
                    return False, aux1
            else:
                cliente_act.reset()
                return False, error_5
        else:
            cliente_act.reset()
            return False, error_3
    else:
        cliente_act.reset()
        return False, error_2

def cargar_cliente(dict_id):            #Carga la info del cliente (desde el diccionario), a la clase de cliente.
    global data
    if (cliente_act.name_set(data[dict_id]['Nombre']) and
        cliente_act.sname_set(data[dict_id]['Apellido']) and
        cliente_act.cbu_set(data[dict_id]['CBU']) and
        cliente_act.pin_set(data[dict_id]['PIN']) and
        cliente_act.saldo_ars_set(data[dict_id]['SALDO (PESOS)']) and
        cliente_act.saldo_usd_set(data[dict_id]['SALDO (USD)'])):
        return cliente_act
    else:
        return False

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

def main():                             #Main
    global data, xlsx, archivo, hoja_datos
    print(espaciador)
    print(f"Bienvenido al sistema bancario de {hoja_datos}")
    input("Cargando base de datos. Presiona enter para continuar.")
    for i in range(96):                 #No sé que hace todo esto pero me gusto.
        sys.stdout.write('\r')
        sys.stdout.write("[%-10s] %d%%" % ('='*i, 1*i))
        sys.stdout.flush()
        sleep(0.02)

    xlsx, data = cargar_xlsx(archivo, hoja_datos)     #Intento de carga del documento.
    
    if not xlsx:                        #Si no se pudo cargar el excel, pregunta si desea crear una base de datos nueva.
        if data == error_6_0:
            print("\n"+error_6_1)
            aux = input()
            aux = aux.upper().strip()
            while aux not in respuestas:
                print("Tu respuesta no concuerda con la pregunta, intenta nuevamente.")
                print(error_6_1)
                aux = input()
                aux = aux.upper().strip()
            if aux == respuestas[0]:
                data = {}
                xlsx = True
            elif aux == respuestas[1]:
                print("\nSin conexión con la base de datos no se pueden administrar los clientes, el programa se cerrará. Presiona enter para continuar.")
                input()
                return exit()
        else:
            print("\n" + error_4, "El programa se cerrará. Presiona enter para continuar.")
            input()
            return exit()
    print(espaciador)
    print(f"\nAdministración de clientes - {hoja_datos}")
    print("A continuación se muestran las opciones para el manejo de datos de la clientela.")
    print_opciones()
    aux = input()                       #Input auxiliar
    while type(data) != "<class 'NoneType'>":
        aux = str(aux).strip().upper()
        while aux not in acciones:      #Si el input no es una opción válida, se pregunta nuevamente.
            print(f"La accion ingresada {aux} no está en la lista, prueba nuevamente o ingresa '{acciones[4]}' para mostrar una ayuda")
            aux = input()
            aux = str(aux).strip().upper()
        if acciones[0] == aux:          #Mostrar lista de clientes.
            print(espaciador)
            print("La lista de clientes registrados en nuestra base de datos es la siguiente:")
            print_clientes()
            aux = var_continuar()
        elif acciones[1] == aux:        #Mostrar info de un cliente en especificio
            print(espaciador)
            print("Buscador de clientes. Complete los campos aqui abajo:")
            nombre = input("\nIngresa el nombre del cliente: ")
            apellido = input("Ingresa el apellido del cliente: ")
            nombre, apellido = nombre.capitalize(), apellido.capitalize()
            if check_Existe(nombre, apellido):
                cliente_act = cargar_cliente((check_Existe(nombre, apellido, True)))
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
            aux, aux1 = crear_cliente(nombre,apellido,pin)
            if aux == True:
                print(f"Cliente creado con éxico, se le asigno el siguiente número de cuenta:{aux1}")
            else:
                print(aux1)
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
                print_clientes()
                id = input("\nIngresa el ID del cliente: ")
                while not isinstance(id, int):
                    if id.isnumeric():
                        id = int(id)
                    else:
                        id = input("El ID ingresado no es válido, prueba nuevamente: ")
                historia = data[id]
                aux = eliminar_cliente(id)
                if aux == True:
                    print(f"Se eliminaron los registros del cliente: {historia['Nombre']} {historia['Apellido']}")
                    guardar_xlsx(archivo, hoja_datos)
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
                if check_Existe(nombre, apellido):
                    aux = eliminar_cliente((check_Existe(nombre, apellido, True)))
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
            guardar_xlsx(archivo, hoja_datos)
            return exit()

cliente_act = Cliente()                 #Objeto de cliente manipulable
main()                                  #Llamado a la función main