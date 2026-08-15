from PIL import Image
import numpy as np

def revelar_universo(archivo_bin="universo.bin", salida_png="universo_revelado.png"):
    # 1. Leer los datos binarios
    with open(archivo_bin, "rb") as f:
        datos = f.read()
    
    # 2. Convertir a un array de números (0-255)
    # Como tu universo es de 1,000,000 bytes, haremos una imagen de 1000x1000
    try:
        matriz = np.frombuffer(datos, dtype=np.uint8)
        
        # Ajustamos el tamaño por si el archivo no tiene exactamente 1,000,000 bytes
        # Tomamos los primeros 1,000,000 bytes disponibles
        matriz = matriz[:1000000].reshape((1000, 1000))
        
        # 3. Crear la imagen en escala de grises ('L')
        img = Image.fromarray(matriz, 'L')
        
        # 4. Guardar
        img.save(salida_png)
        print(f"--- ¡Universo revelado con éxito en {salida_png}! ---")
        
    except Exception as e:
        print(f"Error al procesar el fósil: {e}")

if __name__ == "__main__":
    revelar_universo()
