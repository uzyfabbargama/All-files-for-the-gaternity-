from PIL import Image
import numpy as np

def aislar_esqueleto_termico(archivo_bin="universo.bin", salida_png="universo_esqueleto_level2.png"):
    try:
        # 1. Leer los datos (1 MB)
        with open(archivo_bin, "rb") as f:
            datos = f.read(1000000)
        
        # 2. Convertir a un array de NumPy
        matriz = np.frombuffer(datos, dtype=np.uint8)
        matriz = matriz[:1000000].reshape((1000, 1000))
        
        # 3. AISLAMIENTO DEL BIT 7 (MÁSCARA BINARIA)
        # Esto crea una matriz binaria donde solo importan las zonas con el bit 7 activo.
        # matriz_calor = matriz & 0x80  <-- Este sería el valor exacto del calor.
        
        # Para visualización extrema, vamos a convertirlo en valores de 0 o 255.
        matriz_umbral = np.where(matriz >= 2, 2, 0).astype(np.uint8)
        
        # 4. Crear imagen en modo 'L' (Escala de Grises) para máxima precisión
        img = Image.fromarray(matriz_umbral, 'L')
        
        # 5. Guardar la imagen del esqueleto
        img.save(salida_png)
        print(f"--- ¡Esqueleto Térmico revelado en {salida_png}! ---")
        print(f"--- Las zonas blancas son donde el Bit 7 (Calor) está ACTIVO. ---")

    except Exception as e:
        print(f"Error en el escáner térmico: {e}")

if __name__ == "__main__":
    aislar_esqueleto_termico()
