#include <iostream>
#include <string> // Necesario para std::getline si se usa, pero no en este caso.

int main() {
    // 1. Declaración de variables y entrada de usuario
    int Valor; // Usamos 'int' para enteros.
    
    std::cout << "Escriba un número: ";
    // Reemplaza input() de Python
    if (!(std::cin >> Valor)) { 
        // Manejo de error si la entrada no es un número (opcional pero buena práctica)
        std::cerr << "Error: Entrada no válida." << std::endl;
        return 1;
    }

    // El resto del código es una traducción directa de las operaciones:
    
    // Operaciones iniciales
    Valor = Valor % 8000000;
    Valor += 1 * 100 + 1 * 20000 + 1 * 4000000;
    
    // Variables de datos y control (se redefinen dentro del bucle, pero se inicializan aquí)
    int X = (Valor) % 100;
    int C = (Valor / 100) % 2; // División entera en C++
    int Y = (Valor / 200) % 100;
    int C1 = (Valor / 20000) % 2;
    int Z = (Valor / 40000) % 100;
    int C2 = (Valor / 4000000) % 2;

    int caso = 0;
    
    // Bucle 'while'
    while (caso != 3) {
        // Recálculo de variables dentro del bucle
        X = (Valor) % 100;
        C = (Valor / 100) % 2;
        Y = (Valor / 200) % 100;
        C1 = (Valor / 20000) % 2;
        Z = (Valor / 40000) % 100;
        C2 = (Valor / 4000000) % 2;

        // Algunas variables no se usan directamente pero se mantienen por coherencia con el original
        int actualizar_C = (Valor / 100); 
        int actualizar_C1 = (Valor / 20000) % 2; 
        int actualizar_C2 = (Valor / 4000000) % 2;
        
        // Variables de posición
        const int posicion_X = 100;
        const int posicion_Y = 20000;
        const int posicion_Z = 4000000;

        // Para los detectores (Puertas NOT)
        int D = 1 - C; 
        int D1 = 1 - C1; 
        int D2 = 1 - C2; 

        // Restas
        Valor -= D * posicion_Z + D1 * posicion_X + D2 * posicion_Y;

        // Sumas para reestablecer valores de control
        Valor += D * posicion_X + D2 * posicion_Z + D1 * posicion_Y;
        
        caso = C1 + C2 + C;
        // La línea comentada del Python original se mantiene comentada aquí:
        // Valor += actualizar_C + actualizar_C1 + actualizar_C2
    }
    
    // Re-evaluar los valores finales para la salida
    X = (Valor) % 100;
    C = (Valor / 100) % 2;
    Y = (Valor / 200) % 100;
    C1 = (Valor / 20000) % 2;
    Z = (Valor / 40000) % 100;
    C2 = (Valor / 4000000) % 2;

    // 2. Salida a consola (Reemplaza print() y f-string)
    std::cout << Valor << std::endl;
    
    // Salida con formato similar al f-string
    std::cout << "control 3: " << C2 << ",Z: " << Z 
              << ", control 2: " << C1 << ",Y: " << Y 
              << ",control 1: " << C << ",X: " << X << std::endl;
              
    std::cout << C2 << " " << Z << " " << C1 << " " << Z << " " << C << " " << X << std::endl;

    return 0;
}
