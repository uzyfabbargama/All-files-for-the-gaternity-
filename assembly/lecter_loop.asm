; =================================================================
; N-LANG LEXER SHELL (x86-64 Linux)
; Encargado de I/O y el Bucle de Ejecución
; =================================================================

section .data
    file_name db "source_code.n", 0 ; Nombre del archivo de código fuente
    buffer    db 0                ; Buffer para leer 1 byte (1 carácter)
    rdx_initial equ 32            ; El RDX inicial para el mapa de 32 bits

section .bss
    fd resq 1                     ; Descriptor de archivo (File Descriptor)

section .text
global _start

_start:
    ; Inicializar Registros de Estado del Lexer
    mov r8, 0                     ; R8: CLASS/Mapa de Contexto Atómico (Debe ser inicializado con el patrón base 010101...)
    mov rcx, 0                    ; RCX: Registro de Contexto (Contexto 'semántico')
    mov r12, rdx_initial          ; R12: Copia del RDX inicial (el índice de bits)

    ; -------------------------------------------------------------
    ; 1. ABRIR EL ARCHIVO (sys_open: RAX=2)
    ; -------------------------------------------------------------
    mov rax, 2                    ; syscall number 2 (sys_open)
    mov rdi, file_name            ; 1er arg: Nombre del archivo
    mov rsi, 0                    ; 2do arg: O_RDONLY (solo lectura)
    mov rdx, 0                    ; 3er arg: Modo de archivo (no relevante aquí)
    syscall                       ; Ejecuta la apertura
    
    cmp rax, 0
    jl error_exit                 ; Si RAX < 0, hubo un error al abrir.
    mov [fd], rax                 ; Guarda el File Descriptor (FD) en la variable 'fd'

.read_loop:
    ; -------------------------------------------------------------
    ; 2. LEER UN CARÁCTER (sys_read: RAX=0)
    ; -------------------------------------------------------------
    mov rax, 0                    ; syscall number 0 (sys_read)
    mov rdi, [fd]                 ; 1er arg: File Descriptor
    mov rsi, buffer               ; 2do arg: Dirección del buffer (donde almacenar 1 byte)
    mov rdx, 1                    ; 3er arg: Leer 1 byte
    syscall                       ; Ejecuta la lectura
    
    cmp rax, 0                    ; Compara el número de bytes leídos.
    jle .end_of_file              ; Si RAX <= 0, es Fin de Archivo (EOF) o error.
    
    ; -------------------------------------------------------------
    ; 3. EJECUTAR EL LEXER ATÓMICO (NIF)
    ; -------------------------------------------------------------
    
    ; El byte leído está en [buffer]. Debemos 'tokenizarlo' primero:
    ; (Este paso es el más complejo y generalmente se hace con un mapa de saltos o un array de tokens)
    
    ; SIMULACIÓN: Asumimos que la comparación con el caracter leído ('"') ocurrió
    ; y el siguiente registro (RAX) contiene el ÍNDICE DEL TOKEN
    
    ; POR AHORA: Simplemente ejecutamos la lógica NIF *unrolled*
    
    mov r12, rdx_initial          ; Reinicia el lector RDX a 32 (o 64) en cada Token.
    mov rdx, r12
    
    ; Aquí se INSERTA tu código NIF UNROLLED de 32 pares de CTRL/VAR.
    ; Lo simplificamos aquí con la lógica del primer par:

    ; ------------------------------------------
    ; INICIO BLOQUE NIF ATÓMICO (CTRL y VAR)
    ; ------------------------------------------

    ; CTRL separador[15]{0} (Tokenizado: Asumimos que el token es un 'Match')
        mov r9, r8      
        sub rdx, 1       
        shr r9, rdx      
        and r9, 0x1      
        cmp r9, 1        
        cmovz r11, 1   
        shl r11, rdx    
        sub r8, r11     
    ; VAR condición[15](1) '"'
        mov r9, r8      
        sub rdx, 1      
        shr r9, rdx     
        and r9, 0x1      
        cmp r9, 1       
        cmovz r11, 3    
        shl r11, rdx    
        add r8, r11     
        add rcx, r11    ; Actualización de RCX (Contexto)
        
    ; ... Aquí se insertan los otros 30 pares de CTRL/VAR ...
    ; ------------------------------------------
    ; FIN BLOQUE NIF ATÓMICO
    ; ------------------------------------------

    jmp .read_loop                ; Continúa leyendo el siguiente byte

.end_of_file:
    ; -------------------------------------------------------------
    ; 4. CERRAR EL ARCHIVO (sys_close: RAX=3)
    ; -------------------------------------------------------------
    mov rax, 3                    ; syscall number 3 (sys_close)
    mov rdi, [fd]                 ; 1er arg: File Descriptor
    syscall                       ; Ejecuta el cierre

    ; -------------------------------------------------------------
    ; 5. SALIR DEL PROGRAMA (sys_exit: RAX=60)
    ; -------------------------------------------------------------
    mov rax, 60                   ; syscall number 60 (sys_exit)
    mov rdi, 0                    ; 1er arg: Código de salida 0 (éxito)
    syscall                       ; Salir

error_exit:
    mov rax, 60                   ; sys_exit
    mov rdi, 1                    ; Código de salida 1 (error)
    syscall
    
        // mov r11, byte_file      ; 1. Cargar el byte (SOLO UNA VEZ)
        // movzx r10, r11b         ; 2. Extender el byte a un índice de 64 bits (para seguridad)
        // mov r9, [r_LUT_base + r10*8] ; 3. ¡CARGAR MÁSCARA DIRECTAMENTE!
        // ; r_LUT_base es la dirección de la tabla, r10*8 es el desplazamiento.
        
        // ; 4. (Opcional) Si r9 es 0, el byte es irrelevante. Si no es 0, es el token.
        // add rcx, r9             ; 5. Aplicar la máscara al contexto RCX