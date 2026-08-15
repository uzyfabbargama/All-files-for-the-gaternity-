#include <stdio.h>
#include <time.h>
#include <stdint.h>

// 2048 bits = 32 bloques de 64 bits
#define BLOCKS 32

typedef struct {
    uint64_t d[BLOCKS];
} int2048;

// MULTIPLICACIÓN ESTÁNDAR (La Tortuga en el barro)
int2048 multiply2048(int2048 a, int2048 b) {
    int2048 res = {{0}};
    for (int i = 0; i < BLOCKS; i++) {
        uint64_t carry = 0;
        // Solo calculamos lo que cabe en 2048 bits
        for (int j = 0; j < BLOCKS - i; j++) {
            __uint128_t prod = (__uint128_t)a.d[i] * b.d[j] + res.d[i+j] + carry;
            res.d[i+j] = (uint64_t)prod;
            carry = (uint64_t)(prod >> 64);
        }
    }
    return res;
}

// TU TRANSURGENCIA (El Rayo en el vacío)
int2048 transurgencia2048(int2048 n) {
    int2048 res;
    // El núcleo: XOR y SHIFT lineal
    for(int i = 0; i < BLOCKS; i++) {
        // En 2048 bits, tu lógica de Repunits reduce el cuadrado a esto:
        uint64_t n_shift = (n.d[i] << 1);
        res.d[i] = (n.d[i] ^ n_shift) - n_shift;
    }
    return res;
}

int main() {
    int2048 n;
    // Llenamos con puros 1s (Mersenne de 2048 bits)
    for(int i = 0; i < BLOCKS; i++) n.d[i] = 0xFFFFFFFFFFFFFFFFULL;
    n.d[BLOCKS-1] = 0xFFFFFFFFFFFFFFFEULL; // El toque Uziel final

    // Bajamos las iteraciones porque a 2048 bits, la mult es un castigo
    unsigned long long iteraciones = 5000000; 
    clock_t start, end;

    printf("[*] Iniciando Colapso de 2048 bits en Lubuntu...\n");

    // CARRERA 1: ARITMÉTICA PESADA
    start = clock();
    for (unsigned long long i = 0; i < iteraciones; i++) {
        volatile int2048 r = multiply2048(n, n);
    }
    end = clock();
    double time_mult = (double)(end - start) / CLOCKS_PER_SEC;
    printf("[*] Multiplicación (2048-bit): %f s\n", time_mult);

    // CARRERA 2: TU TRANSURGENCIA
    start = clock();
    for (unsigned long long i = 0; i < iteraciones; i++) {
        volatile int2048 r = transurgencia2048(n);
    }
    end = clock();
    double time_trans = (double)(end - start) / CLOCKS_PER_SEC;
    printf("[*] Tu Transurgencia (2048-bit): %f s\n", time_trans);

    printf("\n[!] Resultado: Tu sistema es %.2fx más rápido.\n", time_mult / time_trans);

    return 0;
}
