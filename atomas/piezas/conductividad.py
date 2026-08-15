def conductividad(atom):
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    # 1. Factor de mecha (tu idea)
    longitud = 8 - capas  # 1-6
    if longitud <= 0:
        factor_mecha = 0.1
    else:
        factor_mecha = longitud / 6  # 0.17 a 1.0
    
    # 2. O efectivos (corregidos por la mecha)
    O_efectivos = palitos_O * factor_mecha
    
    # 3. Conductividad base
    base = capas * 12
    base += palitos_I * 10
    
    # 4. Efecto de los O (usando O_efectivos)
    if O_efectivos <= 2:
        base += O_efectivos * 15
    elif O_efectivos <= 4:
        base += (4 - O_efectivos) * 8
    else:
        base -= (O_efectivos - 4) * 20
    
    # 5. Bonus por metales nobles (I alto)
    if palitos_I >= 6:
        base += 30
    
    if carga != 0:
        base -= abs(carga) * 8
    
    return max(base, 0)
