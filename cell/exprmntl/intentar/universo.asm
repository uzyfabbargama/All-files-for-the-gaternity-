section .bss
universo: resb 1000000
%include "visual.asm"
section .text
global _start


_start:
	;--- Cargar Universo previo del disco ---
	mov rax, 2			; syscall open
	mov rdi, filename	; "universo.bin"
	mov rsi, 0			; O_RDONLY (solo lectura)
	syscall
	
	; Si no existe (primera carga
	cmp rax, 0
	jl .saltar_carga	; Si rax es negativo, hubo error, (no hay archivo)
	
	mov rdi, rax		; ID del archivo
	mov rax, 0			; syscall read
	mov rsi, universo	; Destino: nuestra RAM
	mov rdx, 1000000	; Leer 1 MB
	syscall
	;close
	mov rdi, rdi
	mov rax, 3
	syscall
.saltar_carga:
	; Ahora sí, inicializar los registros para el bucle
	;--- Registros
	xor r12, r12
	mov rsi, universo	;RSI apunta al inicio del universo
	add rsi, 2000 	; Primera línea (Margen de seguridad)
	mov rcx, 996000	; Contadir de celdas por "año"
	;--- Definiciones de Vencindad
	mov r10, 1
bucle_eterno:
	push rcx		; Guardamos el contador global
	%define up -1000	
	%define down 1000
	%define left -1
	%define right 1
	%define center 0
	; Para acceder a cada uno
	%define up_data 36
	%define down_data 27
	%define left_data 18
	%define right_data 9
	%define center_data 0
	; Para cada slot
	%define slot 0	;bit 1
	%define slot1 1	;bit 2
	%define slot2 2	;bit 3
	%define slot3 3	;bit 4
	%define slot4 4	;bit 5
	%define slot5 5	;bit 6
	%define slot6 5	;bit 7
	%define slot7 7	;bit 8
	;--- special nine
	%define special 8	;bit 9
	;--- Macro de Carga Transurgente
	; Cargamos la celda y la desplazamos para hacer espacio a la siguiente
	%macro cell_load 1
	movzx rbx, byte [rsi + %1] 	; movzx limpia los bits altos de RBX al cargar
	or rax, rbx					; insertamos la celda en la parte baja
	shl rax, 9					; Desplazamos 9 bits a la izquierda
	%endmacro
	%macro update_cell 2; 1: ubicación1, 2: ubicación2
	mov r9, rax			; r9 = foto de la sección
	shr r9, %1			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, %2			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, %1			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, %2			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	%endmacro
	%macro weat_cell 1 	; Celda
	mov r9, 0		; Limpiamos r9
	mov r9, rax		; Tomamos la foto
	shr r9, %1		; Vamos a la celda
	shr r9, slot7 	; Extraemos el calor
	and r9, 0x1 	; Aislamos el bit
	shl r9, 3		; r9 = 8, (la explosión de bits
	add r10, r9 	; Sumamos el calor si pasa al bit 9
	shl r9, %1		; volvemos a la posición inicial
	sub rax, r9		; Eliminamos ese calor residual
	%endmacro
	%macro disip 2
	mov r8, %2
	shl r8, %1
	add rax, r8
	%endmacro
	;--- Ciclo de Captura (5 celdas = 40 bits)
	xor rax, rax 		;registro de carga
	xor r9, r9			; operación
	xor r8, r8			; objetivo
	mov r10, [calor_persistente]		; calor
	;celda central
	cell_load up		;44-36 up
	;celda izquierda
	cell_load down		;35-27 down
	;celda derecha
	cell_load left		;26-18 left
	;celda arriba
	cell_load right		;17-9 right
	;celda abajo
	cell_load center	;8-0 center
	shr rax, 8			; eliminamos el desplazamiento innecesario
	jmp update
update:
	;---UP
	update_cell up_data, center_data
	update_cell up_data, right_data
	update_cell up_data, left_data
	update_cell up_data, down_data
	;---DOWN
	update_cell down_data, center_data
	update_cell down_data, right_data
	update_cell down_data, left_data
	update_cell down_data, up_data
	;---LEFT
	update_cell left_data, center_data
	update_cell left_data, right_data
	update_cell left_data, up_data
	update_cell left_data, down_data
	;---RIGHT
	update_cell right_data, center_data
	update_cell right_data, up_data
	update_cell right_data, down_data
	update_cell right_data, left_data
	;---CENTER
	update_cell center_data, up_data
	update_cell right_data, down_data
	update_cell right_data, left_data
	update_cell right_data, right_data

	jmp weat ;calor
weat:
	weat_cell up_data
	weat_cell down_data
	weat_cell left_data
	weat_cell right_data
	weat_cell center_data
	movzx r9, r10b 	; Para comparar
	not r9b			; Invertimos
	
	movzx r8, dil	; Movemos DIL (8 bits) a R8 (64 bits)
	add r9, r8		; comparación sin cmp
	
	
	shr r9, special	; Despejamos los 8 bits
	and r9, 1		; sumamos para complemento a 2
	
	inc dil			; RDI (Parte baja: DIL) aumenta de 0 a 255 y vuelve a 0 solo
	mov r11, r9		; R11 = 1 o 0
		 
	disip up_data, r11
	disip down_data, r11
	disip right_data, r11
	disip left_data, r11
	disip center_data, r11
	mov [calor_persistente], r10
	; --- [ SECCIÓN RENDER ] ---
    mov r13, rcx            ; Usamos el contador actual
    and r13, 0x1          ; Filtro de densidad (1 de cada 1024)
    jnz .saltar_render

    push rax                ; Protegemos el estado del universo
    push rcx
    push rsi
    mov rax, 1              ; syscall: write
    mov rdi, 1              ; stdout
    mov rsi, rsi            ; celda actual
    mov rdx, 1              ; 1 byte
    syscall
    pop rsi
    pop rcx
    pop rax

.saltar_render:
    ; [tu código existente de update]
    push rax
    push rcx
    push rsi
    push r10
    ; CADA render (no solo cada 60000 años)
    ; --- PRUEBA: forzar un mensaje visible ---
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_test
    mov rdx, msg_len
    syscall

    call renderizar_pantalla
    call detectar_criaturas
    
    pop r10              ; <--- RESTAURA EL CALOR AQUÍ
    pop rsi
    pop rcx
    pop rax
    ; Si quieres guardar fotos de criaturas especiales:
    cmp qword [num_criaturas], 0
    je .no_criaturas
    ; guardar_foto r12, "criatura"  (solo si hay)
.no_criaturas:

    ; Movimiento de cámara opcional
    update_camara_con_mouse
    
    jmp guardar_y_avanzar
	
guardar_y_avanzar:
	; Extraemos la celda central de RAX (bits 0-7) y guardamos en memoria
	mov rbx, rax
	and rbx, 0xFF
	mov [rsi], bl		;Devolvemos la vida procesada a la RAM
	
	inc rsi					; Avanzamos a la siguiente molécula
	pop rcx					; Recuperamos el contador del año
	dec rcx					; Decrementamos manualmente el contador
	jnz bucle_eterno		;Si RCX > 0, repetimos
	
	; Nanosleep para que el Athlon respire 1ms cada año
	 mov rax, 35           ; nanosleep
    mov rdi, timespec
    xor rsi, rsi
    syscall
    
    inc r12               ; un año más
    cmp r12, 60000
    je .guardar_eon
    
.reseteo_normal:
    mov rsi, universo
    add rsi, 2000
    mov rcx, 996000
    jmp bucle_eterno

.guardar_eon:
    ; ... guardar en disco ...

	;--- Abrir/Crear archivo (Syscall 2: open)
	mov rax, 2			; syscall open
	mov rdi, filename	; nombre del archivo
	mov rsi, 101o		; flags: O_WRITE_ONLY | O_CREAT (octal)
	mov rdx, 644o		; permisos: rw-r--r--
	syscall
	mov rdi, rax
	;--- Escribir el universo (Syscall 1:write)
	mov rax, 1		; syscall write
	; rdi ya tiene el identificador
	mov rsi, universo	;la dirección de la RAM (1MB)
	mov rdx, 1000000	; cuántos bytes
	syscall
	
	;--- Cerrar archivo (Syscall 3: close)
	mov rax, 3
	syscall
	mov rsi, universo
	add rsi, 2000
	mov rcx, 996000
    xor r12, r12
    jmp .reseteo_normal				; Saltamos a guardar (y luego losv debe volver aquí)

section .data
	filename db "universo.bin", 0
	timespec:
		dq 0			; segundos
		dq 1000000		; 0 nanosegundos
	calor_persistente: dq 0 ;frío
	msg_test db ">>> RENDERIZANDO <<<", 10
    msg_len equ $ - msg_test

;--- Fin
fin:
	mov rax, 35		; Syscall nanosleep
	mov rdi, timespec
	xor rsi, rsi
	syscall
	;exit
	mov eax, 60		;Syscall para exit en Linux x86_64
	xor edi, edi	; Código de error 0
	syscall
