;lo hicimos mal
section .data
    INPUT db "cif: 3, num: 123, mod: 10, sto: 1,"
section .bss
    resultado resb 0x100 ;reservamos 256 bytes
section .text
    global _start
;constantes
%define id_cif 1172
%define id_num 1160
%define id_mod 1100
%define id_sto 1368
%macro is_kw 1 ;pondremos por ahora un argumento
    mov r8b, [INPUT+rsi] ;tomamos el input byte x byte
    xor rax, r8          ;xoreamos
    shl rax, 1           ;desplazamos
    mov r8b, [INPUT+rsi+1]
    xor rax, r8
    shl rax, 1
    mov r8b, [INPUT+rsi+2]
    xor rax, r8
    shl rax, 1
    mov r8b, [INPUT+rsi+3]
    xor rax, r8
    shl rax, 1
    xor rax, %1
    setz r9b
    movzx r9, r9b
    xor r9, 1  ;1 = 0, 0 = 1
    dec r9     ;1 = -1, 0 = 0
    and r9, 5  ;1 = 5, 0 = 0
    add rsi, r9;1 = 5, 0 = 0
    ;mov rbx, %2 por ahora no es necesario
    ;jmp [rbx]
%endmacro
%macro capturar_byte 1
        xor %1, %1
    %%inicio:
        shl %1, 8            ;desplazamos 8
	    mov r8b, [INPUT+rsi] ;tomamos 1 byte
	    and r8, 0xFF
	    add %1, r8           ;(ahora acumulamosS)
	    
	    mov r9b, [INPUT+rsi+1];tomamos el siguiente byte y lo ponemos en r9
	    xor r9b, ","         ;si es una , (antes era r9, (8 bytes) mejor tomar byte por byte)
	    jz %%fin             ;detenemos
	    inc rsi              ;sino, incrementamos rsi
	    jmp %%inicio         ;y volvemos al inicio
	%%fin:
	    nop
%endmacro
%macro mul_10 1 
    test r9, r9
    jz %%skip_mul
    imul %1, 10
%%skip_mul:
%endmacro

%macro suma_cond 2 
    xor rax, rax            
    mov rax, r9         
    neg rax             
    and rax, %1         
    add %2, rax        
%endmacro

%macro if_num 3 
    cmp dl, %2          
    setz r9b
    movzx r9, r9b
    mul_10 %3 
    suma_cond %1, %3    
%endmacro

; --- 3. Macro Capturar Número (Corregida) ---
%macro capturar_numero 2
%%ciclo:
    mov dl, [%2 + rsi] ;<-- pusimos RDI, ups, culpa mía, reemplazamos a un argumento, para generalidad
    cmp dl, '0'
    jl %%fin
    cmp dl, '9'
    jg %%fin
    
    if_num 1, '1', %1
    if_num 2, '2', %1
    if_num 3, '3', %1
    if_num 4, '4', %1
    if_num 5, '5', %1
    if_num 6, '6', %1
    if_num 7, '7', %1 
    if_num 8, '8', %1
    if_num 9, '9', %1
    if_num 0, '0', %1
    
    inc rsi
    jmp %%ciclo
%%fin:
%endmacro
%macro procesar_bytes 2
    xor rcx, rcx
    dec rcx
    ror %1, 8          ; rotación de 8 BITs
%%inicio:
    shr %1, 8          ; "10" → "1"
    movzx r9, %1b      ; byte bajo después de rotar
    inc rcx
    cmp r9, "1"        ; ¿es '0'? (cuando damos vuelta bits)
    jnz %%inicio        ; si es 0x18, sigue rotando
    jmp %%fin
%%fin:
        mov r8, 8		;movemos 8 a r8
        shl r8, cl      ;desplazamos la cantidad de 0s a cl (si son 2 0s, cl = 1 8 → 16)
        add rcx, 1      ;como comenzamos en -1, hay que sumar 1, para el valor del contador real
        mov %2, rcx		;movemos la cantidad de bytes
        sub rcx, 1      ;lo llevamos al original
        mov rcx, r8     ;rcx ahora vale el 16 de r8
        mov r8, 1       ;r8, ahora vale 1
        ;add rcx, 1      ;le sumamos 1 (ahora vale 16)
        shl r8, cl      ;lo desplazamos 17 lugares
        dec r8          ;generamos una máscara que borra los primeros 2 bytes
        mov %1, r8      ;movemos esa máscara a nuestro primer argumento
%endmacro
%macro salir 0
    mov rax, 60         ; syscall exit
    xor rdi, rdi        ; status 0
    syscall
%endmacro

%macro imprimir 2          ; %1: buffer, %2: longitud
    mov rax, 1          ; syscall write
    mov rdi, 1          ; file descriptor stdout
    mov rsi, %1         ; dirección del buffer
    mov rdx, %2         ; tamaño a imprimir
    syscall
%endmacro
_start:
    sub rsi, rsi
    xor r9, r9
    xor rax, rax
    xor r8, r8
    jmp .cif
.cif:
    is_kw id_cif
    capturar_numero r12, INPUT;<--- ahora tiene generalidad
    jmp .num
.num:
    is_kw id_num
    capturar_byte r13
    jmp .mod
.mod:
    is_kw id_mod
    capturar_byte r15
    procesar_bytes r15, r10
    jmp .sto
.sto:
    is_kw id_sto
    capturar_numero r14, INPUT
    and r14, 0x100
   jmp logic
logic:
    mov r9, r12
    mov rcx, r12
    dec r9      ;restamos 1 (3 → 2)
    shl r9, cl  ;mul rcx (16)
    add cl, 1   ;sumamos 1
    shl r9, cl  ;r9 = 2¹⁷
    ;dec r9     ;r9 = 1 2e16
    mov r15, rcx
    shl r9, cl ;desplazamos los bytes de r15 byte
    xor r8, r8  ;r8 = 0
    dec r8      ;r8 = -1
    and r8, 0xff;r8 = 1 2e8
    or r9, r8   ;la máscara
    ;hacemos un and
    and r13, r9 ;"123" = "3"
    mov [resultado+r14], r13  ;ahora guardamos el resultado en una de esas seciones, (el valor)
   imprimir resultado, r10
   salir
