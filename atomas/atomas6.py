# ============================================
# GENERADOR DE ÁTOMOS PARA MOTOR DE SIMULACIÓN
# ============================================

def generar_todos_los_atomos():
    """
    Genera todos los átomos posibles según el modelo de palitos.
    
    Reglas:
    - capas: 1 a 7 (periodos de la tabla periódica)
    - I_max = capas² (número máximo de palitos_I)
    - O_max = 2 * capas (número máximo de palitos_O)
    - I + O <= capas * 2 (regla del octeto generalizada)
    """
    
    atomos = []
    
    # Configuración por capa
    config = {
        1: {'I_max': 1, 'O_max': 2},   # K
        2: {'I_max': 4, 'O_max': 6},   # L
        3: {'I_max': 9, 'O_max': 10},  # M
        4: {'I_max': 16, 'O_max': 14}, # N
        5: {'I_max': 25, 'O_max': 18}, # O
        6: {'I_max': 36, 'O_max': 22}, # P
        7: {'I_max': 49, 'O_max': 26}, # Q
    }
    
    numero_atomico = 1
    
    for capas in range(1, 8):
        I_max = config[capas]['I_max']
        O_max = config[capas]['O_max']
        
        # Generar todas las combinaciones válidas
        for I in range(I_max + 1):
            for O in range(O_max + 1):
                # Regla de validez: I + O <= I_max + O_max
                if I + O > I_max + O_max:
                    continue
                
                # Generar nombre técnico
                nombre_tecnico = f"Atom_{numero_atomico:03d}"
                
                atomo = {
                    'numero': numero_atomico,
                    'nombre': nombre_tecnico,
                    'capas': capas,
                    'palitos_I': I,
                    'palitos_O': O,
                    'carga': 0,
                    'I_max': I_max,
                    'O_max': O_max,
                }
                
                atomos.append(atomo)
                numero_atomico += 1
    
    return atomos


# ============================================
# MODELO DE ÁTOMOS E IONES (VERSIÓN SIMPLE)
# ============================================
from math import log2

def punto_fusion(atom):
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    base = palitos_I * 128
    base += capas * 64
    longitud = 8 - capas
    if longitud > 0:
        base += 50 / longitud
    if es_ionico:
        # MODO IÓNICO: SUMAMOS O (Anti-Noble)
        base += palitos_O * 32
        if palitos_O > 0 and palitos_O % 2 == 0:
            base += 187 << int(log2(palitos_O))
    else:
        base -= palitos_O * 32
        
        if palitos_O > 0 and palitos_O % 2 == 0:
            base -= 187 << int(log2(palitos_O))
        
        if carga != 0:
            base += abs(carga) * 256
    
    return max(base, -273)

def electrones_desapareados(atom):
    """
    Calcula electrones desapareados SOLO con palitos.
    Regla: electrones desapareados = electrones que NO están apareados.
    
    Para elementos de transición (capas ≥ 3):
    - Si palitos_I ≤ 5: todos están desapareados
    - Si palitos_I > 5: empiezan a aparearse (10 - palitos_I)
    
    ¡Los palitos_O indican cuántos ya están apareados!
    """
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    capas = atom['capas']
    carga = atom.get('carga', 0)
    
    # Ajuste por carga (quitar electrones de los I)
    electrones_efectivos = palitos_I - carga
    
    if electrones_efectivos <= 0:
        return 0
    
    # Elementos de transición (capas 3 o 4)
    if capas >= 3:
        # Máximo 5 electrones desapareados (regla de Hund)
        if electrones_efectivos <= 5:
            desapareados = electrones_efectivos
        else:
            desapareados = 10 - electrones_efectivos
        
        # ¡Los palitos_O fuerzan el apareamiento!
        # Cada 2 palitos_O aparean 1 electrón desapareado
        factor_apareamiento = palitos_O // 2
        desapareados = max(0, desapareados - factor_apareamiento)
        
        # CASO ESPECIAL: Configuración d¹⁰ (Cu, Zn, Ga)
        # Si hay muchos O y pocos I, todos los electrones están apareados
        if palitos_O >= 2 and electrones_efectivos >= 6:
            # d¹⁰ es diamagnético (0 desapareados)
            if electrones_efectivos >= 10:
                return 0
            # Si tiene 9 o menos, pueden quedar algunos
            desapareados = max(0, desapareados - palitos_O)
        
        return max(0, desapareados)
    
    # Elementos del bloque p (capas 2)
    elif capas == 2:
        if electrones_efectivos <= 3:
            desapareados = electrones_efectivos
        else:
            desapareados = 6 - electrones_efectivos
        
        factor_apareamiento = palitos_O // 2
        desapareados = max(0, desapareados - factor_apareamiento)
        return max(0, desapareados)
    
    # Elementos del bloque s (capas 1)
    else:
        return min(electrones_efectivos, 1)

def fuerza_magnetica(atom, temperatura=300):
    """
    Predice la fuerza magnética SOLO con palitos.
    
    Factores:
    1. Electrones desapareados (calculados con palitos)
    2. Temperatura (más frío = más magnético)
    3. Capas (más capas = magnetismo más persistente)
    """
    capas = atom['capas']
    palitos_O = atom['palitos_O']
    
    # Calcular desapareados sin tabla
    desapareados = electrones_desapareados(atom)
    
    if desapareados == 0:
        return 0.0
    
    # Fuerza base: más desapareados = más fuerza
    fuerza_base = desapareados * 1.8
    
    # Factor de capas: más capas = electrones más lejos = más persistentes
    if capas >= 3:
        factor_capas = 1 + (capas - 3) * 0.15
    else:
        factor_capas = 1 + (capas - 1) * 0.1
    
    fuerza_base *= factor_capas
    
    # BONUS por ferromagnetismo (Fe, Co, Ni)
    # Son elementos con I alto y O bajo
    if palitos_O == 0 and atom['palitos_I'] in [7, 8, 9]:
        fuerza_base *= 1.8  # ¡Ferromagnético!
    
    # Corrección por temperatura
    if fuerza_base > 0:
        T_critica = capas * 200  # 600-800K para capas 3-4
        factor_temperatura = 1 - (temperatura / T_critica)
        factor_temperatura = max(0, factor_temperatura)
        return fuerza_base * factor_temperatura
    
    return 0.0

def es_magnetico(atom):
    """Determina si un átomo es magnético (fuerza > 0.5)"""
    return fuerza_magnetica(atom) > 0.5

def conductividad(atom):
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    # 1. Factor de mecha (tu idea)
    longitud = 8 - capas  # 1-6
    if longitud <= 0:
        factor_mecha = 0.1
    else:
        factor_mecha = longitud / 6  # 0.17 a 1.0
    
    # 2. O efectivos (corregidos por la mecha)
    O_efectivos = palitos_O * factor_mecha
    
    # 3. Conductividad base
    base = capas * 12
    base += palitos_I * 10
    
    # 4. Efecto de los O (usando O_efectivos)
    if O_efectivos <= 2:
        base += O_efectivos * 15
    elif O_efectivos <= 4:
        base += (4 - O_efectivos) * 8
    else:
        base -= (O_efectivos - 4) * 20
    
    # 5. Bonus por metales nobles (I alto)
    if palitos_I >= 6:
        base += 30
    
    if carga != 0:
        base -= abs(carga) * 8
    
    return max(base, 0)

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
def radiactividad(atom):
    """
    Predice la radiactividad de un átomo o ion.
    """
    capas = atom['capas']
    palitos_I = atom['palitos_I']
    palitos_O = atom['palitos_O']
    carga = atom.get('carga', 0)
    
    # 1. Radio atómico
    electrones_totales = palitos_I + palitos_O
    radio_atomico = capas * 0.5 + electrones_totales * 0.1
    
    # 2. Fuerza nuclear fuerte
    fuerza_nuclear = 100 / (capas * 2 + electrones_totales * 0.5)
    
    # 3. Tensión electrónica
    tension_electronica = electrones_totales * 0.1 + capas * 2
    
    # 4. Inestabilidad nuclear
    inestabilidad = (radio_atomico * 0.5) + (1 / fuerza_nuclear) + tension_electronica * 0.3
    
    # 5. Umbral: elementos con capas > 5 son radiactivos
# ORDEN DESCENDENTE (corregido)
    if capas >= 7:
        return inestabilidad * 10
    elif capas >= 6:
        return inestabilidad * 5
    elif capas >= 5:
        return inestabilidad * 2
    
    return 0
    
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


# ============================================
# EJECUTAR
# ============================================

if __name__ == "__main__":
    print("🔬 Generando tabla periódica de palitos...")
    atomos = generar_todos_los_atomos()
    print(f"✅ Generados {len(atomos)} átomos")
    
    # Cabecera CSV (actualizada con radiactividad)
    print("\n" + "="*130)
    print("N°,Nombre,Capas,I,O,Longitud,P.Fusion,Desap,Mag,Fuerza,Conduct,React,Radiact")
    print("-"*130)
    
    for atom in atomos:
        print(mostrar_propiedades(atom))
    
    print("="*130)
    print(f"✅ Total: {len(atomos)} átomos generados")
