# Tu "lenguaje estructurado" traducido a Python real
"""
Estructura de datos en bytearray:

[0x1000000] = 16,777,216 bytes (16 MB) para el mundo
[0x32500]   = 205,312 bytes para el índice de objetos
"""

class MotorMundo:
    def __init__(self):
        # Memoria del mundo (16 MB)
        self.mundo = bytearray(0x1000000)  # 16,777,216 bytes
        # Índice de objetos (0x32500 = 205,312 bytes)
        self.indice = bytearray(0x32500)
        
        # Punteros
        self.byte_actual = 0  # Dónde estamos escribiendo
        self.objetos_registrados = 0
        
        # Metadatos (estado del jugador en memoria)
        self.vida = 100
        self.hambre = 100
        self.sed = 100
        self.baño = 100
    
    def crear_seccion(self, nombre):
        """Crea una nueva sección en el mundo"""
        inicio = self.byte_actual
        
        # Escribir el nombre de la sección
        for i, char in enumerate(nombre):
            self.mundo[self.byte_actual + i] = ord(char)
        self.byte_actual += len(nombre)
        
        # Agregar separador (2 bytes de 0)
        self.mundo[self.byte_actual] = 0
        self.mundo[self.byte_actual + 1] = 0
        self.byte_actual += 2
        
        # Registrar en el índice
        total_bytes = self.byte_actual - inicio
        self._registrar_en_indice(total_bytes)
        
        print(f"📍 Sección '{nombre}' creada en byte {inicio} (tamaño: {total_bytes})")
        return inicio
    
    def agregar_objeto(self, nombre):
        """Agrega un objeto a la sección actual"""
        # Escribir el objeto
        for i, char in enumerate(nombre):
            self.mundo[self.byte_actual + i] = ord(char)
        self.byte_actual += len(nombre)
        
        # Separador de 1 byte
        self.mundo[self.byte_actual] = 0
        self.byte_actual += 1
        
        # Registrar
        self._registrar_en_indice(1)  # Solo el separador
        
        print(f"📦 Objeto '{nombre}' agregado en byte {self.byte_actual - len(nombre) - 1}")
    
    def crear_linker(self, id_seccion):
        """Crea un enlace a otra sección"""
        # Escribir el ID en 3 bytes (little endian)
        self.mundo[self.byte_actual] = id_seccion & 0xFF
        self.mundo[self.byte_actual + 1] = (id_seccion >> 8) & 0xFF
        self.mundo[self.byte_actual + 2] = (id_seccion >> 16) & 0xFF
        self.byte_actual += 3
        
        # Registramos (3 bytes)
        self._registrar_en_indice(3)
        print(f"🔗 Linker a sección {id_seccion} creado")
    
    def _registrar_en_indice(self, bytes_usados):
        """Registra cuántos bytes se usaron en el índice"""
        if bytes_usados > 255:
            # Si es más de 255 bytes, guardamos en múltiples bytes
            temp = bytes_usados
            i = 0
            while temp > 0:
                self.indice[(self.objetos_registrados << 8) + i] = temp & 0xFF
                temp >>= 8
                i += 1
        else:
            self.indice[self.objetos_registrados << 8] = bytes_usados
        
        self.objetos_registrados += 1
    
    def leer_seccion(self, inicio):
        """Lee una sección desde el byte de inicio"""
        print(f"\n--- Leyendo sección en byte {inicio} ---")
        i = inicio
        
        # Leer el nombre
        nombre = ""
        while self.mundo[i] != 0:
            nombre += chr(self.mundo[i])
            i += 1
        i += 1  # Saltar el separador
        print(f"🏠 Sección: {nombre}")
        
        # Leer objetos y linkers
        while self.mundo[i] != 0 or self.mundo[i+1] != 0:
            # Es un linker? (verificamos si son 3 bytes que representan un número)
            if i < len(self.mundo) - 3:
                posible_id = self.mundo[i] | (self.mundo[i+1] << 8) | (self.mundo[i+2] << 16)
                if posible_id > 0 and posible_id < 1000:  # Es un ID válido
                    print(f"  🔗 Enlace a sección: {posible_id}")
                    i += 3
                    continue
            
            # Es un objeto
            objeto = ""
            while self.mundo[i] != 0:
                objeto += chr(self.mundo[i])
                i += 1
            if objeto:
                print(f"  📦 Objeto: {objeto}")
            i += 1  # Saltar separador
        
        print("--- Fin de sección ---")

# ===== CONSTRUYENDO EL MUNDO =====
print("🌍 INICIALIZANDO MUNDO VIRTUAL...\n")

mundo = MotorMundo()

# Construir sala principal
print("\n=== CONSTRUYENDO SALA PRINCIPAL ===")
mundo.crear_seccion("sala_principal")
mundo.agregar_objeto("sofá")
mundo.crear_linker(1)  # Enlace a cocina
mundo.agregar_objeto("cocina")
mundo.crear_linker(2)  # Enlace a patio
mundo.agregar_objeto("patio")
mundo.crear_linker(3)  # Enlace a escaleras
mundo.agregar_objeto("escaleras")

# Construir cocina
print("\n=== CONSTRUYENDO COCINA ===")
mundo.crear_seccion("cocina")
mundo.crear_linker(4)  # Enlace a heladera
mundo.agregar_objeto("heladera")
mundo.crear_linker(5)  # Enlace a mesa
mundo.agregar_objeto("mesa")
mundo.agregar_objeto("alacena")
mundo.agregar_objeto("horno")

# Construir patio
print("\n=== CONSTRUYENDO PATIO ===")
mundo.crear_seccion("patio")
mundo.agregar_objeto("pasto")
mundo.agregar_objeto("salida")
mundo.crear_linker(6)  # Enlace a jardín

print("\n✅ MUNDO CONSTRUIDO")
print(f"📊 Memoria usada: {mundo.byte_actual} bytes de 16,777,216")
print(f"📊 Porcentaje usado: {(mundo.byte_actual / 0x1000000) * 100:.4f}%")
print(f"📊 Objetos registrados: {mundo.objetos_registrados}")

# Leer el mundo para verificar
print("\n=== VERIFICANDO MUNDO ===")
mundo.leer_seccion(0)  # Leer desde el inicio

# Mostrar el estado en bytes
print(f"\n📝 PRIMEROS 50 BYTES DEL MUNDO:")
for i in range(50):
    print(f"{i:02x}: {mundo.mundo[i]:02x} ({chr(mundo.mundo[i]) if mundo.mundo[i] > 32 else '.'})")
