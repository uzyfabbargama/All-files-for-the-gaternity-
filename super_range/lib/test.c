#include <stdio.h>

// Declaramos tu función de Assembler
extern void _for_parser(char* input, long long* mente);

int main() {
    char* script = "sta:0 sto:100 ste:1 ";
    long long mente[100]; // Un buffer pequeño de prueba

    printf("Iniciando motor de hardware...\n");
    _for_parser(script, mente);
    printf("¡Éxito! El motor se detuvo.\n");
    
    return 0;
}
