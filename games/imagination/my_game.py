print("Bienvenido al juego")
#constantes
vida = 100
hambre = 100
sed = 100
juego = bytearray(0x1000000)
COUNT = bytearray(0x8000000) # o 0x32500
byte_in_game = 0
cosas_agregadas = 0
#funciones
def crear_seccion(str(seccion)):
	byte_in_game_actual = byte_in_game
	byte_in_game += 2
	
	for byte in cosa:
		juego[byte_in_game] = ord(seccion)
		byte_in_game += 1
	byte_in_game += 2
	total_bytes = byte_in_game-byte_in_game_actual
	if total_bytes > 255:
		unready = True
		bytes = total_bytes
		i = 0
		while unready:
			byte = bytes&0xff>>(i<<3)
			COUNT[cosas_agregadas<<8] = byte
			bytes >>= 8
			if bytes == 0:
				unready = False
		cosas_agregadas += 1
	else:
		COUNT[cosas_agregadas<<8] = total_bytes
		cosas_agregadas += 1
		
def crear_linker (int(linker)):
	byte_in_game_actual = byte_in_game
	byte_in_game += 3
	
	num = linker
	if num > 255:
		unready = True
		bytes = total_bytes
		i = 0
		while unready:
			byte = bytes&0xff>>(i<<3)
			juego[byte_in_game] = byte
			bytes >>= 8
			if bytes == 0:
				unready = False
			byte_in_game += 3
		total_bytes = byte_in_game-byte_in_game_actual
		if total_bytes > 255:
		unready = True
		bytes = total_bytes
		i = 0
		while unready:
			byte = bytes&0xff>>(i<<3)
			COUNT[cosas_agregadas<<8] = byte
			bytes >>= 8
			if bytes == 0:
				unready = False
def agregar_cosa_al_juego (str(cosa)):
	byte_in_game_actual = byte_in_game
	byte_in_game += 1
	
	for byte in cosa:
		juego[byte_in_game] = ord(cosa)
		i += 1
	byte_in_game += 1
	total_bytes = byte_in_game-byte_in_game_actual
		if total_bytes > 255:
		unready = True
		bytes = total_bytes
		i = 0
		while unready:
			byte = bytes&0xff>>(i<<3)
			COUNT[cosas_agregadas<<8] = byte
			bytes >>= 8
			if bytes == 0:
				unready = False
#sala_principal
#sala_principal = ["sofá", "cocina", "patio", "escaleras"]
#cocina = ["heladera", "mesa", "alacena", "horno"]
#patio = ["pasto", "salida"]
#escaleras = ["habitación", "baño", "ático"]
#cocina
#heladera = ["manzana", "lechuga", "carne", "huevos", ]
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
#while True:
#	print("Estás en una casa a tu alrededor hay")
#	print(f"1. {sala_principal[0]}")
#	print(f"2. {sala_principal[1]}")
#	print(f"3. {sala_principal[2]}")
