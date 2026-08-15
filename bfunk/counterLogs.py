b = 0
c = input("Introduce log: ")
d = "0"
loop_mode = 0
print("Comandos")
print("cl = change log")
print("lm = loop mode")
print("cc = change_command")
print("undo")
print("load")
print("save")
def e_commands(_ecomand):
    #_ecomand = e
    global c, d, loop_mode, e
    if _ecomand == "cl":
        c = input("Introduce log nuevo: ")
    elif _ecomand == "lm":
        d = int(d)
        #if not type(d) is not int:
            #d = ord(str(d)[0]) & 0
        #    d = int(d)
        
        f = int(input("Iteración del bucle: ")) - 1
        d += f
        loop_mode = 1
        print("¡Modo bucle activado!")
    elif _ecomand == "cc":
        loop_mode = 0
        d = "0"
        print("Comandos")
        print("cl = change log")
        print("lm = loop mode")
        print("cc = change_command")
        _ecomand = input("Introduce comando: ")
        e_commands(_ecomand)
    elif _ecomand == "undo":
        b -= last_step
        print(f"Deshecho. Pasos actuales: {b}")
    elif _ecomand == "save":
        with open("debug_state.txt", "w") as f:
            f.write(f"{b}\n{c}\n{d}\n{loop_mode}\n")
        print("Estado guardado en debug_state.txt")
    elif _ecomand == "load":
        with open("debug_state.txt", "r") as f:
            b = int(f.readline())
            c = f.readline().strip()
            d = f.readline().strip()
            loop_mode = int(f.readline())
        print(f"Estado cargado: n {b} = {c}")
    #_ecomand = ord(str(_ecomand)[0]) & 0
    _ecomand = ""
    e = _ecomand
    #return d, c, _ecomand
e = input("Introduce comando: ")
while True:
   # d, c, e = e_commands(e)
    e_commands(e)
    a = input("> ")
    g = a[0]
    try:
        a = int(a)  # Acepta cualquier número (incluido -1)
        b += a
    except ValueError:
        # No es un número, es un comando
        e = a
        e_commands(e)
    #if b == 0:
        #print("ALERTA: b es 0")
        #print(f"DEBUG: {a}")
    #if type(d) is str:
        #print("DEBUG: d es string")
        #print(f"d vale: {d}")
        #print("ARREGLADO: d ahora es int")
        d = ord(str(d)[0]) & 0
    if type(d) is not str:
        d += loop_mode
    #print(f"DEBUG: Avance de iteracion: {loop_mode}")
    #print(f"DEBUG: Comando actual: {e}")
    if loop_mode:
        print(f"n {b} = {d} {c}")
    else:
        print(f"n {b} = {c}")
