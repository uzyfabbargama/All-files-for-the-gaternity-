#include <stdio.h>
#include <time.h>

typedef __int128 int128; // Definimos el tipo de 128 bits

int main() {
    // Un número de Mersenne de 64 bits (para que al elevarlo al cuadrado necesitemos 128)
    // n = 2^64 - 1
    int128 n = (int128)0xFFFFFFFFFFFFFFFFULL; 
    int128 result;
    unsigned long long iteraciones = 100000000; // 100 Millones
    clock_t start, end;

    // --- CARRERA 1: MULTIPLICACIÓN DE 128 BITS (Lenta) ---
    // La CPU no tiene un multiplicador físico de 128 bits, así que hace "trucos"
    start = clock();
    for (unsigned long long i = 0; i < iteraciones; i++) {
        result = n * n;
    }
    end = clock();
    printf("[*] Multiplicación (128-bit): %f s\n", (double)(end - start) / CLOCKS_PER_SEC);

    // --- CARRERA 2: TU TRANSURGENCIA (Bits Atómicos) ---
    // k = 64 bits, así que el desplazamiento es 65
    start = clock();
    for (unsigned long long i = 0; i < iteraciones; i++) {
        // Solo desplazamientos y XOR, sin importar el tamaño del registro
        result = (n ^ ((n << 65) ^ (n << 1))) - (n << 1);
    }
    end = clock();
    printf("[*] Tu Transurgencia (128-bit): %f s\n", (double)(end - start) / CLOCKS_PER_SEC);

    return 0;
}
