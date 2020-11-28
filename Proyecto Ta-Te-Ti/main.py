import random

sb = {
    "Jugador 1" : "O",
    "IA" : "X"
}

jl = ["Jugador 1", "IA"]

tablero = None
posiciones = None

def limpiar_tablero():
    global tablero
    global posiciones
    posiciones = ["1","2","3","4","5","6","7","8","9"]
    tablero = {
        "1": "-", "2": "-", "3": "-",
        "4": "-", "5": "-", "6": "-",
        "7": "-", "8": "-", "9": "-"
    }

def print_tablero():
    print("╔═══════╗")
    print("║ "+tablero["1"]+" "+tablero["2"]+" "+tablero["3"]+" ║")
    print("║ "+tablero["4"]+" "+tablero["5"]+" "+tablero["6"]+" ║")
    print("║ "+tablero["7"]+" "+tablero["8"]+" "+tablero["9"]+" ║")
    print("╚═══════╝")
    return
    
def print_posiciones():
    print("1" + " " + "2" + " " + "3")
    print("4" + " " + "5" + " " + "6")
    print("7" + " " + "8" + " " + "9")
    return

def check_linea():
    if tablero["1"] != "-":
        if tablero["1"] == tablero["2"]     and tablero["1"] == tablero["3"]:
            return tablero["1"] #"linea horizontal, primera fila"
        elif tablero["1"] == tablero["4"]   and tablero["1"] == tablero["7"]:
            return tablero["1"] #"linea vertical, primera columna"
        elif tablero["1"] == tablero["5"]   and tablero["1"] == tablero["9"]:
            return tablero["1"] #"linea diagonal descendente"
    if tablero["2"] != "-":
        if tablero["2"] == tablero["5"]     and tablero["2"] == tablero["8"]:
            return tablero["2"] #"linea vertical segunda columna"
    if tablero["3"] != "-":
        if tablero["3"] == tablero["6"]     and tablero["3"] == tablero["9"]:
            return tablero["3"] #"linea vertical tercera columna"
        elif tablero["3"] == tablero["5"]   and tablero["3"] == tablero["7"]:
            return tablero["3"] #"Linea diagonal ascendente"
    if tablero["4"] != "-":
        if tablero["4"] == tablero["5"]     and tablero["4"] == tablero["6"]:
            return tablero["4"] #"Linea horizontal, segunda fila"
    if tablero["7"] != "-":
        if tablero["7"] == tablero["8"]     and tablero["7"] == tablero["9"]:
            return tablero["7"] #"Linea horizontal, tercera fila"
    return ""

def check_lleno():
    for k,v in tablero.items():
        if v == "-":
            return False
    return True

def getplayer(x):
    for k,v in sb.items():
        if v == x:
            return k

def IApos():
    posibles = []
    descarte = {
        "1":["2","3","4","5","7","9"],
        "2":["1","3","5","8"],
        "3":["1","2","5","6","7","9"],
        "4":["1","5","6","7"],
        "5":["1","2","3","4","6","7","8","9"],
        "6":["3","4","5","9"],
        "7":["1","3","4","5","8","9"],
        "8":["2","5","7","9"],
        "9":["1","3","5","6","7","8"],
    }
    ord_dic = {}
    for k,v in tablero.items():
        if v == "-":
            for x in range(len(descarte[k])+1):
                posibles.append(k)
    for x in list(descarte.keys()):
        if x in posibles:
            for y in descarte[x]:
                if y not in posibles:
                    posibles.pop(posibles.index(x))
    for x in posibles:
        if x in ord_dic:
            ord_dic[x] += 1
        else:
            ord_dic[x] = 1
    def cantPerList(e):
        return ord_dic[e]
    posibles.sort(key=cantPerList, reverse=True)
    ord_dic = None
    print(posibles)
    return posibles[0]

def juega(player_simbol, pos=None):
    if getplayer(player_simbol) != "IA":
        if pos == None:
            pos = input(f"Ingrese su posición a jugar ({getplayer(player_simbol)} - Ficha {sb[getplayer(player_simbol)]}):\n")
    else:
        pos = IApos()
    while (pos not in posiciones) or (tablero[pos] != "-"):
        if (pos not in posiciones):
            pos = input(f"La posición ingresada '{pos}' no es válida. Prueba con otra diferente ({getplayer(player_simbol)} - Ficha {sb[getplayer(player_simbol)]}):\n")
        else:
            pos = input(f"La posición ingresada '{pos}' ya está ocupada. Prueba con otra diferente ({getplayer(player_simbol)} - Ficha {sb[getplayer(player_simbol)]}):\n")
    tablero[pos] = player_simbol
    return

def finalcheck():
    print_tablero()
    if bool(check_linea()) or check_lleno():
        if not bool(check_linea()):
            print("Empate!!!")
        else:
            print(f"Ganador: {getplayer(check_linea())} - Ficha: {sb[getplayer(check_linea())]} ")
        return True
    return False

def main():
    limpiar_tablero()
    while True:
        juega(sb[jl[0]])
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nActualizando tablero...")
        if finalcheck():
            break
        juega(sb[jl[1]])
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nLa IA está jugando.. Actualizando tablero...")
        if finalcheck():
            break

main()