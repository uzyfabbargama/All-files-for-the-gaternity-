section bss
	papeles resb 4096*64
	papeles_counter resb 2*64
	papelwriter resb 4096
	%assign i 0
	b resb 8*64 ;bookshelfs
	h resb 8*2
section data
	font_code ""
	
section text
global _start
_start:
	%define kw_shl 736
	%define kw_shr 732
	%define kw_mov 568
	%define kw_escribir 20160
	%define kw_leer 1176
	%define kw_literal_y "y"
	%define kw_literal_Y "Y"
	%define kw_literal_o "o"
	%define kw_literal_O "O" 
	%define kw_poner 2800
	
	%macro extraer_registro 2
		mov %1, %2
	%endmacro
	
	%macro shl_registro 2
		mov cl, %2
		and cl, 0x3f
		shl %1, cl
	%endmacro
	
	%macro shr_registro 2
		mov cl, %2
		and cl, 0x3f
		shr %1, cl
	%endmacro
	
	%macro y_registro 2
		and %1, %2
	%endmacro
	
	%macro o_registro 2
		xor %1, %2
	%endmacro
	
	%macro poner_registro 2
		or %1, %2
	%endmacro
	
	%macro xorid 3
		mov rax, [%1 + rsi]
		ror rax, 8
		mov r8, 0
		%rep %3
			mov r9b, al
			xor r8, r9
			shl r8, 1
			shr rax, 8
		%endrep
		cmp r8, %2
		je %%no
		add rsi, %3
		xor r9, r9 ;pone la flag zero en 1
		%%no:
			inc rsi
	%endmacro
	
	xorid font_code, kw_mov, 3
	jz .mover
	xorid font_code, kw_shr, 3
	jz .desder
	xorid font_code, kw_shl, 3
	jz .desizq
	xorid font_code, kw_escribir, 8
	jz .wrtr
	xorid font_code, kw_leer, 4
	jz .reader
	xorid font_code, kw_poner, 5
	jz .orear
	%macro numcond 4 ;1: acumulador(r12), 2: shift/view, 3: base(10), 4: loop_label
    ; r9 entra con 1 (es número) o 0 (no lo es)
    neg r9              ; 1 = -1 (0xFF...FF), 0 = 0
    
    ; 1. Aislamos el carácter de la ventana r11
    mov r11, rdx
    %assign shift_val %2 << 3
    shr r11, shift_val
    and r11, 0xFF       ; Nos quedamos estrictamente con el byte que miramos
    
    ; 2. Aplicamos la máscara condicional
    and r11, r9         ; Si r9 era 0 -> r11 = 0. Si era -1 -> r11 tiene el ASCII.
    
    ; 3. Convertimos de ASCII a entero plano ('0' es 48)
    ; Ojo: solo restamos 48 si realmente r9 era -1, para evitar que un 0 se vuelva -48.
    mov r8, 48
    and r8, r9          ; Si r9 era 0 -> r8 = 0. Si era -1 -> r8 = 48.
    sub r11, r8         ; r11 ahora tiene el valor numérico puro (0-9) o 0.
    
    ; 4. ALGORITMO ACUMULADOR: Primero multiplicamos el acumulador anterior por 10
    mov r8, %3          ; r8 = 10
    and r8, r9          ; Si r9 es 0 -> r8 = 0. Si era -1 -> r8 = 10.
    
    cmp r8, 0
    jz %%no_mul         ; Si es cero, saltamos la multiplicación interna
    
    imul %1, r8         ; r12 = r12 * 10 (¡Branchless condicional gracias al AND anterior!)
%%no_mul:

    ; 5. Ahora sí sumamos el nuevo dígito al acumulador
    add %1, r11         ; r12 = r12 + dígito
    
    ; 6. Avanzamos en el buffer masivo de 8 bytes si el bit era válido
    ; Si r9 era 0, no queremos saltar ni recargar rdx de la RAM.
    cmp r9, 0
    jz %%skip_stream
    
    add rsi, 1          ; Avanzamos de a 1 byte en tu puntero indexado
    mov rdx, [rdi+rsi]  ; Recargamos la ventana de 8 bytes futuros
    ror rdx, 8
    jmp %4              ; Hacemos el loop al estado actual (%%num)
    
%%skip_stream:
%endmacro
	%macro buscar_registro 3
		;[mov ]b64,  
		mov eax, [%1 + rsi]
		ror eax, 8
		cmp al, "b"
		je %%is_bookshelf
		;[mov ]h1, 
		cmp al, "h"
		je %%is_hand
		;[mov ]papel64, 
		cmp eax, "papel"
		je %%is_paper
		jmp %%fin
	%%is_bookshelf:
		inc rsi
	%%num_bookshelf:
		;[mov b]64
		numcond %2, 0, 10, %%num_bookshelf
		dec %2, 1 ;para que sólo quede del 0 al 63
		and %2, 0x3ff ;limitamos 63
		shl %2, 8 ;elegimos el registro directamente
		jmp %%comma
	%%is_hand:
		inc rsi
	%%num_hand:
		numcond %2, 0, 10, %%num_hand
		and %2, 0x1
		shl %2, 8
		jmp %%comma
	%%is_paper
		;[mov ]papel64, "hola mundo"
		add rsi, 4
	%%num_paper:
		numcond %2, 0, 10, %%num_paper
		dec %2
		and %2, 0x3f
		shl %2, 12 ;2¹² = 4096
		
		mov al, [%1 + rsi]
		mov r10, %2 ;usaremos r10, para puntero de texto
		cmp al, '"'
		je %%texto
	%%texto:
		inc rsi
		mov rax, [%1 + rsi]
		ror rax, 8
		mov rcx, '"'
		%rep 8
			cmp al, cl ;detecta en el byte bajo "
			setz r9b ;si es r9, es 1, sino es 0
			and r9, 1 ;es igual que movzx ;aislamos ese bit
			neg r9 ;0 = 0, 1 = -1 ;invertimos
			and r9, rcx ;si es 0, r9 es 0, si es 1, r9 es comillas
			test r9, r9 ;verificamos comillas
			jnz %%fin ;si en algún punto del texto es comilla, cortar
			
			mov [%3 + r10], al ;movemos ese byte si no es comilla
			inc r10 ;movemos el puntero del byte
			shr rax, 8 ;siguiente byte
		%endrep
			add rsi, 7 ;avanzamos próximo bloque (cuando volvamos arriba, ya suma rsi 1, así que con esto sumamos 8 limpiamente)
			jmp %%texto ;volvemos al prinicipio
	%%comma:
		;suponiendo que numcond no avanza rsi, si no es un número
		inc rsi
		;[mov b64],
		mov al, [%1 + rsi]
		cmp al, ","
		jmp %%fin
	%%fin:
	%endmacro
.mover:
	inc rsi
	buscar_registro font_code, r12, papeles
	;nos falta el binnum (convierte texto a binario, 
	%macro binnum 2
		xor rcx, rcx
		mov rax, [%1]
		;ejemplo
		;49 49 49 49 49 49
		and rax, 0x0101010101010101 ; Aislamos los bits bajos ASCII
		mov r9, 0x0102040810204080 ; Cargamos tu constante de dispersión
		imul rax, r9               ; Multiplicamos en caliente (eficiente y limpio)
		shr rax, 56
		or rcx, rax
		shl rcx, 8
	%endmacro
	extraer_registro r13, [r12] ;listo, arreglado, (¿innecesario?)
