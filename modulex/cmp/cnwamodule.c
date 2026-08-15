#include <stdio.h>
#include <time.h>

#define ITERATIONS 1000000

int main() {
    // El número ya está como entero (simulando que ya lo parseamos)
    long num = 12345;
    long mod = 10;
    
    clock_t start = clock();
    
    for (int i = 0; i < ITERATIONS; i++) {
        long result = num % mod;
    }
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("C optimizado: %f segundos\n", time_spent);
    
    return 0;
}
