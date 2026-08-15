import numpy as np

def contar_bits_universo(archivo_bin="universo.bin"):
    try:
        with open(archivo_bin, "rb") as f:
            datos = f.read()
        
        # Convertimos a un array de bytes
        arreglo_bytes = np.frombuffer(datos, dtype=np.uint8)
        
        # Contamos los bits encendidos (1s) usando una operación vectorizada
        # unpackbits convierte cada byte en 8 elementos de un array (0 o 1)
        bits = np.unpackbits(arreglo_bytes)
        total_unos = np.sum(bits)
        total_posibles = len(bits)
        
        # Cálculo de densidad (porcentaje de "calor" en el sistema)
        densidad = (total_unos / total_posibles) * 100
        
        print(f"--- Análisis del Eón ---")
        print(f"Bits Totales en el Contenedor: {total_posibles}")
        print(f"Bits Encendidos (Energía Activa): {total_unos}")
        print(f"Densidad Energética: {densidad:.4f}%")
        
        return total_unos

    except Exception as e:
        print(f"Error al leer la esencia: {e}")

if __name__ == "__main__":
    contar_bits_universo()
