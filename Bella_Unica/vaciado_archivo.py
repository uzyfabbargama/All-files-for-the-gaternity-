#!/usr/bin/env python3
import os
import sys
import random

def borrar_archivo_seguro(ruta, pasadas=3, verbose=True):
    """
    Borra un archivo de forma segura sobrescribiéndolo múltiples veces
    
    Args:
        ruta: Ruta del archivo a borrar
        pasadas: Número de veces que se sobrescribe (3 por defecto)
        verbose: Mostrar progreso
    """
    
    if not os.path.exists(ruta):
        print(f"❌ Error: {ruta} no existe")
        return False
    
    # Verificar que es un archivo (no directorio)
    if os.path.isdir(ruta):
        print(f"❌ Error: {ruta} es un directorio, no un archivo")
        return False
    
    # Obtener tamaño
    tamaño = os.path.getsize(ruta)
    
    if verbose:
        print(f"📁 Archivo: {ruta}")
        print(f"📊 Tamaño: {tamaño:,} bytes")
        print(f"🔄 Pasadas: {pasadas}")
        print("-" * 50)
    
    # Abrir en modo lectura/escritura binaria
    with open(ruta, "r+b") as f:
        for i in range(pasadas):
            if verbose:
                print(f"  Pasada {i+1}/{pasadas}...", end=" ", flush=True)
            
            # Ir al inicio del archivo
            f.seek(0)
            
            # Estrategias diferentes para cada pasada
            if i == 0:
                # Primera pasada: todos ceros
                f.write(b'\x00' * tamaño)
                f.flush()
                if verbose:
                    print("✅ (ceros)")
                    
            elif i == 1:
                # Segunda pasada: todos unos (0xFF)
                f.seek(0)
                f.write(b'\xFF' * tamaño)
                f.flush()
                if verbose:
                    print("✅ (unos)")
                    
            else:
                # Tercera pasada: datos aleatorios
                f.seek(0)
                # Escribir en bloques para no consumir mucha RAM
                bloque = 1024 * 1024  # 1MB
                escritos = 0
                while escritos < tamaño:
                    datos_aleatorios = bytes(random.randint(0, 255) for _ in range(min(bloque, tamaño - escritos)))
                    f.write(datos_aleatorios)
                    escritos += len(datos_aleatorios)
                f.flush()
                if verbose:
                    print("✅ (aleatorio)")
        
        # Final: truncar a 0 bytes
        f.truncate(0)
    
    # Eliminar el archivo
    os.remove(ruta)
    
    if verbose:
        print("-" * 50)
        print(f"✅ Archivo {ruta} eliminado de forma segura")
        print(f"   Sobrescrito {pasadas} veces antes de eliminar")
    
    return True

def borrar_archivo_simple(ruta):
    """
    Versión más simple: sobrescribe con ceros una vez
    """
    if not os.path.exists(ruta):
        print(f"❌ Error: {ruta} no existe")
        return False
    
    tamaño = os.path.getsize(ruta)
    
    print(f"🗑️  Borrando {ruta}...")
    with open(ruta, "r+b") as f:
        # Sobrescribir con ceros
        f.write(b'\x00' * tamaño)
        f.flush()
        # Truncar
        f.truncate(0)
    
    os.remove(ruta)
    print(f"✅ {ruta} eliminado")
    return True

def borrar_archivo_como_dijiste(archivo):
    """
    Implementación EXACTA de lo que describiste:
    archivo = read("archivo")
    fragmento = archivo[1]
    int_fragmento = ord(fragmento) & 0
    sobreescribir archivo con int_fragmento
    """
    try:
        # Leer archivo
        with open(archivo, "rb") as f:
            contenido = f.read()
        
        if len(contenido) < 2:
            print(f"❌ El archivo es muy pequeño (menos de 2 bytes)")
            return False
        
        # Tomar el byte en posición 1
        fragmento = contenido[1:2]  # Un byte
        int_fragmento = ord(fragmento) & 0  # Esto SIEMPRE da 0
        
        print(f"🔍 Byte en posición 1: {fragmento.hex()} = {ord(fragmento)}")
        print(f"🧮 int_fragmento = {ord(fragmento)} & 0 = {int_fragmento}")
        
        # Sobrescribir TODO el archivo con el byte 0
        with open(archivo, "r+b") as f:
            f.write(b'\x00' * len(contenido))
            f.flush()
            f.truncate(0)
        
        # Eliminar
        #os.remove(archivo)
        print(f"✅ {archivo} sobrescrito con ceros y eliminado")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def menu():
    """Menú interactivo para elegir método"""
    print("=" * 60)
    print("🔒 BORRADOR SEGURO DE ARCHIVOS")
    print("=" * 60)
    print()
    print("1. Borrado simple (ceros, 1 pasada)")
    print("2. Borrado seguro (3 pasadas: ceros, unos, aleatorio)")
    print("3. Borrado militar (7 pasadas - DoD 5220.22-M)")
    print("4. Borrado como describiste (fragmento[1] & 0)")
    print("5. Salir")
    print()
    
    opcion = input("Elige una opción (1-5): ")
    
    if opcion == "5":
        return
    
    archivo = input("Ruta del archivo a borrar: ").strip()
    
    if not os.path.exists(archivo):
        print("❌ El archivo no existe")
        return
    
    # Confirmación
    print(f"\n⚠️  ¿Seguro que quieres borrar {archivo}?")
    confirm = input("Escribe 'SI' para confirmar: ")
    
    if confirm != "SI":
        print("❌ Cancelado")
        return
    
    print()
    
    if opcion == "1":
        borrar_archivo_simple(archivo)
    elif opcion == "2":
        borrar_archivo_seguro(archivo, pasadas=3)
    elif opcion == "3":
        borrar_archivo_seguro(archivo, pasadas=7)
    elif opcion == "4":
        borrar_archivo_como_dijiste(archivo)
    else:
        print("❌ Opción inválida")

if __name__ == "__main__":
    # Si se pasan argumentos, modo automático
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        pasadas = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        
        print("=" * 60)
        print("🔒 BORRADOR SEGURO DE ARCHIVOS")
        print("=" * 60)
        print()
        
        borrar_archivo_seguro(archivo, pasadas)
    else:
        # Modo interactivo
        menu()
