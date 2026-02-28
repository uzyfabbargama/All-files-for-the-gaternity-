def calcular_randomixer_hex(semilla):
    # Convertimos la semilla hex a una lista de enteros (Base 16)
    s_str = str(semilla).zfill(8).upper()
    try:
        valores = [int(char, 16) for char in s_str]
    except ValueError:
        return print("Error: Usa solo caracteres 0-9 o A-F")

    # Formamos las duplas de 2 en 2
    duplas = [(valores[i], valores[i+1]) for i in range(0, 8, 2)]
    
    # 1. Jerarquía por valor máximo (Igual que en tu sistema original)
    jerarquia = sorted(duplas, key=lambda x: max(x), reverse=True)
    g_p, m_p, p_p, me_p = jerarquia[0], jerarquia[1], jerarquia[2], jerarquia[3]
    
    # 2. Regla del Cero para la Gravedad
    if 0 in g_p:
        gravedad = g_p[0] + g_p[1]
    else:
        gravedad = g_p[0] * g_p[1]
    
    # Si la gravedad resulta 0 (semilla 00000000), evitamos el colapso
    if gravedad == 0: gravedad = 1 

    def calc_dureza(pair):
        # (gravedad - d1 * d2) + d1 
        return abs((gravedad - (pair[0] * pair[1])) + pair[0])

    # Cálculos de Dureza y Altura 
    d_agua, d_madera = calc_dureza(g_p), calc_dureza(m_p)
    d_piedra, d_metal = calc_dureza(p_p), calc_dureza(me_p)
    
    a_madera = (d_madera**2) / gravedad
    
    # 3. Eficiencia y Conexión 
    f_carbon = m_p[0] * m_p[1]
    f_hierro = me_p[0] * me_p[1]
    eficiencia_hierro = f_carbon / f_hierro if f_hierro != 0 else 0
    n_agua = g_p[0] - g_p[1]

    print(f"--- MOTOR HEXADECIMAL: {semilla} ---")
    print(f"Gravedad: {gravedad}")
    print(f"Altura Jugador: {a_madera * 0.1:.4f} m")
    print(f"Dureza Metal: {d_metal} | Dureza Madera: {d_madera}")
    print(f"Conexión Agua: {n_agua} ({'+' if n_agua >=0 else '-'})")

seed = input("Escriba su semilla Hex (Ej: A1B2C3D4): ")
calcular_randomixer_hex(seed)
