from PIL import Image
import numpy as np

def revelar_universo_color(archivo_bin="universo.bin", salida_png="universo_color.png"):
    try:
        # 1. Leer los datos (1 MB)
        with open(archivo_bin, "rb") as f:
            datos = f.read(1000000)
        
        matriz = np.frombuffer(datos, dtype=np.uint8)
        matriz = matriz[:1000000].reshape((1000, 1000))
        
        # 2. Crear imagen en modo 'P' (Paleta de 8 bits)
        img = Image.fromarray(matriz, 'P')
        
        # 3. Crear una paleta personalizada
        # Vamos a generar un degradado que vaya de:
        # Negro (0) -> Azul (Frío) -> Verde (Vida) -> Rojo (Calor/XOR) -> Blanco (Explosión)
        paleta = []
        for i in range(256):
            if i < 64: # Frío (Azules)
                paleta.extend([0, 0, i * 4])
            elif i < 128: # Transurgencia (Verdes/Cian)
                paleta.extend([0, (i-64) * 4, 255 - (i-64) * 4])
            elif i < 192: # Energía Alta (Amarillos/Rojos)
                paleta.extend([(i-128) * 4, 255 - (i-128) * 4, 0])
            else: # Punto Crítico / Bit 9 (Blancos/Magenta)
                paleta.extend([255, (i-192) * 4, 255])
        
        img.putpalette(paleta)
        
        # 4. Guardar
        img.save(salida_png)
        print(f"--- ¡Universo cromático revelado en {salida_png}! ---")

    except Exception as e:
        print(f"Error en la cámara transurgente: {e}")

if __name__ == "__main__":
    revelar_universo_color()
