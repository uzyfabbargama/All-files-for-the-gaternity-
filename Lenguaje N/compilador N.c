#include <stdint.h>
#include <stdio.h>

// Definición de la memoria del sistema. El ID CPC es el índice.
// Asumimos un máximo de 1000 variables CPC para el ejemplo.
#define MEMORY_SIZE 1000
uint64_t REGISTRO_CPC[MEMORY_SIZE];

// Constantes de tu sistema (la base que usaste en BHL, CHS, NS.py)
#define BASE 1000 
#define UMBRAL_BASE 100 // Para el ejemplo de umbral 100

// La IND generada por el parser.
// Ejemplo: 19009 (Simula una operación densa)
typedef uint64_t InstruccionDensa;

// Función que extrae el valor o flag de una posición CPC sin usar división lenta.
// En un compilador real, el Posicionamiento (base * 1000^N) se traduce a un bit-shift
uint64_t extraer_valor_cpc(InstruccionDensa ind, uint64_t posicion_cpc) {
    // Si la posición fuera una potencia de 2 (ej. 2^10), esto sería un bit-shift instantáneo.
    // Usando tu base 1000, la optimización es trabajo del compilador C.
    // La operación más eficiente es la siguiente:
    
    // 1. Desplazar el IND a la posición del flag.
    uint64_t valor_desplazado = ind / posicion_cpc; 
    
    // 2. Extraer solo el dígito en esa posición (usando el módulo de la base).
    return valor_desplazado % BASE;
}
// =======================================================
// NUEVAS FUNCIONES PARA COMUNICACIÓN (Añadir a compilador N.c)
// =======================================================

// 1. Inicializa la memoria (REGISTRO_CPC) desde Python
// Es crucial para cargar los umbrales iniciales de tu archivo .N
// Declarado para ser exportado a la librería compartida
void inicializar_memoria(uint64_t id_cpc, uint64_t valor_inicial) {
    if (id_cpc < MEMORY_SIZE) {
        REGISTRO_CPC[id_cpc] = valor_inicial;
    }
}

// 2. Función Getter: Permite a Python leer el estado de una variable
// Esto verifica que la operación de C funcionó.
uint64_t obtener_estado_cpc(uint64_t id_cpc) {
    if (id_cpc < MEMORY_SIZE) {
        return REGISTRO_CPC[id_cpc];
    }
    return 0; // Retorna 0 si el ID es inválido
}

// Asegúrate que tu función ejecutar_operacion_densa no tenga la palabra 'static'
// para que sea visible externamente.
// (El resto del código de ejecutar_operacion_densa permanece igual).
// Ejecuta una operación densa (similar a Agente += Agente(consumo) * 100)
void ejecutar_operacion_densa(uint64_t id_bateria, uint64_t valor_consumo, InstruccionDensa ind_control_energia) {
    
    // Paso 1: Realizar la operación aritmética (el corazón de la lógica)
    // Asumimos que la operación es una resta del consumo total
    
    // La resta es una suma con complemento a dos. 
    // uint64_t valor_actual = REGISTRO_CPC[id_bateria];
    // uint64_t nuevo_valor = valor_actual - valor_consumo;
    
    // Simulamos la operación de tu Agente IA: batería(100) - 100
    uint64_t valor_restante = REGISTRO_CPC[id_bateria] - valor_consumo;
    
    // ----------------------------------------------------
    // Paso 2: Detección del Umbral (Acarreo / Overflow)
    // ----------------------------------------------------

    // En un sistema real, se verifica el "Carry Flag" del registro de la CPU.
    // Aquí, simulamos la lógica de umbral (si el valor cae por debajo de 0 o supera 100)
    
    int flag_acarreo = 0;
    
    // Comprobación de tu umbral: Si la batería era 100 y el consumo fue 100,
    // el valor restante es 0. Si el valor es <= 0, el umbral se cruza.
    if (valor_restante <= 0) {
        flag_acarreo = 1; // ¡El umbral se cruzó! (Simula el Acarreo)
    }

    REGISTRO_CPC[id_bateria] = valor_restante; // Actualiza el registro (la memoria)

    // ----------------------------------------------------
    // Paso 3: Ejecución de la Lógica Paralela (El Handler)
    // ----------------------------------------------------

    // Si hubo acarreo (1), la IND de control_energia se activa.
    if (flag_acarreo) {
        // En tu sistema, el IND contiene la fórmula {0, total += "string"}
        
        // Aquí, usamos la lógica BITWISE (simulada por flag_acarreo * X)
        // Lógica: Total += 1 (control_energía suma 1 al total de problemas)
        
        uint64_t id_total = extraer_valor_cpc(ind_control_energia, 1); // Extrae el ID del "Total" (ID CPC 1)
        
        // Esta es la operación BITWISE/Aritmética más rápida:
        // Suma 1 al registro total SOLO si el flag_acarreo es 1 (TRUE).
        REGISTRO_CPC[id_total] += 1; 

        // En un sistema real, esta IND también desencadenaría la impresión del string "Se ha acabado la energía"
    }
}