;#########################################################
;##  MOTOR XIP - VERSIÓN ULTRA-OPTIMIZADA (NASM x64)    ##
;#########################################################
section .text
global _xip_parse

;################
;##   Macros   ##
;################
%macro UPDATE_KW 2 
        mov r9, r15      ;obtener el mapa completo
        xor r9, %2        ;Si es 0 no lo destruye, si es 1, si    
        shr r9, %1       ;desplazado r9 para el tipo de keyword
        and r9, 0x1      ;toma un solo bit
        xor r15, r9     ;Reinicia estado de 1 → 0
        ;Si condición: 0 + keyword 1 = keyword 1
        ;Si condición: 1 + keyword 1 = keyword 0
    %endmacro
%macro save_id 0
    test r14, r14             ; 1. ¿El ID es 0? Si es 0, no hay nada que guardar.
    jz %%skip_save            ; 2. Si es 0, saltamos la escritura (evita corromper el inicio).
    
    ; --- LIMITADOR DE SEGURIDAD (Opcional pero recomendado) ---
    cmp r14, 131072           ; 3. ¿El ID es mayor que nuestro buffer de 1MB?
    jae %%skip_save           ; 4. Si es muy grande, abortamos para evitar el Segfault.

    mov [r10 + r14 * 8], r12  ; 5. ¡INYECCIÓN REAL! 
    xor r14, r14              ; 6. Limpiamos ID para la siguiente variable.
    xor r12, r12              ; 7. Limpiamos Valor para la siguiente variable.
%%skip_save:
%endmacro
 %macro xif 2 ; posición, valor  
    xor r8, r8  
    xor r9, r9 
    mov r8b, byte [rdi + rsi] ; rdi es nuestro INPUT (puntero)
    shl r8, 1         
    xor r8b, byte [rdi + rsi + 1]
    shl r8, 1  
    cmp r8, %2  
    setz r9b                  ; Correcto: r9b
    shl r9, %1   
%endmacro
 %macro do_in 1 
     or %1, r9 
 %endmacro 
 
%macro if 2 ; posición, valor_ascii
    mov r9, 0 
    mov r9b, dl               ; rdx ya trae el byte en el bucle
    xor r9b, %2 
    mov r9, 0 
    setz r9b 
    shl r9, %1 
%endmacro
%macro sumar_indice 0
    add rsi, r9        
%endmacro 
%macro mul_10 0 ;MACRO ACTUALIZADA PARA 64 BITS
    ; Solo multiplicamos si r9 es 1
    test r9, r9
    jz %%skip_mul
    imul r12, 10
%%skip_mul:
%endmacro
 %macro suma_cond 1 
    xor rax, rax            
    mov rax, r9         
    neg rax             
    and rax, %1         
    add r12, rax        
%endmacro 

 %macro xorid 0 
    mov r11, r14                
    add r9, 0xFFFFFFFFFFFFFFFF  
    and r11, r9     
    xor r11b, byte [rdi + rsi]  ; Asegúrate que aquí diga rdi, no INPUT
    add r9, 2       
    and r9, 1       
    
    ; --- CORRECCIÓN TÉCNICA ---
    mov rcx, r9                 ; Movemos r9 a rcx para usar cl
    shl r11, cl                 ; Ahora sí: cl es el único permitido
    ; --- EL FILTRO DE 1 MB ---
    ; Esto asegura que r11 nunca sea mayor a 131,071
    and r11, 0x1FFFF  ; <--- MÁSCARA MÁGICA
    ; Filtro de espacio
    cmp dl, " "
    cmovnz r14, r11 
 %endmacro

  %macro skip 0 
     add rsi, r9;avanza el puntero de bytes, sólo si r9 es 1 
  %endmacro 

     ; %1 = Bit a testear 
     ; %2 = Registro donde mirar (r15 para keywords, r8 para números) 
     %macro elsecond 2 
    	mov rax, %2         ; Usar rax en lugar de rdx
    	shr ax, %1         
    	and rax, 1          
    	xor r9, rax         
    	xor r9, 1           
	%endmacro
   ; %1 = Bit a testear
    ; %2 = Registro donde mirar (r15 para keywords, r8 para números)

    %macro cond 2
    mov rax, %2     ;Accedemos al registro que TÚ decidas
    shr rax, %1     ;Movemos el bit al final
    and rax, 1      ;Filtramos
    and r9, rax     ;Cascada de éxito en r9
    %endmacro 
  %macro FIRSTcond 2
    mov rax, %2     ;Contexto
    shr rax, %1     ;tipo KW
    and rax, 1      ;Filtro and
    mov r9, rax     ;Iniciar
    %endmacro
%macro if_num 2 
    ; 1. ¿Es el carácter actual (dl) igual al dígito buscado?
    cmp dl, %2          
    
    ; 2. r9 se vuelve 1 si es igual, 0 si no. Sin arrastrar estados previos.
    setz r9b
    movzx r9, r9b
    
    ; 3. Si r9 es 1, operamos sobre r12. Si es 0, las macros no hacen nada.
    mul_10
    suma_cond %1    ; %1 es el valor numérico (0-9)
 %endmacro
_xip_parse:
    mov r10, rsi  ; Puntero a memoria
    mov r10, rsi  ; Por si acaso
    xor rsi, rsi  ; Índice string
    xor r14, r14  ; ID
    xor r15, r15  ; Estados
    xor r12, r12  ; Valor acumulado
next_char:
    movzx rdx, byte [rdi + rsi] 
    test dl, dl                 
    jz exit_parse
    ; --- BLOQUE 1: DETECTOR DE TRAMA (Prioridad Alta) ---
    ; Detectar "::"
    xif 0, 156
    test r9, r9
    jz .check_comma
    UPDATE_KW 0, 1    ; Cambiar a Modo Número
    add rsi, 2        ; Saltar "::"
    jmp next_char

.check_comma:
    ; Detectar ",,"
    xif 1, 232
    test r9, r9
    jz .bloque_identidad
    save_id           ; Guardar valor
    xor r15, r15      ; Reset total de estados
    add rsi, 2        ; Saltar ",,"
    jmp next_char
	.bloque_identidad:
    ; --- BLOQUE 2: IDENTIDAD (xorid) ---
    FIRSTcond 0, r15
    test r9, r9       ; ¿Estamos en Modo Key (bit 0 == 0)?
    jnz .bloque_numeros
    xor r9, r9		  ; limpia, resultado de xif
    xorid             ; Calcula ID con máscara 0x1FFFF
    inc rsi           ; Avanzar carácter del nombre
    jmp next_char
        ; --- 5. BLOQUE VALOR (bloq_num.asm) ---
    ; Necesitamos el inverso de r9 para este bloque
    FIRSTcond 0, r15    ; r9 = 1 solo si ya pasamos por "::"
    ; ############################################
	; BLOQUE DE INYECCIÓN NUMÉRICA (0-9)
	; ############################################
	.bloque_numeros:
    ; Si r15 bit 0 es 1, llegamos aquí. rdx ya tiene el carácter actual (dl).
    
    if_num 1, "1"
    if_num 2, "2"
    if_num 3, "3"
    if_num 4, "4"
    if_num 5, "5"
    if_num 6, "6"
    if_num 7, "7"
    if_num 8, "8"
    if_num 9, "9"
    if_num 0, "0"
	inc rsi
    jmp next_char
    ; --- 2. DETECTOR DE TRAMA (Macros XIF) ---
    ; Aquí detectamos los muros :: y ,,
    xif 0, 156   ; Detecta "::" -> Bit 0
    test r9, r9
    jz .no_tokens
    UPDATE_KW 0, 1    ; Activamos/Alternamos Bit 0 de r15
    ; Si r9=1, sumamos 2 a rsi para saltar el "::" completamente
    add rsi, 2   ; Saltamos los 2 bytes de "::"
    jmp next_char ; ¡CLAVE! Volvemos arriba para procesar el primer número sin el 'inc rsi'

.no_tokens:
    xif 1, 232   ; Detecta ",," -> Bit 1
    test r9, r9
    jz .no_save
; Si llegamos aquí, r9 es 1
    save_id           ; ¡Inyección!
    ; Nota: do_in r15 aquí sería redundante porque UPDATE_KW ya opera sobre r15
    xor r15, r15
    add rsi, 2
    jmp next_char 
.no_save:
    ; --- 3. EL SWITCH ARITMÉTICO (elsecond) ---
    ; Si bit 0 de r15 es 0 -> Modo Identidad
    ; Si bit 0 de r15 es 1 -> Modo Inyección
    elsecond 0, r15 
    


    
; --- EL FILTRO DE ESCAPE ---
    ; Si r9 terminó en 1 después de pasar por los dígitos, 
    ; significa que SÍ procesamos un número y rsi ya avanzó gracias a 'sumar_indice'.
    test r9, r9
    jnz next_char  ; Si procesamos un número, saltamos arriba de inmediato.

    ; Si llegamos aquí, NO era un número.
    inc rsi        ; Avanzamos 1 byte (para no quedar en bucle infinito)
    jmp next_char
	
exit_parse:
    ret
section .note.GNU-stack noalloc noexec nowrite progbits
