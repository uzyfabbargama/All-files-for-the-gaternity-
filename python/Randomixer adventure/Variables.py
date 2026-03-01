#Variables
B, H, L = 0,0,1
D = int(B)
BA = 0
#Generación del operador

#Nota: exec() solo puede asiganar variables si se usa en un diccionario
#para el namespace local

#Creamos el diccionario para el resultado

OB = chr(43 + 4*(bool(B)*bool(BA)))
código_a_ejecutar = f"B {OB} BA"
D = eval(código_a_ejecutar)
print(D)


