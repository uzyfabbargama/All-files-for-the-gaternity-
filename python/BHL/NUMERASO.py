ask = 0
while ask == "exit":
    def Numeraso(): #lógica del Numeraso, acarreo, y controladores, sin if 
        Bondad = int(input("Define la bondad: ")) % 100 #para bondad
        Hostilidad = int(input("Define la hostilidad: ")) % 100 #para hostilidad
        Lógica = int(input("Define la Lógica: ")) % 100 #para lógica
        Numero_generado = Bondad*(10**(3*2)) + Hostilidad*(10**3) + Lógica + 9*10**8 + 9*10**5 + 9*10**2 #construcción del numeraso
        C1 = (Numero_generado // 10**8) % 10 #primer controlador
        C2 = (Numero_generado // 10**5) % 10 #segundo controlador
        C3 = (Numero_generado // 10**2) % 10 #tercer controlador
        D1 = ((C1 - 8) - 1) * -1 #detector del controlador, usa una compuerta not, que detecta 9 y 0 (si es 9, se convierte en 0, y si es 0, se convierte en 1)
        D2 = ((C2 - 8) - 1) * -1 #lo mismo
        D3 = ((C3 - 8) - 1) * -1 #lo mismo
        C1 += D1*9 #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0)
        C2 += D2*9
        C3 += D3*9
        Numero_generado += D1 #activa ciclo, sumando 1 a lógica
        Numero_generado -= D1*(10**3) #le resta 1 a hostilidad
        Numero_generado -= D2 #le resta uno a lógica
        Numero_generado -= D3*(10**(3*2)) #le resta 1 a bondad
    #las sumas, se hacen automáticamente con el acarreo, 
    #PD: los D1, D2, D3, sólo restan o suman 1, si los controladores están activos
        return Numero_generado
num = Numeraso()    
ask = (input())