def adder(a, b):
    while b != 0:
        carry = (a & b) << 1
        a = a ^ b 
        b = carry
    return a
def nitenle():
    a = adder
    c = a << 1
    print(f"C = {c}")
    return c
num1 = int(input("Ingresa el primer número: "))
num2 = int(input("ingresa el segundo número: "))
resultado = adder(num1, num2)
nine = nitenle()
print(f"El primer número: {num1}. Es {bin(num1)} en binario")
print(f"El segundo número: {num2}. Es {bin(num2)} en binario")
print(f"El resultado en binario es: {bin(resultado)}")
print(f"El resultado del noveno bit es {bin(nine)}")