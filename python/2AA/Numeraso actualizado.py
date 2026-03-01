Valor = int(input("Escriba un número")) %8000000
Valor += 1*100 + 1*20000 + 1*4000000
X = (Valor) % 100 #dato (para enteros de 1 al 100)
C = (Valor // 100) % 2 #control (sólo pueden estar en 1 o 0)
Y = (Valor // 200) % 100 #dato (para enteros de 1 al 100)
C1 = (Valor // 20000) % 2 #control (sólo pueden estar en 1 o 0)
Z = (Valor // 40000) % 100 #dato (para enteros de 1 al 100)
C2 = (Valor // 4000000) % 2 #control (sólo pueden estar en 1 o 0)

caso = 0
while caso != 3:
	X = (Valor) % 100 #dato (para enteros de 1 al 100)
	C = (Valor // 100) % 2 #control (sólo pueden estar en 1 o 0)
	Y = (Valor // 200) % 100 #dato (para enteros de 1 al 100)
	C1 = (Valor // 20000) % 2 #control (sólo pueden estar en 1 o 0)
	Z = (Valor // 40000) % 100 #dato (para enteros de 1 al 100)
	C2 = (Valor // 4000000) % 2 #control (sólo pueden estar en 1 o 0)
	actualizar_C = (Valor // 100)
	actualizar_C1 = (Valor // 20000) % 2
	actualizar_C2 = (Valor // 4000000) % 2
	posición_X = 100
	posición_Y = 20000
	posición_Z = 4000000
	#para los detectores
	D = 1 - C #(puerta not para detectar X) 
	D1 = 1 - C1 #(puerta not para detectar Y) 
	D2 = 1 - C2 #(puerta not para detectar Z)
	#Valor += D2*posición_X #si Z se pasa, le suma 1 a X
	Valor -= D*posición_Z + D1*posición_X + D2*posición_Y #X, le resta 1 a Z, Y, le resta 1 a X, Z le resta 1 a Y
	Valor += D*posición_X + D2*posición_Z + D1*posición_Y #reestablecer valores de control.
	caso = C1 + C2 + C
	#Valor += actualizar_C + actualizar_C1 + actualizar_C2
	
print(Valor)
print(f"control 3: {C2},Z: {Z}, control 2: {C1},Y: {Y},control 1: {C},X: {X}")
print(C2,Z,C1,Z,C,X)
