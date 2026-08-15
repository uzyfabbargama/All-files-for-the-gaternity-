def modelar_polimero(atom, grado_polimerizacion=1000, temperatura=300):
    """
    Simula un polímero a partir de un átomo base (monómero).
    La flexibilidad y propiedades cambian con la longitud de la cadena.
    """
    # 1. Copiar el átomo base (monómero)
    polimero = atom.copy()
    
    # 2. Ajustar propiedades según grado de polimerización
    # Más repeticiones = palitos más largos efectivos = más flexibilidad
    longitud_efectiva = (8 - atom['capas']) * (1 + grado_polimerizacion / 1000)
    
    # 3. La conductividad disminuye con el grado de polimerización (los electrones quedan atrapados)
    conductividad_ajustada = conductividad(atom) / (1 + grado_polimerizacion / 10000)
    
    # 4. La reactividad disminuye (los extremos de la cadena son menos reactivos)
    reactividad_ajustada = reactividad(atom) / (1 + grado_polimerizacion / 5000)
    
    # 5. Punto de fusión (los polímeros se ablandan, no funden como metales)
    pf_ajustado = punto_fusion(atom) * 0.6  # Los polímeros funden a menor temperatura
    
    return {
        'nombre': f"Polímero de {atom['nombre']}",
        'capas': atom['capas'],
        'grado_polimerizacion': grado_polimerizacion,
        'flexibilidad': flexibilidad(atom)['valor'] * (1 + grado_polimerizacion / 5000),
        'conductividad': round(conductividad_ajustada, 2),
        'reactividad': round(reactividad_ajustada, 2),
        'punto_fusion': round(pf_ajustado, 2),
        'descripcion': f"Polímero con {grado_polimerizacion} unidades de repetición."
    }
