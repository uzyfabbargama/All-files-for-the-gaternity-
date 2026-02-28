def calcular_randomixer_v3(semilla):
    s_str = str(semilla).zfill(8)
    duplas = [(int(s_str[i]), int(s_str[i+1])) for i in range(0, 8, 2)]
    
    # 1. Jerarquía por el valor máximo de cada par
    jerarquia = sorted(duplas, key=lambda x: max(x), reverse=True)
    
    # Asignación de duplas
    g_p, m_p, p_p, me_p = jerarquia[0], jerarquia[1], jerarquia[2], jerarquia[3]
    
    # 2. Regla del Cero para la Gravedad
    if 0 in g_p:
        gravedad = g_p[0] + g_p[1] # Suma si hay un cero
    else:
        gravedad = g_p[0] * g_p[1] # Multiplicación estándar [cite: 1]
    
    def calc_dureza(pair):
        # (gravedad - d1 * d2) + d1 
        return abs((gravedad - (pair[0] * pair[1])) + pair[0])
    d_agua = calc_dureza(g_p)
    d_madera = calc_dureza(m_p)
    d_piedra = calc_dureza(p_p)
    d_metal = calc_dureza(me_p)
    a_agua = (d_agua**2) / gravedad
    a_madera = (d_madera**2) / gravedad
    a_piedra = (d_piedra**2) / gravedad
    a_metal = (d_metal**2) / gravedad
    # 3. Eficiencia de Fundición (Fuerza Madera / Producto Material) 
    f_carbon = m_p[0] * m_p[1]
    f_roca = p_p[0] * p_p[1]
    f_hierro = me_p[0] * me_p[1]
    f_agua = g_p[0] * g_p[1]
    eficiencia_piedra = f_carbon / f_roca if f_roca != 0 else 0
    eficiencia_hierro = f_carbon / f_hierro if f_hierro != 0 else 0

    print(f"--- MOTOR ESCALABLE: {semilla} ---")
    print(f"Gravedad: {gravedad}")
    print(f"Altura Jugador: {((d_madera**2)/gravedad)*0.1:.4f} m")
    print(f"Altura olas y precipitaciones: {a_agua}")
    print(f"Altura metal: {a_metal}")
    print(f"Altura piedra: {a_piedra}")
    print(f"Altura madera/árboles: {a_madera}")
    print(f"Eficiencia Carbón -> Hierro: {eficiencia_hierro:.4f} unidades")
    print(f"Dureza Metal: {d_metal}")
    print(f"Dureza Piedra: {d_piedra}")
    print(f"Dureza Madera: {d_madera}")
    print(f"Dureza Agua: {d_agua}")
    # Conexión d1 - d2 
    n_agua = g_p[0] - g_p[1]
    print(f"Conexión Agua: {n_agua} ({'+' if n_agua >=0 else '-'})")
seed = input("Escriba su semilla")
calcular_randomixer_v3(seed)
