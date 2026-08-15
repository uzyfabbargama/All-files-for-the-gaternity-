import sys

def cifrado_not(texto):
    # Definimos el límite de 512 bits
    BITS = 512
    MAX_VAL = (1 << BITS) - 1
    
    resultado_final = ""
    
    # En Python, 'for caracter in texto' es como recorrer un array 
    # hasta encontrar el fin de la cadena.
    for caracter in texto:
        # Obtenemos el valor ASCII/Unicode
        valor_numerico = ord(caracter)
        
        # Aplicamos tu lógica de inversión de 512 bits
        valor_cifrado = MAX_VAL ^ valor_numerico
        
        # El truco de la concatenación: usamos el operador +
        # Convertimos el número a string para poder pegarlo
        resultado_final += str(valor_cifrado) + " "
    
    return resultado_final.strip()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Unimos todos los argumentos por si el texto tiene espacios
        entrada = " ".join(sys.argv[1:])
        salida = cifrado_not(entrada)
        
        print("----- Resultado 512-bit NOT -----")
        print(f"Entrada: {entrada}")
        print(f"Salida: {salida}")
    else:
        print("Uso: python3 cifrador.py <texto>")
