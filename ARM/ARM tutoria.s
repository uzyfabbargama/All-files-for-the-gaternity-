//x0 - x7 → temporales
//Aquí pasas los argumentos a tus funciones y recibes el resultado (en x0).
//x8 El Portero → temporales
//Crucial en Android: Aquí pones el número de la syscall (ej. 93 para exit).
//x9 - x15 → borrador → temporal
//Úsalos para cálculos rápidos. Si llamas a una función, esta puede borrarlos sin permiso.
//x16 - x17 → Intra-Call → temporales
//Los usa el enlazador (linker). Mejor no tocarlos si no es necesario.
//x19 - x28 → Cajas Fuertes → permanentes
//Ideales para tu Contexto de Keywords o el xorid. Si los usas, debes restaurarlos al final.

//Registros de Propósito Especial (PS)
//x29 (FP - Frame Pointer): Para rastro de la pila (como tu rbp).
//x30 (LR - Link Register): Guarda la dirección a la que debes volver después de un ret. Es tu salvavidas para no perderte.
//sp (Stack Pointer): Puntero de la pila. Ojo: En ARM64 debe estar alineado a 16 bytes o el celular te dará un error.
//xzr (Zero Register): Es un registro que siempre vale 0. Si escribes en él, el dato desaparece. Si lees de él, obtienes 0. (Ahorra muchos mov x0, 0).
//pc (Program Counter): La dirección de la instrucción actual. No puedes moverle datos directamente con mov.
//Se llaman NZCV y están dentro del registro de estado:

    //N (Negative)

    //Z (Zero) -> Este es el que usas con cset para tu lógica de comparaciones.

    //C (Carry)

    //V (oVerflow)
 