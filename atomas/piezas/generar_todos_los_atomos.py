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

