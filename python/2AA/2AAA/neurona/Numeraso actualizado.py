base = 1000

Valor = int(input("Escriba un número")) %(base**3)*2**3
Valor += 1*base + 1*(base**2)*2 + 1*(base**3)*2**2
X = (Valor) % base #dato (para enteros de 1 al 100)
C = (Valor // base) % 2 #control (sólo pueden estar en 1 o 0)
Y = (Valor // base*2) % base #dato (para enteros de 1 al 100)
C1 = (Valor // base**2 * 2) % 2 #control (sólo pueden estar en 1 o 0)
Z = (Valor // base**2 * 2**2) % base #dato (para enteros de 1 al 100)
C2 = (Valor // base**3) % 2 #control (sólo pueden estar en 1 o 0)
posición_X = 1
posición_C = base
posición_Y = base*2
posición_C1 = base**2 * 2
posición_Z = base**2 * 2**2
posición_C2 = base**3
caso = 0
ejecutar= input("quiere ejecutar? s/n")
if ejecutar == "s":
		while caso != 3:
			X = (Valor) % base #dato (para enteros de 1 al 100)
			C = (Valor // base) % 2 #control (sólo pueden estar en 1 o 0)
			Y = (Valor // posición_Y) % base #dato (para enteros de 1 al 100)
			C1 = (Valor // posición_C1) % 2 #control (sólo pueden estar en 1 o 0)
			Z = (Valor // posición_Z) % base #dato (para enteros de 1 al 100)
			C2 = (Valor // posición_C2) % 2 #control (sólo pueden estar en 1 o 0)
			actualizar_C = (Valor // posición_C) % 2
			actualizar_C1 = (Valor // posición_C1) % 2
			actualizar_C2 = (Valor // posición_C2) % 2
			#para los detectores
			D = 1 - C #(puerta not para detectar X)
			if D == 1:
				print("controlador 1 activo")
			D1 = 1 - C1 #(puerta not para detectar Y) 
			if D1 == 1:
				print("controlador 2 activo")
			D2 = 1 - C2 #(puerta not para detectar Z)
			if D2 == 2:
				print("controlador 3 activo")
			#Valor += D2*posición_X #si Z se pasa, le suma 1 a X
			Valor -= D*posición_Z + D1*posición_X + D2*posición_Y #X, le resta 1 a Z, Y, le resta 1 a X, Z le resta 1 a Y
			Valor += D*posición_X + D2*posición_Z + D1*posición_Y #reestablecer valores de control.
			caso = C1 + C2 + C
			Valor += D*posición_C + D1*posición_C1 + D2*posición_C2
			#Valor += actualizar_C + actualizar_C1 + actualizar_C2
else:
	print(Valor)
	print(f"control 3: {C2},Z: {Z}, control 2: {C1},Y: {Y},control 1: {C},X: {X}")
	print(C2,Z,C1,Z,C,X)
