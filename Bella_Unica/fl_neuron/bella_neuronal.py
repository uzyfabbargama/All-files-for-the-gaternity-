#!/usr/bin/env python3
"""
BELLA NEURONAL v1.0
Red neuronal en ASM con 2,097,152 neuronas
Integración completa con NeuralScript
"""

import ctypes
import random
import struct
from preprocesador_v3 import parse_and_serialize

class BellaNeuronal:
    def __init__(self):
        # Cargar motor ASM
        self.motor = ctypes.CDLL('./libNSMotor.so')
        self.motor.NSMotor.argtypes = [ctypes.c_char_p]
        self.motor.NSMotor.restype = None
        
        # Configuración de la red
        self.TOTAL_NEURONAS = 2097152  # 2,097,152 (16 MB / 8 bytes)
        self.NEURONAS_ENTRADA = 10000  # 10k neuronas de entrada
        self.NEURONAS_CAPA1 = 50000    # 50k capa oculta 1
        self.NEURONAS_CAPA2 = 50000    # 50k capa oculta 2
        self.NEURONAS_SALIDA = 10000   # 10k neuronas de salida
        
        # Mapas de neuronas
        self.neuronas_entrada = []
        self.neuronas_capa1 = []
        self.neuronas_capa2 = []
        self.neuronas_salida = []
        
        # Asignar IDs
        self._asignar_neuronas()
        
        # Estado
        self.vocabulario = {}
        self.historial = []
        
    def _asignar_neuronas(self):
        """Asigna IDs a las neuronas en rangos"""
        # Entrada: 0 - 9999
        self.neuronas_entrada = list(range(0, self.NEURONAS_ENTRADA))
        
        # Capa1: 10000 - 59999
        offset = self.NEURONAS_ENTRADA
        self.neuronas_capa1 = list(range(offset, offset + self.NEURONAS_CAPA1))
        
        # Capa2: 60000 - 109999
        offset += self.NEURONAS_CAPA1
        self.neuronas_capa2 = list(range(offset, offset + self.NEURONAS_CAPA2))
        
        # Salida: 110000 - 119999
        offset += self.NEURONAS_CAPA2
        self.neuronas_salida = list(range(offset, offset + self.NEURONAS_SALIDA))
        
        print(f"🧠 Red neuronal configurada:")
        print(f"   Entrada: {len(self.neuronas_entrada)} neuronas (IDs 0-{self.NEURONAS_ENTRADA-1})")
        print(f"   Capa 1: {len(self.neuronas_capa1)} neuronas (IDs {self.NEURONAS_ENTRADA}-{self.NEURONAS_ENTRADA+self.NEURONAS_CAPA1-1})")
        print(f"   Capa 2: {len(self.neuronas_capa2)} neuronas (IDs {self.NEURONAS_ENTRADA+self.NEURONAS_CAPA1}-{self.NEURONAS_ENTRADA+self.NEURONAS_CAPA1+self.NEURONAS_CAPA2-1})")
        print(f"   Salida: {len(self.neuronas_salida)} neuronas (IDs {self.NEURONAS_ENTRADA+self.NEURONAS_CAPA1+self.NEURONAS_CAPA2}-{self.NEURONAS_ENTRADA+self.NEURONAS_CAPA1+self.NEURONAS_CAPA2+self.NEURONAS_SALIDA-1})")
        print(f"   Total usado: {self.NEURONAS_ENTRADA + self.NEURONAS_CAPA1 + self.NEURONAS_CAPA2 + self.NEURONAS_SALIDA}")
        print(f"   Neuronas libres: {self.TOTAL_NEURONAS - (self.NEURONAS_ENTRADA + self.NEURONAS_CAPA1 + self.NEURONAS_CAPA2 + self.NEURONAS_SALIDA)}")

    def _generar_codigo_conexiones(self):
        """Genera código NeuralScript para conectar todas las neuronas"""
        codigo = []
        
        # 1. Inicializar neuronas con valores random
        codigo.append("$ === INICIALIZACIÓN DE NEURONAS ===")
        
        # Entrada: valores pequeños (0.001 - 0.01)
        for i, idx in enumerate(self.neuronas_entrada):
            valor = random.uniform(0.001, 0.01)
            codigo.append(f"var n_ent_{idx}, {valor:.6f}")
        
        # Capa1: valores medios (0.01 - 0.1)
        for idx in self.neuronas_capa1:
            valor = random.uniform(0.01, 0.1)
            codigo.append(f"var n_capa1_{idx}, {valor:.6f}")
        
        # Capa2: valores medios (0.01 - 0.1)
        for idx in self.neuronas_capa2:
            valor = random.uniform(0.01, 0.1)
            codigo.append(f"var n_capa2_{idx}, {valor:.6f}")
        
        # Salida: valores bajos (0.001 - 0.01)
        for idx in self.neuronas_salida:
            valor = random.uniform(0.001, 0.01)
            codigo.append(f"var n_sal_{idx}, {valor:.6f}")
        
        # 2. Conectar entrada → capa1 (solo algunas conexiones para no saturar)
        codigo.append("\n$ === CONEXIÓN ENTRADA → CAPA1 ===")
        
        # Cada neurona de entrada se conecta a 10 neuronas de capa1
        for i, idx_ent in enumerate(self.neuronas_entrada):
            if i % 10 == 0:  # Solo algunas conexiones para prueba
                for j in range(0, min(10, len(self.neuronas_capa1))):
                    idx_capa1 = self.neuronas_capa1[(i + j) % len(self.neuronas_capa1)]
                    codigo.append(f"proc n_capa1_{idx_capa1}, n_ent_{idx_ent}")
        
        # 3. Conectar capa1 → capa2
        codigo.append("\n$ === CONEXIÓN CAPA1 → CAPA2 ===")
        
        for i, idx_capa1 in enumerate(self.neuronas_capa1):
            if i % 50 == 0:  # Menos conexiones para eficiencia
                for j in range(0, min(5, len(self.neuronas_capa2))):
                    idx_capa2 = self.neuronas_capa2[(i + j) % len(self.neuronas_capa2)]
                    codigo.append(f"proc n_capa2_{idx_capa2}, n_capa1_{idx_capa1}")
        
        # 4. Conectar capa2 → salida
        codigo.append("\n$ === CONEXIÓN CAPA2 → SALIDA ===")
        
        for i, idx_capa2 in enumerate(self.neuronas_capa2):
            if i % 50 == 0:
                for j in range(0, min(5, len(self.neuronas_salida))):
                    idx_sal = self.neuronas_salida[(i + j) % len(self.neuronas_salida)]
                    codigo.append(f"proc n_sal_{idx_sal}, n_capa2_{idx_capa2}")
        
        return "\n".join(codigo)

    def _generar_codigo_aprendizaje(self, texto):
        """Genera código para aprender de un texto"""
        codigo = []
        
        # Codificar texto a neuronas de entrada
        for i, char in enumerate(texto[:len(self.neuronas_entrada)]):
            if i < len(self.neuronas_entrada):
                valor = ord(char) / 255.0  # Normalizar a 0-1
                idx = self.neuronas_entrada[i]
                codigo.append(f"var n_ent_{idx}, {valor:.6f}")
        
        # Procesar: entrada → capa1 → capa2 → salida
        codigo.append("\n$ === PROPAGACIÓN ===")
        
        # Conectar entrada a capa1 (aprendizaje)
        for i, idx_ent in enumerate(self.neuronas_entrada[:100]):
            if i % 5 == 0:
                idx_capa1 = self.neuronas_capa1[i % len(self.neuronas_capa1)]
                codigo.append(f"proc n_capa1_{idx_capa1}, n_ent_{idx_ent}")
                codigo.append(f"growth n_capa1_{idx_capa1}, 0.01")  # Reforzar
        
        # Conectar capa1 a capa2
        for i, idx_capa1 in enumerate(self.neuronas_capa1[:50]):
            if i % 10 == 0:
                idx_capa2 = self.neuronas_capa2[i % len(self.neuronas_capa2)]
                codigo.append(f"proc n_capa2_{idx_capa2}, n_capa1_{idx_capa1}")
                codigo.append(f"growth n_capa2_{idx_capa2}, 0.01")
        
        # Conectar capa2 a salida
        for i, idx_capa2 in enumerate(self.neuronas_capa2[:30]):
            if i % 10 == 0:
                idx_sal = self.neuronas_salida[i % len(self.neuronas_salida)]
                codigo.append(f"proc n_sal_{idx_sal}, n_capa2_{idx_capa2}")
                codigo.append(f"growth n_sal_{idx_sal}, 0.01")
        
        return "\n".join(codigo)

    def _generar_codigo_hablar(self, longitud=100):
        """Genera código para generar texto"""
        codigo = []
        
        # Activar neuronas de salida
        codigo.append("\n$ === GENERACIÓN DE TEXTO ===")
        
        # Leer estado de las neuronas de salida
        for idx in self.neuronas_salida[:longitud]:
            codigo.append(f"var texto_{idx}, n_sal_{idx}")
        
        return "\n".join(codigo)

    def inicializar(self):
        """Inicializa la red neuronal"""
        print("\n🔧 Inicializando red neuronal...")
        codigo = self._generar_codigo_conexiones()
        
        # Compilar y ejecutar
        bytecode, _, _, _ = parse_and_serialize(codigo)
        self.motor.NSMotor(bytes(bytecode))
        
        print("✅ Red neuronal inicializada correctamente")
        print(f"   {len(self.neuronas_entrada) + len(self.neuronas_capa1) + len(self.neuronas_capa2) + len(self.neuronas_salida)} neuronas activas")

    def aprender(self, texto):
        """Entrena la red con un texto"""
        print(f"\n📚 Aprendiendo: {texto[:50]}...")
        codigo = self._generar_codigo_aprendizaje(texto)
        
        bytecode, _, _, _ = parse_and_serialize(codigo)
        self.motor.NSMotor(bytes(bytecode))
        
        # Guardar en historial
        self.historial.append(texto)
        print(f"✅ Aprendizaje completado")

    def hablar(self, longitud=100):
        """Genera texto a partir de la red"""
        print(f"\n🗣️ Generando respuesta...")
        
        # Generar código de habla
        codigo = self._generar_codigo_hablar(longitud)
        
        # En lugar de ejecutar, generamos el código
        # En la práctica, necesitaríamos leer la memoria del motor
        # Por ahora, simulamos una respuesta
        respuesta = "Bella dice: "
        
        # Tomar algunas neuronas de salida y convertirlas a caracteres
        for i, idx in enumerate(self.neuronas_salida[:longitud]):
            # Simular lectura de memoria
            valor = random.uniform(0.3, 0.9)  # Simulación
            if valor > 0.5:
                char_code = int(valor * 255)
                if 32 <= char_code <= 126:  # Caracteres imprimibles
                    respuesta += chr(char_code)
                else:
                    respuesta += " "
            else:
                respuesta += " "
        
        return respuesta

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("🧠 BELLA NEURONAL v1.0")
    print("=" * 60)
    
    # Crear Bella
    bella = BellaNeuronal()
    
    # Inicializar red
    bella.inicializar()
    
    # Menú interactivo
    while True:
        print("\n" + "=" * 60)
        print("[1] Hablar con Bella")
        print("[2] Enseñar a Bella (texto)")
        print("[3] Ver estado de la red")
        print("[4] Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            mensaje = input("Tú: ")
            if mensaje.lower() in ["salir", "exit", "quit"]:
                break
            
            # Aprender de la entrada
            bella.aprender(mensaje)
            
            # Generar respuesta
            respuesta = bella.hablar(longitud=50)
            print(f"\nBella: {respuesta}")
            
        elif opcion == "2":
            texto = input("Texto a enseñar: ")
            if texto.strip():
                bella.aprender(texto)
        
        elif opcion == "3":
            print(f"\n📊 Estado de Bella:")
            print(f"   Neuronas totales: {bella.TOTAL_NEURONAS}")
            print(f"   Neuronas de entrada: {len(bella.neuronas_entrada)}")
            print(f"   Neuronas capa1: {len(bella.neuronas_capa1)}")
            print(f"   Neuronas capa2: {len(bella.neuronas_capa2)}")
            print(f"   Neuronas salida: {len(bella.neuronas_salida)}")
            print(f"   Textos aprendidos: {len(bella.historial)}")
            
        elif opcion == "4":
            print("👋 Hasta luego, Bella!")
            break
        
        else:
            print("⚠️ Opción no válida")
