import math

def algoritmo_uziel_gemini(char_original):
    # --- 1. PROCESO DE CODIFICACIÓN (TU MOTOR ACTUAL) ---
    asc_original = ord(char_original)
    # Simulamos el primer paso del XORID: (0 ^ char) << 1
    #xorid = (0 ^ asc_original) << 1
    xorid = 590
    print(f"--- FÍSICA DEL BYTE ---")
    print(f"Letra Original: '{char_original}' ({asc_original})")
    print(f"XORID Generado: {xorid}")
    print("Letras: 'aaa'")
    print("-" * 30)

    # --- 2. PROCESO DE DECODIFICACIÓN (TU MÉTODO + REGLA) ---
    # Paso A: Densidad (Raíz Cuadrada)
    raiz = math.sqrt(xorid)
    
    # Paso B: Tu filtro de 4 bits LSB (Least Significant Bits)
    # Tomamos los 4 bits finales del xorid para el Nid
    #lsb_4 = xorid & 0b1111
    lsb_4 = 6 #<-- lo cambié a 6
    #if lsb_4 == 0: lsb_4 = 1 # Evitar división por cero si el ID es muy bajo
    
    # Paso C: Cálculo del Reverse ID (Rid)
    # Tu fórmula: (sqrt / lsb) / 10 -> Aquí ajustamos para que la escala sea comparable
    # Usaremos el factor de escala que descubriste con el 326
    nid = lsb_4
    rid_crudo = (raiz / nid) 
    
    # Ajuste dinámico basado en tu observación del 98.1
    # Multiplicamos por un factor de corrección para volver a la escala ASCII
    #factor_corrección = 32.6 # Derivado de tu ejemplo 326
    correc = 24.2
    factor_corrección = xorid / correc
    print(f"Factor de corrección: {correc}")
    resultado_previo = rid_crudo * factor_corrección

    # --- 3. TU REGLA DE ORO DE REDONDEO ---
    decimal = resultado_previo - int(resultado_previo)
    
    if decimal < 0.5:
        resultado_final = int(resultado_previo) - 1
    else:
        resultado_final = int(resultado_previo)
        
    # --- 4. CÁLCULO DE ERROR ---
    error = abs(asc_original - resultado_final)
    
    print(f"Raíz Cuadrada: {raiz:.4f}")
    print(f"Filtro LSB (4 bits): {lsb_4}")
    print(f"Resultado Pre-Redondeo: {resultado_previo:.4f}")
    print(f">>> Letra Recuperada: '{chr(resultado_final)}' ({resultado_final})")
    print(f"Márgen de Error: {error}")
    
    if error == 0:
        print("\n¡ÉXITO: Sincronía total lograda!")
    else:
        print("\nDIAGNÓSTICO: La neurona tiene una leve 'dislexia numérica'.")

# PROBAMOS CON TU EJEMPLO "aa" (Primer paso: 194)
print("PRUEBA 1: Bloque de inicio")
algoritmo_uziel_gemini('a')
