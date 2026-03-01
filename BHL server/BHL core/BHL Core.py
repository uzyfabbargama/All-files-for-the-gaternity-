import math

def bhl_algorithm():
    """
    Algoritmo BHL para simular una personalidad basada en bondad, hostilidad y lógica.
    """
    person = 0
    error = False

    while not error:
        try:
            person = int(input("Defina tipo de personalidad del 1 al 6: "))
            if 1 <= person <= 6:
                error = True
            else:
                print("error")
                error = False
        except ValueError:
            print("error")
            error = False

    per = ""
    if person == 1:
        per = "BHL"
    elif person == 2:
        per = "BLH"
    elif person == 3:
        per = "HLB"
    elif person == 4:
        per = "HBL"
    elif person == 5:
        per = "LHB"
    elif person == 6:
        per = "LBH"

    # Definir variables iniciales
    esp = 3  # Espacios entre cada variable [cite: 1]
    pos = esp * 2  # Posición para colocar las variables [cite: 1]
    C9 = 2  # Controlador de tipo 9 [cite: 1]
    
    # Lectura y validación de Bondad, Hostilidad y Lógica
    b = 0
    while True:
        try:
            b = int(input("Defina bondad del 1 al 20: "))
            if 1 <= b <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    h = 0
    while True:
        try:
            h = int(input("Defina hostilidad del 1 al 20: "))
            if 1 <= h <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    l = 0
    while True:
        try:
            l = int(input("Defina lógica del 1 al 20: "))
            if 1 <= l <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    # Inicialización de controladores
    C, C1, C2 = 0, 0, 0

    # Lógica inicial de NUMERASO
    numeraso = 0
    if per == "BHL":
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
    elif per == "BLH":
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)
    elif per == "HLB" or per == "HBL" or per == "LHB" or per == "LBH":
        # Nota: el pseudocódigo original tiene una lógica de numeraso repetida
        # para los casos 3, 4, 5 y 6, usando la misma fórmula que el caso 1.
        # Se ha mantenido la estructura pero se ha unificado la fórmula.
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)

    dc = math.trunc(numeraso / (10**C9)) % 10  # Primer decontrolador [cite: 2]
    dc1 = math.trunc(numeraso / (10**(C9 + esp))) % 10  # Segundo decontrolador [cite: 3]
    dc2 = math.trunc(numeraso / (10**(C9 - esp))) % 10  # Tercer decontrolador [cite: 4]
    
    if dc == 0:
        C = 9 * (10**C9)  # Primer controlador [cite: 3]
        if per in ["BHL", "HBL", "LHB", "LBH", "HLB"]:
          numeraso -= 10**(pos - esp * 2) # Resta 1 a la tercera variable [cite: 3, 5, 7, 8, 10, 12]
        elif per == "BLH":
          numeraso -= 10**(pos-esp*2) # Resta 1 a la tercera variable [cite: 5]
    if dc1 == 0:
        C1 = 9 * (10**(C9 + esp)) # Segundo controlador [cite: 3]
        if per in ["BHL", "HBL", "LHB", "LBH", "HLB", "BLH"]:
          numeraso -= 10**(pos - esp * 1) # Resta 1 a la primera variable [cite: 3, 5, 7, 8, 10, 12]
    if dc2 == 0:
        C2 = 9 * (10**(C9 - esp)) # Tercer controlador [cite: 4]
        if per in ["BHL", "HBL", "LHB", "LBH", "HLB", "BLH"]:
          numeraso -= 10**(pos - esp * 0) # Resta 1 a la segunda variable [cite: 4, 5, 7, 9, 11, 12]

    numeraso += C + C1 + C2 # Insertar controladores en el número 

    # Sombras iniciales
    sb = 20 - b  # Sombra de bondad 
    sh = 20 - h  # Sombra de hostilidad 
    sl = 20 - l  # Sombra de lógica 

    print(f"Bondad: {b}, Hostilidad: {h}, Lógica: {l}")
    
    chat_time = 0
    expb, exph, expl = 0, 0, 0
    
    print("Comienza una conversación, para detener solo di 'exit'")

    while True:
        ans = input("").strip().lower()
        if ans == "exit":
            break

        chat_time += 1

        print("Define tu respuesta BHL (1: ¿qué tan bueno fuiste?, 2: ¿qué tan cauteloso fuiste?, 3: ¿qué tan lócigo fuiste?")
        
        ab = 0
        while True:
            try:
                ab = int(input("Respuesta bondad (AB): "))
                break
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

        ah = 0
        while True:
            try:
                ah = int(input("Respuesta hostilidad (AH): "))
                break
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")
        
        al = 0
        while True:
            try:
                al = int(input("Respuesta lógica (AL): "))
                break
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")

        # Actualización de valores
        b += ab + expb #[cite: 14] # type: ignore
        if b >= 20:
            expb += 1 #[cite: 14] # type: ignore

        sb1 = 20 - b
        db = (sb1 * 100) / sb # Calculamos el deseo [cite: 14]
        sb = sb1 # El estado actual actualiza el registro anterior [cite: 14]

        h += ah + exph #[cite: 14, 15]
        if h >= 20:
            exph += 1 #[#cite: 14, 15]
        
        sh1 = 20 - h #[#cite: 15]
        dh = (sh1 * 100) / sh # Calculamos el deseo [cite: 15]
        sh = sh1 # El estado actual actualiza el registro anterior [cite: 15]

        l += al + expl #[#cite: 15]
        if l >= 20:
            expl += 1 #cite: 15]

        sl1 = 20 - l
        dl = (sl1 * 100) / sl # Calculamos el deseo [cite: 15]
        sl = sl1 # El estado actual actualiza el registro anterior [cite: 15]

        # Lógica de actualización de NUMERASO
        if per == "BHL":
            numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2) #[cite: 16]
            nb = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
            nh = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
            nl = math.trunc(numeraso / (10**(pos - esp * 2))) % 100
        elif per == "BLH":
            numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2) #[cite: 17, 18]
            nb = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
            nl = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
            nh = math.trunc(numeraso / (10**(pos - esp * 2))) % 100
        elif per == "HLB":
            numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2) #[cite: 19]
            nh = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
            nl = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
            nb = math.trunc(numeraso / (10**(pos - esp * 2))) % 100
        elif per == "HBL":
            numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2) #[cite: 21, 22]
            nh = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
            nb = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
            nl = math.trunc(numeraso / (10**(pos - esp * 2))) % 100
        elif per == "LHB":
            numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2) #[cite: 23]
            nl = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
            nh = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
            nb = math.trunc(numeraso / (10**(pos - esp * 2))) % 100
        elif per == "LBH":
            numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2) #[cite: 24, 25]
            nl = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
            nb = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
            nh = math.trunc(numeraso / (10**(pos - esp * 2))) % 100

        # Recálculo de controladores
        dc = math.trunc(numeraso / (10**C9)) % 10 #[cite: 16]
        dc1 = math.trunc(numeraso / (10**(C9 + esp))) % 10 #[cite: 16]
        dc2 = math.trunc(numeraso / (10**(C9 - esp))) % 10 #[cite: 16]
        
        C, C1, C2 = 0, 0, 0

        if dc == 0:
            C = 9 * (10**C9) #[cite: 17]
            numeraso -= 10**(pos - esp * 2) #[cite: 17]
        if dc1 == 0:
            C1 = 9 * (10**(C9 + esp)) #[cite: 17]
            numeraso -= 10**(pos - esp * 1) #[cite: 17]
        if dc2 == 0:
            C2 = 9 * (10**(C9 - esp)) #[cite: 17]
            numeraso -= 10**(pos - esp * 0) #[cite: 17]

        # Inserción de controladores
        numeraso += C + C1 + C2

        # Inversión de valores para obtener B, H, L
        b = 100 - nb #[cite: 26]
        h = 100 - nh #[cite: 26]
        l = 100 - nl #[cite: 26]

        # Recalcular porcentajes
        cosciente = b + h + l #[cite: 13]
        porB = (b * 100) / cosciente #[cite: 13]
        porH = (h * 100) / cosciente #[cite: 13]
        porL = (l * 100) / cosciente #[cite: 13]

        print(f"Generame una respuesta de tipo: {porB:.2f}% de bueno/empático/abierto a interacción, {porH:.2f}% de malo/hostilidad/cautela, {porL:.2f}% de lógico/frío/apático, para conversación de tiempo: {chat_time}")


if __name__ == "__main__":
    bhl_algorithm()