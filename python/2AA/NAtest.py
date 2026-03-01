Valor = int(input("Escriba un número")) %8000000
print(f"se recibió el número: {Valor}")
Valor += 1*100 + 1*20000 + 1*4000000
print("Se agregaron los controladores")
X = (Valor) % 100 #dato (para enteros de 1 al 100)
print(f"Se detectó X: {X}")
C = (Valor // 100) % 2 #control (sólo pueden estar en 1 o 0)
print(f"Se detectó C: {C}")
Y = (Valor // 200) % 100 #dato (para enteros de 1 al 100)
print(f"Se detectó Y: {Y}")
C1 = (Valor // 20000) % 2 #control (sólo pueden estar en 1 o 0)
print(f"Se detectó C1: {C1}")
Z = (Valor // 40000) % 100 #dato (para enteros de 1 al 100)
print(f"Se detectó Z: {Z}")
C2 = (Valor // 4000000) % 2 #control (sólo pueden estar en 1 o 0)
print(f"Se detectó X: {C2}")

caso = 0
print(f"Se Estableció caso a: {caso}")
while caso != 3:
	print(f"Se empieza el bucle")
	X = (Valor) % 100 #dato (para enteros de 1 al 100)
	print(f"Se detectó X: {X}")
	C = (Valor // 100) % 2 #control (sólo pueden estar en 1 o 0)
	print(f"Se detectó C: {C}")
	Y = (Valor // 200) % 100 #dato (para enteros de 1 al 100)
	print(f"Se detectó Y: {Y}")
	C1 = (Valor // 20000) % 2 #control (sólo pueden estar en 1 o 0)
	print(f"Se detectó C1: {C}")
	Z = (Valor // 40000) % 100 #dato (para enteros de 1 al 100)
	print(f"Se detectó Z: {Z}")
	C2 = (Valor // 4000000) % 2 #control (sólo pueden estar en 1 o 0)
	print(f"Se detectó C2: {C2}")
	actualizar_C = (Valor // 100)
	print(f"Se detectó actualizar_C: {actualizar_C}")
	actualizar_C1 = (Valor // 20000) % 2
	print(f"Se detectó actualizar_C1: {actualizar_C1}")
	actualizar_C2 = (Valor // 4000000) % 2
	print(f"Se detectó actualizar_C3: {actualizar_C3}")
	posición_X = 100
	posición_Y = 20000
	posición_Z = 4000000
	#para los detectores
	D = C - 1 #(puerta not para detectar X) 
	D1 = C1 - 1 #(puerta not para detectar Y) 
	D2 = C2 - 1 #(puerta not para detectar Z)
	#Valor += D2*posición_X #si Z se pasa, le suma 1 a X
	Valor -= D*posición_Z + D1*posición_X + D2*posición_Y #X, le resta 1 a Z, Y, le resta 1 a X, Z le resta 1 a Y
	Valor += C*posición_X + C2*posición_Z + C1*posición_Y #reestablecer valores de control.
	caso = C1 + C2 + C
	#Valor += actualizar_C + actualizar_C1 + actualizar_C2
	
print(Valor)
print(f"control 3: {C2},Z: {Z}, control 2: {C1},Y: {Y},control 1: {C},X: {X}")
print(C2,Z,C1,Z,C,X)
