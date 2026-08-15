def fuerza_magnetica(atom, temperatura=300):
    """
    Predice la fuerza magnética SOLO con palitos.
    
    Factores:
    1. Electrones desapareados (calculados con palitos)
    2. Temperatura (más frío = más magnético)
    3. Capas (más capas = magnetismo más persistente)
    """
    capas = atom['capas']
    palitos_O = atom['palitos_O']
    
    # Calcular desapareados sin tabla
    desapareados = electrones_desapareados(atom)
    
    if desapareados == 0:
        return 0.0
    
    # Fuerza base: más desapareados = más fuerza
    fuerza_base = desapareados * 1.8
    
    # Factor de capas: más capas = electrones más lejos = más persistentes
    if capas >= 3:
        factor_capas = 1 + (capas - 3) * 0.15
    else:
        factor_capas = 1 + (capas - 1) * 0.1
    
    fuerza_base *= factor_capas
    
    # BONUS por ferromagnetismo (Fe, Co, Ni)
    # Son elementos con I alto y O bajo
    if palitos_O == 0 and atom['palitos_I'] in [7, 8, 9]:
        fuerza_base *= 1.8  # ¡Ferromagnético!
    
    # Corrección por temperatura
    if fuerza_base > 0:
        T_critica = capas * 200  # 600-800K para capas 3-4
        factor_temperatura = 1 - (temperatura / T_critica)
        factor_temperatura = max(0, factor_temperatura)
        return fuerza_base * factor_temperatura
    
    return 0.0
