import numpy as np
from PIL import Image

def crear_microscopio(archivo_bin="universo.bin", salida_png="microscopio_bits.png", tam_muestra=100):
    try:
        # 1. Leer datos
        with open(archivo_bin, "rb") as f:
            datos = np.frombuffer(f.read(), dtype=np.uint8)
        
        # Tomamos una muestra de la parte superior (donde están los filtros y muros)
        # 100x100 celdas del universo real
        muestra = datos[:tam_muestra*1000].reshape((tam_muestra, 1000))[:, :tam_muestra]
        
        # 2. Configurar la imagen de salida (Cada celda es 8x8 píxeles reales)
        img_final = Image.new('RGB', (tam_muestra * 8, tam_muestra * 8))
        pixels = img_final.load()

        for y in range(tam_muestra):
            for x in range(tam_muestra):
                byte_val = muestra[y, x]
                
                # --- Definir Color de Fondo (Tu paleta de Transurgencia) ---
                if byte_val < 64:
                    bg_color = (0, 0, 150)       # Azul (Frío)
                elif byte_val < 128:
                    bg_color = (0, 150, 0)       # Verde (Vida/Flujo)
                elif byte_val < 192:
                    bg_color = (200, 0, 0)       # Rojo (Calor)
                else:
                    bg_color = (200, 0, 200)     # Magenta (Saturación/F7)

                # --- Dibujar bloque de 8x8 ---
                for j in range(8):
                    for i in range(8):
                        # La fila central (j=4) mostrará los 8 bits
                        if j == 4:
                            # Extraer el bit correspondiente (del 7 al 0)
                            bit = (byte_val >> (7 - i)) & 1
                            color_bit = (255, 255, 255) if bit else (0, 0, 0)
                            pixels[x*8 + i, y*8 + j] = color_bit
                        else:
                            # Resto del bloque es el color de fondo
                            pixels[x*8 + i, y*8 + j] = bg_color

        img_final.save(salida_png)
        print(f"--- Microscopio listo: {salida_png} ---")

    except Exception as e:
        print(f"Error en el laboratorio: {e}")
def crear_microscopio_total(archivo_bin="universo.bin", salida_png="gran_microscopio.png"):
    try:
        # 1. Leer el millón de bytes completo
        with open(archivo_bin, "rb") as f:
            # Cargamos el binario y lo reformateamos a una matriz de 1000x1000
            datos = np.frombuffer(f.read(), dtype=np.uint8)
            muestra = datos.reshape((1000, 1000))
        
        tam_universo = 1000
        # 2. Configurar imagen de salida: 1000 celdas * 8 píxeles = 8000 px
        img_final = Image.new('RGB', (tam_universo * 8, tam_universo * 8))
        pixels = img_final.load()

        print(f"Iniciando renderizado del Gran Microscopio (8000x8000)...")

        for y in range(tam_universo):
            for x in range(tam_universo):
                byte_val = muestra[y, x]
                
                # --- Definir Color de Fondo (Tu paleta de Transurgencia) ---
                if byte_val < 64:
                    bg_color = (0, 0, 150)       # Azul (Frío)
                elif byte_val < 128:
                    bg_color = (0, 150, 0)       # Verde (Vida/Flujo)
                elif byte_val < 192:
                    bg_color = (200, 0, 0)       # Rojo (Calor)
                else:
                    bg_color = (200, 0, 200)     # Magenta (Saturación/F7)

                # --- Dibujar bloque de 8x8 por cada byte ---
                for j in range(8):
                    for i in range(8):
                        # La fila central (j=4) muestra los 8 bits individuales
                        if j == 4:
                            bit = (byte_val >> (7 - i)) & 1
                            color_bit = (255, 255, 255) if bit else (0, 0, 0)
                            pixels[x*8 + i, y*8 + j] = color_bit
                        else:
                            pixels[x*8 + i, y*8 + j] = bg_color

        # 3. Guardar el titán de 80MB aprox.
        img_final.save(salida_png)
        print(f"--- Microscopio Total listo: {salida_png} ---")

    except Exception as e:
        print(f"Error en el laboratorio: {e}")
    
if __name__ == "__main__":
    #crear_microscopio()
	crear_microscopio_total()
