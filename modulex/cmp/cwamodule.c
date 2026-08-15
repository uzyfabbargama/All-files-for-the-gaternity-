#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ITERATIONS 1000000

int main() {
    char input[] = "num: 12345, mod: 10, sto: 1,";
    clock_t start = clock();
    
    for (int i = 0; i < ITERATIONS; i++) {
        // Extraer el número del string
        char *num_start = strstr(input, "num: ") + 5;
        long num = atol(num_start);
        
        // Extraer el módulo
        char *mod_start = strstr(input, "mod: ") + 5;
        long mod = atol(mod_start);
        
        // La operación
        long result = num % mod;
    }
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    printf("C: %f segundos\n", time_spent);
    
    return 0;
}
