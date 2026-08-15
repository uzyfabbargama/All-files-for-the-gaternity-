# Ensamblar con información de depuración DWARF
nasm -f elf64 -g -F dwarf brain_funk.asm -o brain_funk.o

# Enlazar (sin strip, para mantener los símbolos)
ld brain_funk.o -o brain_funk

# Ejecutar con GDB
gdb ./brain_funk
