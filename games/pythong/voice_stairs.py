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
CHUNK = 1024  # Tamaño del buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Frecuencia de muestreo

# Inicializar PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=2,
                frames_per_buffer=CHUNK)
# Listar dispositivos de audio
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} - inputs: {info['maxInputChannels']}")

# ========== CLASE DEL JUEGO ==========
class JuegoVoz:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Voz Escalera - Controla con tu voz")
        self.reloj = pygame.time.Clock()
        
        # Posición de la esfera (eje Y)
        self.y_esfera = ALTO // 2
        self.velocidad = 0
        
        # Zona dorada (objetivo)
        self.zona_y = ALTO // 2
        self.zona_altura = 80
        self.tiempo_cambio_zona = 0
        
        # Puntuación
        self.puntuacion = 0
        self.fuente = pygame.font.Font(None, 36)
        
        # Estado del juego
        self.jugando = True
        self.modo_tormenta = False
        self.tiempo_tormenta = 0
        
        # Para medir volumen
        self.volumen = 0
        self.volumen_suavizado = 0
        
    def obtener_volumen(self):
        """Lee el micrófono y devuelve el volumen (0-100)"""
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            # Calcular RMS (Root Mean Square) como medida de volumen
            rms = np.sqrt(np.mean(audio_data**2))
            # Convertir a escala 0-100 (logarítmica para mejor sensación)
            if rms > 0:
                volumen = min(100, int(20 * np.log10(rms) + 90))
                volumen = max(0, volumen)
            else:
                volumen = 0
            return volumen
        except:
            return 0
    
    def actualizar_zona(self):
        """Cambia la posición de la zona dorada cada cierto tiempo"""
        self.tiempo_cambio_zona += 1
        if self.tiempo_cambio_zona > 120:  # Cada 2 segundos (60 FPS)
            self.tiempo_cambio_zona = 0
            # Nueva posición aleatoria, pero no muy cerca de los bordes
            self.zona_y = np.random.randint(100, ALTO - 100)
            # Cambiar altura de la zona
            self.zona_altura = np.random.randint(50, 120)
    
    def actualizar_esfera(self, volumen):
        """Mueve la esfera según el volumen"""
        # Suavizar el volumen para movimientos más fluidos
        self.volumen_suavizado = self.volumen_suavizado * 0.7 + volumen * 0.3
        
        # La esfera sube con volumen alto, baja con volumen bajo
        # Mapear volumen (0-100) a posición Y (ALTO - 0)
        objetivo_y = ALTO - (self.volumen_suavizado / 100) * ALTO
        
        # Movimiento suave hacia el objetivo
        self.y_esfera += (objetivo_y - self.y_esfera) * 0.1
        
        # Evitar que se salga de la pantalla
        self.y_esfera = max(20, min(ALTO - 20, self.y_esfera))
    
    def verificar_colision(self):
        """Verifica si la esfera está dentro de la zona dorada"""
        if abs(self.y_esfera - self.zona_y) < self.zona_altura // 2:
            self.puntuacion += 1
            return True
        return False
    
    def dibujar(self):
        self.pantalla.fill(NEGRO)
        
        # Dibujar zona dorada
        pygame.draw.rect(self.pantalla, AMARILLO, 
                        (ANCHO//4, self.zona_y - self.zona_altura//2, 
                         ANCHO//2, self.zona_altura))
        # Borde de la zona
        pygame.draw.rect(self.pantalla, BLANCO, 
                        (ANCHO//4, self.zona_y - self.zona_altura//2, 
                         ANCHO//2, self.zona_altura), 2)
        
        # Dibujar esfera
        pygame.draw.circle(self.pantalla, VERDE, 
                          (ANCHO//2, int(self.y_esfera)), 25)
        # Brillo de la esfera
        pygame.draw.circle(self.pantalla, BLANCO, 
                          (ANCHO//2 - 8, int(self.y_esfera) - 8), 8)
        
        # Mostrar volumen
        texto_vol = self.fuente.render(f"Volumen: {int(self.volumen_suavizado)}%", 
                                       True, BLANCO)
        self.pantalla.blit(texto_vol, (10, 10))
        
        # Mostrar puntuación
        texto_puntos = self.fuente.render(f"Puntos: {self.puntuacion}", 
                                         True, BLANCO)
        self.pantalla.blit(texto_puntos, (10, 50))
        
        # Mostrar modo tormenta si está activado
        if self.modo_tormenta:
            texto_tormenta = self.fuente.render("🌩️ MODO TORMENTA ACTIVADO", 
                                               True, ROJO)
            self.pantalla.blit(texto_tormenta, (ANCHO//2 - 150, 10))
        
        # Instrucciones
        if self.puntuacion < 10:
            instrucciones = self.fuente.render("Habla fuerte para subir, susurra para bajar", 
                                              True, (150, 150, 150))
            self.pantalla.blit(instrucciones, (ANCHO//2 - 200, ALTO - 40))
        
        pygame.display.flip()
    
    def ejecutar(self):
        while self.jugando:
            # Manejar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.jugando = False
                    if evento.key == pygame.K_t:  # Activar tormenta manual
                        self.modo_tormenta = not self.modo_tormenta
            
            # Obtener volumen del micrófono
            self.volumen = self.obtener_volumen()
            
            # Actualizar zona dorada
            self.actualizar_zona()
            
            # Actualizar posición de la esfera
            self.actualizar_esfera(self.volumen)
            
            # Verificar si está en la zona
            if self.verificar_colision():
                # Efecto visual de acierto
                pass
            
            # Modo tormenta: se activa cada 30 puntos
            if self.puntuacion > 0 and self.puntuacion % 30 == 0 and not self.modo_tormenta:
                self.modo_tormenta = True
                self.tiempo_tormenta = 0
            
            if self.modo_tormenta:
                self.tiempo_tormenta += 1
                if self.tiempo_tormenta > 300:  # 5 segundos
                    self.modo_tormenta = False
                    self.tiempo_tormenta = 0
            
            # Dibujar todo
            self.dibujar()
            
            # Control de FPS
            self.reloj.tick(60)
        
        # Limpiar
        stream.stop_stream()
        stream.close()
        p.terminate()
        pygame.quit()
        sys.exit()

# ========== EJECUTAR ==========
if __name__ == "__main__":
    juego = JuegoVoz()
    juego.ejecutar()
