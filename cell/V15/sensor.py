def analizar_universo(file_path):
    try:
        with open(file_path, 'rb') as f:
            # Leemos todo el binario del "universo"
            datos = f.read()
        
        # Creamos el set de bytes presentes
        bytes_presentes = set(datos)
        
        # El rango completo de un byte: 0 a 255
        rango_completo = set(range(256))
        
        # Encontramos los que faltan (Diferencia de conjuntos)
        bytes_faltantes = sorted(list(rango_completo - bytes_presentes))
        
        print(f"--- Análisis de: {file_path} ---")
        print(f"Total de bytes leídos: {len(datos)}")
        print(f"Total de valores únicos encontrados: {len(bytes_presentes)}")
        print(f"Cantidad de valores inexistentes: {len(bytes_faltantes)}")
        print("-" * 30)
        
        if not bytes_faltantes:
            print("Increíble: Es ruido blanco puro. No falta ningún byte.")
        else:
            print("Los bytes que NO existen son:")
            for b in bytes_faltantes:
                # Mostramos en Decimal y Hexadecimal para tu modo Assembler
                print(f"Dec: {b:3} | Hex: 0x{b:02X}")
                
    except FileNotFoundError:
        print("Error: No encontré el archivo 'universo.bin'.")

if __name__ == "__main__":
    analizar_universo('universo.bin')
