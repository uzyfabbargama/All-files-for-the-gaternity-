package net.mcreator.uzyopt;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class UzyGridBridge {
    public static UzyGridBridge instance = new UzyGridBridge();
    
    // Cargar la librería nativa (tus códigos en C)
    static {
        try {
            System.loadLibrary("uzynative");
        } catch (UnsatisfiedLinkError e) {
            System.err.println("UzyNative no encontrada, usando fallback en Java");
        }
    }

    // --- EL FILTRO DE PRECISIÓN (Sustituye a DADD en el Bytecode) ---
    // Este método será llamado por Minecraft cada vez que sume una posición
    // En UzyGridBridge.java
	public static void processChunkBatch(ByteBuffer buffer, int count) {
    	// Mandamos el buffer directo a tu C para que procese 
    	// 1000 posiciones de chunks en un solo ciclo de CPU
    	instance.processDirect(buffer, buffer, count); 
	}
    public static double preciseAdd(double pos, double motion) {
        // Convertimos a nuestro sistema de punto fijo de 64 bits
        long lPos = (long) (pos * 1000000L);
        long lMotion = (long) (motion * 1000000L);
        
        // Aplicamos tu lógica de Mersenne/Peajes para evitar el jitter
        long result = uzyLogic64(lPos, lMotion);
        
        return (double) result / 1000000.0D;
    }

    private static long uzyLogic64(long p, long m) {
        long res = p + m;
        // Si el resultado cae en un número de Mersenne, aplicamos tu 'Transurgencia'
        if (((res + 1) & res) == 0 && res > 0) {
            return res ^ (p >> 32); // Estabilización por bit-flip
        }
        return res;
    }

    // --- INTEGRACIÓN CON TU C PURO ---
    public native long processNativePrecision(long p, long m);
}
