import pygame
import pyaudio
import numpy as np
import sys
import math

# ========== CONFIGURACIÓN ==========
ANCHO, ALTO = 800, 600
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)

# ========== CONFIGURACIÓN DE AUDIO ==========
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# ========== SELECCIONAR DISPOSITIVO ==========
def seleccionar_dispositivo():
    """Muestra los dispositivos y permite elegir uno"""
    p = pyaudio.PyAudio()
    print("\n🎤 DISPOSITIVOS DE AUDIO DISPONIBLES:")
    print("-" * 60)
    dispositivos = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:  # Solo los que tienen entrada
            dispositivos.append((i, info['name'], info['maxInputChannels']))
            print(f"[{i}] {info['name']} - {info['maxInputChannels']} canales de entrada")
    print("-" * 60)
    
    if not dispositivos:
        print("❌ No se encontraron dispositivos con entrada de audio")
        p.terminate()
        return None, None
    
    # Intentar usar el índice 2 si existe, o el primero disponible
    indice = 4
    for idx, nombre, canales in dispositivos:
        if idx == indice:
            print(f"✅ Usando dispositivo: [{idx}] {nombre}")
            return p, idx
    
    # Si no existe el índice 2, usar el primero
    idx, nombre, canales = dispositivos[0]
    print(f"✅ Usando dispositivo: [{idx}] {nombre}")
    return p, idx

# ========== CLASE DEL JUEGO ==========
class JuegoVoz:
    def __init__(self, p, dispositivo_idx):
        self.p = p
        self.dispositivo_idx = dispositivo_idx
        
        # Inicializar pygame
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Voz Escalera - Controla con tu voz")
        self.reloj = pygame.time.Clock()
        
        # Estado del juego
        self.jugando = True
        self.puntuacion = 0
        self.fuente = pygame.font.Font(None, 36)
        
        # Posición de la esfera
        self.y_esfera = ALTO // 2
        self.volumen = 0
        self.volumen_suavizado = 0
        
        # Zona dorada
        self.zona_y = ALTO // 2
        self.zona_altura = 80
        self.tiempo_cambio_zona = 0
        
        # Modo tormenta
        self.modo_tormenta = False
        self.tiempo_tormenta = 0
        
        # Intentar abrir el stream de audio
        try:
            self.stream = self.p.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      input_device_index=self.dispositivo_idx,
                                      frames_per_buffer=CHUNK)
            print("✅ Stream de audio abierto correctamente")
        except Exception as e:
            print(f"❌ Error al abrir el stream: {e}")
            print("💡 Probando con el dispositivo por defecto...")
            try:
                self.stream = self.p.open(format=FORMAT,
                                          channels=CHANNELS,
                                          rate=RATE,
                                          input=True,
                                          frames_per_buffer=CHUNK)
                print("✅ Stream abierto con dispositivo por defecto")
            except Exception as e2:
                print(f"❌ Error fatal: {e2}")
                pygame.quit()
                sys.exit()
    
    def obtener_volumen(self):
        """Lee el micrófono y devuelve el volumen (0-100)"""
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Calcular RMS
            if len(audio_data) > 0:
                rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))
                # Convertir a decibelios (escala 0-100)
                if rms > 1:  # Umbral mínimo para evitar ruido
                    volumen = min(100, int(20 * np.log10(rms) + 90))
                    volumen = max(0, volumen)
                else:
                    volumen = 0
                return volumen
            return 0
        except Exception as e:
            return 0
    
    def actualizar_zona(self):
        """Cambia la posición de la zona dorada cada cierto tiempo"""
        self.tiempo_cambio_zona += 1
        if self.tiempo_cambio_zona > 120:
            self.tiempo_cambio_zona = 0
            self.zona_y = np.random.randint(100, ALTO - 100)
            self.zona_altura = np.random.randint(50, 120)
    
    def actualizar_esfera(self, volumen):
        """Mueve la esfera según el volumen"""
        # Suavizar el volumen
        self.volumen_suavizado = self.volumen_suavizado * 0.7 + volumen * 0.3
        
        # Mapear volumen a posición Y (invertido: volumen alto = esfera arriba)
        objetivo_y = ALTO - (self.volumen_suavizado / 100) * ALTO
        
        # Movimiento suave
        self.y_esfera += (objetivo_y - self.y_esfera) * 0.1
        self.y_esfera = max(20, min(ALTO - 20, self.y_esfera))
    
    def verificar_colision(self):
        """Verifica si la esfera está dentro de la zona dorada"""
        if abs(self.y_esfera - self.zona_y) < self.zona_altura // 2:
            self.puntuacion += 1
            return True
        return False
    
    def dibujar(self):
        self.pantalla.fill(NEGRO)
        
        # Zona dorada
        pygame.draw.rect(self.pantalla, AMARILLO,
                        (ANCHO//4, self.zona_y - self.zona_altura//2,
                         ANCHO//2, self.zona_altura))
        pygame.draw.rect(self.pantalla, BLANCO,
                        (ANCHO//4, self.zona_y - self.zona_altura//2,
                         ANCHO//2, self.zona_altura), 2)
        
        # Esfera
        pygame.draw.circle(self.pantalla, VERDE,
                          (ANCHO//2, int(self.y_esfera)), 25)
        pygame.draw.circle(self.pantalla, BLANCO,
                          (ANCHO//2 - 8, int(self.y_esfera) - 8), 8)
        
        # Información
        texto_vol = self.fuente.render(f"Volumen: {int(self.volumen_suavizado)}%",
                                      True, BLANCO)
        self.pantalla.blit(texto_vol, (10, 10))
        
        texto_puntos = self.fuente.render(f"Puntos: {self.puntuacion}",
                                        True, BLANCO)
        self.pantalla.blit(texto_puntos, (10, 50))
        
        # Indicador del dispositivo
        texto_dev = self.fuente.render(f"Mic: {self.dispositivo_idx}",
                                      True, (150, 150, 150))
        self.pantalla.blit(texto_dev, (10, ALTO - 30))
        
        if self.modo_tormenta:
            texto_tormenta = self.fuente.render("🌩️ MODO TORMENTA",
                                              True, ROJO)
            self.pantalla.blit(texto_tormenta, (ANCHO//2 - 80, 10))
        
        if self.puntuacion < 10:
            instrucciones = self.fuente.render("Habla fuerte para subir, susurra para bajar",
                                              True, (150, 150, 150))
            self.pantalla.blit(instrucciones, (ANCHO//2 - 200, ALTO - 60))
        
        pygame.display.flip()
    
    def ejecutar(self):
        while self.jugando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.jugando = False
                    if evento.key == pygame.K_t:
                        self.modo_tormenta = not self.modo_tormenta
            
            # Obtener volumen
            self.volumen = self.obtener_volumen()
            
            # Actualizar zona
            self.actualizar_zona()
            
            # Actualizar esfera
            self.actualizar_esfera(self.volumen)
            
            # Colisión
            self.verificar_colision()
            
            # Modo tormenta
            if self.puntuacion > 0 and self.puntuacion % 30 == 0 and not self.modo_tormenta:
                self.modo_tormenta = True
                self.tiempo_tormenta = 0
            
            if self.modo_tormenta:
                self.tiempo_tormenta += 1
                if self.tiempo_tormenta > 300:
                    self.modo_tormenta = False
                    self.tiempo_tormenta = 0
            
            self.dibujar()
            self.reloj.tick(60)
        
        # Limpiar
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        pygame.quit()
        sys.exit()

# ========== EJECUTAR ==========
if __name__ == "__main__":
    # Seleccionar dispositivo primero
    p, dispositivo_idx = seleccionar_dispositivo()
    
    if p is None or dispositivo_idx is None:
        print("❌ No se pudo seleccionar un dispositivo de audio")
        sys.exit()
    
    # Crear y ejecutar el juego
    juego = JuegoVoz(p, dispositivo_idx)
    juego.ejecutar()
