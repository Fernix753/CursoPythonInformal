"""
Nim es un juego sencillo donde el segundo jugador (si conoce el truco) siempre ganará. 
Tiene 3 simples reglas:
- Se empieza con 12 tokens
- Cada jugador debe tomar 1, 2 o 3 tokens en su turno
- El jugador que toma el ultimo token gana
Para ganar, el segundo jugador (en este caso, la computadora) debe tomar 4 menos el número de tokens que tomo el jugador en su turno.
El objetivo es diseñar un juego de Nim (Jugador vs Computadora) donde la computadora siempre gane.
"""
fsimb = "#" #filled simb
esimb = "-" #empty simb
quites = [1,2,3]
pila = list(fsimb*12)
actual = None
lista_jugadores = ['Jugador', 'IA']
espaciador = "\n"*45

def limpiar_tablero():
    pila = list(fsimb*12)
    lista_jugadores = ['Jugador', 'IA']

def limpiar_List(x):
    return str(x).replace("[", "").replace("]", "").replace("'", "").replace(",", "")

def setlong(cadena, long):
    long = long if (isinstance(long, int)) else int(long)
    cadena = cadena if (isinstance(cadena, str)) else str(cadena)
    if len(cadena) == long: return cadena
    elif len(cadena) > long: return cadena[:long]
    else: return cadena+" "* (long - len(cadena))


def print_tablero(lp, actual): #Lp - Last Player
    print( "╔══════════════╦══════════╗")
    print(F"║ {setlong(lp,12)} ║ Tks:{setlong(actual,4)} ║")
    print( "╠══════════════╩══════════╣")
    print( "║",   limpiar_List(pila),"║")
    print( "╚═════════════════════════╝")

def retirar(n):
    if bool(n) and (isinstance(n, int) or n.isdigit()):
        actual, n = pila.count(fsimb), n if isinstance(n, int) else int(n)
    else:
        return False
    if n > max(quites) or n < min(quites) or n > actual:
        return False
    else:
        for x in range(n):
            pila[pila.index(fsimb)] = esimb
        return True

def tks_IA():
    actual = pila.count(fsimb)
    for x in quites:
        if ((actual - x )%(max(quites)+1) == 0):
            return x
    print("Verga la cague")

def juegar(i):
    jugador = lista_jugadores[i]
    if lista_jugadores[i] == "IA":
        tks = tks_IA()
    else:
        tks = input(f"Introduce la cantidad de fichas a retirar ({jugador}):")
    while not(retirar(tks)):
        tks = input(f"Lo introducido anteriormente, {tks}, intenta nuevamente:")
    else:
        actual = pila.count(fsimb)
        print_tablero(jugador, actual)
        if actual <= 0: return True

def opciones_input():
    print("A continuación las opciones para continuar:")
    print(">>  1  << -  Jugar contra la IA")
    print(">>  2  << -  Jugar multiplayer local")
    print(">>  3  << -  Jugar multiplayer online")
    return print(">>  z  << -  Salir")

def main():
    print(espaciador)
    print(espaciador)
    print("Bienvenido al increible y poderosisimo videojuego del Nim! Recomendamos discreción con los gráficos explicitos del mismo!")
    opciones = ["1", "2", "3", "ayuda", "z"]
    opcion = None
    opciones_input()
    opcion = input(f"Opción deseada:\n")
    while True:
        limpiar_tablero()
        if   opciones[0] == opcion:                                            # Jugar contra la IA
            print(espaciador)
            i=0
            while True:
                if juegar(i):
                    print(f"Ganador: {lista_jugadores[i]}")
                    opcion = input(f"Opción deseada:\n")
                    break
                i=1 if i==0 else 0
        elif opcion != None and opciones[1] == opcion.replace(" ", ""):        # Jugar multiplayer local
            print(espaciador)
            print("Elegiste jugar el modo 1vs1 - Necesitas un amigo que juegue con vos (F si no tenes porque no programé ninguna manera de volver atras)!")
            aux = input("A continuación puedes ingresar tu nombre (Jugador 1) para usar uno personalizado. Puedes dejarlo en blanco para usar por defecto:")
            if bool(aux.replace(" ", "")):
                lista_jugadores[0] = aux
            else:
                lista_jugadores[0] = "Jugador 1"
            aux = input("A continuación puedes ingresar tu nombre (Jugador 2) para usar uno personalizado. Puedes dejarlo en blanco para usar por defecto:")
            if bool(aux.replace(" ", "")):
                lista_jugadores[1] = aux
            else:
                lista_jugadores[1] = "Jugador 2"
            print(espaciador)
            i=0
            while True:
                if juegar(i):
                    print(f"Ganador: {lista_jugadores[i]}")
                    opcion = input(f"Opción deseada:\n")
                    break
                i=1 if i==0 else 0
        elif opcion != None and opciones[2] == opcion.replace(" ", ""):        # Jugar multiplayer online
            print(espaciador)
            aux = input("Flasheaste confianza bro jajaja no es por ahi!\nAcabas de romper tu pc, y exploto python")
            exit()
        elif opcion != None and opciones[3] == opcion.replace(" ", "").lower():# Ayuda
            opciones_input()
            opcion = input(f"Opción deseada:\n")
        elif opcion != None and opciones[4] == opcion.replace(" ", "").lower():# Salir
            print(espaciador)
            aux = input("Gracias por probar el programa!")
            exit()
        else:
            print(espaciador)
            opcion = input(f"La opcion elegida '{opcion}' no es válida. Prueba ingresando otra o usando >>  ayuda  << para ver las posibles opciones!:\n") 
main()