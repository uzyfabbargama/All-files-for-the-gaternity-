import ctypes
import os

# 1. Localizar y cargar la librería (.so)
# Asegúrate de haber compilado con: 
# nasm -f elf64 lib.asm -o lib.o && ld -shared lib.o -o libnumex.so
lib_path = os.path.abspath("./libnumex.so")
numex = ctypes.CDLL(lib_path)

# 2. Configurar los tipos de entrada para execute_numex(rdi, rsi, rdx, rcx, r8)
# rdi=tipo, los demás son los datos que se sumarán en .top o .bottom
numex.execute_numex.argtypes = [
    ctypes.c_uint64, # rdi
    ctypes.c_uint64, # rsi
    ctypes.c_uint64, # rdx
    ctypes.c_uint64, # rcx
    ctypes.c_uint64  # r8
]

def run_double_calculation():
    print("--- Ronda 1: Cargando base en el motor ---")
    # Inyectamos los primeros valores en la parte baja (.bottom)
    numex.execute_numex(0, 100, 200, 300, 400)
    
    print("--- Ronda 2: Sumando sobre la RAM existente ---")
    # Volvemos a llamar. Gracias a start.inc, rax ya no vale 0, vale 100.
    numex.execute_numex(0, 50, 50, 50, 50)

    # Verificamos el resultado final
    resultado_tipo = (ctypes.c_uint64 * 8)
    resultado = resultado_tipo.in_dll(numex, "numex_state")
    
    print("\nEstado Final (Suma persistente):")
    for i, reg in enumerate(resultado):
        print(f"Registro {i:02d}: {hex(reg)}")
def desafio_desborde():
    print("--- Ronda 1: Llevando el Registro 00 al límite ---")
    # 0x8000000000000000 activa exactamente el bit 63
    limite = 0x8000000000000000
    numex.execute_numex(0, limite, 0, 0, 0)
        
    print("--- Ronda 2: Sumando sobre la RAM existente ---")
    # Volvemos a llamar. Gracias a start.inc, rax ya no vale 0, vale 100.
    numex.execute_numex(0, 50, 50, 50, 50)

    # Verificamos el resultado final
    resultado_tipo = (ctypes.c_uint64 * 8)
    resultado = resultado_tipo.in_dll(numex, "numex_state")
    
    print("\nEstado Final (Suma persistente):")
    for i, reg in enumerate(resultado):
        print(f"Registro {i:02d}: {hex(reg)}")
    # En la ejecución, la macro 'num rax, rbx' detectará ese bit
    # Lo transferirá a rbx (Registro 01) y lo limpiará de rax (Registro 00)
if __name__ == "__main__":
    desafio_desborde()
