def propiedades_opticas(atom):
    """
    Predice el comportamiento óptico basado en la relación I/O.
    Regla de Uziel: I = absorción, O = transparencia, I≈O = reflectancia.
    """
    I = atom['palitos_I']
    O = atom['palitos_O']
    total = I + O
    
    if total == 0:
        return {
            'color': 'Transparente (vacío)',
            'opacidad': 0,
            'reflectividad': 0,
            'descripcion': 'Sin electrones, material perfectamente transparente.'
        }
    
    # Relaciones
    proporcion_I = I / total
    proporcion_O = O / total
    
    # Opacidad (0-100): mayor I = más opaco
    opacidad = proporcion_I * 100
    
    # Reflectividad (0-100): máxima cuando I ≈ O
    reflectividad = 100 - abs(proporcion_I - proporcion_O) * 200
    reflectividad = max(0, min(100, reflectividad))  # Clamp entre 0 y 100
    
    # Clasificación de color (simplificada)
    if proporcion_I > 0.8:
        color = "Negro / Opaco (alta absorción)"
    elif proporcion_O > 0.8:
        color = "Transparente / Incoloro (alta transmisión)"
    elif 0.4 < proporcion_I < 0.6:
        color = "Metálico / Reflectante (plateado, dorado o cobrizo)"
    elif proporcion_I > proporcion_O:
        color = "Gris oscuro / Semimetálico"
    else:
        color = "Gris claro / Semitransparente"
    
    return {
        'color': color,
        'opacidad': round(opacidad, 2),
        'reflectividad': round(reflectividad, 2),
        'descripcion': f"I={I}, O={O} → {color}"
    }

# Ejemplo:
# propiedades_opticas(atom) → {'color': 'Metálico / Reflectante', 'opacidad': 50.0, 'reflectividad': 85.0}
