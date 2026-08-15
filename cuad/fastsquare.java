public static long transurgenteSquare(long n) {
    // 1. El Peaje: ¿Es puro 1s (Mersenne) o termina en 0 (Casi-Mersenne)?
    // Usamos (n | 1) para que el truco funcione con ambos casos
    long test = n | 1;
    if (test > 0 && (test & (test + 1)) == 0) {
        
        // Obtenemos la posición del bit más alto
        int b = 64 - Long.numberOfLeadingZeros(n);
        
        // 2. Tu Geometría de Bits (Duplicar y XOR)
        long x = (n << (b + 1)) ^ (n << 1);
        long r = n ^ x;
        
        // 3. La Compensación Eureka (Si terminaba en 0, restamos 2n)
        if ((n & 1) == 0) {
            return r - (n << 1);
        }
        return r;
    }
    
    // El camino aburrido de Mojang
    return n * n;
}
