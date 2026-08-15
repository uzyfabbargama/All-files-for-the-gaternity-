def mostrar_propiedades(atom):
    """Muestra todas las propiedades de un átomo en formato CSV-friendly"""
    nombre = atom['nombre']
    carga = atom.get('carga', 0)
    capas = atom['capas']
    I = atom['palitos_I']
    O = atom['palitos_O']
    
    if carga > 0:
        estado = f"{nombre}^{carga}+"
    elif carga < 0:
        estado = f"{nombre}^{abs(carga)}-"
    else:
        estado = nombre
    
    return f"{atom['numero']},{estado},{capas},{I},{O},{8-capas},{punto_fusion(atom):.1f},{electrones_desapareados(atom)},{fuerza_magnetica(atom):.2f},{'Si' if es_magnetico(atom) else 'No'},{conductividad(atom):.1f},{reactividad(atom):.1f},{radiactividad(atom):.2f}"
