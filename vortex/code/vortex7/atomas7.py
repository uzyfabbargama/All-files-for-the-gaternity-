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

def punto_fusion(atom, es_ionico=False):
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
        # MODO METÁLICO: RESTAMOS O (Noble)
        base -= palitos_O * 32
        if palitos_O > 0 and palitos_O % 2 == 0:
            base -= 187 << int(log2(palitos_O))
    
    # ⚠️ CORRECCIÓN: esto va fuera del else
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
def electrones_f_desapareados(Z):
    """
    Calcula electrones f desapareados sin tablas.
    Usa la posición relativa en el periodo.
    """
    # Lantánidos: Z = 57 a 71 (periodo 6, bloque f)
    if 57 <= Z <= 71:
        posicion = Z - 56  # 1 a 15
        if posicion <= 8:
            return posicion  # 1 a 7 (con el 8 dando 7)
        else:
            return 16 - posicion  # 7 a 1
    
    # Actínidos: Z = 89 a 103 (periodo 7, bloque f)
    elif 89 <= Z <= 103:
        posicion = Z - 88  # 1 a 15
        if posicion <= 8:
            return posicion  # 1 a 7
        else:
            return 16 - posicion  # 7 a 1
    
    # No es lantánido ni actínido
    return 0
def fuerza_magnetica(atom, temperatura=300):
    """
    Magnetismo = Integridad de la red 2D
    ===================================
    La materia es una red cuadrada 2D que se pliega en 3D.
    
    Demostración:
    - En 2D, cada punto tiene 8 vecinos (2³)
    - Los orbitales son primos × 2: s=2, p=6, d=10, f=14
    - La suma de orbitales da 2 × n²: 2, 8, 18, 32
    - El spin tiene 2 estados (2¹)
    - Un cuadrado tiene 4 lados (2²)
    
    El magnetismo mide la integridad de la red:
    - I = vecinos ocupados (máximo 8)
    - O = huecos en la red
    - capas = lado del cuadrado (n)
    - f = pliegues de la red 2D en 3D
    """
    capas = atom['capas']
    I = atom['palitos_I']
    O = atom['palitos_O']
    Z = atom.get('Z', 0)
    
    # ==========================================
    # 1. Red 2D perfecta = 8 vecinos ocupados, 0 huecos
    # ==========================================
    VECINOS_PERFECTOS = 8  # 2³
    
    # ¿Qué tan perfecta es la red?
    # - Si I=8 y O=0 → integridad = 8 (red perfecta)
    # - Si I=7 y O=0 → integridad = 7 (un vecino menos)
    # - Si I=8 y O=1 → integridad = 7 (un hueco)
    integridad_red = VECINOS_PERFECTOS - abs(I - VECINOS_PERFECTOS) - O
    
    # ==========================================
    # 2. Penalización por capa (la red se estira)
    # ==========================================
    # La capa 4 es la red perfecta (Fe, Co, Ni)
    # Capas más grandes = red más estirada = menos magnetismo
    # 0.25 = 2⁻² (factor natural por ser cuadrado)
    penalizacion_capa = (capas - 4) * 0.25
    
    # ==========================================
    # 3. Fuerza de valencia (metales de transición)
    # ==========================================
    fuerza_valencia = integridad_red - penalizacion_capa
    
    # ==========================================
    # 4. Pliegues f (lantánidos y actínidos)
    # ==========================================
    # Los electrones f son pliegues de la red 2D en 3D
    # Cada pliegue aporta 1 unidad de magnetismo (2⁰)
    f_desapareados = electrones_f_desapareados(Z)
    fuerza_f = f_desapareados * 1.0
    
    # ==========================================
    # 5. Combinar: el magnetismo es la suma de
    #    la red 2D + los pliegues f
    # ==========================================
    if f_desapareados > 0 and capas >= 6:
        # Lantánido: dominan los pliegues f
        fuerza_total = fuerza_f
        
        # Bonus si la red 2D también está intacta
        if I == 8 and O == 0:
            fuerza_total += 1.0  # 2⁰
    else:
        # Metal de transición: domina la red 2D
        fuerza_total = fuerza_valencia
    
    # ==========================================
    # 6. Clamp entre 0 y 10
    # ==========================================
    return max(0, min(10, fuerza_total))

def es_magnetico(atom):
    #Determina si un átomo es magnético (fuerza > 0.5)
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
    
    # Factores por capas y carga
    if capas >= 7:
        factor_capa = 10
    elif capas >= 6:
        factor_capa = 5
    elif capas >= 5:
        factor_capa = 2
    else:
        factor_capa = 0
    
    # La carga reduce la radiactividad hasta un 21%
    factor_carga = 1 - (abs(carga) * 0.03)
    factor_carga = max(0.79, factor_carga)
    
    # 1. Radio atómico
    electrones_totales = palitos_I + palitos_O
    radio_atomico = capas * 0.5 + electrones_totales * 0.1
    
    # 2. Fuerza nuclear fuerte
    fuerza_nuclear = 100 / (capas * 2 + electrones_totales * 0.5)
    
    # 3. Tensión electrónica
    tension_electronica = electrones_totales * 0.1 + capas * 2
    
    # 4. Inestabilidad nuclear
    inestabilidad = (radio_atomico * 0.5) + (1 / fuerza_nuclear) + tension_electronica * 0.3
    
    # 5. Radiactividad total
    rad = inestabilidad * factor_capa * factor_carga
    return rad
    
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

    if es_magnetico(atom) and atom['palitos_O'] == 0:
        # El ferromagnetismo puro destruye la SC en la práctica
        # pero tu modelo predice la SC teórica
        pass
    
    return sc_base * factor_temp

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
def electronegatividad(atom, factor_escala=2.65):
    """
    Calcula la electronegatividad efectiva de un átomo basada en palitos.
    
    Regla de Uziel:
    EN = (1 / capas) * O_efectivos
    Solo si I > 0 (si hay electrones libres).
    """
    capas = atom['capas']
    I = atom['palitos_I']
    O = atom['palitos_O']
    
    if I == 0:
        return 0  # Sin electrones libres, no hay enlaces
    
    # Factor de mecha (longitud del palito)
    longitud = 8 - capas
    factor_mecha = longitud / 6 if longitud > 0 else 0.1
    O_efectivos = O * factor_mecha
    #if longitud <= 0:
    #    factor_mecha = 0.1
    #else:
     #   factor_mecha = longitud / 6
    
    #O_efectivos = O * factor_mecha
    
    # EN = (1 / capas) * O_efectivos
    en = factor_escala * (1 / capas) * O_efectivos
    return round(en, 4)

def angulo_palito(atom):
    """
    Predice el ángulo del palito basado en la electronegatividad.
    
    Regla de Uziel:
    - EN alta → ángulo < 60°
    - EN baja → ángulo > 60°
    """
    en = electronegatividad(atom)
    
    if en == 0:
        return 90.0  # Ángulo por defecto para átomos sin enlaces (gases nobles)
    
    # Ángulo inversamente proporcional a EN
    # Normalizamos EN a un rango típico (0.1 a 2.0)
    factor_capa = 1 + (atom['capas'] - 2) * 0.05
    
    en_norm = max(0.1, min(2.0, en))
    
    # θ = 60° * (1 / EN_norm)
    angulo = 60.0 * (1 / (en_norm*factor_capa))
    
    # Limitar a rango razonable (10° a 170°)
    angulo = max(10, min(170, angulo))
    
    return max(10, min(170, angulo))

def geometria_molecular(atom):
    """
    Clasifica la geometría molecular basada en el ángulo del palito.
    """
    angulo = angulo_palito(atom)
    I = atom['palitos_I']
    O = atom['palitos_O']
    
    if I == 0:
        return "Sin enlaces (gas noble)"
    elif angulo < 60:
        return f"Angular / Doblada ({angulo}°) - Alta electronegatividad"
    elif angulo < 90:
        return f"Pirámide / Trigonal ({angulo}°) - Electronegatividad media-alta"
    elif angulo < 120:
        return f"Plana / Trigonal ({angulo}°) - Electronegatividad media"
    else:
        return f"Lineal / Metálica ({angulo}°) - Baja electronegatividad"

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
