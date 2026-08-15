def reactividad(atom):
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    if palitos_I == 0:
        return 0
    
    # Factor de mecha
    longitud = 8 - capas
    if longitud <= 0:
        factor_mecha = 1
    else:
        factor_mecha = longitud / 6
    O_efectivos = palitos_O * factor_mecha
    
    # Reactividad (usando O_efectivos)
    base = longitud * 20
    
    if palitos_I <= 3:
        base += (4 - palitos_I) * 25
    elif palitos_I >= 6:
        base += (palitos_I - 5) * 10
    else:
        base += 5
    
    if palitos_O >= 6:
        base += O_efectivos * 15
    elif palitos_O >= 3:
        base += O_efectivos * 8
    else:
        base += palitos_O * 3
    
    total_valencia = palitos_I + O_efectivos
    if total_valencia < 8:
        base += (8 - total_valencia) * 10
    elif total_valencia > 8:
        base += (total_valencia - 8) * 5
    
    if carga > 0:
        base -= carga * 5
    elif carga < 0:
        base += abs(carga) * 10
    
    return max(base, 0)
