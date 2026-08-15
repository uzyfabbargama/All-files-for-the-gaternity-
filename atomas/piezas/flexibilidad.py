def flexibilidad(atom):
    """
    Predice la flexibilidad de un material basado en la longitud de su "palito".
    Basado en la intuición de Uziel: palitos largos = flexibles, palitos cortos = quebradizos.
    """
    capas = atom['capas']
    longitud_palito = 8 - capas  # Rango típico: 1 (muy corto) a 7 (muy largo)
    
    # Normalizar a escala 0-100
    flexibilidad = (longitud_palito / 7) * 100
    
    # Clasificación cualitativa
    if flexibilidad > 80:
        clasificacion = "Elastómero (muy flexible, como caucho)"
    elif flexibilidad > 60:
        clasificacion = "Polímero flexible (como plástico de bolsa)"
    elif flexibilidad > 40:
        clasificacion = "Plástico semirrígido (como PVC)"
    elif flexibilidad > 20:
        clasificacion = "Metal dúctil (como cobre o aluminio)"
    else:
        clasificacion = "Material quebradizo (como cerámica o vidrio)"
    
    return {
        'valor': round(flexibilidad, 2),
        'clasificacion': clasificacion
    }

# Ejemplo:
# flexibilidad(atom) → {'valor': 75.0, 'clasificacion': 'Polímero flexible'}
