import os
import random
import time

# --- CONFIGURACIÓN ESTRUCTURAL ---
N_GLOBALES = 200   # Cuántos agentes holónicos compiten en la ruleta macro
N_INTERNOS = 16   # La "sociedad interna" (neuronas/agentes) de cada nodo global

# 1. Inicialización limpia del ecosistema fractal (Estructuras puras, sin objetos)
agentes_globales = []
for i in range(N_GLOBALES):
    # Cada sub-agente empieza equilibrado con 10 puntos base
    internos = [{"id_interno": j, "puntos": 10} for j in range(N_INTERNOS)]
    
    agentes_globales.append({
        "id": i,
        "puntos_globales": 10,
        "agentes_internos": internos
    })


def calcular_tension_interna(global_node):
    """
    EMERGENCIA (Abajo hacia arriba): Mide el caos del micromundo.
    Calcula el promedio de diferencias absolutas entre vecinos internos.
    """
    internos = global_node["agentes_internos"]
    if len(internos) < 2:
        return 0
    
    suma_diferencias = 0
    for j in range(len(internos)):
        idx_sig = (j + 1) % len(internos)
        suma_diferencias += abs(internos[j]["puntos"] - internos[idx_sig]["puntos"])
        
    return suma_diferencias // len(internos)


def repartir_mitad_hacia_abajo(global_node, cantidad, es_daño=False):
    """
    REPARTICIÓN EN CASCADA BITWISE: Magnifica la cantidad a centipuntos (<< 8)
    y la reparte de forma exponencial por mitades sucesivas (>> 1).
    Provoca desigualdad extrema y dispara la tensión interna.
    """
    internos = global_node["agentes_internos"]
    if not internos:
        return

    # Pasamos la masa entrante a centipuntos en base 256
    centipuntos_restantes = cantidad << 8

    # Repartimos en cascada pura por el orden natural de los agentes (0 a 15)
    for idx in range(len(internos)):
        if centipuntos_restantes <= 0:
            break
            
        # El agente actual se lleva la mitad de lo que queda
        cuota = centipuntos_restantes >> 1
        
        # Si es el último agente, se lleva todo el remanente para no perder bits
        if idx == len(internos) - 1:
            cuota = centipuntos_restantes
            
        centipuntos_restantes -= cuota

        # Aplicamos la cuota al agente interno (en escala de centipuntos)
        if es_daño:
            internos[idx]["puntos"] -= cuota
            if internos[idx]["puntos"] < 0:
                internos[idx]["puntos"] = 0
        else:
            internos[idx]["puntos"] += cuota


def simular_ecosistema():
    paso = 0
    while len(agentes_globales) > 1:
        paso += 1
        
        # --- FASE 1: SELECCIÓN EXTERNA (EL AZAR DEL ENTORNO) ---
        idx_sel = random.randint(0, len(agentes_globales) - 1)
        global_sel = agentes_globales[idx_sel]
        
        # El premio macro se inyecta y altera el micro-orden
        global_sel["puntos_globales"] += 20
        repartir_mitad_hacia_abajo(global_sel, cantidad=20, es_daño=False)
        
        # --- FASE 2: DECISIÓN COGNITIVA (UMBRAL DE TENSIÓN) ---
        idx_defensor = (idx_sel + len(agentes_globales) // 2) % len(agentes_globales)
        global_defensor = agentes_globales[idx_defensor]
        
        pts_atq = global_sel["puntos_globales"]
        daño_potencial = 0
        eliminar_atacante = False
        
        if pts_atq == 0:
            eliminar_atacante = True
        elif pts_atq == 1:
            daño_potencial = 1
            eliminar_atacante = True
        elif pts_atq > 1:
            daño_potencial = pts_atq >> 1

        # Filtro de transurgencia: Solo hay acción externa si la tensión interna supera el daño
        tension = calcular_tension_interna(global_sel)
        ataco = False
        
        if tension > daño_potencial and daño_potencial > 0:
            ataco = True
            global_sel["puntos_globales"] -= daño_potencial
            
            # --- FASE 3: IMPACTO, TRANSMISIÓN Y ABSORCIÓN DE ENERGÍA ---
            global_defensor["puntos_globales"] -= daño_potencial
            repartir_mitad_hacia_abajo(global_defensor, cantidad=daño_potencial, es_daño=True)
            
            # Manejo de la deuda energética (Absorción biológica de los vecinos)
            if global_defensor["puntos_globales"] < 0:
                exceso = abs(global_defensor["puntos_globales"])
                global_defensor["puntos_globales"] = 0
                
                mitad_der = exceso >> 1
                mitad_izq = exceso - mitad_der
                
                idx_izq = (idx_defensor - 1) % len(agentes_globales)
                idx_der = (idx_defensor + 1) % len(agentes_globales)
                
                if len(agentes_globales) > 1:
                    agentes_globales[idx_der]["puntos_globales"] += mitad_der
                    repartir_mitad_hacia_abajo(agentes_globales[idx_der], mitad_der, es_daño=False)
                    
                    agentes_globales[idx_izq]["puntos_globales"] += mitad_izq
                    repartir_mitad_hacia_abajo(agentes_globales[idx_izq], mitad_izq, es_daño=False)
                
                agentes_globales.pop(idx_defensor)
                if idx_sel > idx_defensor: 
                    idx_sel -= 1
            
            elif global_defensor["puntos_globales"] == 0:
                agentes_globales.pop(idx_defensor)
                if idx_sel > idx_defensor: 
                    idx_sel -= 1

        if eliminar_atacante and idx_sel < len(agentes_globales):
            agentes_globales.pop(idx_sel)

        # --- FASE 4: RENDERIZADO DE LA CONSOLA ---
        os.system("clear")
        print(f"=== MOTOR TRANSURGENTE MULTICAPA | PASO {paso} ===")
        print(f"Seleccionado: Agente {global_sel['id']} (Tensión interna: {tension})")
        if ataco:
            print(f"¡FUEGO! Agente {global_sel['id']} drena {daño_potencial} pts al Agente {global_defensor['id']}\n")
        else:
            print(f"Bloqueado: Tensión interna menor que el daño ({daño_potencial}). El Holón se contiene.\n")
            
        for g in agentes_globales:
            barra_macro = "█" * (g["puntos_globales"] // 2) if g["puntos_globales"] > 0 else ""
            print(f"Agente Global {g['id']:02d} ({g['puntos_globales']:03d} pts) {barra_macro}")
            
            # Sub-trama de la sociedad de agentes internos (primeros 8 para scannear rápido)
            internos_str = " ".join([f"{i['puntos']}" for i in g["agentes_internos"][:8]])
            print(f"  └─ Internos (sub-red 1-8): [{internos_str}]")
            
        print("\nCtrl+C para detener la evolución.")
        time.sleep(0.8)

    print(f"\n¡Homeostasis alcanzada! El holón superviviente es el Agente {agentes_globales[0]['id']}.")


if __name__ == "__main__":
    try:
        simular_ecosistema()
    except KeyboardInterrupt:
        print("\nEvolución pausada por el usuario.")
