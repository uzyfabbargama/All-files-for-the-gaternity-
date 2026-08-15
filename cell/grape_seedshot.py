import os
import random

def sembrar_universo(archivo="universo.bin", tamano=1000000):
    # Creamos un mar de ruido base muy bajo (energía 0 o 1)
    universo = bytearray([random.choice([0, 1]) for _ in range(tamano)])
    
    # Sembramos "estrellas" (puntos de alta energía 255) en lugares aleatorios
    for _ in range(1000):
        pos = random.randint(0, tamano - 1)
        universo[pos] = 255
        
    # Sembramos una "nebulosa" en el centro (bits densos)
    centro = tamano // 2
    for i in range(centro - 5000, centro + 5000):
        if random.random() > 0.7:
            universo[i] = random.randint(100, 200)

    with open(archivo, "wb") as f:
        f.write(universo)
    print(f"--- Universo sembrado en {archivo} ---")

if __name__ == "__main__":
    sembrar_universo()
