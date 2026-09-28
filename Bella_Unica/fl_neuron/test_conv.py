# test_conv.py
def float_to_custom56(val: float) -> int:
    """ Convierte un float (0.0 a 1.999...) al formato entero de 56 bits. """
    entero = 1 if val >= 1.0 else 0
    frac = val - entero
    frac_bits = int(frac * (2 ** 55))
    return (entero << 55) | (frac_bits & ((1 << 55) - 1))

def custom56_to_float(val_int: int) -> float:
    """ Convierte el entero de 56 bits de vuelta a float. """
    entero = (val_int >> 55) & 1
    frac_bits = val_int & ((1 << 55) - 1)
    return entero + (frac_bits / (2 ** 55))

def procesar_conv(val_a: float, val_b: float, bias: float):
    """Simula la instrucción conv en Python"""
    r12 = float_to_custom56(val_a)
    r13 = float_to_custom56(val_b)
    
    # Procesar como conv
    r15 = r12
    r15 = (r15 & r13) & 0xFFFFFFFFFFFFFFFF
    r12 = (r12 + r15) & 0xFFFFFFFFFFFFFFFF
    r13 = (r13 + r15) & 0xFFFFFFFFFFFFFFFF
    r13 = (r13 + r12) & 0xFFFFFFFFFFFFFFFF
    r15 = (r15 + r13) & 0xFFFFFFFFFFFFFFFF
    
    # Añadir bias
    r15 = (r15 + float_to_custom56(bias)) & 0xFFFFFFFFFFFFFFFF
    
    return custom56_to_float(r15)

# Test
N1 = float(input("Primer  valor: "))
N2 = float(input("Segundo valor: "))
Bias = float(input("Bias         : "))
print(procesar_conv(N1, N2, Bias))
