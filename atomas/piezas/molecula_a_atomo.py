def molecula_a_atomo(molecula, escala=1):
    """
    Convierte una molécula (dict con elementos y proporciones) en un átomo virtual.
    
    Ejemplo:
    molecula = {
        'C': {'cantidad': 6, 'capas': 2, 'I': 4, 'O': 0},
        'H': {'cantidad': 12, 'capas': 1, 'I': 1, 'O': 0},
        'O': {'cantidad': 6, 'capas': 2, 'I': 2, 'O': 4}
    }
    """
    total_atomos = sum([molecula[el]['cantidad'] for el in molecula])
    
    capas_prom = sum([molecula[el]['cantidad'] * molecula[el]['capas'] for el in molecula]) / total_atomos
    I_prom = sum([molecula[el]['cantidad'] * molecula[el]['I'] for el in molecula]) / total_atomos
    O_prom = sum([molecula[el]['cantidad'] * molecula[el]['O'] for el in molecula]) / total_atomos * escala
    
    return {
        'nombre': 'Molecula_Virtual',
        'capas': capas_prom,
        'palitos_I': I_prom,
        'palitos_O': O_prom,
        'carga': 0,
        'numero': -1,
        'I_max': 10,
        'O_max': 10
    }
