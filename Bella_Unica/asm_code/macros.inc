;################
;##   Macros   ##
;################
%macro xif_multi 3 ; posición, valor, byte
	xor r8, r8
	xor r9, r9
	mov r8b, byte [rdi + rsi]
	%assign i 0
	%rep %2
	    xor r8b, byte [rdi + rsi + i]
		shl r8, 1
	%endrep
	xor r8, %2
	setz r9b
	add r9, %1
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
%macro xif_flex  2; posición, valor  
    xor r8, r8  
    xor r9, r9 
    mov r8b, byte [rdi + rsi] ; rdi es nuestro INPUT (puntero)
    shl r8, 1         
    xor r8b, byte [rdi + rsi + 1]
    shl r8, 1
    xor r8b, byte [rdi + rsi + 2] ;<--- Nueva función
    shl r8, 1  
    cmp r8, %2  
    setz r9b                  ; Correcto: r9b
    shl r9, %1   
%endmacro
%macro save_id 0
    test r14, r14             ; 1. ¿El ID es 0? Si es 0, no hay nada que guardar.
    jz %%skip_save            ; 2. Si es 0, saltamos la escritura (evita corromper el inicio).
    
    ; --- LIMITADOR DE SEGURIDAD (Opcional pero recomendado) ---
    cmp r14, 16777216           ; 3. ¿El ID es mayor que nuestro buffer de 1MB?
    jae %%skip_save           ; 4. Si es muy grande, abortamos para evitar el Segfault.

    mov [r10 + r14 * 8], r12  ; 5. ¡INYECCIÓN REAL! 
    xor r14, r14              ; 6. Limpiamos ID para la siguiente variable.
    xor r12, r12              ; 7. Limpiamos Valor para la siguiente variable.
%%skip_save:
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
    and r11, 0xFFFFFF  ; <--- MÁSCARA MÁGICA 128 MBs
    ; Filtro de espacio
    cmp dl, " "
    cmovnz r14, r11 
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

 %macro if_num 2 
    ; 1. ¿Es el carácter actual (dl) igual al dígito buscado?
    cmp dl, %2          
    
    ; 2. r9 se vuelve 1 si es igual, 0 si no. Sin arrastrar estados previos.
    setz r9b
    movzx r9, r9b
    
    ; 3. Si r9 es 1, operamos sobre r12. Si es 0, las macros no hacen nada.
    mul_10 ;(listo
    suma_cond %1    ; %1 es el valor numérico (0-9) (listo)
 %endmacro
%macro UPDATE_KW 2 
        mov r9, r15      ;obtener el mapa completo
        xor r9, %2        ;Si es 0 no lo destruye, si es 1, si    
        shr r9, %1       ;desplazado r9 para el tipo de keyword
        and r9, 0x1      ;toma un solo bit
        xor r15, r9     ;Reinicia estado de 1 → 0
        ;Si condición: 0 + keyword 1 = keyword 1
        ;Si condición: 1 + keyword 1 = keyword 0
    %endmacro
