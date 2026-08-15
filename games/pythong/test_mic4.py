import pyaudio
import numpy as np
import time
import sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

def probar_microfono():
    p = pyaudio.PyAudio()
    
    print("\n" + "="*60)
    print("🔍 DIAGNÓSTICO COMPLETO DE MICRÓFONO")
    print("="*60)
    
    # Mostrar información detallada de cada dispositivo
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"\n📌 Dispositivo [{i}]: {info['name']}")
            print(f"   Canales de entrada: {info['maxInputChannels']}")
            print(f"   Tasa por defecto: {int(info['defaultSampleRate'])} Hz")
            print(f"   Latencia por defecto: {info['defaultLowInputLatency']:.3f}s")
    
    print("\n" + "="*60)
    print("🎤 PROBANDO DISPOSITIVOS (HABLA FUERTE)")
    print("="*60)
    
    # Probar cada dispositivo con entrada
    for idx in range(p.get_device_count()):
        info = p.get_device_info_by_index(idx)
        if info['maxInputChannels'] == 0:
            continue
            
        print(f"\n▶ Probando dispositivo [{idx}]: {info['name']}")
        
        # Probar diferentes configuraciones
        for rate in [44100, 22050, 16000, 8000]:
            for chunk in [512, 1024, 2048]:
                try:
                    stream = p.open(format=FORMAT,
                                  channels=min(2, info['maxInputChannels']),
                                  rate=rate,
                                  input=True,
                                  input_device_index=idx,
                                  frames_per_buffer=chunk)
                    
                    # Leer varios buffers
                    datos = []
                    for _ in range(20):  # ~0.5 segundos
                        data = stream.read(chunk, exception_on_overflow=False)
                        datos.append(np.frombuffer(data, dtype=np.int16))
                    
                    stream.stop_stream()
                    stream.close()
                    
                    # Analizar datos
                    todos = np.concatenate(datos)
                    pico = np.max(np.abs(todos))
                    media = np.mean(np.abs(todos))
                    rms = np.sqrt(np.mean(todos.astype(np.float32)**2))
                    
                    print(f"  rate={rate}, chunk={chunk}: Pico={pico:6d}, Media={media:6.1f}, RMS={rms:6.1f}")
                    
                    if pico > 100:
                        print(f"  ✅ ¡ÉXITO! Dispositivo [{idx}] funciona con rate={rate}, chunk={chunk}")
                        print(f"  🔊 Volumen detectado: Pico={pico}")
                        
                        # Guardar configuración
                        with open('config_mic.txt', 'w') as f:
                            f.write(f"{idx}\n{rate}\n{chunk}")
                        
                        p.terminate()
                        return idx, rate, chunk
                    
                except Exception as e:
                    # Si hay error, continuar con la siguiente configuración
                    pass
    
    print("\n❌ No se detectó sonido en ningún dispositivo")
    print("💡 Verifica que el micrófono esté desmutado en 'alsamixer'")
    print("💡 Prueba con 'arecord -d 5 test.wav' y luego 'aplay test.wav'")
    p.terminate()
    return None, None, None

if __name__ == "__main__":
    idx, rate, chunk = probar_microfono()
    
    if idx is not None:
        print(f"\n✅ Configuración encontrada: dispositivo {idx}, rate={rate}, chunk={chunk}")
        print(f"📁 Guardado en config_mic.txt")
    else:
        print("\n❌ No se pudo encontrar configuración válida")
