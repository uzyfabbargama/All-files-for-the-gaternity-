import pyaudio
import numpy as np
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

# Mostrar TODOS los dispositivos
print("\n=== TODOS LOS DISPOSITIVOS ===")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"[{i}] {info['name']}")
    print(f"    Entradas: {info['maxInputChannels']}")
    print(f"    Salidas: {info['maxOutputChannels']}")
    print(f"    Tasa por defecto: {int(info['defaultSampleRate'])}")
    print()

# Probar cada dispositivo con entrada
print("=== PROBANDO DISPOSITIVOS CON ENTRADA ===\n")
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Probando dispositivo [{i}]: {info['name']}")
        try:
            stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          input_device_index=i,
                          frames_per_buffer=CHUNK,
                          timeout=2)
            
            print("  ✅ Abierto correctamente")
            
            # Leer 3 segundos de audio
            print("  Habla durante 3 segundos...")
            data = stream.read(CHUNK * 3, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Calcular volumen
            rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))
            if rms > 10:
                db = 20 * np.log10(rms)
                print(f"  🔊 Volumen detectado: {db:.1f} dB")
            else:
                print("  🔇 Silencio (¿hablaste?)")
            
            stream.stop_stream()
            stream.close()
            print()
            
        except Exception as e:
            print(f"  ❌ Error: {e}\n")

p.terminate()
