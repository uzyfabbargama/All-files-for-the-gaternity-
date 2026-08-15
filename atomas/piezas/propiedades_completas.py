def propiedades_completas(atom, es_polimero=False, grado_polimerizacion=1):
    """
    Devuelve TODAS las propiedades del material en un solo diccionario.
    Incluye: estructurales, eléctricas, magnéticas, ópticas, mecánicas y nucleares.
    """
    if es_polimero:
        # Si es polímero, usamos la función específica
        pol = modelar_polimero(atom, grado_polimerizacion)
        return {
            'nombre': pol['nombre'],
            'flexibilidad': pol['flexibilidad'],
            'conductividad': pol['conductividad'],
            'reactividad': pol['reactividad'],
            'punto_fusion': pol['punto_fusion'],
            'opticas': propiedades_opticas(atom),
            'magnetico': es_magnetico(atom),
            'radiactividad': radiactividad(atom),
            'clasificacion': 'Polímero',
            'descripcion': pol['descripcion']
        }
    else:
        # Material cristalino / metálico
        return {
            'nombre': atom['nombre'],
            'capas': atom['capas'],
            'I': atom['palitos_I'],
            'O': atom['palitos_O'],
            'punto_fusion': punto_fusion(atom),
            'conductividad': conductividad(atom),
            'reactividad': reactividad(atom),
            'radiactividad': radiactividad(atom),
            'magnetico': es_magnetico(atom),
            'fuerza_magnetica': fuerza_magnetica(atom),
            'flexibilidad': flexibilidad(atom),
            'opticas': propiedades_opticas(atom),
            'clasificacion': 'Cristalino / Metálico'
        }
