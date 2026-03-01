#Nuanot

def adder():
    limite = 2**9
    PA = int(input("Valor A: ")) # pide valor para A (materia prima, sin procesar aún)
    PAZ = (PA + 1)%2 #aquí es el primer proceso, que invierte el valor, para convertir los posibles 0 en 1
    PB = int(input("Valor B: "))
    PBZ = (PB + 1)%2 #Aquí el primer proceso de inversión, pero para el valor B 
    AOR = PA + PAZ #Aquí aplicamos la OR, que combina los valores (para A)
    BOR = PB + PBZ #Aquí aplicamos la OR, que combina los valores (para B)
    A = AOR % limite #Valor A del 0 al 512
    B = BOR % limite #Valor B del 0 al 512
    CAB = ((A + B) // limite) % 2 #Control de A y B, expulsa un bit para la nitenle
    total = A + B
    return CAB, total #devuelce el control de A y B, además del total
def nitenle():
    CAB, total = adder() #Acceder a los controladores 
    nitenle = int("Valor del 0 al 7") + CAB % 64 #3 bits de control + 1 de else 
    nine = ((nitenle // 2)%2) #primer bit de control
    ten = ((nitenle // 4)%2) #segundo bit de control
    eleven = ((nitenle // 8)%2) #tercer bit de control
    output = ((nitenle // 16)%2) #bit de salida
    eraser = ((nitenle // 32)%2) #bit de borrado para nine
    eraser1 = ((nitenle // 64)%2) #bit de borrado para ten
    memonine = (nine - 1) * ((nine + CAB) * (eraser - 1)) #bit 9 negado and (bit 9 sumado a control de A y B and con eraser negado)
    memoten = (ten - 1) * ((ten + CAB) * (eraser1 - 1)) #bit 10 negado and (bit 10 sumado a control A y B and con eraser negado)
    return nine, ten, eleven, output, memonine, memoten 