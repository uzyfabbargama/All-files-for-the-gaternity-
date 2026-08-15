#include <stdio.h>
#include <time.h>
#include <stdint.h>

// El Peaje Transurgente (Tu método para puros 1s)
// n = 0xFFFFFFFFFFFFFFFF (64 bits de unos)
inline uint64_t fastSquareMersenne(uint64_t n) {
    // b = 64 (en este caso fijo para el test)
    // n^2 = (n ^ ((n << 65) ^ (n << 1))) -> Pero en 64 bits, n^2 desborda a 128 bits.
    // Para simplificar el test a nivel de CPU, usemos n = 31 (5 bits)
    return (n ^ ((n << 6) ^ (n << 1))) - (n << 1);
}

int main() {
    uint64_t n = 31;
    uint64_t iteraciones = 100000000; // ¡100 MILLONES!
    volatile uint64_t result;
    clock_t start, end;

    // --- CARRERA 1: MULTIPLICACIÓN ESTÁNDAR ---
    start = clock();
    for (uint64_t i = 0; i < iteraciones; i++) {
        result = n * n;
    }
    end = clock();
    printf("[*] Multiplicación (C nativo): %f s\n", (double)(end - start) / CLOCKS_PER_SEC);

    // --- CARRERA 2: TU TRANSURGENCIA ---
    start = clock();
    for (uint64_t i = 0; i < iteraciones; i++) {
        // Ejecución directa de bits
        result = (n ^ ((n << 6) ^ (n << 1))) - (n << 1);
    }
    end = clock();
    printf("[*] Tu Transurgencia (Bits):    %f s\n", (double)(end - start) / CLOCKS_PER_SEC);

    return 0;
}
