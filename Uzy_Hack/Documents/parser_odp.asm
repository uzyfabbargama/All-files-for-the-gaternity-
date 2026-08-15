d; ============================================
;  TRANSPILADOR DE PRESENTACIONES EN ASSEMBLER
; ============================================

section .data
    font_code db "diapositiva 1 : 
    titulo: 'Mi presentación' 
        ancho : ...
        alto : ...
        x : ...
        y : ... 
    subtitulo: 'Hola'
	    ancho : ...
	    alto : ...
	    x : ...
	    y : ...
	texto: 'Hola mundo'
		ancho: ...
		alto: ...
		y: ...
		x : ...
    ", 0
    ;ready db 0
    
    ; Hashes de keywords (calculados con tu algoritmo)
    keyword_diapositiva equ 136562
    keyword_titulo      equ 5542
    keyword_subtitulo   equ 47014
    keyword_texto       equ 2590
    keyword_ancho       equ 2214
    keyword_alto        equ 1150

section .bss
    buffer_titulo     resb 4096
    buffer_subtitulo  resb 4096
    buffer_texto      resb 4096

section .text
    global _start
;=========================
;=DEFINITIONS && MACROS  =
;=========================
%macro reservar_buffer 1
    push rsi                ; Guardar puntero al input
    push rbx                ; Guardar registro de trabajo
    mov rax, 9              ; sys_mmap
    xor rdi, rdi            ; Dirección (dejar al kernel)
    mov rsi, %1             ; Tamaño
    mov rdx, 3              ; PROT_READ | PROT_WRITE
    mov r10, 0x22           ; MAP_PRIVATE | MAP_ANONYMOUS
    mov r8, -1              ; fd = -1
    mov r9, 0               ; offset = 0
    syscall
    mov rbx, rax            ; Guardar puntero al buffer
    pop rbx                 ; Restaurar rbx
    pop rsi                 ; Restaurar puntero al input
%endmacro
%macro saltear_comentarios 0
        %%skip:
            mov al, [font_code+rsi]
            cmp al, "#"
            inc rsi
            je %%skip1
        %%skip1:
           mov al, [font_code+rsi
           cmp al, "10"
           inc rsi
           je %%skip1
%endmacro
%define keyword_diapositiva 136562
%define keyword_titulo 5542
%define keyword_subtitulo 47014
%define keyword_texto 2590

%macro leer_keyword 3 ; correcto, longitud, saltar si correctp
    xor r8, r8
    %rep %2 ;longitud
        mov al, [font_code+rsi]
        xor r8, al
        shl r8, 1
        inc rsi
    %endrep
    cmp r8, %1 ;correcto
    je %3
    sub rsi, %2 ;longitud
%endmacro

%define capturar_entre_10 0xF6
; = 246 en decimal = -10 en complemento a dos
; Se usa para detectar si un carácter es número (0-9)
; Si valor - 48 + 246 = 246-255 → bit alto = 1 → es número
; Si valor - 48 + 246 = 0-245 → bit alto = 0 → no es número

%define convertir_texto_a_num 48
; = ASCII '0'
; Convierte el carácter ASCII a su valor numérico

%define extraer_bit_alto_de_byte 7
; = Desplaza 7 bits a la derecha para obtener el bit más significativo
; En un byte, el bit 7 es el de signo (0-127 = positivo, 128-255 = negativo)

%define siguiente_byte 8
; = Desplaza 8 bits (1 byte) para guardar el siguiente dígito
; Ejemplo: si tienes "123", guardas '1', desplazas, guardas '2', etc.
    %rep 7
        mov al, [font_code+rsi]
        mov r9b, al
        sub r9b, convertir_texto_a_num
        add r9b, capturar_entre_10
        shr r9b, extraer_bit_alto_de_byte
        and r9b, 1
        jz %%no_num
        mov %1b, al
        shl %1, siguiente_byte
        inc rsi
    %endrep
    %%no_num
%endmacro
%macro detectar_espacio 0
    %%skip:
        mov al, [font_code +rsi]
        cmp al, " "
        jne %%fin
        inc rsi
        jmp %%skip
    %%fin:
%endmacro
%macro parsear_string 2
    mov rdi, %1          ; Buffer destino
    mov al, [font_code + rsi]
    cmp al, '"'
    je %%str_doble
    cmp al, "'"
    je %%str_simple
    jmp %%error

    %%str_simple:
        inc rsi
        %%simple_loop:
            mov al, [font_code + rsi]
            cmp al, "'"
            je %%ready
            mov [rdi], al
            inc rdi
            inc rsi
            jmp %%simple_loop

    %%str_doble:
        inc rsi
        %%doble_loop:
            mov al, [font_code + rsi]
            cmp al, '"'
            je %%ready
            mov [rdi], al
            inc rdi
            inc rsi
            jmp %%doble_loop

    %%ready:
        mov byte [rdi], 0   ; Null terminator
        inc rsi
        jmp %%fin

    %%error:
        ; Si no hay comillas, es error
        jmp error

    %%fin:
%endmacro
%define keyword_ancho 2214
%define keyword_alto 1150
%macro detectar_letra_normalizada 3
   mov al, [font_code+rsi]
   cmp al, %1
   je %3
   cmp al, %2
   je %%menor
   %%menor:
       sub al, 32
       je %3
%endmacro

%macro leer_ancho_alto 1 ;donde si falla
    leer_keyword keyword_ancho, 5, %%ancho
    leer_keyword keyword_alto, 4, %%alto    
    detectar_letra_normalizada "X", "x", %%x
    detectar_letra_normalizada "Y", "y", %%y
    %%ancho:
        detectar_espacio
        inc rsi
        mov al, [font_code+rsi]
        cmp al, ":"
        jne %1
        capturar_numstr r15
    %%alto:
        detectar_espacio
        inc rsi
        mov al, [font_code+rsi]
        cmp al, ":"
        jne %1
        captutar_numstr r14
    %%x:
        detectar_espacio
        mov al, [font_code +rsi]
        cmp al, ":"
        capturar_numstr r11
    %%y:
        detectar_espacio
        mov al, [font_code+rsi]
        cmp al, ":"
        capturar_numstr r13
%endmacro
_start:
    xor rsi, rsi
    saltear_comentarios
; estructura contenido
    leer_keyword keyword_diapositiva, 11, .struct_diapositiva
;diapositiva
.struct_diapositiva
    inc rsi
    capturar_numstr ;capturamos la diapositiva, en un numstr (no int, sino directamente el símbolo del número)
    inc rsi
    mov al, [font_code + rsi]
    cmp al, ":"
    jne error ;si no hay dos puntos, error
    leer_keyword keyword_titulo, 6, .struct_titulo
    leer_keyword keyword_subtitulo, .struct_subtitulo
    leer_keyword keyword_texto, .struct_texto
	
.struct_titulo:
;    inc rsi
    mov al, [font_code + rsi]
    cmp al, ":"
    jne error
    detectar_espacio
    reservar_buffer 4096 ;aquí la syscall
    mov rbx, rax ; movemos la dirección que nos dió el kernel
    parsear_string
    inc rsi
    leer_ancho_alto error
;subtiulo
.struct_subtitulo:
 ;   inc rsi
    mov al, [font_code + rsi]
    cmp al, ":"
    jne error
    detectar_espacio
    reservar_buffer 4096 ;aquí la syscall
    mov rbx, rax ; movemos la dirección que nos dió el kernel
    parsear_string
    inc rsi
    leer_ancho_alto error
.struct_texto:
  ;  inc rsi
    mov al, [font_code + rsi]
    cmp al, ":"
    jne error
    detectar_espacio
    reservar_buffer 4096 ;aquí la syscall
    mov rbx, rax ; movemos la dirección que nos dió el kernel
    parsear_string
    inc rsi
    leer_ancho_alto error
error:
	xor rdi, rdi
	mov rax, 60
	syscall


