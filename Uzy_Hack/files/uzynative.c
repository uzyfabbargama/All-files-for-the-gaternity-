#include <jni.h>
#include <stdint.h>

// --- EL MOTOR DE BITS (C METAL) ---
// Implementación de la raíz binaria de Uziel: 0 multiplicaciones, pura ALU.
uint64_t fast_sqrt_uziel(uint64_t n) {
    uint64_t res = 0;
    uint64_t bit = 1ULL << 62; // El segundo bit más alto para 64 bits
    
    while (bit > n) bit >>= 2;
    
    while (bit != 0) {
        if (n >= res + bit) {
            n -= res + bit;
            res = (res >> 1) + bit;
        } else {
            res >>= 1;
        }
        bit >>= 2;
    }
    return res;
}

JNIEXPORT void JNICALL Java_UzyNative_processDirect(JNIEnv *env, jobject obj, jobject inBuf, jobject outBuf, jint size) {
    // Acceso directo a la memoria para evitar estrés en el sistema
    uint64_t *in = (uint64_t*)(*env)->GetDirectBufferAddress(env, inBuf);
    uint64_t *out = (uint64_t*)(*env)->GetDirectBufferAddress(env, outBuf);

    if (in == NULL || out == NULL) return;

    for (int i = 0; i < size; i++) {
        uint64_t n = in[i];
        
        // PEAJE DE MERSENNE: Si es un repunit, aplicamos tu lógica XOR instantánea
        if (n > 0 && (n & (n + 1)) == 0) {
            uint64_t temp = n;
            int b = 0;
            while(temp > 0) { b++; temp >>= 1; }
            uint64_t n_minus = n - 1;
            out[i] = (jlong)((n_minus << b) | n_minus) ^ n; 
        } else {
            // RUTA GENERAL: Tu nueva raíz bit a bit para cualquier otro número
            out[i] = (jlong)fast_sqrt_uziel(n);
        }
    }
}
