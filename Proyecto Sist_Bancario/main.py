import pandas as pd
import random as rd

# Formato de datos
# data = {
#     0: {'CBU':'9876543210123456', 'Nombre': 'Juan', 'Apellido': 'Pérez', 'PIN': 1234, 'SALDO (PESOS)': 1, 'SALDO (USD)': 0},
#     1: {'CBU':'9876543210123457', 'Nombre': 'Rodrigo', 'Apellido': 'Saez', 'PIN': 1122, 'SALDO (PESOS)': 50, 'SALDO (USD)': 0}
#     entero,    string de 16 numeros,         String,                String,      entero,                entero          entero
# }
# Formato para agregar datos al diccionario
# data[2]={'CBU':'9876543210123222', 'Nombre': 'Pedro', 'Apellido': 'Nuñez', 'PIN': 1322, 'SALDO (PESOS)': 25, 'SALDO (USD)': 0}

xlsx = None
data = None
error_1 = "Al parecer los datos ya estaban cargados."
error_2 = "Al parecer no se ha cargardo correctamente la base datos."
error_3 = "Al parecer alguno de los datos es invalido."
error_4 = "Hubo un error al intentar guardar la base de datos."
archivo = "./bna_topoland.xlsx"
hoja_datos = "BANCO TOPOLAND"

def cargar_xlsx(data,archivo,hoja):
    if data==None:
        data = pd.read_excel(archivo,sheet_name=hoja, index_col=0)
        data = data.to_dict('index')
        return True, data
    else:
        return False, error_1

xlsx, data = cargar_xlsx(data, archivo, hoja_datos)

def guardar_xlsx(data,archivo,hoja):
    if data!=None:
        data = pd.DataFrame.from_dict(data , orient='index')
        try:
            data.to_excel(archivo,sheet_name=hoja_datos)
        except PermissionError:
            return False, error_4
        else:
            return True, True
    else:
        return False, error_2

def check_string(nombre):
    aux = 0
    if isinstance(nombre, int): return False #Si es un entero, retorna False.
    for x in nombre:
        if x.isnumeric() or x.isspace(): #Si encuentra un número o un espacio, retorna False
            aux += 1
            break
    aux = True if aux < 1 else False
    return aux

def check_16digit(valor):
    if isinstance(valor, int): return False #Si es un entero, retorna False.
    if valor.isnumeric() and len(str(valor))==16: #Checkea si es numerico y de 16 digitos
        return True
    else:
        return False

def check_pin(valor):
    if isinstance(valor, int) and len(str(valor))==4: #Checkea si es entero y de 4 digitos
        return True
    else:
        return False

def generar_cbu():
    cbu_set = set()
    if xlsx == True:
        for x in data:
            cbu_set.add(data[x]['CBU'])
        cbu = rd.randrange(1000000000000000, 9999999999999999)
        while cbu in cbu_set:
            cbu = rd.randrange(1000000000000000, 9999999999999999)
        return str(cbu)
    else:
        return False

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
        if isinstance(v, int):
            self.saldo_ars=v
            return True
        else:
            return False
    def saldo_usd_set(self, v):
        if isinstance(v, int):
            self.saldo_usd=v
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

def crear_cliente(nombre,apellido,pin):
    if xlsx == True:
        cliente_act.reset()
        un_cbu = generar_cbu()
        if cliente_act.name_set(nombre) and cliente_act.sname_set(apellido) and cliente_act.cbu_set(un_cbu) and cliente_act.pin_set(pin) and cliente_act.saldo_ars_set(0) and cliente_act.saldo_usd_set(0):
            return True, True
        else:
            cliente_act.reset()
            return False, error_3
    else:
        return False, error_2

def guardar_cliente(class_id):
    if xlsx == True:
        if data!=None:
            data[max(data.keys())+1] = {'CBU':class_id.cbu_get(), 'Nombre': class_id.name_get(), 'Apellido': class_id.sname_get(),
                                        'PIN': class_id.pin_get(), 'SALDO (PESOS)': class_id.saldo_ars_get(), 'SALDO (USD)': class_id.saldo_usd_get()}
            return True, True
        else:
            return False, error_2
    else:
        return False, error_2

cliente_act = Cliente()
retorno, error = crear_cliente("Fernando", "Hru", 3232)

# retorno, error = guardar_xlsx(data, archivo, hoja_datos)
# print(retorno, error)
# fer = Cliente()
# fer.pin_set(4562)
# print(fer.pin_get())