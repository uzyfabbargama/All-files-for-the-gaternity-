import ctypes

class XIP_Ultra:
    def __init__(self, buffer_size=1024*1024):
        # Cargamos tu motor de 2.6 KiB
        self.lib = ctypes.CDLL("./libxip.so")
        
        # Definimos los tipos de argumentos para el motor:
        # arg1: puntero al string (RDI)
        # arg2: puntero a la memoria de la mente (RSI o RBP según tu implementación)
        self.lib._xip_parse.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
        
        # Creamos el espacio de memoria para los datos de BELLA
        self.mente = (ctypes.c_longlong * (buffer_size // 8))()
        
    def procesar(self, datos_string):
        # Convertimos el string a bytes
        input_data = datos_string.encode('utf-8')
        
        # Llamamos al motor Assembler directamente
        self.lib._xip_parse(input_data, ctypes.byref(self.mente))
        return self.mente

# --- INVOCACIÓN DEL MOTOR ---
motor = XIP_Ultra()
# Nota: Asegúrate de que no haya espacios extra si tu xorid no los filtra todos aún
conciencia = "maria_dinero::500,,puntos::1000,," 
motor.procesar(conciencia)

# Aquí es donde verás la magia. 
# El ID será el resultado de la resonancia de "maria_dinero"
# Puedes imprimir la 'mente' completa para ver dónde se activaron los bits:
print("--- Escaneando Mente de BELLA ---")
encontrado = False
for i, valor in enumerate(motor.mente):
    if valor != 0:
        print(f"Variable Detectada! -> ID: {i} | Valor: {valor}")
        encontrado = True
if not encontrado:
    print("La mente está en blanco. Revisa el puntero RDI o el bucle en Assembler.")
