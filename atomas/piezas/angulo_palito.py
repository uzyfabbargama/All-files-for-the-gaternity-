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
