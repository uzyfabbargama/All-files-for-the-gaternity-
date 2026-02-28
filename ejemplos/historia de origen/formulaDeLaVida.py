def ciclo_vida_entropical(energia_inicial, perdida_base=0.833):
    células = 10
    energia_actual = energia_inicial
    print(f"Energía Inicial: {energia_actual}")
    
    for i in range(células):
        utilizada = energia_actual * (1 - perdida_base)
        residuo_calor = energia_actual * perdida_base
        # La homeostasis: el residuo mantiene el sistema caliente para la siguiente iteración
        print(f"Célula {i+1}: Usa {utilizada:.2f} | Expulsa calor: {residuo_calor:.2f}")
        # La siguiente célula aprovecha la 'presión' del calor residual
        energia_actual = residuo_calor 

ciclo_vida_entropical(100)
