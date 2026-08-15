# ============================================
# MODELO DE ÁTOMOS E IONES (VERSIÓN SIMPLE)
# ============================================

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
