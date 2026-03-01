
Total = 10 #tomamos la variable de umbral 10
STotal = 16 ** (len(str(hex(Total)[2:]))) - Total #le aplicamos el complemento según cifras
CTotal = 16 ** len(str(hex(Total)[2:])) # 90
#print(STotal)
control_energía = 3 #controladores binarios
Dcontrol_energía = ((control_energía  %2) - 1) #si el controlador se torna par, le suma uno a total con acarreo (no hace falta escribir + Total)
Ccontrol_energía = 4

batería = 100 #tomamos el umbral de batería
Sbatería = 16 ** (len(str(hex(batería)[2:]))) - batería #900 aquí le aplicamos el complemento según cifras
Cbatería = 16 ** len(str(hex(batería)[2:])) #1000, obtenemos el factor para meter el número
#print(Sbatería)
#print(Cbatería)
consumo = 1 #umbral de consumo
Sconsumo = 16 ** (len(str(hex(consumo)[2:]))) - consumo #10 ** 1 - 1 = 9 #apicamos complemento
Cconsumo = 16 ** len(str(hex(consumo)[2:])) #10 #factor para agregar la variable
#print(Sconsumo)
#print(Cconsumo)
control_volar = 1 #controlador binario sin acarreo, (aquí se aclara +Total para sumarle 1 o 0 al total)
Dcontrol_volar = ((control_volar % 2)- 1) + Total
Ccontrol_volar = 4

no_vuela = 1 #umbral de no_vuela
Sno_vuela = 16 ** (len(str(hex(no_vuela)[2:]))) - no_vuela #9 aplicamos complemento
Cno_vuela = 16 ** len(str(hex(no_vuela)[2:])) #10 #factor para agregar la variable
#print(Sno_vuela)
#print(Cno_vuela)
control_calor = 1 #controlador binario de calor
Dcontrol_calor = ((control_calor % 2) - 1) + Total #le suma a total
Ccontrol_calor = 4

calor = 100 #umbral de calor
Scalor = 16 ** (len(str(hex(calor)[2:]))) - calor # 900 #aplicamos complemento
Ccalor = 16 ** len(str(hex(calor)[2:])) #1000 #factor para agregar variable


Agente = ((((((((((((((STotal*Ccontrol_energía)+control_energía)*Cbatería)+Sbatería)*Cconsumo)+Sconsumo)*Ccontrol_volar)+control_volar)*Cno_vuela)+Sno_vuela)*Ccontrol_calor)+control_calor)*Ccalor)+Scalor)

print (Agente) #imprimimos clase
Agente_ori = hex((((((((((((((6*4)+3)*256)+156)*16)+15)*4)+1)*16)+15)*4)+1)*256)+156) #valores de muestra (valor original)
print(f"Valor original: {Agente_ori}") #imprimimos la muestra
#la diferencia esperada es de un 1
posS, posT, posU, posV, posW, posX, posY, posZ = [2**2, len(str(bin(2**2)[2:]))], [2**4, len(str(bin(2**4)[2:]))], [2**12, len(str(bin(2**12)[2:]))], [2**16, len(str(bin(2**16)[2:]))], [2**18, len(str(bin(2**18)[2:]))], [2**22, len(str(bin(2**22)[2:]))], [2**24, len(str(bin(2**24)[2:]))], [2**32, len(str(bin(2**32)[2:]))]
count = len(str(bin(Agente)))
print(posS[1])
VTotal = Agente // 2 ** (count - posS[1]) % 16
Vcontrol_energía = Agente // 2 ** (count - posT[1]) %4
Vbatería = Agente // 2 ** (count - posU[1]) %256
print(VTotal)
#y =input()
#y + 0