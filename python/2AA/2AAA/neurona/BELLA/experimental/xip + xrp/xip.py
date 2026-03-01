import ctypes
import os

class XIP:
    def __init__(self, buffer_size_mb=1):
        # Cargar la librería desde el mismo directorio
        path = os.path.join(os.path.dirname(__file__), 'libxip.so')
        self.lib = ctypes.CDLL(path)
        
        # Alocar la "Mente" (8 bytes por posición = qword)
        # 1MB / 8 = 131072 posiciones
        self._size = (buffer_size_mb * 1024 * 1024) // 8
        self.mente = (ctypes.c_longlong * self._size)()
    def generar_id(self, nombre):
        """Calcula el ID XORID exactamente igual que el motor ASM."""
        r14 = 0
        for char in nombre:
            # Replicamos la lógica: xor r11b, [rdi+rsi] -> shl r11, 1 -> and r11, 0x1FFFF
            r11 = r14
            r11 ^= ord(char)
            r11 <<= 1
            r14 = r11 & 0x1FFFF
        return r14
    def inyectar(self, data_string):
        """Procesa el string y llena la memoria interna."""
        if isinstance(data_string, str):
            data_string = data_string.encode('utf-8')
        
        # Llamada al motor BELLA en Assembler
        self.lib._xip_parse(ctypes.c_char_p(data_string), self.mente)
    def guardar_mente(self, filename="bella.xip"):
        """Vuelca el buffer de 1MB directo al disco."""
        with open(filename, "wb") as f:
            f.write(self.mente)
            
    def cargar_mente(self, filename="bella.xip"):
        """Succiona el archivo de disco directo a la RAM."""
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                f.readinto(self.mente)
            return True
        return False
    def obtener(self, key_id):
        """Recupera un valor usando su ID (el resultado del XORID)."""
        # Aquí aplicamos la misma máscara que en el ASM para seguridad
        idx = key_id & 0x1FFFF 
        return self.mente[idx]

    # Y mejoramos el getitem para que acepte el nombre directamente
    def __getitem__(self, key):
        if isinstance(key, str):
            key = self.generar_id(key)
        return self.obtener(key)
