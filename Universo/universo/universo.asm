section .bss
universo: resb 1000000

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
        xor rdi, rdi
	mov rsi, universo	;RSI apunta al inicio del universo
	add rsi, 2000 	; Primera línea (Margen de seguridad)
	mov rcx, 996000	; Contadir de celdas por "año"
	;--- Definiciones de Vencindad
	mov r10, 1
bucle_eterno:
	push rcx		; Guardamos el contador global
	;--- Ciclo de Captura (5 celdas = 40 bits)
	xor rax, rax 		;registro de carga
	xor r9, r9			; operación
	xor r8, r8			; objetivo
	mov r10, [calor_persistente]		; calor
	;celda central
	movzx rbx, byte [rsi - 1000] 	; movzx limpia los bits altos de RBX al cargar
	or rax, rbx					; insertamos la celda en la parte baja
	shl rax, 9					; Desplazamos 9 bits a la izquierda;44-36 up
	;celda izquierda
	movzx rbx, byte [rsi + 1000] 	; movzx limpia los bits altos de RBX al cargar
	or rax, rbx					; insertamos la celda en la parte baja
	shl rax, 9					; Desplazamos 9 bits a la izquierda		;35-27 down
	;celda derecha
	movzx rbx, byte [rsi - 1] 	; movzx limpia los bits altos de RBX al cargar
	or rax, rbx					; insertamos la celda en la parte baja
	shl rax, 9					; Desplazamos 9 bits a la izquierda		;26-18 left
	;celda arriba
	movzx rbx, byte [rsi + 1] 	; movzx limpia los bits altos de RBX al cargar
	or rax, rbx					; insertamos la celda en la parte baja
	shl rax, 9					; Desplazamos 9 bits a la izquierda		;17-9 right
	;celda abajo
	movzx rbx, byte [rsi + 0] 	; movzx limpia los bits altos de RBX al cargar
	or rax, rbx					; insertamos la celda en la parte baja
	shl rax, 9					; Desplazamos 9 bits a la izquierda	;8-0 center
	shr rax, 8			; eliminamos el desplazamiento innecesario
	jmp update
update:
	;---UP
	;update_cell up_data, center_data

	mov r9, rax			; r9 = foto de la sección
	shr r9, 36			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 0			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 36			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 0			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;update_cell up_data, right_data
        mov r9, rax			; r9 = foto de la sección
        shr r9, 36			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 9			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 36			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 9			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;update_cell up_data, left_data
        mov r9, rax			; r9 = foto de la sección
	shr r9, 36			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 18			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 36			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 18			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;update_cell up_data, down_data
        mov r9, rax			; r9 = foto de la sección
	shr r9, 36			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 27			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 36			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 27			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;---DOWN
	;update_cell down_data, center_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 27			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 0			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 27			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 0			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

;	update_cell down_data, right_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 27			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 9			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 27			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 9			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;update_cell down_data, left_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 27			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 18			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 27			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 18			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;update_cell down_data, up_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 27			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 36			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 27			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 36			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8

	;---LEFT
	;update_cell left_data, center_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 18			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 0			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 18			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 0			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell left_data, right_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 18			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 9			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 18			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 9			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell left_data, up_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 18			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 36			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 18			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 36			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell left_data, down_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 18			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 27			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 18			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 27			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;---RIGHT
	;update_cell right_data, center_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 0			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 0			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell right_data, up_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 36			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 36			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell right_data, down_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 27			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 27			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell right_data, left_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 0			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 0			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;---CENTER
	;update_cell center_data, up_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 0			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 9			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 0			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 9			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell right_data, down_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 27			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 27			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell right_data, left_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 18			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 18			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	;update_cell right_data, right_data
	mov r9, rax			; r9 = foto de la sección
	shr r9, 9			; Vamos a la celda de arriba
	and r9, 0xFF 		; despejamos los bits de arriba
	mov r8, rax			;r8 = foto de la sección
	shr r8, 9			; Vamos a la celda central
	and r8, 0xFF		; Despejamos el byte
	xor r9, r8			; Detectamos las diferencias de energía en los 8 canales
	shl r9, 9			; subimos r9
	and r9, 0xFF		; Máscara de seguridad
	shl r8, 9			; subimos r8
	and r8, 0xFF		; Máscara de seguridad
	sub rax, r9			; agregamos r9
	add rax, r8			; agregamos r8
	jmp weat ;calor
weat:
	;weat_cell up_data
	mov r9, 0		; Limpiamos r9
	mov r9, rax		; Tomamos la foto
	shr r9, 36		; Vamos a la celda
	shr r9, 7 	; Extraemos el calor
	and r9, 0x1 	; Aislamos el bit
	shl r9, 3		; r9 = 8, (la explosión de bits
	add r10, r9 	; Sumamos el calor si pasa al bit 9
	shl r9, 36		; volvemos a la posición inicial
	sub rax, r9		; Eliminamos ese calor residua
	;weat_cell down_data
	mov r9, 0		; Limpiamos r9
	mov r9, rax		; Tomamos la foto
	shr r9, 27		; Vamos a la celda
	shr r9, 7 	; Extraemos el calor
	and r9, 0x1 	; Aislamos el bit
	shl r9, 3		; r9 = 8, (la explosión de bits
	add r10, r9 	; Sumamos el calor si pasa al bit 9
	shl r9, 27		; volvemos a la posición inicial
	sub rax, r9		; Eliminamos ese calor residua
	;weat_cell left_data
	mov r9, 0		; Limpiamos r9
	mov r9, rax		; Tomamos la foto
	shr r9, 18		; Vamos a la celda
	shr r9, 7 	; Extraemos el calor
	and r9, 0x1 	; Aislamos el bit
	shl r9, 3		; r9 = 8, (la explosión de bits
	add r10, r9 	; Sumamos el calor si pasa al bit 9
	shl r9, 18		; volvemos a la posición inicial
	sub rax, r9		; Eliminamos ese calor residua
	;weat_cell right_data
	mov r9, 0		; Limpiamos r9
	mov r9, rax		; Tomamos la foto
	shr r9, 9		; Vamos a la celda
	shr r9, 7 	; Extraemos el calor
	and r9, 0x1 	; Aislamos el bit
	shl r9, 3		; r9 = 8, (la explosión de bits
	add r10, r9 	; Sumamos el calor si pasa al bit 9
	shl r9, 9		; volvemos a la posición inicial
	sub rax, r9		; Eliminamos ese calor residua
	;weat_cell center_data
	mov r9, 0		; Limpiamos r9
	mov r9, rax		; Tomamos la foto
	shr r9, 0		; Vamos a la celda
	shr r9, 7 	; Extraemos el calor
	and r9, 0x1 	; Aislamos el bit
	shl r9, 3		; r9 = 8, (la explosión de bits
	add r10, r9 	; Sumamos el calor si pasa al bit 9
	shl r9, 0		; volvemos a la posición inicial
	sub rax, r9		; Eliminamos ese calor residua
	movzx r9, r10b 	; Para comparar
	not r9b			; Invertimos
	
	movzx r8, dil	; Movemos DIL (8 bits) a R8 (64 bits)
	add r9, r8		; comparación sin cmp
	
	
	shr r9, 9	; Despejamos los 8 bits
	and r9, 1		; sumamos para complemento a 2
	
	inc dil			; RDI (Parte baja: DIL) aumenta de 0 a 255 y vuelve a 0 solo
	mov r11, r9		; R11 = 1 o 0
		 
;	disip up_data, r11
	mov r8, r11
	shl r8, 36
	add rax, r8
;	disip down_data, r11
	mov r8, r11
	shl r8, 27
	add rax, r8
;	disip right_data, r11
	mov r8, r11
	shl r8, 18
	add rax, r8
;	disip left_data, r11
	mov r8, r11
	shl r8, 9
	add rax, r8
;	disip center_data, r11
	mov r8, r11
	shl r8, 0
	add rax, r8
	mov [calor_persistente], r10
	jmp guardar_y_avanzar
	
guardar_y_avanzar:
        ;pop rcx ;Listo, se guardó rcx, en un lugar donde no haga daño
	; Extraemos la celda central de RAX (bits 0-7) y guardamos en memoria
	mov rbx, rax
	and rbx, 0xFF
	mov [rsi], bl		;Devolvemos la vida procesada a la RAM
	
	inc rsi					; Avanzamos a la siguiente molécula
	pop rcx					; Recuperamos el contador del año
	dec rcx					; Decrementamos manualmente el contador
	jnz bucle_eterno		;Si RCX > 0, repetimos
	
	; Nanosleep para que el Athlon respire 1ms cada año
	mov rax, 35
	mov rdi, timespec
	xor rsi, rsi
	syscall	
	
	;2. Contador de Eones
	inc r12					; Un año más ha pasado
	cmp r12, 60000			; ¿Llegamos a los 10,000 años?
	je .guardar_eon			; Si, sí, vamos a guardar al disco
	
	;3. Reinicio normal (si no llegó a 10,000)
	mov rsi, universo
	add rsi, 2000			; Reset puntero
	mov rcx, 998000			; Reser contador
	jmp bucle_eterno		; ¡Saltamos al inicio! ¡Feliz año nuevo!

.guardar_eon:
	xor r12, r12			; Reseteamos el contador de eones
	jmp losv				; Saltamos a guardar (y luego losv debe volver aquí)
losv:
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
	jmp bucle_eterno		;¡El universo sigue después de guardar!
section .data
	filename db "universo.bin", 0
	timespec:
		dq 0			; segundos
		dq 1000000		; 0 nanosegundos
	calor_persistente: dq 1

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
