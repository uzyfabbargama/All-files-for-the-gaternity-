import math

def to_nmxt(lista_numeros, parte_entera_bits=32, parte_decimal_bits=32):
    buffer_nmxt = []
    
    for num in lista_numeros:
        # 1. Separamos el número en su representación de punto fijo
        # Multiplicamos el número por 2^bits_decimales para "subirlo" al entero
        valor_total = int(num * (2 ** parte_decimal_bits))
        
        # 2. Creamos la cadena legible
        linea = (f"int: {parte_entera_bits} "
                 f"frac: {parte_decimal_bits} "
                 f"sep {valor_total} ,,")
        buffer_nmxt.append(linea)
    
    return "\n".join(buffer_nmxt)

# Ejemplo: Pesos de una IA
pesos_ia = [0.15, -0.89, 1.618, 3.1415]
data_final = to_nmxt(pesos_ia)

with open("modelo.nmxt", "w") as f:
    f.write(data_final)
