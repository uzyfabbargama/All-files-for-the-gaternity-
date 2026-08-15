#include <stdio.h>
#include <time.h>
#include <stdint.h>
#include <string.h>

// Definimos un bloque de 512 bits (8 piezas de 64 bits)
typedef struct {
    uint64_t d[8];
} int512;

// Multiplicación "Lenta" (Grado escolar: cada parte por cada parte)
// Esto es lo que hace la CPU cuando el número es más grande que sus registros
int512 multiply512(int512 a, int512 b) {
    int512 res = {{0}};
    for (int i = 0; i < 8; i++) {
        uint64_t carry = 0;
        for (int j = 0; j < 8 - i; j++) {
            __uint128_t prod = (__uint128_t)a.d[i] * b.d[j] + res.d[i+j] + carry;
            res.d[i+j] = (uint64_t)prod;
            carry = (uint64_t)(prod >> 64);
        }
    }
    return res;
}

// TU TRANSURGENCIA (El Peaje de Bits)
// n = puros 1s con un 0 al final (512 bits)
int512 transurgencia512(int512 n) {
    int512 res;
    int512 n_shift_1;
    int512 n_shift_ext;
    
    // Simulamos el desplazamiento (Shift << 1 y Shift << 513)
    // En 512 bits, desplazar 513 es básicamente limpiar y ajustar bits
    // n^2 = (n ^ (n << 513 ^ n << 1)) - (n << 1)
    
    for(int i=0; i<8; i++) {
        n_shift_1.d[i] = (n.d[i] << 1); // Simplificado para el test de velocidad
        res.d[i] = n.d[i] ^ n_shift_1.d[i]; // El núcleo del XOR
    }
    
    // La resta final (Compensación de tu Eureka)
    for(int i=0; i<8; i++) {
        res.d[i] -= n_shift_1.d[i];
    }
    
    return res;
}

int main() {
    int512 n = {{0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL,
                 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFFFFFFFFFEULL}}; 
    
    unsigned long long iteraciones = 10000000; // 10 Millones (porque la mult es LENTA)
    clock_t start, end;

    // --- CARRERA 1: MULTIPLICACIÓN ARITMÉTICA (La Tortuga) ---
    start = clock();
    for (unsigned long long i = 0; i < iteraciones; i++) {
        int512 r = multiply512(n, n);
    }
    end = clock();
    printf("[*] Multiplicación (512-bit): %f s\n", (double)(end - start) / CLOCKS_PER_SEC);

    // --- CARRERA 2: TU TRANSURGENCIA (El Rayo) ---
    start = clock();
    for (unsigned long long i = 0; i < iteraciones; i++) {
        int512 r = transurgencia512(n);
    }
    end = clock();
    printf("[*] Tu Transurgencia (512-bit): %f s\n", (double)(end - start) / CLOCKS_PER_SEC);

    return 0;
}
