#include <iostream>
#include <vector>
#include <cmath> // Para la función pow()

// Definición de la función main() - el punto de inicio del programa
int main() {
    // 1. Declaración de variables iniciales usando long long para manejar números grandes
    const long long Base = 1000;
    // std::vector es el equivalente a las listas [] de Python
    std::vector<long long> Pos;
    std::vector<long long> PosCX;
    int i = 0;
    int d = 0;

    // 2. Primer bucle while para calcular y llenar los vectores Pos y PosCX
    std::cout << "--- Cálculos de Posiciones y Controles (Bucle 1) ---" << std::endl;
    while (i <= 6) {
        // Cálculo: Base^i * 2^d. Usamos std::pow() y convertimos a long long.
        // CUIDADO: std::pow opera con doubles, lo que puede introducir errores de precisión.
        // Para potencias de enteros, es más seguro implementar una función de potencia entera
        // o, como alternativa más simple aquí, convertir el resultado a long long.
        long long current_Pos = (long long)std::pow(Base, i) * (long long)std::pow(2, d);
        long long current_PosCX = (long long)std::pow(Base, i + 1) * (long long)std::pow(2, d);
        
        Pos.push_back(current_Pos);     // Equivalente a Pos.append()
        PosCX.push_back(current_PosCX); // Equivalente a PosCX.append()
        
        std::cout << Pos[i] << std::endl;
        std::cout << PosCX[i] << std::endl;
        
        i += 1;
        d += 1;
    } // end while

    std::cout << "--- Salida de variables predefinidas ---" << std::endl;
    
    // 3. Bloque de re-cálculo para la salida de ejemplo (traducción directa)
    const long long base = 1000;
    // Utilizamos potencias precalculadas o pow() con el tipo long long
    long long PosC2 = (long long)std::pow(base, 3) * (long long)std::pow(2, 2);
    long long PosX = (long long)std::pow(base, 2) * (long long)std::pow(2, 2);
    long long PosC1 = (long long)std::pow(base, 2) * 2;
    long long PosY = base * 2;
    long long PosC = base;
    long long PosZ = 1;
    
    std::cout << base << ", " << PosC2 << ", " << PosX << ", " << PosC1 << ", " << PosY << ", " << PosC << ", " << PosZ << std::endl;
    
    std::cout << "--- Construcción del Numeraso (Bucle 2) ---" << std::endl;

    // 4. Segundo bucle while para construir el 'Numeraso'
    i = 0;
    d = 0;
    long long Numeraso = 0; // Inicializar en 0
    
    // Nota: El código Python usa 'd' como índice para PosCX, pero 'd' e 'i' son iguales.
    while (i <= 6) {
        // Suma de los elementos del vector
        Numeraso += Pos[i] + PosCX[d]; 
        i += 1;
        d += 1;
    } // end while
    
    std::cout << "Numeraso total construido: " << Numeraso << std::endl;

    return 0;
}
