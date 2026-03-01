base = 1_000
posX, posY, posZ = 4_000_000, 2_000, 1 #las bases de las coordenadas
posC, posC1, posC2 = 4_000_000_000, 2_000_000, 1_000 #los controladores
pos1, pos2, pos3, pos4 = 8_000_000_000, 4_000_000, 2_000, 1
pos1C, pos2C, pos3C, pos4C = 8_000_000_000_000, 4_000_000_000, 2_000_000, 1_000
def player_generator(X, Y, Z, wood, stone, iron, water):
	posición_jugador = X * posX + posY * Y + posZ + Z + (posC + posC1 + posC2)
	física_jugador = wood * pos1 + stone * pos2 + iron * pos3 + water * pos4 + (pos1C + pos2C + pos3C + pos4C)
	return posición_jugador, física_jugador

def player_updater(posición_jugador, física_jugador):
	#---- posición
	C = (posición_jugador // posC) % base
	C1 = (posición_jugador // posC1) % base
	C2 = (posición_jugador // posC2) % base
	D = 1 - C
	D1 = 1 - C1
	D2 = 1 - C2
	caso = D + D1 + D2
	while caso != 3:
		posición_jugador -= posC*D + posC1*D1 + posC2*D2 #evita que se pase del límite de coordenadas
	#---- físicas
	C3 = (física_jugador // pos1C) % base #carne
	C4 = (física_jugador // pos2C) % base #huesos
	C5 = (física_jugador // pos3C) % base #sangre
	C6 = (física_jugador // pos4C) % base #agua
	D3 = 1 - C3
	D4 = 1 - C4
	D5 = 1 - C5
	D6 = 1 - C6
	caso1 = D3 +  D4 + D5 + D6
	#aquí definimos las reglas
	#que si agua alcanza límite, carne reacciona (como madera, aumentando) pero también, requiera algo de calcio, y afecte a hierro (bajandolo)
	#agua ↑ = madera ↑, hierro ↓, piedra ↓
	#madera ↑ = hierro ↑, piedra ↓, agua ↓
	#hierro ↑ = piedra ↑, madera ↓, agua ↓
	#piedra ↑ = madera ↓, agua ↓, hierro ↑
	#madera = pos1
	#piedra = pos2
	#hierro = pos3
	#agua   = pos4
	while caso1 != 4:
		#agua ↑
		física_jugador -= (-pos1)*D6 + pos2*D6 + pos3*D6 
		#madera ↑
		física_jugador -= pos2*D3 + (-pos3)*D3 + pos4*D3
		#hierro ↑
		física_jugador -= (-pos2)*D5 + pos1*D5 + pos4*D5
		#piedra ↑
		física_jugador -= pos1*D4 + pos4*D4 +(-pos3)*D4
	return física_jugador, posición_jugador
def cmpzf (val, val1):
	ZF = 0#zero flag 
	ZF = not(bool(val - val1))
	return ZF
def controls ():
	#w = 119
	#W = 87
	#a = 97
	#A = 65
	#s = 115
	#S = 183
	#d = 100
	#D = 68
	#e = 101
	#E = 69
	#i = 105
	#I = 73
	key = input()
	value_key = ord(key)
	pos_w = 0
	pos_W = 1
	pos_a = 2
	pos_A = 3
	pos_s = 4
	pos_S = 5
	pos_d = 6
	pos_D = 7
	pos_i = 8
	pos_I = 9
	data_key = (cmpzf(119, value_key) << pos_w) | (cmpzf(87, value_key) << pos_W) | (cmpzf(97, value_key) << pos_a) | (cmpzf(65, value_key) << pos_A) | (cmpzf(115, value_key) << pos_s) | (cmpzf(183, value_key) << pos_S) | (cmpzf(100, value_key) << pos_d) | (cmpzf(68, value_key) << pos_D) | (cmpzf(105, value_key) << pos_i) | (cmpzf(73, value_key) << pos_I)
	pos_0 = 0
	pos_1 = 1
	pos_2 = 2
	pos_3 = 3
	pos_4 = 4
	pos_5 = 5
	pos_6 = 6
	pos_7 = 7
	pos_8 = 8
	pos_9 = 9
	
	#w = avanzar normal, gasta energía min
	#a = girar 45 grados izquierda
	#s = avanzar atrás
	#d = girar 45 grados derecha
	#W = correr gasta energía max
	#A = girar 90 grados izquierda
	#D = girar 90 grados derecha
	#e = agarrar con cuidado
	#E = golpear
	#i = inventario
	#I = inventario secundario
	inventory = (cmpzf(48, value_key) << pos_0) | (cmpzf(49, value_key) << pos_1) |	(cmpzf(50, value_key) << pos_2) | (cmpzf(51, value_key) << pos_3) | (cmpzf(52, value_key) << pos_4) | (cmpzf(53, value_key) << pos_5) | (cmpzf(54, value_key) << pos_6) | (cmpzf(55, value_key) << pos_7) | (cmpzf(56, value_key) << pos_8) | (cmpzf(57, value_key) << pos_9)
	#para ir a los 10 slots
	return data_key
def actions(data_key, física_jugador, posición_jugador, inventory, angle):
	#data_key = movimientos
	#física_jugador = necesidades, fisiología
	#posición_jugador = posición actuañ
	#inventory = inventario actual
	angle += cmpzf(1, ((data_key >> 2) & 0x1))*-45 #se compara si data_key, tenía la a, y se suma -45 grados
	angle += cmpzf(1, ((data_key >> 3) & 0x1))*-90 #se compara si data_key, tenía la A, y se suma 90 grados
	angle += cmpzf(1, ((data_key >> 6) & 0x1))*45 #se compara si data_key, tenía la d, y se suma 45 grados
	angle += cmpzf(1, ((data_key >> 7) & 0x1))*90 #se compara si data_key, tenía la D, y se suma 90 grados
	control_P = 76 #10110100 → 01001011 (76 = 1001100 → 1001011)
	control_N = 180
	detect = (((control_P + angle) >> 8)& 1) ^ (((control_N + angle) >> 8)& 1) #detecta errores
	#mov, mueve el personaje, según los ángulos
	#+000 = +X
	#+045 = +X, +Z
	#+090 = 00, +Z
	#+135 = -X, +Z
	#+180 = -X, 00
	#-045 = +X, -Z
	#-090 = 00, -Z
	#-135 = -X, -Z
	mov1 = cmpzf((data_key << 0)) + cmpzf((data_key << 1))
	mov += cmpzf(0, angle) * (posX) * mov1
	mov += cmpzf(45, angle) * (posX + posZ) * mov1
	mov += cmpzf(90, angle) * (posZ) * mov1
	mov += cmpzf(135, angle) * (-posX + posZ) * mov1
	mov += cmpzf(-45, angle) * (posX - posZ) * mov1
	mov += cmpzf(-90, angle) * (-posZ) * mov1
	mov += cmpzf(-135, angle) * -(posX + posZ) * mov1
	posición_jugador += mov
	física_jugador -= pos4*2 + (- pos1) + (-pos2) #por ahora, haré que gaste aguax2, suba madera (regeneración celular) y aumente roca (regeneración ósea)
def create_block(X, Y, Z, wood, stone, iron, water):
	posición_bloque = X * posX + posY * Y + posZ + Z + (posC + posC1 + posC2)
	física_bloque = wood * pos1 + stone * pos2 + iron * pos3 + water * pos4 + (pos1C + pos2C + pos3C + pos4C)
	return posición_bloque, física_bloque

def block_block(posición_bloque, física_bloque):
		#---- posición
	C = (posición_bloque // posC) % base
	C1 = (posición_bloque // posC1) % base
	C2 = (posición_bloque // posC2) % base
	D = 1 - C
	D1 = 1 - C1
	D2 = 1 - C2
	caso = D + D1 + D2
	while caso != 3:
		posición_bloque -= posC*D + posC1*D1 + posC2*D2 #evita que se pase del límite de coordenadas
	#---- físicas
	C3 = (física_bloque // pos1C) % base #carne
	C4 = (física_bloque // pos2C) % base #huesos
	C5 = (física_bloque // pos3C) % base #sangre
	C6 = (física_bloque // pos4C) % base #agua
	D3 = 1 - C3
	D4 = 1 - C4
	D5 = 1 - C5
	D6 = 1 - C6
	caso1 = D3 +  D4 + D5 + D6
	#aquí definimos las reglas
	#que si agua alcanza límite, carne reacciona (como madera, aumentando) pero también, requiera algo de calcio, y afecte a hierro (bajandolo)
	#agua ↑ = madera ↑, hierro ↓, piedra ↓
	#madera ↑ = hierro ↑, piedra ↓, agua ↓
	#hierro ↑ = piedra ↑, madera ↓, agua ↓
	#piedra ↑ = madera ↓, agua ↓, hierro ↑
	#madera = pos1
	#piedra = pos2
	#hierro = pos3
	#agua   = pos4
	while caso1 != 4:
		#agua ↑
		física_bloque -= (-pos1)*D6 + pos2*D6 + pos3*D6 
		#madera ↑
		física_bloque -= pos2*D3 + (-pos3)*D3 + pos4*D3
		#hierro ↑
		física_bloque -= (-pos2)*D5 + pos1*D5 + pos4*D5
		#piedra ↑
		física_bloque -= pos1*D4 + pos4*D4 +(-pos3)*D4
	return física_bloque, posición_bloque
#luego agregaré más cosas
#player_generator(30, 32, 30, 580, 580, 580, 580)
#world = []
#world.append(1)
#controls()
