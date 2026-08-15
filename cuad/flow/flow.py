#1ro lo que hacemos es tomar un número
Numero = 11
print(Numero)
print(bin(Numero)[2:])
#2do, lo elevamos al cuadrado
Cuadrado = Numero ** 2
print(f"Cuadrado es: {Cuadrado}")
#3ro, lo pasamos a bits
binario = bin(Cuadrado)
binario = binario[2:]
print(binario)
#4. su xor es:
xor = bin(Numero ^ Cuadrado)[2:]
print(f"Su xor es: {xor}")
