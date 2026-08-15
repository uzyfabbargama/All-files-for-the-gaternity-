import sounddevice as sd
import numpy as np
var = 1
ver = 1
# Configuramos para que escuche tu dispositivo 65
def callback(indata, frames, time, status):
    global var, ver
    canal_actual = indata[:, int(var)]
    volume_norm = np.linalg.norm(canal_actual) * 10
    #if volume_norm > 0.35:  # Ajusta este número según tu voz promedio
    print(f"Canal:{int(var)} | Nivel: {volume_norm:.8f}")
    ver += 0.0000005 
    if ver > 1.0001: #umbral
        var = (var + 1) % 2
        ver = 1.0
with sd.InputStream(device=1, channels=2, callback=callback):
    print("Escuchando... presiona Ctrl+C para parar")
    sd.sleep(10**10)
