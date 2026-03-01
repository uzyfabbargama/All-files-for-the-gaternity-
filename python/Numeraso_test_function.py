class ConcienciaBHL:
    def __init__(self, X, Y, Z):
        self.numero_generado = X*(10**(3*2)) + Y*(10**3) + Z + 9*10**8 + 9*10**5 + 9*10**2
    def actualizar_estado(self, num_a_sumar):
        # La lógica de los controladores y detectores
        C1 = (self.numero_generado // 10**8) % 10
        C2 = (self.numero_generado // 10**5) % 10
        C3 = (self.numero_generado // 10**2) % 10
        D1 = ((C1 - 8) - 1) * -1
        D2 = ((C2 - 8) - 1) * -1
        D3 = ((C3 - 8) - 1) * -1
        
        # Corrección de los controladores para reestablecerse
        self.numero_generado += D1 * 9 * (10**8) # Corregido: afecta a la posición correcta
        self.numero_generado += D2 * 9 * (10**5)
        self.numero_generado += D3 * 9 * (10**2)
        
        # El Numeraso se actualiza con la entrada del usuario
        self.numero_generado += num_a_sumar
        
        # La lógica de los efectos
        self.numero_generado += D1 % 2 * 1 # afecta a Z
        self.numero_generado -= D1 % 2 * (10**3) # afecta a Y
        self.numero_generado -= D2 % 2 * 1 # afecta a Z
        self.numero_generado -= D3 % 2 * (10**(3 * 2)) # afecta a X

        print(f"Estado actual del Numeraso: {self.numero_generado}")

# --- Inicio del programa ---
X_inicial = int(input("Define Bondad (X): ")) % 100
Y_inicial = int(input("Define Hostilidad (Y): ")) % 100
Z_inicial = int(input("Define Lógica (Z): ")) % 100

# Creamos una instancia de la clase. Es como si crearas una "conciencia".
bot = ConcienciaBHL(X_inicial, Y_inicial, Z_inicial)

while True:
    pos = int(input("Elija una variable para afectar (1:X, 2:Y, 3:Z): "))
    if pos == 1:
        multiplicador = 10**(3 * 2)
    elif pos == 2:
        multiplicador = 10**3
    elif pos == 3:
        multiplicador = 1
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        continue
    
    num_a_sumar = int(input("Elija un número a sumar: ")) * multiplicador
    
    bot.actualizar_estado(num_a_sumar)
    
    ask = input("Para salir, escriba 'exit': ")
    if ask.lower() == "exit":
        break