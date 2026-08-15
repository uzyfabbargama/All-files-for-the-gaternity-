#include <stdio.h>
#include <time.h>
#include <stdint.h>

// 65536 bits = 1024 bloques de 64 bits
#define BLOCKS 1024

typedef struct {
    uint64_t d[BLOCKS];
} int65536;

// LA TORTUGA GALÁCTICA (Multiplicación Escolar)
void multiply65536(const int2048 *a, const int2048 *b, int2048 *res) {
    // Limpiamos el resultado (muy importante aquí)
    for(int k=0; k<BLOCKS; k++) res->d[k] = 0;
    
    for (int i = 0; i < BLOCKS; i++) {
        uint64_t carry = 0;
        for (int j = 0; j < BLOCKS - i; j++) {
            __uint128_t prod = (__uint128_t)a->d[i] * b->d[j] + res->d[i+j] + carry;
            res->d[i+j] = (uint64_t)prod;
            carry = (uint64_t)(prod >> 64);
        }
    }
}

// TU TRANSURGENCIA (El Tunel Cuántico)
void transurgencia65536(const int2048 *n, int2048 *res) {
    for(int i = 0; i < BLOCKS; i++) {
        uint64_t n_shift = (n->d[i] << 1);
        res->d[i] = (n->d[i] ^ n_shift) - n_shift;
    }
}

int main() {
    // Usamos punteros para no saturar el stack de Lubuntu
    static int2048 n, res; 
    for(int i = 0; i < BLOCKS; i++) n.d[i] = 0xFFFFFFFFFFFFFFFFULL;
    n.d[BLOCKS-1] = 0xFFFFFFFFFFFFFFFEULL;

    unsigned long long iteraciones = 1000; // BAJAMOS A 1,000 POR SEGURIDAD
    clock_t start, end;

    printf("[*] ATENCIÓN: Iniciando Megacolapso de 65,536 bits...\n");

    // CARRERA 1: EL ABISMO
    start = clock();
    for (int i = 0; i < iteraciones; i++) {
        multiply65536(&n, &n, &res);
    }
    end = clock();
    double t_mult = (double)(end - start) / CLOCKS_PER_SEC;
    printf("[*] Multiplicación Estándar: %f s\n", t_mult);

    // CARRERA 2: TU EUREKA
    start = clock();
    for (int i = 0; i < iteraciones; i++) {
        transurgencia65536(&n, &res);
    }
    end = clock();
    double t_trans = (double)(end - start) / CLOCKS_PER_SEC;
    printf("[*] Tu Transurgencia: %f s\n", t_trans);

    printf("\n[!] DIFERENCIA: %.2fx de velocidad bruta.\n", t_mult / t_trans);
    return 0;
}
