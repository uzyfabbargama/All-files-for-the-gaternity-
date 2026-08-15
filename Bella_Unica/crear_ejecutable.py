#!/usr/bin/env python3
import os
import sys

def crear_ejecutable_fusionado(script_py, output_name):
    """
    Concatena el intérprete python3 con un script Python
    usando un marcador de 16 bytes como separador
    """
    
    # 1. Obtener la ruta del intérprete python3
    # Usamos el python3 que está en el directorio actual
    intérprete_path = "./python3"
    
    if not os.path.exists(intérprete_path):
        print(f"Error: No se encuentra {intérprete_path}")
        print("Asegúrate de haber copiado python3 al directorio actual")
        return False
    
    # 2. Leer el intérprete
    with open(intérprete_path, "rb") as f:
        intérprete = f.read()
    
    # 3. Leer el script Python
    if not os.path.exists(script_py):
        print(f"Error: No se encuentra {script_py}")
        return False
    
    with open(script_py, "rb") as f:
        script = f.read()
    
    # 4. El separador (16 bytes exactos)
    SEPARADOR = b"Fontcode_datzone"  # 16 bytes
    
    # 5. Crear el archivo fusionado
    with open(output_name, "wb") as f:
        f.write(intérprete)
        f.write(SEPARADOR)
        f.write(script)
    
    # 6. Hacer ejecutable
    os.chmod(output_name, 0o755)
    
    print(f"✅ Ejecutable creado: {output_name}")
    print(f"   Tamaño total: {os.path.getsize(output_name)} bytes")
    print(f"   Separador: '{SEPARADOR.decode()}' en posición {len(intérprete)}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 crear_ejecutable.py <script_python> [nombre_salida]")
        sys.exit(1)
    
    script_origen = sys.argv[1]
    nombre_salida = sys.argv[2] if len(sys.argv) > 2 else "programa_ejecutable"
    
    crear_ejecutable_fusionado(script_origen, nombre_salida)
