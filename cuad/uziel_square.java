public class UzielOptimizer {

    // El Peaje de Bits de Uziel
    public static long fastSquare(long n) {
        // Solo aceptamos n > 0 para evitar errores de bits leading zeros
        if (n <= 0) return n * n;

        // 1. Detección: ¿Es un número de puros 1s (7, 15, 31...)?
        // (n & (n + 1)) == 0 es el truco clásico para detectar Mersenne
        if ((n & (n + 1)) == 0) {
            int b = 64 - Long.numberOfLeadingZeros(n);
            return n ^ ((n << (b + 1)) ^ (n << 1));
        }

        // 2. Detección: ¿Es un Mersenne x 2 (6, 14, 30, 62...)?
        // Si al sumarle 2, los bits se "limpian", es un Casi-Mersenne par
        long testPar = n + 2;
        if (n > 2 && (n & 1) == 0 && (testPar & (testPar - 1)) == 0) {
            int b = 64 - Long.numberOfLeadingZeros(n);
            long x = (n << (b + 1)) ^ (n << 1);
            long r = n ^ x;
            return r - (n << 1); // Tu compensación Eureka
        }

        // 3. Si no es un número sagrado, usamos la aritmética de Mojang
        return n * n;
    }
}
