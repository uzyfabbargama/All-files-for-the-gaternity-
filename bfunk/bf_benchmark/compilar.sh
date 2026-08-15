# Ensamblar el código
nasm -f elf64 brain_funk.asm -o brain_funk.o

# Enlazar
ld brain_funk.o -o brain_funk

# Verificar que funciona
./brain_funk
