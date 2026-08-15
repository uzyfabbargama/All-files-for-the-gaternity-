import ctypes
import os

# 1. Localizar y cargar la librería (.so)
# Asegúrate de haber compilado con: 
# nasm -f elf64 lib.asm -o lib.o && ld -shared lib.o -o libnumex.so
lib_path = os.path.abspath("./libnumex.so")
numex = ctypes.CDLL(lib_path)

# 2. Configurar los tipos de entrada para execute_numex(rdi, rsi, rdx, rcx, r8) [cite: 4, 5]
# rdi=tipo, los demás son los datos que se sumarán en .top o .bottom
numex.execute_numex.argtypes = [
    ctypes.c_uint64, # rdi
    ctypes.c_uint64, # rsi
    ctypes.c_uint64, # rdx
    ctypes.c_uint64, # rcx
    ctypes.c_uint64  # r8
]

def run_numex():
    print("--- Iniciando motor Numex (567 bits) ---")
    
    # 3. Definir la semilla de datos (Transurgencia en acción) [cite: 4]
    tipo = 0  # 0 para .top, 1 para .bottom (según tu lógica de jnz/jz)
    val1, val2, val3, val4 = 100, 200, 300, 400
    
    # 4. Llamada directa al silicio
    # Esto activará start.inc, data.inc y finalmente la cadena num.inc [cite: 3, 6]
    numex.execute_numex(tipo, val1, val2, val3, val4)
    
    print("Ciclo branchless completado con éxito.")

    # 5. Acceder a la memoria compartida 'numex_state'
    # 'in_dll' busca el símbolo exacto que definiste en la sección .data de lib.asm 
    # Creamos un array de 8 elementos de 64 bits (los 8 registros volcados)
    resultado_tipo = (ctypes.c_uint64 * 8)
    resultado = resultado_tipo.in_dll(numex, "numex_state")

    print("\nEstado de la realidad Numex (Registros de 64 bits):")
    print("-" * 45)
    for i, reg in enumerate(resultado):
        # Verás que el bit 63 (max) está encendido si todo salió bien [cite: 2]
        print(f"Registro {i:02d}: {hex(reg)}")
    print("-" * 45)

if __name__ == "__main__":
    run_numex()
