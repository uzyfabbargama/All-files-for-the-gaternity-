from PIL import Image

def transformar_universo(archivo_bin, salida_img):
    with open(archivo_bin, 'rb') as f:
        # Leemos el bloque necesario para 333x333 pixeles RGB
        # 333 * 333 * 3 = 998,001 bytes
        ancho, alto = 333, 333
        bytes_necesarios = ancho * alto * 3
        
        datos = f.read(bytes_necesarios)
    
    if len(datos) < bytes_necesarios:
        print(f"Aviso: El archivo solo tiene {len(datos)} bytes. Faltan datos.")
        return

    # Creamos la imagen en modo RGB (8 bits por canal, 24 bits total)
    img = Image.frombytes('RGB', (ancho, alto), datos)
    
    # Guardamos en un formato sin pérdida para no alterar el binario
    img.save(salida_img)
    print(f"Transurgencia completada: {salida_img} generada (333x333).")

# Ejecución
transformar_universo('universo.bin', 'universo_visual.png')
