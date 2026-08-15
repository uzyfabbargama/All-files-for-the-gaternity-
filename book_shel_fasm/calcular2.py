# 1. Tu string original en ASCII: "01001111"
c = 0x3031303031313131 

# 2. Nos quedamos SOLO con el bit bajo de cada carácter
c &= 0x0101010101010101 

# 3. Multiplicación mágica (Suma y desplaza en paralelo)
# Usamos una máscara de 64 bits de entrada para simular el registro de tu CPU
mágica = 0x0101010101010101
resultado = (c * mágica) & 0xFFFFFFFFFFFFFFFF

# 4. Los bits se juntaron en el byte más alto. Al hacer shr 56, los bajamos al inicio.
final = resultado >> 56

print(f"Bits compactados en entero: {bin(final)}")
