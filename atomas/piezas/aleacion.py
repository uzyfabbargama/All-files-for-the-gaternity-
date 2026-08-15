def aleacion(atomos, proporciones):
    """
    Crea un átomo virtual a partir de una aleación de varios átomos.
    """
    capas_prom = sum([atom['capas'] * p for atom, p in zip(atomos, proporciones)])
    I_prom = sum([atom['palitos_I'] * p for atom, p in zip(atomos, proporciones)])
    O_prom = sum([atom['palitos_O'] * p for atom, p in zip(atomos, proporciones)])
    carga_prom = sum([atom.get('carga', 0) * p for atom, p in zip(atomos, proporciones)])
    
    return {
        'nombre': 'Aleacion',
        'capas': capas_prom,
        'palitos_I': I_prom,
        'palitos_O': O_prom,
        'carga': carga_prom,
        'numero': -1,
        'I_max': max([atom['I_max'] for atom in atomos]),
        'O_max': max([atom['O_max'] for atom in atomos]),
    }
