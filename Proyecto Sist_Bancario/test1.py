import pandas as pd
import random as rd
import os.path
from os import path

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
    _file = "./bna_topoland.xlsx"
    _sheet= "BANCO TOPOLAND"

    def load(self):                     #Carga en un diccionario un dataframe extraido de un excel.
        if self.data==None:
            if path.exists(self._file):
                self.data = pd.read_excel(self._file,sheet_name=self._sheet, index_col=0)
                self.data = self.data.to_dict('index')
                self.dbcheck = True
                print(self.data) #Borrar
                return True, True
            else:
                return False, error_6
        else:
            return False, error_1

    def save(self):                     #Guarda en un excel un dataframe a partir de la variable data.
        if self.data!=None:
            self.data = pd.DataFrame.from_dict(self.data , orient='index')
            try:
                self.data.to_excel(self._file,sheet_name=self._sheet)
            except PermissionError:
                return False, error_4
            else:
                self.data = self.data.to_dict('index')
                return True, True
        else:
            return False, error_2

    def check_exists(self, nombre,      #Verifica (ineficientemente, posible mejora) si ya existe esa combinación de Nombre y apellido en la database.
        apellido, idget=None ): 
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
                    return self.save()
                else:
                    cliente.reset()
                    return False, error_5
            else:
                cliente.reset()
                return False, error_3
        else:
            cliente.reset()
            return False, error_2

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
    
    def print_client(self):             #Recorre el diccionario e imprime los nombres de los clientes.
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

db = Database()
cliente = Cliente()

print(db.load())
# print(db.check_exists("Juan", "Kr"))
# print(db.create_client(cliente, "Luis", "Kr", 9865))