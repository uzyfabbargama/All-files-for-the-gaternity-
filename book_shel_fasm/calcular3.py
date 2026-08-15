#01001111
c = 0x3031303031313131 
c &= 0x0101010101010101 

# Multiplicamos por la constante de dispersión de potencias de 2
#magica = 0x8040201008040201
magica = 0x0102040810204080
resultado = (c * magica) & 0xFFFFFFFFFFFFFFFF

# El resultado ordenado queda en el byte más alto (Byte 7)
final = resultado >> 56

print(f"Bits compactados reales: {bin(final)}")
