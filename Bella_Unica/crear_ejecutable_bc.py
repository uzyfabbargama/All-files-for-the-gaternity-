#!/usr/bin/env python3
import os
import sys
import py_compile
import marshal
import importlib.util

def crear_bytecode(script_py):
    """
    Convierte un script Python a bytecode (.pyc)
    """
    # Compilar a bytecode
    with open(script_py, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Obtener el nombre del módulo
    module_name = os.path.splitext(os.path.basename(script_py))[0]
    
    # Compilar el código
    code_obj = compile(source, script_py, 'exec')
    
    # Crear el header de .pyc (Python 3.7+)
    import time
    magic = importlib.util.MAGIC_NUMBER
    bit_field = 0  # Sin flags especiales
    hash = 0  # Sin hash
    timestamp = int(os.path.getmtime(script_py))
    size = os.path.getsize(script_py)
    
    # Header: magic (4) + bitfield (4) + timestamp (4) + size (4) + hash (8)
    header = magic + bit_field.to_bytes(4, 'little') + \
             timestamp.to_bytes(4, 'little') + size.to_bytes(4, 'little') + \
             hash.to_bytes(8, 'little')
    
    # Serializar el código
    import marshal
    code_bytes = marshal.dumps(code_obj)
    
    # Combinar header + bytecode
    bytecode = header + code_bytes
    
    return bytecode, code_obj

def crear_ejecutable_fusionado(script_py, output_name, usar_bytecode=True):
    """
    Concatena el intérprete python3 con bytecode o código fuente
    """
    intérprete_path = "./python3"
    
    if not os.path.exists(intérprete_path):
        print(f"Error: No se encuentra {intérprete_path}")
        return False
    
    # Leer el intérprete
    with open(intérprete_path, "rb") as f:
        intérprete = f.read()
    
    # Preparar el payload
    if usar_bytecode:
        print("📦 Generando bytecode...")
        payload, code_obj = crear_bytecode(script_py)
        modo = "BYTECODE"
        print(f"   Tamaño bytecode: {len(payload)} bytes")
    else:
        print("📝 Usando código fuente...")
        with open(script_py, "rb") as f:
            payload = f.read()
        modo = "FUENTE"
    
    # Separador de 16 bytes
    SEPARADOR = b"Fontcode_datzone"
    
    # Crear archivo fusionado
    with open(output_name, "wb") as f:
        f.write(intérprete)
        f.write(SEPARADOR)
        f.write(payload)
    
    os.chmod(output_name, 0o755)
    
    print(f"✅ Ejecutable creado: {output_name}")
    print(f"   Modo: {modo}")
    print(f"   Tamaño total: {os.path.getsize(output_name)} bytes")
    print(f"   Separador: '{SEPARADOR.decode()}' en posición {len(intérprete)}")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 crear_ejecutable_bc.py <script_python> [nombre_salida]")
        sys.exit(1)
    
    script_origen = sys.argv[1]
    nombre_salida = sys.argv[2] if len(sys.argv) > 2 else "programa_ejecutable"
    
    crear_ejecutable_fusionado(script_origen, nombre_salida, usar_bytecode=True)
