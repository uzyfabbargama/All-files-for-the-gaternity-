%macro constans_generator 1
	%asign i 0
	%rep 8
	%define %1%i %i
	endrep
%endmacro
%macro rsicontroller 1
	setz r9b
	and r9, 1
	neg r9b
	and r9b, %1
	add rsi, r9
%endmacro
%macro addcontroller 1
	test r10, r10
	jz %%setreset
	jmp %%normal
	%%setreset:
		mov r10, %1
	%%normal:
		mov [cell+rbx], al
		add al, r10
		mov [cell+rbx], al
%endmacro

%macro subcontroller 1
	test r10, r10
	jz %%setreset
	jmp %%normal
	%%setreset:
		mov r10, %1
	%%normal:
		mov [cell+rbx], al
		sub al, r10
		mov [cell+rbx], al
%endmacro

%macro leftcontroller 1
	test r10, r10
	setnz r9b
	neg r9
	sub r10, %1
	and r10, r9
	shl r10, 3
	sub rbx, r10
%endmacro
%macro rightcontroller 1
	test r10, r10
	setnz r9b
	neg r9
	add r10, %1
	and r10, r9
	shl r10, 3
	add rbx, r10
%endmacro
%macros detectar_plus 0
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
    ;Detectamos el +
    cmp al, "+"
    setz r9b
    and r9, 1
    mov rcx, r9
    neg r9
    and al, r9
    xor r8, al ;xor condicional
    shl r8, cl ;desplazamiento condicional
    shr rax, 8 ;desplazamos el siguiente byte
    %endrep
    ;0b1010110 = +
    ;0b11111010 = ++
    ;0b110100010 = +++
    ;0b1100010010 = ++++
    ;0b11001110010 = +++++
    ;0b110010110010 = ++++++
    ;0b1100100110010 = +++++++
    ;0b11001000110010 = ++++++++
    shr r8, 1 ;hacemos todos impares
    ;0b101011 = +
    ;0b1111101 = ++
    ;0b11010001 = +++
    ;0b110001001 = ++++
    ;0b1100111001 = +++++
    ;0b11001011001 = ++++++
    ;0b110010011001 = +++++++
    ;0b1100100011001 = ++++++++
    shr r8, 5
    ;0b1 = +
    ;0b11 = ++
    ;0b110 = +++
    ;0b1100 = ++++
    ;0b11001 = +++++
    ;0b110010 = ++++++
    ;0b1100100 = +++++++
    ;0b11001000 = ++++++++
    
    %assign i 1
    %rep 8
    	mov rax, r8 ;copia
    	shr rax, plus%i
    	cmp rax, 0
    	rsicontroller %i
    	addcontroller %i
    	%assign i i+1
    %enrep
%endmacro

%macro detectar_minus 0
	mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
    ;Detectamos el -
    cmp al, "-"
    setz r9b
    and r9, 1
    mov rcx, r9
    neg r9
    and al, r9
    xor r8, al ;xor condicional
    shl r8, cl ;desplazamiento condicional
    shr rax, 8 ;desplazamos el siguiente byte
    %endrep
    ;0b1011010
	;0b11101110
	;0b110001110
	;0b1101010110
	;0b11011110110
	;0b110110110110
	;0b1101100110110
	;0b11011000110110
	shr r8, 6
	;0b1
	;0b11
	;0b110
	;0b1101
	;0b11011
	;0b110110
	;0b1101100
	;0b11011000
	 %assign i 1
    %rep 8
    	mov rax, r8 ;copia
    	shr rax, minus%i
    	cmp rax, 0
    	rsicontroller %i
    	subcontroller %i
    	%assign i i+1
    %enrep
%endmacro

%macro detectar_left 0
	mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
    ;Detectamos el <
    cmp al, "<"
    setz r9b
    and r9, 1
    mov rcx, r9
    neg r9
    and al, r9
    xor r8, al ;xor condicional
    shl r8, cl ;desplazamiento condicional
    shr rax, 8 ;desplazamos el siguiente byte
    %endrep
    ;0b1111000
    ;0b10001000
    ;0b101101000
    ;0b1010101000
    ;0b10100101000
    ;0b101000101000
    ;0b1010000101000
    ;0b10100000101000
	shr r8, 6
	;0b1
    ;0b10
    ;0b101
    ;0b1010
    ;0b10100
    ;0b101000
    ;0b1010000
    ;0b10100000
	 %assign i 1
    %rep 8
    	mov rax, r8 ;copia
    	shr rax, left%i
    	cmp rax, 0
    	rsicontroller %i
    	leftcontroller %i
    	%assign i i+1
    %enrep
%endmacro

%macro detectar_right 0
	mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
    ;Detectamos el <
    cmp al, "<"
    setz r9b
    and r9, 1
    mov rcx, r9
    neg r9
    and al, r9
    xor r8, al ;xor condicional
    shl r8, cl ;desplazamiento condicional
    shr rax, 8 ;desplazamos el siguiente byte
    %endrep
    ;0b1111100
	;0b10000100
	;0b101110100
	;0b1010010100
	;0b10101010100
	;0b101011010100
	;0b1010111010100
	;0b10101111010100
	shr r8, 6
	;0b1
	;0b10
	;0b101
	;0b1010
	;0b10101
	;0b101011
	;0b1010111
	;0b10101111 
	 %assign i 1
    %rep 8
    	mov rax, r8 ;copia
    	shr rax, left%i
    	cmp rax, 0
    	rsicontroller %i
    	rightcontroller %i
    	%assign i i+1
    %enrep
%endmacro

%macro crear_loop 0
	mov al, [font_code+rsi]
	cmp al, "["
	jne %%exit
	test al, al
	;ahora, buscamos el ], más cercano
	mov r11, rsi ;movemos el puntero actual
%%seek:
	add rsi, 1
	mov rax, [font_code+rsi]
	ror rax, 8
	%rep 8
		cmp al, "]"
		setnz cl
		shl cl, 3
		shr rax, cl ;avanzamos un byte sólo si no es el correcto
	%endrep
	test cl, cl
	jnz %%seek
	mov r10, rbx
	add r10, 1
	add r10, rsi
	mov [cell+r10], r11 ;guardamos en la propia celda la dirección del salto en el fuente
	mov r10, rbx
	add r10, 1
	add r10, r11
	mov [cell+r10], rsi
	;mov rsi, r11
%%exit:
%enmdacro	

%macro access_bucle_start 0
	mov al, [font_code+rsi]
	cmp al, "["
	setz r9b
	and r9, 1
	shl r9, 8
	mov r10, rbx
	mov ah, [cell+r10]
	cmp ah, 0
	setz r9b
	mov rax, r9
	and ah, al ;¿es 0 y hay un [?
	jz %%exit
	mov r10, rbx
	add r10, 1
	mov rsi, [cell+r10]
%%exit:
%endmacro

%macro access_bucle_end 0
	mov al, [font_code+rsi]
	cmp al, "["
	setz r9b
	and r9, 1
	shl r9, 8
	mov r10, rbx
	mov ah, [cell+r10]
	cmp ah, 0
	setnz r9b
	mov rax, r9
	and ah, al ;¿es 0 y hay un [?
	jz %%exit
	mov r10, rbx
	add r10, 1
	mov rsi, [cell+r10]
%%exit:
%endmacro

%macro output_char 0
    ; Comprobar si es '.'
    cmp byte [font_code+rsi], '.'
    jne %%exit
    
    ; Imprimir el valor de la celda actual (rbx)
    movzx rdi, byte [cell+rbx]   ; Valor a imprimir
    mov rax, 1                   ; sys_write
    mov rsi, rsp                 ; Usamos la pila como buffer
    sub rsp, 1
    mov [rsp], dil               ; Guardamos el byte en la pila
    mov rdx, 1                   ; 1 byte
    syscall
    add rsp, 1                   ; Restauramos la pila
    
%%exit:
%endmacro

%macro input_char 0
    ; Comprobar si es ','
    cmp byte [font_code+rsi], ','
    jne %%exit
    
    ; Leer un carácter del teclado
    mov rax, 0                   ; sys_read
    mov rdi, 0                   ; stdin
    sub rsp, 1
    mov rsi, rsp                 ; Buffer en la pila
    mov rdx, 1                   ; 1 byte
    syscall
    
    ; Guardar en la celda actual
    movzx rbx, byte [rsp]
    mov [cell+rbx], al
    add rsp, 1                   ; Restauramos la pila
    
%%exit:
%endmacro
