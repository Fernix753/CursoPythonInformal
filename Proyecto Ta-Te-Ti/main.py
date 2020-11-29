lista_simbolo = ['O', 'X']
lista_jugadores = ['Jugador', 'IA']
simb_vacio  = "-"
espaciador = "\n"*45


tablero, jugadas, ultimo_jugador, posiciones = None,None,None,None

def limpiar_tablero():
    global tablero
    global jugadas
    global ultimo_jugador
    global posiciones
    jugadas = 0
    ultimo_jugador = None
    posiciones = ["1","2","3","4","5","6","7","8","9"]
    tablero = {
        "1": simb_vacio, "2": simb_vacio, "3": simb_vacio,
        "4": simb_vacio, "5": simb_vacio, "6": simb_vacio,
        "7": simb_vacio, "8": simb_vacio, "9": simb_vacio
    }

def print_tablero():
    print("╔═══════╗")
    print("║",tablero["1"],tablero["2"],tablero["3"],"║")
    print("║",tablero["4"],tablero["5"],tablero["6"],"║")
    print("║",tablero["7"],tablero["8"],tablero["9"],"║")
    print("╚═══════╝")
    return

def print_posiciones():
    print("╔═══════╗")
    print("║","1","2","3","║")
    print("║","4","5","6","║")
    print("║","7","8","9","║")
    print("╚═══════╝")
    return

def triple_igualdad(s1, s2, s3):
    if s1 == s2 and s1 == s3:
        return True
    else:
        return False

def contar_igualdad(lista_valores, test_simbol):
    contador = 0
    enemy_simbol = lista_simbolo[lista_simbolo.index(test_simbol)-1]
    for x in lista_valores:
        if x == enemy_simbol:
            return 0
        if x == test_simbol:
            contador += 1
    return contador

def hor_1_fila(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["1"], tablero["2"], tablero["3"]
    if get_empy == True:
        if s1 == simb_vacio: return 1
        if s2 == simb_vacio: return 2
        if s3 == simb_vacio: return 3
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def hor_2_fila(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["4"], tablero["5"], tablero["6"]
    if get_empy == True:
        if s1 == simb_vacio: return 4
        if s2 == simb_vacio: return 5
        if s3 == simb_vacio: return 6
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def hor_3_fila(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["7"], tablero["8"], tablero["9"]
    if get_empy == True:
        if s1 == simb_vacio: return 7
        if s2 == simb_vacio: return 8
        if s3 == simb_vacio: return 9
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def diag__desc(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["1"], tablero["5"], tablero["9"]
    if get_empy == True:
        if s1 == simb_vacio: return 1
        if s2 == simb_vacio: return 5
        if s3 == simb_vacio: return 9
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def diag_ascen(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["7"], tablero["5"], tablero["3"]
    if get_empy == True:
        if s1 == simb_vacio: return 7
        if s2 == simb_vacio: return 5
        if s3 == simb_vacio: return 3
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def vert_1_col(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["1"], tablero["4"], tablero["7"]
    if get_empy == True:
        if s1 == simb_vacio: return 1
        if s2 == simb_vacio: return 4
        if s3 == simb_vacio: return 7
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def vert_2_col(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["2"], tablero["5"], tablero["8"]
    if get_empy == True:
        if s1 == simb_vacio: return 2
        if s2 == simb_vacio: return 5
        if s3 == simb_vacio: return 8
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def vert_3_col(test_simbol = None, get_empy = None):
    s1,s2,s3 = tablero["3"], tablero["6"], tablero["9"]
    if get_empy == True:
        if s1 == simb_vacio: return 3
        if s2 == simb_vacio: return 6
        if s3 == simb_vacio: return 9
        else: return False
    if test_simbol == None:
        if triple_igualdad(s1,s2,s3) and s1 != simb_vacio: return True
        else: return False
    elif test_simbol in lista_simbolo:
        return contar_igualdad([s1,s2,s3], test_simbol)

def check_linea():
    if hor_1_fila():
        return True
    if hor_2_fila():
        return True
    if hor_3_fila():
        return True
    if diag__desc():
        return True
    if diag_ascen():
        return True
    if vert_1_col():
        return True
    if vert_2_col():
        return True
    if vert_3_col():
        return True
    return False

def IA_win_try(player_simbol):
    if hor_1_fila(player_simbol) == 2: return hor_1_fila(get_empy = True)
    if hor_2_fila(player_simbol) == 2: return hor_2_fila(get_empy = True)
    if hor_3_fila(player_simbol) == 2: return hor_3_fila(get_empy = True)
    if diag__desc(player_simbol) == 2: return diag__desc(get_empy = True)
    if diag_ascen(player_simbol) == 2: return diag_ascen(get_empy = True)
    if vert_1_col(player_simbol) == 2: return vert_1_col(get_empy = True)
    if vert_2_col(player_simbol) == 2: return vert_2_col(get_empy = True)
    if vert_3_col(player_simbol) == 2: return vert_3_col(get_empy = True)
    return False

def IA_block_try(player_simbol):
    enemy_simbol = lista_simbolo[lista_simbolo.index(player_simbol)-1]
    if hor_1_fila(enemy_simbol) == 2: return hor_1_fila(get_empy = True)
    if hor_2_fila(enemy_simbol) == 2: return hor_2_fila(get_empy = True)
    if hor_3_fila(enemy_simbol) == 2: return hor_3_fila(get_empy = True)
    if diag__desc(enemy_simbol) == 2: return diag__desc(get_empy = True)
    if diag_ascen(enemy_simbol) == 2: return diag_ascen(get_empy = True)
    if vert_1_col(enemy_simbol) == 2: return vert_1_col(get_empy = True)
    if vert_2_col(enemy_simbol) == 2: return vert_2_col(get_empy = True)
    if vert_3_col(enemy_simbol) == 2: return vert_3_col(get_empy = True)
    return False

def IA_continue_try(player_simbol):
    if diag__desc(player_simbol) == 1: return diag__desc(get_empy = True)
    if diag_ascen(player_simbol) == 1: return diag_ascen(get_empy = True)
    if vert_2_col(player_simbol) == 1: return vert_2_col(get_empy = True)
    if hor_2_fila(player_simbol) == 1: return hor_2_fila(get_empy = True)
    if hor_1_fila(player_simbol) == 1: return hor_1_fila(get_empy = True)
    if hor_3_fila(player_simbol) == 1: return hor_3_fila(get_empy = True)
    if vert_1_col(player_simbol) == 1: return vert_1_col(get_empy = True)
    if vert_3_col(player_simbol) == 1: return vert_3_col(get_empy = True)
    return False

def IA_random_pick(player_simbol):
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
    for k,v in tablero.items():
        if v == simb_vacio:
            for x in range(len(descarte[k])+1):
                posibles.append(k)
    posibles_aux = posibles.copy()
    posibles.sort(key= lambda e: posibles_aux.count(e), reverse=True)
    return posibles[0]

def IA_pos_select(player_simbol):
    eleccion = None
    while eleccion == None or tablero[str(eleccion)] != simb_vacio:
        if IA_win_try(player_simbol):
            eleccion = IA_win_try(player_simbol)
        elif IA_block_try(player_simbol):
            eleccion = IA_block_try(player_simbol)
        elif IA_continue_try(player_simbol):
            eleccion = IA_continue_try(player_simbol)
        else:
            eleccion = IA_random_pick(player_simbol)
    return str(eleccion)
        
def jugar(indice_player): #Funcion de mi jugada, de ser un Jugador, verifica si la posición es válida, si es la IA llamamos a la función correspondiente
    global jugadas
    global ultimo_jugador
    player, player_simbol = lista_jugadores[indice_player], lista_simbolo[indice_player]

    if player != "IA":
        if jugadas < 1:
            print_posiciones()
        pos = input(f"Ingrese su posición a jugar ({player} - Ficha {player_simbol}):\n")
    else:
        pos = IA_pos_select(player_simbol)
    while (pos not in posiciones) or (tablero[pos] != simb_vacio):
        if (pos not in posiciones):
            pos = input(f"La posición ingresada '{pos}' no es válida. Prueba con otra diferente ({player} - Ficha {player_simbol}):\n")
        else:
            pos = input(f"La posición ingresada '{pos}' ya está ocupada. Prueba con otra diferente ({player} - Ficha {player_simbol}):\n")
    else:
        if player != "IA":
            print(espaciador , f"{player} está jugando.. Ficha {player_simbol}. Actualizando tablero...")
        else:
            print(espaciador , f"La {player} está jugando.. Ficha {player_simbol}. Actualizando tablero...")
        ultimo_jugador = player
        jugadas += 1
        tablero[pos] = player_simbol
    return ultimo_jugador, jugadas, player_simbol

def check_final(mvar): #mvar = Variable Multiple - Contiene: ultimo_jugador, jugadas, player_simbol
    ultimo_jugador, jugadas, player_simbol = mvar
    print_tablero()
    if check_linea() or jugadas == 9:
        if not check_linea():
            print("Empate!!!")
        else:
            print(f"Ganador: {ultimo_jugador} - Ficha: {player_simbol} ")
        return True
    return False

def opciones_input():
    print("A continuación las opciones para continuar:")
    print(">>  1  << -  Jugar contra la IA")
    print(">>  2  << -  Jugar multiplayer local")
    print(">>  3  << -  Jugar multiplayer online")
    return print(">>  z  << -  Salir")

def main():
    print(espaciador)
    print(espaciador)
    print("Bienvenido al increible y poderosisimo videojuego del Ta-Te-Ti! Recomendamos discreción con los gráficos explicitos del mismo!")
    
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
                turno = jugar(i)
                if check_final(turno):
                    aux = input()
                    opciones_input()
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
                turno = jugar(i)
                if check_final(turno):
                    aux = input()
                    opciones_input()
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