public class BitwiseRace {
    public static void main(String[] args) {
        int iterations = 10_000_000; // Subimos a 10M para que Lubuntu sude un poco
        long startTime, endTime;

        // --- MÉTODO ESTÁNDAR (JAVA LIB) ---
        startTime = System.nanoTime();
        long sumStd = 0;
        for (int i = 0; i < iterations; i++) {
            sumStd += Integer.bitCount(i); // Un ejemplo de operación estándar
        }
        endTime = System.nanoTime();
        long durationStd = (endTime - startTime);

        // --- TU MÉTODO (BITWISE XOR / REUNIT LOGIC) ---
        // Aquí aplicamos tu lógica de x ^ (x >>> 1) o similar para repunits
        startTime = System.nanoTime();
        long sumUzy = 0;
        for (int i = 0; i < iterations; i++) {
            // Simulando tu lógica de casi-repunits (x2)
            sumUzy += (i ^ (i << 1)) & 0xFFFFFFFF; 
        }
        endTime = System.nanoTime();
        long durationUzy = (endTime - startTime);

        System.out.println("--- RESULTADOS DE LA TRANSURGENCIA ---");
        System.out.println("Iteraciones: " + iterations);
        System.out.println("Java Standard: " + durationStd + " ns");
        System.out.println("Uziel Bitwise:  " + durationUzy + " ns");
        
        double diff = (double)durationStd / durationUzy;
        System.out.printf("¡Tu método es %.2fx más rápido!%n", diff);
    }
}
