package net.mcreator.gnulmod;

public class NumerasoEngine {
    // Definición de posiciones (10 bits de variable + 1 de CTRL)
    public static final int posZ = 0;
    public static final int posC1 = 10;
    public static final int posY = 11;
    public static final int posC2 = 21;
    public static final int posX = 22;
    public static final int posC3 = 32;

    public static final long MASK10 = (1L << 10) - 1;

    public static long makeNumeraso(int a, boolean aC, int b, boolean bC, int c, boolean cC) {
        return ((long) (a & 0x3FF) << posZ) |
               ((aC ? 1L : 0L) << posC1) |
               ((long) (b & 0x3FF) << posY) |
               ((bC ? 1L : 0L) << posC2) |
               ((long) (c & 0x3FF) << posX) |
               ((cC ? 1L : 0L) << posC3);
    }

    public static long[] applyRules(long numeraso, long numerasoxp, 
                                   int aM, int bM, int cM, 
                                   int aA, int bA, int cA) {
        
        // Extracción inicial de estados y controles 
        long a = (numeraso >> posZ) & MASK10;
        long b = (numeraso >> posY) & MASK10;
        long c = (numeraso >> posX) & MASK10;
        
        long c1 = (numeraso >> posC1) & 1;
        long c2 = (numeraso >> posC2) & 1;
        long c3 = (numeraso >> posC3) & 1;

        // Registro de experiencia (XP) 
        long ax = (numerasoxp >> posZ) & MASK10;
        long bx = (numerasoxp >> posY) & MASK10;
        long cx = (numerasoxp >> posX) & MASK10;

        // El bucle de Homeostasis: el sistema itera hasta que los controles se estabilizan 
        long caso = c1 + c2 + c3;
        int seguridad = 0; // Para evitar cualquier anomalía externa
        
        while (caso != 3 && seguridad < 256) {
            long d1 = 1 - c1;
            long d2 = 1 - c2;
            long d3 = 1 - c3;

            // Cálculo de transformación (la "resistencia" del XP al cambio) 
            long aRes = (a / (1 + ax)) * d1;
            long bRes = (b / (1 + bx)) * d2;
            long cRes = (c / (1 + cx)) * d3;

            // Aplicación de fuerzas externas (sumas y restas) 
            long sumas = ((long)aA << posZ)*d1 + ((long)bA << posY)*d2 + ((long)cA << posX)*d3;
            long restas = ((long)aM << posZ)*d1 + ((long)bM << posY)*d2 + ((long)cM << posX)*d3;

            numeraso += sumas + (aRes << posZ | bRes << posY | cRes << posX);
            numeraso -= restas;
            
            // Actualizamos los controles tras la transformación
            c1 = 1; c2 = 1; c3 = 1; 
            caso = c1 + c2 + c3;
            seguridad++;
        }

        // El XP evoluciona según el estado alcanzado 
        numerasoxp = makeNumeraso((int)a, true, (int)b, true, (int)c, true);

        return new long[]{numeraso, numerasoxp};
    }

    public static long sellarNumeraso(long numeraso, String playerName) {
        long dna = 0;
        for (byte b : playerName.getBytes()) {
            dna = (dna ^ b) << 1;
        }
        return (numeraso & 0x1FFFFFFFFL) | (dna << 33);
    }

    public static boolean verificarADN(long numeraso, String playerName) {
        long dnaGuardado = numeraso >>> 33;
        long dnaActual = 0;
        for (byte b : playerName.getBytes()) {
            dnaActual = (dnaActual ^ b) << 1;
        }
        return dnaGuardado == dnaActual;
    }
}
