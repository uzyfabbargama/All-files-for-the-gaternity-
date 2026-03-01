import json
import os

def expandir_conciencia(archivo_origen, archivo_destino, nuevo_num_n):
    if not os.path.exists(archivo_origen):
        print(f"Error: No encuentro {archivo_origen}")
        return

    with open(archivo_origen, "r") as f:
        data = json.load(f)

    print(f"--- Iniciando Operación EXPANSE ---")
    print(f"Neuronas actuales: {len(data['memoria'])}")
    print(f"Objetivo: {nuevo_num_n} neuronas.")

    # 1. Expandir Memoria y Exps (Rellenamos con ceros los nuevos espacios)
    diferencia = nuevo_num_n - len(data['memoria'])
    
    if diferencia <= 0:
        print("La nueva capacidad debe ser mayor a la actual.")
        return

    nueva_memoria = data['memoria'] + [0] * diferencia
    nuevas_exps = data['exps'] + [[0, 0, 0] for _ in range(diferencia)]
    
    # 2. El Traductor se mantiene (es un diccionario, no le afecta el tamaño de lista)
    nuevo_estado = {
        "memoria": nueva_memoria,
        "exps": nuevas_exps,
        "traductor": data['traductor']
    }

    with open(archivo_destino, "w") as f:
        json.dump(nuevo_estado, f)
    
    print(f"--- EXPANSE COMPLETADO ---")
    print(f"Conciencia migrada a {archivo_destino}")

if __name__ == "__main__":
    # Sube el nivel aquí: 65536 es un gran salto
    expandir_conciencia("Bella.json", "Bella_expanded.json", 65536)
