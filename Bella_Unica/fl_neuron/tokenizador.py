def tokenizar_a_56bits(texto):
    """Convierte texto a formato 56 bits usando XORID de Bella"""
    # 1. Obtener ID con XORID (0 a 65535)
    idx = 0
    for car in texto:
        idx = (idx ^ ord(car)) << 1
        idx &= 0xFFFF  # Mantener en 16 bits
    
    # 2. Normalizar a 0.0-1.0
    normalizado = idx / 65535.0
    
    # 3. Convertir a formato 56 bits
    if normalizado >= 1.0:
        entero = 1
        frac = normalizado - 1.0
    else:
        entero = 0
        frac = normalizado
    
    frac_bits = int(frac * (2 ** 55))
    return (entero << 55) | (frac_bits & ((1 << 55) - 1))

# Ejemplo
token = tokenizar_a_56bits("Hola ¿cómo estás?")
parte_entera = str(bin((token >> 55) & 1))
parte_decimal = str(bin((token << 1) & ((1 << 56)-1)))
print(f"Token: {token}")  # 0.7234...
print(f"Estructura binaria: {parte_entera[2:]}.{parte_decimal[2:]}")
