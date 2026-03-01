Numerasos= """
def Numeraso_Exp(ExpB, ExpH, ExpL, PosX, PosC, PosY, PosC1, PosZ, PosC2):
     NumerasoXP = ExpB*PosX + ExpH*PosY + ExpL*PosZ + PosC + PosC1 + PosC2
     C1 = (NumerasoXP // PosC) % 2 #primer controlador
     C2 = (NumerasoXP // PosC1) % 2 #segundo controlador
     C3 = (NumerasoXP // PosC2) % 2 #tercer controlador
     caso = C1 + C2 + C3 #detecta si una variable cambió
     while caso != 3:
        D1 = 1 - C1
        D2 = 1 - C2
        D3 = 1 - C3
        Numero_generado += D1 * PosC + D2 * PosC1 + D3 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
        Numero_generado += D1 #activa ciclo, sumando 1 a lógica
        Numero_generado -= (D1)*PosY #le resta 1 a hostilidad
        Numero_generado -= D2*PosZ #le resta uno a lógica
        Numero_generado -= (D3)*PosX #le resta 1 a bondad
            #las sumas, se hacen automáticamente con el acarreo, 
            #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
        C1 = (Numero_generado // PosC) % 2 #primer controlador
        C2 = (Numero_generado // PosC1) % 2 #segundo controlador
        C3 = (Numero_generado // PosC2) % 2 #tercer controlador
        caso = C1 + C2 + C3
     
     return expB,expH,expL
expB, expL, expH = 0

Numeraso_Exp(expB, expH, expL, PosX, PosC, PosY, PosC1, PosZ, PosC2)
expB, expL, expH = Numeraso_Exp() #Aquí obtenemos las experiencias del numeraso
def Numeraso(a, b, c, PosX, PosC, PosY, PosC1, PosZ, PosC2): #lógica del Numeraso, acarreo, y controladores, sin if 
        Bondad = a #para bondad
        Hostilidad = b #para hostilidad
        Lógica = c #para lógica
        Numero_generado = Bondad*PosX + Hostilidad*PosY + Lógica*PosZ + PosC + PosC1 + PosC2 #construcción del numeraso
        return expB,expH,expL
Numeraso(a,b,c,PosX, PosC, PosY, PosC1, PosZ, PosC2)
def Numeraso_update():        
        Numero_generado = Numeraso(a,b,c,PosX, PosC, PosY, PosC1, PosZ, PosC2)
        C1 = (Numero_generado // PosC) % 2 #primer controlador
        C2 = (Numero_generado // PosC1) % 2 #segundo controlador
        C3 = (Numero_generado // PosC2) % 2 #tercer controlador
        caso = C1 + C2 + C3 #detecta si una variable cambió
        expL = 0
        expB = 0
        expH = 0
        while caso != 3:
            D1 = 1 - C1 #detector del controlador, usa una compuerta not, que detecta 9 y 0 (si es 9, se convierte en 0, y si es 0, se convierte en 1)
            D2 = 1 - C2 #lo mismo
            D3 = 1 - C3 #lo mismo
            expB += D1
            expH += D2
            expL += D3
            Numero_generado += D1 * PosC + D2 * PosC1 + D3 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
            Numero_generado += D1 #activa ciclo, sumando 1 a lógica
            Numero_generado -= (D1)*PosY #le resta 1 a hostilidad
            Numero_generado -= D2*PosZ #le resta uno a lógica
            Numero_generado -= (D3)*PosX #le resta 1 a bondad
            Numero_generado += D1 * (100/(expL+1))%100 + D2 * (100/(expH+1))%100 + D3 * (100/(expB+1))%100 #Esto conserva la energía emocional, ya que si tiene experiencia 1, su valor va a quedare en 50, en lugar de 0
            #las sumas, se hacen automáticamente con el acarreo, 
            #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
            C1 = (Numero_generado // PosC) % 2 #primer controlador
            C2 = (Numero_generado // PosC1) % 2 #segundo controlador
            C3 = (Numero_generado // PosC2) % 2 #tercer controlador
            caso = C1 + C2 + C3
        return Numero_generado % 800000000, expB, expH, expL
baño = 50
hambre = 50
sueño = 50
def Numeraso2(a, b, c,PosX, PosC, PosY, PosC1, PosZ, PosC2): #definir el numeraso de las necesidades
    C = a #ir al baño
    H = b #hambre
    S = c #sueño
    Numero_de_necesidad = C*PosX + H*PosY + S*PosZ #se construye el numeraso
    Numero_de_necesidad += PosC + PosC1 + PosC2 #se le agregam controladores
    return Numero_de_necesidad
Numeraso2(baño, hambre, sueño)
def Numeraso2_update():
    Numero_de_necesidad = Numeraso2(baño, hambre, sueño, PosX, PosC, PosY, PosC1, PosZ, PosC2)
    C4 = (Numero_de_necesidad // PosC) % 2 #cuarto controlador
    C5 = (Numero_de_necesidad // PosC1) % 2 #quinto controlador
    C6 = (Numero_de_necesidad // PosC2) % 2 #sexto controlador
    caso = C4 + C5 + C6
    expS = 0
    expHu = 0
    expC = 0
    while caso != 3:
        D4 =  1 - C4 #los detectores de controladores, con compuerta not
        D5 =  1 - C5
        D6 = 1 - C6
        expS += D4 
        expHu += D5
        expC += D6
        Numero_de_necesidad += (D4)*PosZ #las mismas lógicas que en el numeraso anterior (sueño)
        Numero_de_necesidad -= (D4)*PosY #(hambre)
        Numero_de_necesidad -= D5 * PosZ #(sueño)
        Numero_de_necesidad -= (D6)*PosY #hambre
        Numero_de_necesidad -= (D4)*PosX #Evacuar
        C4 = (Numero_de_necesidad // PosC2) % 10 #cuarto controlador
        C5 = (Numero_de_necesidad // PosC1) % 10 #quinto controlador
        C6 = (Numero_de_necesidad // PosC) % 10 #sexto controlador
        caso = C4 + C5 + C6
        Numero_de_necesidad += PosY
    return Numero_de_necesidad, expS, expHu, expC
Numero, expB, expH, expL = Numeraso_update() #para acceder al número de la personalidad
Numero1, expS, expHu, expC = Numeraso2_update() #para acceder al número de las necesidades
print(f"Númeraso: {Numero}") #mostrar numeraso
print(f"Numeraso1: {Numero1}")
"""
