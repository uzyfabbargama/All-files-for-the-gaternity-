num = 151  # 10010111 en binario (empezando desde el bit 3)
all_results = []

def rules(cut):
    colors_found = []
    # Analizamos cada bit individualmente
    for bit in cut:
        bita = int(bit) # Convertimos el caracter '0' o '1' a entero
        
        if bita == 0:
            colors_found.append("negro")
        elif bita == 1:
            colors_found.append("blanco")
        # Nota: bita nunca será 2, 3... a menos que sumes varios bits,
        # pero para tu ejemplo de 10010111, esto es lo que necesitas.
            
    return " ".join(colors_found) # Une los colores con espacios

# Ejemplo con el número que mencionaste
bina = bin(num)
cut = bina[2:] # En Python, el binario empieza con '0b', cortamos eso
resultado = rules(cut)

print(f"{cut} = {resultado}")
