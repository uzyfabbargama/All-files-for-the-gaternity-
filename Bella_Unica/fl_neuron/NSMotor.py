import ctypes
import os

# Cargar la biblioteca compartida .so creada desde el ensamblador
lib_path = os.path.abspath("./libNSMotor.so")
motor = ctypes.CDLL(lib_path)

# Configuración de tipos según la ABI de Linux x86_64
# Las funciones de NeuralScript devuelven o leen directamente en var_space

# Si exportaste etiquetas globales en NASM (global proc_eval, global growth_eval, etc.):
# motor.procesar_neuronas.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
# motor.procesar_neuronas.restype = ctypes.c_uint64

def float_to_custom56(val: float) -> int:
    entero = 1 if val >= 1.0 else 0
    frac = val - entero
    frac_bits = int(frac * (2 ** 55))
    return (entero << 55) | (frac_bits & ((1 << 55) - 1))

def custom56_to_float(val_int: int) -> float:
    entero = (val_int >> 55) & 1
    frac_bits = val_int & ((1 << 55) - 1)
    return entero + (frac_bits / (2 ** 55))

print("--- MOTOR NEURAL SCRIPT VIA CTYPES ---")
print("Biblioteca nativa cargada exitosamente en memoria.")
