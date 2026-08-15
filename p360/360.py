#python3
A = int(input("coloque su número"))
B = 0
C = 0
D = B

def calcular(base, carry, index, counter):
    print(f"EJECUCIÓN {index}")
    print(f"VALOR {base}")
    print(f"CARRY {carry}")
    print(f"CONTADOR {counter}")
    print("-------------------")
    if base >= 512:
        base -= 512
        carry = 1
        counter += carry
        index += 1
    else:
        carry = 0
        base += A
        counter += carry
        index += 1
    return base, carry, index, counter
    
resultado, carry, indice, contador = calcular(A, B, C, D)
while indice < 100:
    resultado, carry, indice, contador = calcular(resultado, carry, indice, contador)	    
    #print(f"EJECUCIÓN {indice}")
    #print(f"VALOR {resultado}")
    #print(f"CARRY {carry}")
    #print(f"CONTADOR {contador}")
    #print("-------------------")

