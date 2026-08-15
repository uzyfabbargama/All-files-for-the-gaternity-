print("Bienvenido al juego")

# Constantes
vida = 100
hambre = 100
sed = 100
juego = bytearray(0x1000000)
COUNT = bytearray(0x8000000)
byte_in_game = 0
cosas_agregadas = 0

# FUNCIONES CORREGIDAS
def crear_seccion(seccion):  # <-- ¡QUITÉ el "str()"!
    global byte_in_game, cosas_agregadas  # Necesario para modificar variables globales
    
    byte_in_game_actual = byte_in_game
    byte_in_game += 2
    
    for byte in seccion:  # <-- Aquí estaba "cosa" pero debería ser "seccion"
        juego[byte_in_game] = ord(byte)  # <-- Aquí también estaba "seccion"
        byte_in_game += 1
    
    byte_in_game += 2
    total_bytes = byte_in_game - byte_in_game_actual
    
    if total_bytes > 255:
        unready = True
        bytes = total_bytes
        i = 0
        while unready:
            byte = bytes & 0xff >> (i << 3)
            COUNT[cosas_agregadas << 8] = byte
            bytes >>= 8
            if bytes == 0:
                unready = False
        byte_in_game
        cosas_agregadas += 1
    else:
        COUNT[cosas_agregadas << 8] = total_bytes
        cosas_agregadas += 1

def crear_linker(linker):  # <-- ¡QUITÉ el "int()"!
    global byte_in_game, cosas_agregadas
    
    byte_in_game_actual = byte_in_game
    byte_in_game += 3
    
    num = linker
    if num > 255:
        unready = True
        bytes = num  # <-- Esto estaba mal, era "total_bytes" pero debería ser "num"
        i = 0
        while unready:
            byte = bytes & 0xff >> (i << 3)
            juego[byte_in_game] = byte
            bytes >>= 8
            if bytes == 0:
                unready = False
        byte_in_game += 3 # FUERA DEL WHILE (separador)
        total_bytes = byte_in_game - byte_in_game_actual
        if total_bytes > 255:
            unready = True
            bytes = total_bytes
            i = 0
            while unready:
                byte = bytes & 0xff >> (i << 3)
                COUNT[cosas_agregadas << 8] = byte
                bytes >>= 8
                if bytes == 0:
                    unready = False
        else:
            COUNT[cosas_agregadas << 8] = total_bytes

def agregar_cosa_al_juego(cosa):  # <-- ¡QUITÉ el "str()"!
    global byte_in_game, cosas_agregadas
    
    byte_in_game_actual = byte_in_game
    byte_in_game += 1
    
    for byte in cosa:
        juego[byte_in_game] = ord(byte)  # <-- Esto estaba mal, era "cosa" no "byte"
        byte_in_game += 1  # <-- Faltaba incrementar
    
    byte_in_game += 1
    total_bytes = byte_in_game - byte_in_game_actual
    
    if total_bytes > 255:
        unready = True
        bytes = total_bytes
        i = 0
        while unready:
            byte = bytes & 0xff >> (i << 3)
            COUNT[cosas_agregadas << 8] = byte
            bytes >>= 8
            if bytes == 0:
                unready = False
        byte_in_game += 1 # <--- separador
    else:
        COUNT[cosas_agregadas << 8] = total_bytes
        cosas_agregadas += 1

# CREANDO EL MUNDO
crear_seccion("sala_principal")
agregar_cosa_al_juego("sofá")
crear_linker(1)
agregar_cosa_al_juego("cocina")
crear_linker(2)
agregar_cosa_al_juego("patio")
crear_linker(3)
agregar_cosa_al_juego("escaleras")

crear_seccion("cocina")
crear_linker(4)
agregar_cosa_al_juego("heladera")
crear_linker(5)
agregar_cosa_al_juego("mesa")

print("Mundo creado exitosamente")
print(f"Bytes usados: {byte_in_game}")
