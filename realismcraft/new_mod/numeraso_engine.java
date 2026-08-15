public class NumerasoEngine {
    // Definición de posiciones (estáticas para máximo rendimiento)
    public static final int posZ = 0;
    public static final int posC1 = 10;
    public static final int posY = 11;
    public static final int posC2 = 21;
    public static final int posX = 22;
    public static final int posC3 = 32;

    // Máscara de 10 bits: 1023 (0x3FF)
    public static final long MASK10 = (1L << 10) - 1;

    public static long makeNumeraso(int a, boolean aC, int b, boolean bC, int c, boolean cC) {
        return ((long) (a & 0x3FF) << posZ) |
               ((aC ? 1L : 0L) << posC1) |
               ((long) (b & 0x3FF) << posY) |
               ((bC ? 1L : 0L) << posC2) | // Corregido: tú tenías posC1 repetido
               ((long) (c & 0x3FF) << posX) |
               ((cC ? 1L : 0L) << posC3);
    }

    // El "Corazón" de la lógica en Java (Branchless approach)
    public static long[] applyRules(long numeraso, long numerasoxp, 
                                   int aM, int bM, int cM, 
                                   int aA, int bA, int cA) {
        
        // Extracción rápida
        long a = (numeraso >> posZ) & MASK10;
        long b = (numeraso >> posY) & MASK10;
        long c = (numeraso >> posX) & MASK10;
        long c1 = (numeraso >> posC1) & 1;
        long c2 = (numeraso >> posC2) & 1;
        long c3 = (numeraso >> posC3) & 1;

        long ax = (numerasoxp >> posZ) & MASK10;
        long bx = (numerasoxp >> posY) & MASK10;
        long cx = (numerasoxp >> posX) & MASK10;

        // Mientras no todos los controles estén en 1 (tu lógica de 'caso')
        // En un mod de MC, para evitar bucles infinitos en el tick de servidor,
        // solemos procesar esto una vez por tick.
        
        long d1 = 1 - c1;
        long d2 = 1 - c2;
        long d3 = 1 - c3;

        // Lógica aritmética (usamos long para evitar overflow antes de la suma)
        long aRes = (a / (1 + ax)) * d1;
        long bRes = (b / (1 + bx)) * d2;
        long cRes = (c / (1 + cx)) * d3;

        long sumas = ((long)aA << posZ)*d1 + ((long)bA << posY)*d2 + ((long)cA << posX)*d3;
        long restas = ((long)aM << posZ)*d1 + ((long)bM << posY)*d2 + ((long)cM << posX)*d3;

        numeraso += sumas + (aRes << posZ | bRes << posY | cRes << posX);
        numeraso -= restas;

        // Reset de XP (Tu maker de salida)
        numerasoxp = makeNumeraso((int)ax, true, (int)bx, true, (int)cx, true);
// Agregamos esto a tu clase NumerasoEngine
	public static long sellarNumeraso(long numeraso, String playerName) {
    	// Usamos tu lógica de xorid para generar un ID único del nombre
    	long dna = 0;
    	for (byte b : playerName.getBytes()) {
        	dna = (dna ^ b) << 1;
    	}
    	// Limpiamos los bits superiores y pegamos el ADN en el "techo" del long
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
    return new long[]{numeraso, numerasoxp};
    }
}
