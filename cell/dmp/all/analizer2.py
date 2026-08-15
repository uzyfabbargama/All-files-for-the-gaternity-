import numpy as np
import matplotlib.pyplot as plt

def analizar_universo(archivo):
    # Cargamos el MB de RAM de tu simulación
    data = np.fromfile(archivo, dtype=np.uint8)
    # Lo convertimos en una matriz de 1000x1000
    grid = data.reshape((1000, 1000))
    
    # Calculamos la Transformada de Fourier (FFT)
    # Esto nos dirá si hay "frecuencias" dominantes (patrones)
    fft = np.fft.fft2(grid)
    power_spectrum = np.abs(np.fft.fftshift(fft))**2
    return np.log10(power_spectrum)

# Comparación
ps_asimetrico = analizar_universo('universo_asimetrico.bin')
ps_V1 = analizar_universo('universov1.bin')

plt.imshow(ps_asimetrico - ps_V1, cmap='RdBu')
plt.title("Diferencia de Energía: Asimetría vs Simetría")
plt.show()
