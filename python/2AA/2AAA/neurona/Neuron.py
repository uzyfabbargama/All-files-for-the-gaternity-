import Numeraso_Exp as xp
bits = 15
base = 1 << bits # 32768
mask = base - 1  # 0x7FFF (para extraer 15 bits limpios)

# Posiciones de registros y controladores
PosZ = 0
PosC = bits              # Bit 15
PosY = bits + 1          # Bit 16
PosC1 = (bits * 2) + 1   # Bit 31
PosX = (bits * 2) + 2    # Bit 32
PosC2 = (bits * 3) + 2   # Bit 47

# Límites del Numeraso (2**3 controladores + 3 registros de 15 bits)
LIMITE = 1 << (PosC2 + 1)

def Numeraso2(x, y, z): #definir el numeraso de las necesidades
        x = a #Val
        y = b #Val1
        z = c #Val2
        Numero_generado = (x<<PosX) + (y<<PosY) + (z<<PosZ) #se construye el numeraso
        Numero_generado += PosC + PosC1 + PosC2 #se le agregan los controladores
        Numero_generado = int(Numero_generado)
        return Numero_generado

def Numeraso2_update(expx, expy, expz, Numero_generado):
    C4 = (Numero_generado >> PosC) & 1 #cuarto controlador
    C5 = (Numero_generado >> PosC1) & 1 #quinto controlador
    C6 = (Numero_generado >> PosC2) & 1 #sexto controlador
    caso = C4 + C5 + C6
    expx, expy, expz = xp.Numeraso_Exp(expx, expy, expz)
    while caso != 3:
        D4 =  1 - C4 #los detectores de controladores, con compuerta not
        D5 =  1 - C5
        D6 = 1 - C6
        expz += D4 
        expy += D5
        expx += D6
        Numero_generado += (D4)<<PosZ #(Z)
        Numero_generado += (D4 << PosC) + (D5 << PosC1) + (D6 << PosC2) #para reestablecer el valor sólo si D es 1, (osea, cuando el controlador es 0) directamente en el número
        Numero_generado += (D4*expx) << PosZ #(Z)
        Numero_generado -= (D4*expx) << PosY #(Y)
        Numero_generado -= ((D5*expy) << PosZ) - ((D5*expy) << PosX) #Y y X
        Numero_generado -= ((D6*expz) << PosX) - ((D6*expz) << PosY) #X y Y
        C4 = (Numero_generado >> PosC2) & 1 #cuarto controlador
        C5 = (Numero_generado >> PosC1) & 1 #quinto controlador
        C6 = (Numero_generado >> PosC) & 1 #sexto controlador
        caso = C4 + C5 + C6
        Numero_generado += D4 * (base/(expz+1)) % base + D5 * (base/(expy+1))%base + D6 * (base/(expx+1))%base #Esto conserva la energía emocional, ya que si tiene experiencia 1, su valor va a quedare en 50, en lugar de 0
        Numero_generado = int(Numero_generado)
        Numero_generado = int(Numero_generado % ((base**3) * 2**3))
        expz = int(expz) 
        expy = int(expy) 
        expx = int(expx)
    return Numero_generado, expx, expy, expz
