import ctypes
import os

class NumExt:
    def __init__(self, max_numeros=100000):
        # Cargamos tu nueva criatura
        path = os.path.join(os.path.dirname(__file__), 'libnum.so')
        self.lib = ctypes.CDLL(path)
        
        # Alocamos espacio: 2 QWORDS (16 bytes) por cada número .nmxt
        # Estructura: [Entero][Decimal][Entero][Decimal]...
        self.capacidad = max_numeros
        self.mente = (ctypes.c_uint64 * (max_numeros * 2))()

    def procesar_archivo(self, contenido_texto):
        """Envía el texto al motor ASM para extraer todos los números."""
        if isinstance(contenido_texto, str):
            contenido_texto = contenido_texto.encode('utf-8')
        
        # Llamamos a tu parser de NASM
        # RDI = texto, RSI = puntero a nuestra memoria
        self.lib._nmxt_parser(ctypes.c_char_p(contenido_texto), self.mente)

    def obtener_numero(self, indice):
        """Recupera el par (entero, decimal) de la memoria."""
        if indice >= self.capacidad:
            return None
        entero = self.mente[indice * 2]
        decimal = self.mente[indice * 2 + 1]
        return entero, decimal

# --- Ejemplo de uso ---
motor = NumExt()
datos = "int: 2 frac: 2 sep 13 ,, int: 10 frac: 5 sep 1024 ,,"
motor.procesar_archivo(datos)

# Recuperamos el primer número que procesamos
e, d = motor.obtener_numero(0)
print(f"Número 1 -> Entero: {e}, Decimal (bits): {d}")
