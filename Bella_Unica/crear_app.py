#!/usr/bin/env python3
import os
import sys
import marshal
import importlib.util

def crear_app(archivo, salida):
    """
    Crea bella_app - un ejecutable autónomo que se ejecuta con ./bella_app
    """
    
    # 1. Verificar que existe python3 en el directorio actual
    if not os.path.exists("./python3"):
        print("Copiando python3 al directorio actual...")
        os.system("cp /bin/python3 .")
        os.chmod("./python3", 0o755)
    
    # 2. Leer el intérprete
    with open("./python3", "rb") as f:
        interpreter = f.read()
    
    # 3. Leer tu script Bellav3_10low3.py
    if not os.path.exists(archivo):
        print(f"❌ Error: No encuentro {archivo}")
        return False
    
    with open(archivo, "r") as f:
        codigo_fuente = f.read()
    
    # 4. Compilar a bytecode (más rápido y sin comentarios)
    print("📦 Compilando a bytecode...")
    codigo_compilado = compile(codigo_fuente, archivo, "exec")
    bytecode = marshal.dumps(codigo_compilado)
    
    # 5. El separador (16 bytes exactos)
    SEPARADOR = b"Fontcode_datzone"
    
    # 6. Crear bella_app
    print("🔨 Creando bella_app...")
    with open(salida, "wb") as f:
        f.write(interpreter)
        f.write(SEPARADOR)
        f.write(bytecode)
    
    # 7. Hacerlo ejecutable
    os.chmod(salida, 0o755)
    
    print("✅ ¡Listo! bella_app creado")
    print(f"   Tamaño: {os.path.getsize(salida):,} bytes")
    print(f"   Ejecuta con: ./{salida}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 crear_ejecutable_bc.py <script_python> [nombre_salida]")
        sys.exit(1)
    print(f"Argumento 1: {sys.argv[0]}")
    print(f"Argumento 2: {sys.argv[1]}")
    print(f"Argumento 3: {sys.argv[2]}")
    crear_app(sys.argv[1], sys.argv[2])
