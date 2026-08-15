# Compilar (Igual que antes)
nasm -f elf64 pantallav2.asm -o pantallav2.o

# Enlazar especificando explícitamente el cargador dinámico de 64 bits de Linux
ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 pantallav2.o -lX11 -o pantallav2

# 3. Correr tu lienzo negro de baja abstracción
./pantallav2
