
def Numeraso(): #lógica del Numeraso, acarreo, y controladores, sin if 
        Bondad = int(input("Define la bondad: ")) % 100 #para bondad
        Hostilidad = int(input("Define la hostilidad: ")) % 100 #para hostilidad
        Lógica = int(input("Define la Lógica: ")) % 100 #para lógica
        Numero_generado = Bondad*(10**(3*2)) + Hostilidad*(10**3) + Lógica + 9*10**8 + 9*10**5 + 9*10**2 #construcción del numeraso
        return Numero_generado
def Numeraso_update():        
        Numero_generado = Numeraso()
        C1 = (Numero_generado // 10**8) % 10 #primer controlador
        C2 = (Numero_generado // 10**5) % 10 #segundo controlador
        C3 = (Numero_generado // 10**2) % 10 #tercer controlador
        print(C1, C2, C3)
        caso = C1 + C2 + C3 #detecta si una variable cambió
        print(f"Caso = {caso}")
        expL = 0
        expB = 0
        expH = 0
        while caso != 27:
            D1 = 9 - C1 #detector del controlador, usa una compuerta not, que detecta 9 y 0 (si es 9, se convierte en 0, y si es 0, se convierte en 1)
            D2 = 9 - C2 #lo mismo
            D3 = 9 - C3 #lo mismo
            expB += D1%2
            expH += D2%2
            expL += D3%2
            Numero_generado += D1 * 10**8 + D2 * 10**5 + D3 * 10**2 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
            Numero_generado += D1%2 #activa ciclo, sumando 1 a lógica
            Numero_generado -= (D1%2)*(10**3) #le resta 1 a hostilidad
            Numero_generado -= D2%2 #le resta uno a lógica
            Numero_generado -= (D3%2)*(10**(3*2)) #le resta 1 a bondad
            #las sumas, se hacen automáticamente con el acarreo, 
            #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
            C1 = (Numero_generado // 10**8) % 10 #primer controlador
            C2 = (Numero_generado // 10**5) % 10 #segundo controlador
            C3 = (Numero_generado // 10**2) % 10 #tercer controlador
            caso = C1 + C2 + C3
        print(Numero_generado % 10**9)
        return Numero_generado % 10**9, expB, expH, expL
Numero, expB, expH, expL = Numeraso_update()
print(Numero)
print(expB)
print(expH)
print(expL)

