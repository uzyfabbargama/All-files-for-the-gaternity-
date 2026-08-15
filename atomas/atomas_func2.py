# ============================================
# MODELO DE ÁTOMOS E IONES (VERSIÓN SIMPLE)
# ============================================

def punto_fusion(atom):
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    # 1. Cohesión por palitos_I (el "pegamento" estructural)
    base = palitos_I * 128
    
    # 2. Cohesión por capas (fuerzas de dispersión)
    base += capas * 64
    # 3. Cohesión por el inverso de la longitud del palito (efecto de tamaño)
    longitud = 8 - capas
    if longitud > 0:
        base += 50 / longitud  # El inverso de la longitud
    
    # 4. Repulsión por palitos_O
    base -= palitos_O * 32
    
    # 5. Si palitos_O es potencia de 2, repulsión máxima
    if palitos_O in [1, 2, 4, 8]:
        base -= 128
    
    # 6. Iones tienen mayor punto de fusión
    if carga != 0:
        base += abs(carga) * 256
    
    return max(base, -273)
# Tabla de electrones desapareados (configuración d)
ESPINES = {
    'Cu': 0,      # 3d¹⁰ → 0 desapareados
    'Fe': 4,      # 3d⁶ → 4 desapareados (alta espín)
    'Mn': 5,      # 3d⁵ → 5 desapareados
    'Mg': 0,      # sin electrones d
    'Zn': 0,      # 3d¹⁰ → 0 desapareados
    'Ga': 0,      # 3d¹⁰ → 0 desapareados
    'Cu+': 0,     # 3d¹⁰ → 0 desapareados
    'Cu2+': 1,    # 3d⁹ → 1 desapareado
    'Fe3+': 5,    # 3d⁵ → 5 desapareados
    'Mn2+': 5,    # 3d⁵ → 5 desapareados
}

def es_magnetico(atom):
    # Obtener la clave para la tabla de espines
    clave = atom['nombre']
    if atom.get('carga', 0) > 0:
        clave += f"+{atom['carga']}"
    
    # Buscar en la tabla de espines
    desapareados = ESPINES.get(clave, 0)
    return desapareados > 0

def conductividad(atom):
    """Predice la conductividad de un átomo o ion"""
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    base = palitos_O * 10
    if palitos_I > 5:
        base -= palitos_I * 2
    if carga != 0:
        base += abs(carga) * 15
    
    return max(base, 0)

def reactividad(atom):
    """Predice la reactividad de un átomo o ion"""
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    base = palitos_O * 5
    if carga > 0:
        base -= carga * 10
    elif carga < 0:
        base += abs(carga) * 15
    
    return max(base, 0)

def mostrar_propiedades(atom):
    """Muestra todas las propiedades de un átomo o ion"""
    nombre = atom['nombre']
    carga = atom.get('carga', 0)
    
    # Formatear el nombre con la carga
    if carga > 0:
        estado = f"{nombre}^{carga}+"
    elif carga < 0:
        estado = f"{nombre}^{abs(carga)}-"
    else:
        estado = nombre
    
    print(f"\n{'='*40}")
    print(f"Átomo/Ion: {estado}")
    print(f"Capas: {atom['capas']}")
    print(f"Palitos_I: {atom['palitos_I']}")
    print(f"Palitos_O: {atom['palitos_O']}")
    print(f"Longitud del palito: {8 - atom['capas']}")
    print("-" * 40)
    print(f"Punto de fusión: {punto_fusion(atom)}°C")
    print(f"Magnético: {'Sí' if es_magnetico(atom) else 'No'}")
    print(f"Conductividad: {conductividad(atom)}")
    print(f"Reactividad: {reactividad(atom)}")

# ============================================
# DEFINIR ÁTOMOS E IONES (DICCIONARIOS)
# ============================================

# Átomos neutros
Cu = {
    'nombre': 'Cu',
    'capas': 4,
    'palitos_I': 7,
    'palitos_O': 2
}

Fe = {
    'nombre': 'Fe',
    'capas': 4,
    'palitos_I': 8,
    'palitos_O': 0
}

Mn = {
    'nombre': 'Mn',
    'capas': 4,
    'palitos_I': 7,
    'palitos_O': 0
}

Mg = {
    'nombre': 'Mg',
    'capas': 3,
    'palitos_I': 2,
    'palitos_O': 0
}

Zn = {
    'nombre': 'Zn',
    'capas': 4,
    'palitos_I': 6,
    'palitos_O': 3
}

Ga = {
    'nombre': 'Ga',
    'capas': 4,
    'palitos_I': 5,
    'palitos_O': 4
}

# Iones (con carga)
Cu_ion = {
    'nombre': 'Cu',
    'capas': 4,
    'palitos_I': 8,
    'palitos_O': 1,
    'carga': 1
}

Cu_ion2 = {
    'nombre': 'Cu',
    'capas': 4,
    'palitos_I': 7,
    'palitos_O': 1,
    'carga': 2
}

Fe_ion = {
    'nombre': 'Fe',
    'capas': 4,
    'palitos_I': 6,
    'palitos_O': 0,
    'carga': 3
}

Mn_ion = {
    'nombre': 'Mn',
    'capas': 4,
    'palitos_I': 5,
    'palitos_O': 0,
    'carga': 2
}

# ============================================
# EJECUTAR Y MOSTRAR RESULTADOS
# ============================================

if __name__ == "__main__":
    # Lista de todos los átomos e iones
    atomos = [Cu, Fe, Mn, Mg, Zn, Ga, Cu_ion, Cu_ion2, Fe_ion, Mn_ion]
    
    for atom in atomos:
        mostrar_propiedades(atom)
