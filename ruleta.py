import os
import random
import time

# Configuración inicial
N_AGENTES = 20
# Cada agente empieza como un diccionario con su ID y sus puntos
agentes = [{"id": i, "puntos": 10} for i in range(N_AGENTES)]


def mostrar_consola(paso, seleccionado_id, atacante_id, defensor_id):
    os.system("clear")
    print(f"=== SIMULACIÓN DE RULETA CAÓTICA | PASO {paso} ===")
    print(
        f"Seleccionado: Agente {seleccionado_id} (+20) | Atacante: Agente {atacante_id} -> Ataca a: Agente {defensor_id}\n"
    )

    # Renderizado visual simple
    for a in agentes:
        barra = "█" * (a["puntos"] // 2) if a["puntos"] > 0 else ""
        marcador = ""
        if a["id"] == seleccionado_id:
            marcador += " [SELECCIONADO]"
        if a["id"] == atacante_id:
            marcador += " [ATACANTE]"
        if a["id"] == defensor_id:
            marcador += " [RECIBE DAÑO]"

        print(f"Agente {a['id']:02d} ({a['puntos']:03d} pts): {barra}{marcador}")
    print("\nPresioná Ctrl+C para salir.")


paso = 0
while len(agentes) > 1:
    paso += 1

    # 1. Girar ruleta y elegir al azar el "ÍNDICE" actual
    idx_sel = random.randint(0, len(agentes) - 1)
    agente_sel = agentes[idx_sel]

    # Aplicar el bono de selección
    agente_sel["puntos"] += 20

    # 2. Identificar atacante (el seleccionado) y su opuesto (defensor)
    # En una ruleta dinámica, el opuesto es avanzar la mitad del tamaño actual
    idx_defensor = (idx_sel + len(agentes) // 2) % len(agentes)

    # Guardamos IDs para el reporte visual antes de que muten las posiciones
    id_sel = agente_sel["id"]
    id_defensor = agentes[idx_defensor]["id"]

    # 3. Lógica de ataque (Basada en los puntos del ATACANTE)
    daño = 0
    eliminar_atacante = False

    puntos_atq = agente_sel["puntos"]

    if puntos_atq == 0:
        eliminar_atacante = True
    elif puntos_atq == 1:
        daño = 1
        eliminar_atacante = True
    elif puntos_atq > 1:
        daño = puntos_atq >> 1
        agente_sel["puntos"] -= puntos_atq >> 1

    # Ejecutar eliminación del atacante si corresponde
    if eliminar_atacante:
        agentes.pop(idx_sel)
        # Reajustar el índice del defensor si la eliminación alteró su posición
        if idx_sel < idx_defensor:
            idx_defensor -= 1

    # 4. Aplicar daño al DEFENSOR (si sigue vivo y la lista no quedó vacía)
    if len(agentes) > 0 and idx_defensor < len(agentes):
        defensor = agentes[idx_defensor]
        defensor["puntos"] -= daño

        # Manejo de daño excedente (puntos menores a 0)
        if defensor["puntos"] < 0:
            exceso = abs(defensor["puntos"])
            defensor["puntos"] = 0  # Se limpia antes de morir/repartir

            # Calcular mitades para vecinos (atendiendo impares)
            mitad_derecha = exceso >> 1
            mitad_izquierda = exceso - mitad_derecha

            # Al usar % len(agentes), la ruleta es perfectamente circular
            idx_izq = (idx_defensor - 1) % len(agentes)
            idx_der = (idx_defensor + 1) % len(agentes)

            # Si hay suficientes agentes, repartir el exceso
            if len(agentes) > 1:
                agentes[idx_der]["puntos"] += mitad_derecha
                agentes[idx_izq]["puntos"] += mitad_izquierda

            # El defensor muere por el daño masivo
            agentes.pop(idx_defensor)
        elif defensor["puntos"] == 0:
            # Muere de forma limpia
            agentes.pop(idx_defensor)

    # Mostrar estado en consola
    mostrar_consola(paso, id_sel, id_sel, id_defensor)
    time.sleep(0.8)  # Pausa para poder seguir el flujo del juego

print(f"\n¡Simulación terminada! El ganador es el Agente {agentes[0]['id']}.")
