def Numeraso_Exp(ExpX, ExpY, ExpZ):
    NumerasoXP = (ExpX*PosX) + (ExpY*PosY) + (ExpZ*PosZ) + PosC + PosC1 + PosC2
    #NumerasoXP %= ((base**3) * 2**3)
    C1 = (NumerasoXP // PosC) % 2 #primer controlador
    C2 = (NumerasoXP // PosC1) % 2 #segundo controlador
    C3 = (NumerasoXP // PosC2) % 2 #tercer controlador
    caso = C1 + C2 + C3 #detecta si una variable cambió
    while caso != 3:
        D1 = 1 - C1
        D2 = 1 - C2
        D3 = 1 - C3
        NumerasoXP += D1 * PosC + D2 * PosC1 + D3 * PosC2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
        NumerasoXP += D1 #activa ciclo, sumando 1 a lógica
        NumerasoXP -= (D1)*PosY #le resta 1 a hostilidad
        NumerasoXP -= D2*PosZ #le resta uno a lógica
        NumerasoXP -= (D3)*PosX #le resta 1 a bondad
            #las sumas, se hacen automáticamente con el acarreo, 
            #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
        C1 = (NumerasoXP // PosC) % 2 #primer controlador
        C2 = (NumerasoXP // PosC1) % 2 #segundo controlador
        C3 = (NumerasoXP // PosC2) % 2 #tercer controlador
        caso = C1 + C2 + C3
    ExpX = (NumerasoXP // PosX) % base
    ExpY = (NumerasoXP // PosY) % base
    ExpZ = (NumerasoXP // PosZ) % base
    return int(ExpX), int(ExpY), int(ExpZ)
