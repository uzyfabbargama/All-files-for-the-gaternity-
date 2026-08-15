>	Mueve el puntero a la derecha (siguiente celda).
<	Mueve el puntero a la izquierda (celda anterior).
+	Incrementa en 1 el valor de la celda actual.
-	Decrementa en 1 el valor de la celda actual.
.	Imprime el valor de la celda actual como carácter ASCII.
,	Lee un carácter del teclado y lo guarda en la celda actual.
[	Si la celda actual vale 0, salta al ] correspondiente (empieza bucle).
]	Si la celda actual NO vale 0, vuelve al [ correspondiente (fin bucle).


hmm, no es tan complejo
section .data
    font_code db "+"
section .bss
    cells resb 0x1000000 ;1 MB
section .text
global _start
_start:
	xor rsi, rsi
	xor r8, r8
	xor rbx, rbx ;para las células (cada célula es de 2 bytes, 1 byte para el valor, el otro valor para la dirección del bucle MAX 256
	;+
	constantes_mas plus
    ;-
    constans_generator minus
    ;<
    constans_generator left
    ;>
    constans_generator right
    %include "macros.inc"
    jmp loopProcess
loopProcess:
	crear_loop
	inc rsi
	mov dl, [font_code]
	cmp dl, 0 ;si hemos recorrido todo
	jz ready
	jmp loopProcess
ready:
	xor rsi, rsi ;empezamos de nuevo, ahora con los bucles pre-procesados
	jmp running
running:
	detectar_plus
	detectar_minus
	detectar_left
	detectar_right
	input_char
	output_char
	access_bucle_start
	access_bucle_end
	mov dl, [font_code]
	cmp dl, 0 ;si hemos recorrido todo
	jz exit
	jmp running
exit:
	mov rax, 60
	xor rdi, rdi
	syscall
