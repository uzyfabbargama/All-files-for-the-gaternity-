#include <stdio.h>
#include <time.h>

int main() {
    long iterations = 10000; // Subimos a 100 Millones porque C es demasiado rápido
    unsigned int sum = 0;
    
    struct timespec start, end;
    
    // --- INICIO DE LA CARRERA ---
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    for (long i = 0; i < iterations; i++) {
        // Tu método de casi-repunits (x2) en C puro
        sum += (i ^ (i << 1)); 
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    // --- FIN DE LA CARRERA ---

    double time_taken = (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);
    
    printf("--- RESULTADOS EN C ---\n");
    printf("Iteraciones: %ld\n", iterations);
    printf("Tiempo total: %.0f ns\n", time_taken);
    printf("Promedio por operacion: %.2f ns\n", time_taken / iterations);
    
    return 0;
}
