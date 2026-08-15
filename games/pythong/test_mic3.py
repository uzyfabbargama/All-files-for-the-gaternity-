import pyaudio
import numpy as np
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

print("\n=== PROBANDO DISPOSITIVOS CON AJUSTES ===\n")

# Probar diferentes configuraciones con el dispositivo [2]
dispositivos_a_probar = [2, 4, 5, 6]

for idx in dispositivos_a_probar:
    info = p.get_device_info_by_index(idx)
    print(f"Probando dispositivo [{idx}]: {info['name']}")
    
    # Probar con diferentes tamaños de buffer y tasas
    for rate in [44100, 22050, 16000]:
        for chunk in [512, 1024, 2048]:
            try:
                stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=rate,
                              input=True,
                              input_device_index=idx,
                              frames_per_buffer=chunk)
                
                print(f"  ✅ Abierto (rate={rate}, chunk={chunk})")
                
                # Leer varios buffers para asegurar
                datos_totales = []
                for _ in range(10):
                    data = stream.read(chunk, exception_on_overflow=False)
                    datos_totales.append(np.frombuffer(data, dtype=np.int16))
                
                # Calcular el máximo absoluto (pico)
                todos_datos = np.concatenate(datos_totales)
                max_val = np.max(np.abs(todos_datos))
                media = np.mean(np.abs(todos_datos))
                rms = np.sqrt(np.mean(todos_datos.astype(np.float32)**2))
                
                print(f"  📊 Pico: {max_val}, Media: {media:.1f}, RMS: {rms:.1f}")
                
                if max_val > 100:
                    print("  🔊 ¡SONIDO DETECTADO!")
                    if rms > 50:
                        db = 20 * np.log10(rms)
                        print(f"  🔊 Volumen: {db:.1f} dB")
                else:
                    print("  🔇 Silencio (ajustando sensibilidad...)")
                
                stream.stop_stream()
                stream.close()
                print()
                break  # Si funciona con esta configuración, pasar al siguiente dispositivo
                
            except Exception as e:
                print(f"  ❌ Error: {e}\n")
                continue

p.terminate()
