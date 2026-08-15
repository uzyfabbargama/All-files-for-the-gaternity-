def superconductividad(atom, temperatura=300):
    """
    Predice la superconductividad teórica.
    Fórmula: (Magnetismo × Conductividad) / (Temperatura/100)
    """
    mag = fuerza_magnetica(atom)
    cond = conductividad(atom)
    sc_base = mag * cond
    
    # Factor de temperatura inverso
    factor_temp = 1.0 / (temperatura / 100)
    
    # Corrección: si es ferromagnético, la SC se anula en la realidad
    # (pero la dejamos como propiedad teórica)
    if es_magnetico(atom) and atom['palitos_O'] == 0:
        # El ferromagnetismo puro destruye la SC en la práctica
        # pero tu modelo predice la SC teórica
        pass
    
    return sc_base * factor_temp
