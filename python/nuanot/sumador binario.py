def binary_adder(a, b):
    """
    Suma dos números enteros usando operaciones binarias a nivel de bit.
    
    Args:
        a: Primer número entero.
        b: Segundo número entero.
        
    Returns:
        La suma de los dos números.
    """
    
    # Se utiliza un bucle para procesar el acarreo.
    while b != 0:
        # 'carry' es el bit de acarreo, se produce cuando ambos bits son 1.
        # Se desplaza a la izquierda para sumarlo en la siguiente posición.
        carry = (a & b) << 1
        
        # 'a' se convierte en la suma de los bits (sin acarreo), usando XOR.
        a = a ^ b
        
        # 'b' se convierte en el acarreo para la próxima iteración.
        b = carry
        
    return a

# Ejemplo de uso:
num1 = 5  # binario 101
num2 = 3  # binario 011
resultado = binary_adder(num1, num2)
print(f"La suma de {num1} y {num2} es: {resultado}")

# Para verificar que el resultado es 8 (binario 1000)
print(f"El resultado en binario es: {bin(resultado)}")