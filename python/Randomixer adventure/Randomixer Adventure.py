#Constantes funcionales
PosS = 10** 7
PosT = 10** 6
PosU = 10** 5
PosV = 10** 4
PosW = 10** 3
PosX = 10** 2
PosY = 10** 1
PosZ = 10** 0
#Pedir valor de 8 dígitos
#seed = int(input("Elija su mundo (Un número de 8 cifras)"))
seed = 14212153
seed = 12345670
def numeraso_seed(seed):
    S = max(1,(seed // PosS) % 10)
    T = max(1,(seed // PosT) % 10)
    U = max(1,(seed // PosU) % 10)
    V = max(1,(seed // PosV) % 10)
    W = max(1,(seed // PosW) % 10)
    X = max(1,(seed // PosX) % 10)
    Y = max(1,(seed // PosY) % 10)
    Z = max(1,(seed // PosZ) % 10)
    red = max(S, T)
    yellow = max (U, V)
    green = max (W, X)
    blue = max (Y, Z)
    red1 = min (S, T)
    yellow1 = min (U, V)
    green1 = min (W, X)
    blue1 = min (Y, Z)
    #blue1*= -1 #problema: necesitamos el 0. Solución:, le multiplicamos -1 a las variables para obtenerlo (ya que el 0 va a ser el mayor)
    #green1 *= -1
    #yellow1 *= -1
    #red1 *= -1
    total = (red, yellow, green, blue) #tupla de las variables mayores
    orden = sorted(total) #tupla ordenada
    total_min = ((red1-1),(yellow1-1),(green1-1),(blue1-1)) #tupla de las variables menores (decodificada para incluir el 0)
    orden_min1 = sorted(total_min) #tupla ordenada de las variables menores
    orden_min = (orden_min1[0], orden_min1[1], orden_min1[2], orden_min1[3])
    return orden, orden_min
valor = max(5, 6)
orden, orden_min = numeraso_seed(seed)
print(orden, orden_min)
red = [orden[0], orden_min[0]]
yellow = [orden[1], orden_min[1]]
green = [orden[2], orden_min[2]]
blue =  [orden[3], orden_min[3]]
print (f"el valor de rojo es:{red}")
print (f"el valor de amarillo es:{yellow}")
print (f"el valor de verde es:{green}")
print (f"el valor de azul es:{blue}")
#43 suma
#42 multiplicación
#operación =chr (42 + (1 - orden[3]*orden[3]))
B = bool(orden[3])
B1 = bool(orden_min[3])
A = orden[3]
A1 = orden_min[3]
print(A, A1)
operación = chr(42 + (1 - B*B1) )
print (f"La operación es: {operación}")
resultado = exec(f"resultado = A {operación} A1; print(resultado)")
print(resultado)
#print (min(7, 0))