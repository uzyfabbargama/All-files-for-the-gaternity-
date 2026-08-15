def electronegatividad(atom, factor_escala=2.65):
    """
    Calcula la electronegatividad efectiva de un átomo basada en palitos.
    
    Regla de Uziel:
    EN = (1 / capas) * O_efectivos
    Solo si I > 0 (si hay electrones libres).
    """
    capas = atom['capas']
    I = atom['palitos_I']
    O = atom['palitos_O']
    
    if I == 0:
        return 0  # Sin electrones libres, no hay enlaces
    
    # Factor de mecha (longitud del palito)
    longitud = 8 - capas
    factor_mecha = longitud / 6 if longitud > 0 else 0.1
    O_efectivos = O * factor_mecha
    #if longitud <= 0:
    #    factor_mecha = 0.1
    #else:
     #   factor_mecha = longitud / 6
    
    #O_efectivos = O * factor_mecha
    
    # EN = (1 / capas) * O_efectivos
    en = factor_escala * (1 / capas) * O_efectivos
    return round(en, 4)

