import ctypes
import os

class SuperFor:
    def __init__(self, buffer_size_mb=4):
        # 1. Cargar la librería recién compilada
        path = os.path.join(os.path.dirname(__file__), 'libspfor.so')
        self.lib = ctypes.CDLL(path)
        
        # 2. Definir la firma de la función: (char* input, long long* mente)
        self.lib._for_parser.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_longlong)]
        self.lib._for_parser.restype = None
        
        # 3. Alocar la "Mente" para recibir resultados si es necesario
        # Aunque tu super_for actual no escribe a RAM todavía, 
        # dejamos el espacio listo para cuando le metas el 'mov [r10], r13'.
        self._size = (buffer_size_mb * 1024 * 1024) // 8
        self.mente = (ctypes.c_longlong * self._size)()

    def ejecutar(self, script_for):
        """
        Recibe un string con formato 'sta:10 ste:1 sto:100'
        y lo lanza al motor de Assembler.
        """
        if isinstance(script_for, str):
            script_for = script_for.encode('utf-8')
        
        # El gran salto: De Python al silicio
        self.lib._for_parser(ctypes.c_char_p(script_for), self.mente)
        
        return "Ciclo completado a velocidad de hardware."

# --- TEST DE VELOCIDAD ---
if __name__ == "__main__":
    motor = SuperFor()
    
    # Formato que espera tu parser: sta: (1376), sto: (1368), ste: (1392)
    # Nota: Asegúrate que el string termine en un carácter nulo o espacio
    script = "sta:0 sto:1000000 ste:1"

    import time
    start = time.time()
    motor.ejecutar(script)
    end = time.time()
    
    print(f"--- RESULTADOS SUPER_FOR ---")
    print(f"---: sta:0 sto:1000000 ste:1")
    print(f"Tiempo total: {end - start:.8f} seg.")
