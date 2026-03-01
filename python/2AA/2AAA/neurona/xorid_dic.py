def calcular_id_personalizado():
    print("Introduce la palabra (el programa se detendrá al presionar Enter):")
    
    # Capturamos la entrada del usuario
    # input() en Python lee hasta encontrar un salto de línea (\n)
    palabra = input("> ")
    
    id_acumulado = 0
    
    print("\nPasos del cálculo:")
    print("-" * 30)
    
    for caracter in palabra:
        # Obtenemos el valor ASCII del caracter (byte)
        byte_val = ord(caracter)
        
        # Aplicamos la fórmula: (ID xor byte) desplazado 1 bit a la izquierda
        nuevo_id = (id_acumulado ^ byte_val) << 1
        
        print(f"Carácter '{caracter}' ({byte_val}) | ({id_acumulado} ^ {byte_val}) << 1 = {nuevo_id}")
        
        # Actualizamos el ID para la siguiente iteración
        id_acumulado = nuevo_id

    print("-" * 30)
    print(f"Resultado final del ID: {id_acumulado}")

if __name__ == "__main__":
    calcular_id_personalizado()
