import os
from collections import Counter

def analizar_universo(file_path):
    if not os.path.exists(file_path):
        print(f"Error: No encontré el archivo {file_path}")
        return

    with open(file_path, "rb") as f:
        datos = f.read()

    total_bytes = len(datos)
    frecuencia = Counter(datos)
    
    print(f"--- Análisis del Eón: {file_path} ---")
    print(f"Total de bytes analizados: {total_bytes}")
    print("-" * 40)

    # Identificar bytes prohibidos (los que NO aparecen en el MB)
    prohibidos = [b for b in range(256) if b not in frecuencia]
    
    # Identificar bytes dominantes (los más comunes)
    comunes = frecuencia.most_common(5)

    print(f"Bytes Prohibidos (0 apariciones): {len(prohibidos)}")
    if prohibidos:
        # Los mostramos en grupos para que no saturen tu terminal
        print(f"Muestra de prohibidos: {prohibidos[:15]}...")
    
    print("\nBytes Dominantes (Los pilares del sistema):")
    for byte, count in comunes:
        porcentaje = (count / total_bytes) * 100
        print(f"Byte 0x{byte:02X} ({byte}): {count} veces ({porcentaje:.2f}%)")

    print("-" * 40)
    # Teoría de la Carne vs Bloques
    zeros = frecuencia.get(0, 0)
    print(f"Presencia de Vacío (0x00): {zeros} bytes")

if __name__ == "__main__":
    # Asegúrate de estar en la carpeta donde está tu universo activo
    analizar_universo("universo.bin")
