def rules(cut):
    colors_found = []
    i = 0
    n = len(cut)
    
    # Tabla de reglas basada en la cantidad de '1's consecutivos
    palette = {
        1: "blanco",
        2: "rojo",
        3: "verde",
        4: "azul",
        5: "verde rojo",
        6: "azul rojo",
        7: "azul verde",
        8: "blanco rojo verde rojo"
    }

    while i < n:
        if cut[i] == '0':
            colors_found.append("negro")
            i += 1
        else:
            # Si encontramos un 1, contamos cuántos siguen
            start = i
            while i < n and cut[i] == '1':
                i += 1
            count = i - start
            # Buscamos en la paleta según cuántos 1 hubo
            colors_found.append(palette.get(count, f"overload({count})"))
            
    return " ".join(colors_found)

# Prueba con tu ejemplo exacto: 00110110
test_bits = "00110110"
print(f"{test_bits} = {rules(test_bits)}")

# Integración con tu bucle de la Biblioteca
num = 0
for _ in range(0, 256):
    bina = bin(num)[2:] # Usamos el corte que te gusta
    print(f"{bina} = {rules(bina)}")
    num += 1
