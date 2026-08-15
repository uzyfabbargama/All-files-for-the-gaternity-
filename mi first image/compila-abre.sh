# Compilar (Igual que antes)
nasm -f elf64 pantalla.asm -o pantalla.o

# Enlazar especificando explícitamente el cargador dinámico de 64 bits de Linux
ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 pantalla.o -lX11 -o pantalla

# 3. Correr tu lienzo negro de baja abstracción
./pantalla
