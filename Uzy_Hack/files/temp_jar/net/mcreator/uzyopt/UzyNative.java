import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class UzyNative {
    static {
        System.loadLibrary("uzynative");
    }

    // El método que habla directamente con la RAM de C
    public native void processDirect(ByteBuffer inputs, ByteBuffer outputs, int size);

    public static void main(String[] args) {
        int size = 1000000; // 1 Millón para empezar fuerte
        
        // Creamos Buffers Directos (8 bytes por cada long)
        ByteBuffer inBuf = ByteBuffer.allocateDirect(size * 8).order(ByteOrder.nativeOrder());
        ByteBuffer outBuf = ByteBuffer.allocateDirect(size * 8).order(ByteOrder.nativeOrder());

        UzyNative uzy = new UzyNative();

        // Llenamos los datos (como longs)
        for(int i = 0; i < size; i++) {
            inBuf.putLong(i * 8, (1L << ((i % 10) + 5)) - 1);
        }

        System.out.println("--- CARRERA MASIVA: DIRECT BUFFER ---");

        // --- ROUND 1: JAVA (Trabajando sobre el buffer) ---
        long startJava = System.nanoTime();
        for(int i = 0; i < size; i++) {
            long val = inBuf.getLong(i * 8);
            outBuf.putLong(i * 8, val * val);
        }
        long timeJava = System.nanoTime() - startJava;
        System.out.println("Java Standard: " + timeJava + " ns");

        // --- ROUND 2: UZY-TRANSURGENCIA (C puro sobre la misma RAM) ---
        long startC = System.nanoTime();
        uzy.processDirect(inBuf, outBuf, size);
        long timeC = System.nanoTime() - startC;
        System.out.println("Uzy Mass JNI:  " + timeC + " ns");

        System.out.println("\nEjemplo resultado[0]: " + outBuf.getLong(0));
        System.out.println("Diferencia: " + (double)timeJava / timeC + "x de velocidad.");
    }
}
