Total = 10 #tomamos la variable de umbral 10
STotal = 10 ** (len(str(Total))) - Total #le aplicamos el complemento según cifras
CTotal = 10 ** len(str(Total)) # 90
#print(STotal)
control_energía = 3 #controladores binarios
Dcontrol_energía = ((control_energía  %2) - 1) #si el controlador se torna par, le suma uno a total con acarreo (no hace falta escribir + Total)

batería = 100 #tomamos el umbral de batería
Sbatería = 10 ** (len(str(batería))) - batería #900 aquí le aplicamos el complemento según cifras
Cbatería = 10 ** len(str(batería)) #1000, obtenemos el factor para meter el número
#print(Sbatería)
#print(Cbatería)
consumo = 1 #umbral de consumo
Sconsumo = 10 ** (len(str(consumo))) - consumo #10 ** 1 - 1 = 9 #apicamos complemento
Cconsumo = 10 ** len(str(consumo)) #10 #factor para agregar la variable
#print(Sconsumo)
#print(Cconsumo)
control_volar = 1 #controlador binario sin acarreo, (aquí se aclara +Total para sumarle 1 o 0 al total)
Dcontrol_volar = ((control_volar % 2)) + Total


no_vuela = 1 #umbral de no_vuela
Sno_vuela = 10 ** (len(str(no_vuela))) - no_vuela #9 aplicamos complemento
Cno_vuela = 10 ** len(str(no_vuela)) #10 #factor para agregar la variable
#print(Sno_vuela)
#print(Cno_vuela)
control_calor = 1 #controlador binario de calor
Dcontrol_calor = ((control_calor % 2) - 1) + Total #le suma a total


calor = 100 #umbral de calor
Scalor = 10 ** (len(str(calor))) - calor # 900 #aplicamos complemento
Ccalor = 10 ** len(str(calor)) #1000 #factor para agregar variable


Agente = "1" + str(((((((STotal*4 + control_energía)*Cbatería + Sbatería)*Cconsumo + Sconsumo)*4 + control_volar)*Cno_vuela + Sno_vuela)*4 + control_calor)*Ccalor + Scalor) #Toda la data y comportamiento + reglas de la clase + el 1 que permite un acarreo para detener un bucle o para conectarla con otras clases
print (Agente) #imprimimos clase
Agente_ori = ((((((90*4 + 3)*1000 + 900)*10 + 9)*4 + 1)*10 + 9)*4 + 1)*1000 + 900 #valores de muestra (valor original)
print(f"Valor original: {Agente_ori}") #imprimimos la muestra
#la diferencia esperada es de un 1
PosX = 10*4*1000*10*4*10*4*1000 #total
print(PosX)
PosY = 4*1000*10*4*10*4*1000 #control_energía

PosZ = 1000*10*4*10*4*1000 #batería

PosW = 10*4*10*4*1000 #consumo

PosV = 4*10*4*1000 #control_volar

PosU = 10*4*1000 #no_vuela

PosT = 4*1000 #control_calor

PosR = 1000 # calor 