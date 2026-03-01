
  %macro xif 2 ;posición, valor  
      mov r8, 0  
      mov r9, 0 ;reinicio de contexto por cada xif  
      movzx r8, rdx[INPUT + rsi]  
      shl r8, 1         
      xor r8, rdx[INPUT + rsi + 1]
      shl r8, 1  
      cmp r8, %2  
      setz r9l  
      shl r9, %1 ;para la posición en el r15  
 junto con el 
 %macro do_in 1 
     or %1, r9 
 %endmacro 
 %macro if 2 ;valor, condición
 mov r9, 0 ;para aislar contexto
mov r9l, rdx ;movemos el input
xor r9l, %2 ;para comparar
mov r9, 0 ;mov no afecta flags
setz r9l ;destruye los 8 bits, para ver si era 1 o 0
shl r9, %1 ;si es correcto desplaza
%endmacro 
 %macro if_num 3 ;la posición, el número, registro
if %1, %2
do_in %3
%endmacro 
%macro sumar_indice 0
add rsi, r9         ;agregar 1 a RSI, sólo si r9 es 1       
%endmacro 
 %macro mul_10 0
    ; Supongamos que r9 es 1 (éxito) o 0 (nada)
    
    ; --- PREPARAR EL X8 ---
    mov cl, r9b        ; cl = 1 o 0
    lea rcx, [rcx * 2 + rcx] ; cl = 3 (si era 1) o 0 (si era 0)
    ; Ahora cl vale 3 o 0. Magia de LEA.
    
    mov ax, r12w       ; Copiamos r12
    shl ax, cl         ; Si cl=3 -> ax = r12 * 8. Si cl=0 -> ax = r12.
    
    ; --- PREPARAR EL X2 ---
    mov cl, r9b        ; cl = 1 o 0
    shl r12w, cl       ; Si cl=1 -> r12 = r12 * 2. Si cl=0 -> r12 = r12.
    
    ; --- EL COLAPSO ---
    ; Aquí hay un detalle: si r9 era 0, ax=r12 y r12=r12. 
    ; Si los sumas, r12 se duplica aunque no quieras.
    ; Necesitamos que AX sea 0 si r9 es 0.
    
    neg r9             ; r9 = 0xFFFF... (si era 1) o 0 (si era 0)
    and ax, r9w        ; Si r9 era 0, ax se vuelve 0.

    add r12w, ax       ; r12 = (r12*2) + (r12*8)  O  r12 = r12 + 0
%endmacro
 %macro suma_cond 1 

     mov rdx, 0            ; Limpiamos 

     mov rdx, r9         ; Copiamos el éxito (0 o 1) a rdx 

     neg rdx             ; rdx = 0 o FFFFFFFFFFFFFFFF 

     and rdx, %1         ; rdx = 0 o VALOR 

     add r12, rdx        ; ¡Inyección segura! r9 sigue vivo para el siguiente if 

 %endmacro 

     %macro xorid 0 

     mov r11, r14                ;para la iteración actual 

     add r9, 0xFFFFFFFFFFFFFFFF  ;1 = 0, 0 = FFFFFFFFFFFFFFFF 

     and r11, r9     ;si r9 es 1, r11 desaparece, si es 0, no 

     xor r11, [INPUT+rsi]  ;se aplica la fórmula: id = id xor byte[i] << 1 

     add r9, 2       ;FFFFFFFFFFFFFFFF = 1, 0 = 0b10 

     and r9, 1       ;1 = 1, 0b10 = 0 

     shl r11, r9     ;depende r9 

     cmp rdx, " "; si es espacio, añadir 

     cmovnz r14, r14 ;mantiene el estado, sólo si es espacio (aquí se guarda), si no es espacio sigue igual 

     %endmacro 

 %macro skip 0 

     add rsi, r9;avanza el puntero de bytes, sólo si r9 es 1 

 %endmacro 

     ; %1 = Bit a testear 

     ; %2 = Registro donde mirar (r15 para keywords, r8 para números) 

     %macro elsecond 2 

     mov rdx, %2         ;Acceder al contexto 

     shr rdx, %1         ;Ubicación 

     and rdx, 1          ;Filtro and 

     xor r9, rdx         ;conexión inversa 

     xor r9, 1           ;negación 

     %endmacro 
     
 ;################

;MAPA DE TOKENS

;################

;r15 = registro maestro

;r13 = registro de números

;r9 = condicional

;rdx = datos

;r12: valores del número

;:: = 0

;,, = 1

xorid ;aquí iría el nombre (por ahora: 1 byte)
xif 0, 156
do_in r15
skip
if 0, ":" ;verifica que el próximo token sea ";" para saltarlo
skip
if_num 0, "1", r13
    sumar_indice
    mul_10
    suma_cond 1
xif 1, 232
    do_in r15
    skip
if 0, ","
    skip
