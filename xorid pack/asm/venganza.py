import ctypes
import time
import json
import random
import string

# --- CONFIGURACIÓN DEL MOTOR ---
class XIP_Motor:
    def __init__(self, buffer_size=1024*1024): # 1MB de "mente"
        self.lib = ctypes.CDLL('./libxip.so')
        self.mente = (ctypes.c_longlong * (buffer_size // 8))()
        
    def parse(self, data):
        # rdi = string, rsi = puntero a mente
        self.lib._xip_parse(ctypes.c_char_p(data.encode('utf-8')), self.mente)

# --- GENERADOR DE DATASET ---
def generar_dataset(n=100000):
    variables = {}
    raw_xip = ""
    for i in range(n):
        key = f"var_{i}"
        val = random.randint(1, 9999)
        variables[key] = val
        raw_xip += f"{key}::{val},,"
    
    json_data = json.dumps(variables)
    return json_data, raw_xip

# --- COMPETENCIA ---
N = 100000
print(f"--- GENERANDO {N} VARIABLES ---")
json_str, xip_str = generar_dataset(N)

# T1: JSON
start = time.time()
data_json = json.loads(json_str)
end_json = time.time() - start
print(f"JSON finalizado en: {end_json:.5f} segundos")

# T2: XIP (BELLA)
motor = XIP_Motor()
start = time.time()
motor.parse(xip_str)
end_xip = time.time() - start
print(f"XIP finalizado en:  {end_xip:.5f} segundos")

# RESULTADO
ventaja = end_json / end_xip
print(f"\nRESULTADO: ¡XIP es {ventaja:.2f} veces más rápido que JSON!")
