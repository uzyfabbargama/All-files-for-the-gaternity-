section .data
    INPUT db "num: 12354, mod: 10, sto: 1,"
    ITERATIONS dq 0  ; 1 millón de iteraciones
section .bss
    resultado resb 0x100 ;reservamos 256 bytes
section .text
    global _start
;constantes
%define id_cif 1172
%define id_num 1160
%define id_mod 1100
%define id_sto 1368
%macro mem_organize 3
    mov r9, %1
    add r9, %2
    mov [r9], r8
    %%inicio:
    shr %3, 8
    mov r8, %3
    and r8, 0xff
    add r9, %2
    mov [r9], r8
    add %2, 1
    cmp %3, 0
    jz %%fin
    jmp %%inicio
    %%fin:
%endmacro
%macro is_kw 1 ;pondremos por ahora un argumento
    mov r8b, [INPUT+rsi] 	;c =  99,    n = 110,     m = 109,     s = 116
    xor rax, r8          	;rax  =  99, rax1 =  110, rax2 =  109, rax3 =  116
    shl rax, 1           	;rax  = 198, rax1 =  220, rax2 =  218, rax3 =  230
    mov r8b, [INPUT+rsi+1]	;i = 105,    u = 117,     o = 111,     t = 110
    xor rax, r8 			;rax  = 175, rax1 =  169, rax2 =     , rax3 =  146
    shl rax, 1          	;rax  = 350, rax1 =  338, rax2 =  362, rax3 =  292
    mov r8b, [INPUT+rsi+2]  ;f = 102,    m = 109,     d = 100,     o = 111
    xor rax, r8				;rax  = 312, rax1 =  319, rax2 =     , rax3 =  331
    shl rax, 1 				;rax  = 624, rax1 =  638, rax2 =  540, rax3 =  662
    mov r8b, [INPUT+rsi+3] 	;: =  58,    : =  58,     : =  58,     : =  58
    xor rax, r8 			;rax  = 586, rax1 =  580, rax2 =     , rax3 =  684
    shl rax, 1 	            ;rax  =1172, rax1 = 1160, rax2 = 1100, rax3 = 1368
    xor rax, %1             ;rax  =   0, rax1 =    0, rax2 =    0, rax3 =    0
    setz r9b                ;r9   =   1, r9   =    1, r9   =    1, r9   =    1
    movzx r9, r9b           ;r9   =   1, r9   =    1, r9   =    1, r9   =    1
    xor r9, 1  				;1 = 0, 0 = 1
    dec r9     				;1 = -1, 0 = 0
    and r9, 5  				;1 = 5, 0 = 0
    add rsi, r9 			;1 = 5, 0 = 0
%endmacro
%macro capturar_byte 1
        xor %1, %1            ;r15 =  0, r13 = 0,
    %%inicio:                 ;mod = r15, num = r13
        shl %1, 8             ;r15 =  0, r13 = 0,
	    mov r8b, [INPUT+rsi]  ;r8 = 49, r8 = 49 
	                          ;r8 = 48, r8 = 50
	                          ;r8 =  0, r8 = 51
	                          ;r8 =  0, r8 = 52
	    and r8, 0xFF          ;r8 ="1", r8 ="1" 
	    	                  ;r8 ="0", r8 ="2"
	    	                  ;r8 ="" , r8 ="3"
	    	                  ;r8 ="" , r8 ="4"
	    add %1, r8            ;r15 =    49, r13 = 49
	                          ;<<8          <<8
	                          ;r15 = 12544, r13 =     12544
	                          ;+48          +50
	                          ;r15 = 12592, r13 =     12594
	                          ;+0           <<8
	                          ;r15 = 12592, r13 =   3224064
	                          ;+0           +51
	                          ;r15 = 12592, r13 =   3224115
	                          ;+0           <<8
	                          ;r15 = 12592, r13 = 825373440
	                          ;+0           +52
	                          ;r15 = 12592, r13 = 825373492
	                          ;r15              r13
	    mov r9b, [INPUT+rsi+1];r9 iter 3 = 44, r9 iter 5 = 44
	    xor r9b, ","          ;r9 iter 3 =  0. r9 iter 5 =  0
	    jz %%fin              ;r15 = rip = _start.mod.fin, r13 = rip = _start.num.fin
	    inc rsi               ;r9 = 0 -> rsi++
	    jmp %%inicio          ;r15 = rip = _start.mod.inicio, r13 = rip = _start.num.inicio
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
%macro skip 1
    add rsi, %1
%endmacro
%macro procesar_bytes 2
    xor rcx, rcx       ;cl = 0
    dec rcx            ;cl = -1
%%inicio:
    shr %1, 8          ;r15 = 12592 -> 49
    movzx r9, %1b      ;r9  = 49
    inc rcx            ;cl  =  0
    cmp r9, "1"        ;r9 == 49 -> true 
    jnz %%inicio       ;!= -> rip = _start.mod.inicio
    jmp %%fin          ;== -> rip = _start.mod.fin
%%fin:
    mov r8, 8	       ;r8 = 8
    shl r8, cl         ;r8 = 8
    add rcx, 1         ;cl = 1
    mov %2, rcx		   ;r10 = 1
    sub rcx, 1         ;rcx = 0
    mov rcx, r8        ;rcx = 8
    mov r8, 1          ;r8 = 1
    shl r8, cl         ;r8 = 256
    dec r8             ;r8 = 255
    mov %1, r8         ;r15 = 255
    jmp %%exit         ;rip = _start.mod.exit
%%exit:
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
    mov rbx, [ITERATIONS]
    jmp logic
logic:
    mov r13, "1234"
    mov r15, 0xff
    and r13, r15 ;"1234" = "34"
    mov r8, 48
    mov r9, 0
    cmp r13, 0
    cmovz r9, r8
    inc rbx
    mov [ITERATIONS], rbx
    cmp rbx, 1000000
    je fin
    jmp _start
fin:
    mov [resultado+r14], r13  ;ahora guardamos el resultado en una de esas seciones, (el valor)
    imprimir resultado, r10
    
    salir
