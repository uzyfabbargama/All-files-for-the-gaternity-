#include <stdint.h>

uint64_t fast_sqrt_uziel(uint64_t n) {
    uint64_t res = 0;
    uint64_t bit = 1ULL << 62;
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
// Definimos el ángulo como un entero de 64 bits [32 int][32 frac]
typedef int64_t uzy_angle_t;

// Esta función suma el movimiento del mouse directamente al ángulo global
// El desbordamiento (overflow) crea el círculo perfecto automáticamente
uzy_angle_t calculate_uzy_rotation(uzy_angle_t current, int64_t mouse_delta) {
    return current + mouse_delta;
}
