def radiactividad(atom):
    """
    Predice la radiactividad de un átomo o ion.
    """
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    # Factores por capas y carga
    if capas >= 7:
        factor_capa = 10
    elif capas >= 6:
        factor_capa = 5
    elif capas >= 5:
        factor_capa = 2
    else:
        factor_capa = 0
    
    # La carga reduce la radiactividad hasta un 21%
    factor_carga = 1 - (abs(carga) * 0.03)
    factor_carga = max(0.79, factor_carga)
    
    # 1. Radio atómico
    electrones_totales = palitos_I + palitos_O
    radio_atomico = capas * 0.5 + electrones_totales * 0.1
    
    # 2. Fuerza nuclear fuerte
    fuerza_nuclear = 100 / (capas * 2 + electrones_totales * 0.5)
    
    # 3. Tensión electrónica
    tension_electronica = electrones_totales * 0.1 + capas * 2
    
    # 4. Inestabilidad nuclear
    inestabilidad = (radio_atomico * 0.5) + (1 / fuerza_nuclear) + tension_electronica * 0.3
    
    # 5. Radiactividad total
    rad = inestabilidad * factor_capa * factor_carga
    return rad
