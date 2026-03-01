import os
import math

# Definimos un alfabeto que incluye todos los caracteres comunes del 
# rango ASCII extendido (valores 32-255). Esto soluciona el problema de la "ñ" y otros caracteres especiales.
ALFABETO_CRIPTOGRAPHIUM = ''.join([chr(i) for i in range(32, 256)])

def criptographium_cipher(texto, modo="codificar"):
    """
    Implementa la lógica de cifrado/descifrado "Criptographium" para un texto dado.

    Args:
        texto (str): El texto a codificar o decodificar.
        modo (str): "codificar" para cifrar o "decodificar" para descifrar.
    
    Returns:
        str: El texto procesado o un mensaje de error si el modo no es válido.
    """
    
    # La clave de cifrado es la longitud del texto. Esto lo hace dinámico y único.
    clave = len(texto)
    texto_procesado = ""

    # Aseguramos que el modo es válido
    if modo not in ["codificar", "decodificar"]:
        return "Error: El modo debe ser 'codificar' o 'decodificar'."

    if modo == "codificar":
        # Parte de la lógica de "basura" para el Criptographium.
        print(f"DEBUG: Este texto tiene {clave} caracteres.")

        for caracter in texto:
            try:
                # Obtenemos la posición del carácter en nuestro alfabeto
                posicion_original = ALFABETO_CRIPTOGRAPHIUM.index(caracter)
                # Aplicamos el cifrado César en la posición
                nueva_posicion = (posicion_original + clave) % len(ALFABETO_CRIPTOGRAPHIUM)
                # Obtenemos el nuevo carácter del alfabeto
                texto_procesado += ALFABETO_CRIPTOGRAPHIUM[nueva_posicion]
            except ValueError:
                # Si el carácter no está en el alfabeto, lo dejamos como está
                texto_procesado += caracter
        
        return texto_procesado

    elif modo == "decodificar":
        for caracter in texto:
            try:
                # Obtenemos la posición del carácter en nuestro alfabeto
                posicion_original = ALFABETO_CRIPTOGRAPHIUM.index(caracter)
                # Invertimos el proceso de cifrado (resta en lugar de suma)
                # El '+ len(ALFABETO_CRIPTOGRAPHIUM)' asegura que el resultado no sea negativo
                nueva_posicion = (posicion_original - clave + len(ALFABETO_CRIPTOGRAPHIUM)) % len(ALFABETO_CRIPTOGRAPHIUM)
                # Obtenemos el carácter decodificado
                texto_procesado += ALFABETO_CRIPTOGRAPHIUM[nueva_posicion]
            except ValueError:
                # Si el carácter no está en el alfabeto, lo dejamos como está
                texto_procesado += caracter
            
        return texto_procesado

# --- Ejemplo de uso ---
if __name__ == "__main__":
    
    # Pedir al usuario el modo
    while True:
        modo_elegido = input("¿Qué quieres hacer? (codificar/decodificar): ").lower()
        if modo_elegido in ["codificar", "decodificar"]:
            break
        else:
            print("Modo no válido. Por favor, elige 'codificar' o 'decodificar'.")

    # Pedir al usuario el texto
    texto_usuario = input("Introduce el texto: ")

    # Procesar el texto según el modo elegido
    texto_resultante = criptographium_cipher(texto_usuario, modo=modo_elegido)
    
    print(f"\nTexto original: {texto_usuario}")
    print(f"Texto procesado: {texto_resultante}")
    
    # Si se codificó, se puede probar a decodificarlo
    if modo_elegido == "codificar":
        print("\n--- Probando a decodificarlo ---")
        texto_decodificado = criptographium_cipher(texto_resultante, modo="decodificar")
        print(f"Texto decodificado: {texto_decodificado}")

