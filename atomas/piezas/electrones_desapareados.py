def electrones_desapareados(atom):
    """
    Calcula electrones desapareados SOLO con palitos.
    Regla: electrones desapareados = electrones que NO están apareados.
    
    Para elementos de transición (capas ≥ 3):
    - Si palitos_I ≤ 5: todos están desapareados
    - Si palitos_I > 5: empiezan a aparearse (10 - palitos_I)
    
    ¡Los palitos_O indican cuántos ya están apareados!
    """
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    capas = atom['capas']
    carga = atom.get('carga', 0)
    
    # Ajuste por carga (quitar electrones de los I)
    electrones_efectivos = palitos_I - carga
    
    if electrones_efectivos <= 0:
        return 0
    
    # Elementos de transición (capas 3 o 4)
    if capas >= 3:
        # Máximo 5 electrones desapareados (regla de Hund)
        if electrones_efectivos <= 5:
            desapareados = electrones_efectivos
        else:
            desapareados = 10 - electrones_efectivos
        
        # ¡Los palitos_O fuerzan el apareamiento!
        # Cada 2 palitos_O aparean 1 electrón desapareado
        factor_apareamiento = palitos_O // 2
        desapareados = max(0, desapareados - factor_apareamiento)
        
        # CASO ESPECIAL: Configuración d¹⁰ (Cu, Zn, Ga)
        # Si hay muchos O y pocos I, todos los electrones están apareados
        if palitos_O >= 2 and electrones_efectivos >= 6:
            # d¹⁰ es diamagnético (0 desapareados)
            if electrones_efectivos >= 10:
                return 0
            # Si tiene 9 o menos, pueden quedar algunos
            desapareados = max(0, desapareados - palitos_O)
        
        return max(0, desapareados)
    
    # Elementos del bloque p (capas 2)
    elif capas == 2:
        if electrones_efectivos <= 3:
            desapareados = electrones_efectivos
        else:
            desapareados = 6 - electrones_efectivos
        
        factor_apareamiento = palitos_O // 2
        desapareados = max(0, desapareados - factor_apareamiento)
        return max(0, desapareados)
    
    # Elementos del bloque s (capas 1)
    else:
        return min(electrones_efectivos, 1)
