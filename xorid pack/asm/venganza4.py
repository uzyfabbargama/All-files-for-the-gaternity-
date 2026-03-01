import ctypes
import time
import json
import pickle
import random

# --- CARGAR MOTOR XIP ---
lib = ctypes.CDLL('./libxip.so')
buffer_size = 1024 * 1024 # 1MB
mente = (ctypes.c_longlong * (buffer_size // 8))()

def xip_parse(data):
    lib._xip_parse(ctypes.c_char_p(data.encode('utf-8')), mente)

# --- GENERADOR DE DATASET ---
N = 1000000
print(f"--- PREPARANDO {N} VARIABLES ---")
dict_base = {f"var_{i}": random.randint(1, 9999) for i in range(N)}

# Formatos
json_data = json.dumps(dict_base)
pickle_data = pickle.dumps(dict_base) # Serialización binaria
xip_data = "".join([f"{k}::{v},," for k, v in dict_base.items()])

print("¡EMPIEZA LA COMPETENCIA!\n")

# 1. JSON
start = time.time()
res_json = json.loads(json_data)
t_json = time.time() - start
print(f"JSON:   {t_json:.5f}seg")

# 2. PICKLE
start = time.time()
res_pickle = pickle.loads(pickle_data)
t_pickle = time.time() - start
print(f"PICKLE: {t_pickle:.5f} seg")

# 3. XIP (BELLA)
start = time.time()
xip_parse(xip_data)
t_xip = time.time() - start
print(f"XIP:    {t_xip:.5f} seg")

print("-" * 30)
print(f"RESULTADO: XIP es {t_pickle/t_xip:.2f}x más rápido que Pickle")
print(f"RESULTADO: XIP es {t_json/t_xip:.2f}x más rápido que JSON")
print(f"BASE: Pickle es {t_json/t_pickle:.2f}x más rápido que JSON")
