%macro id_variable 0
    %%xorid:
        mov al, [font_code]
        cmp al, " "
        je %%fin
        cmp al, "\"
        je %%next
        movzx rax, al
        xor r8, rax
        shl r8, 1
        jmp %%xorid
    %%next:
        inc rsi
        inc rcx
        cmp cl, 32
        je %%next_line
        jmp %%xorid
    %%next_line:
    	mov al, [font_code+rsi+1]
    	cmp al, 0
    	je %%exit
        inc rdx
        xor cl, cl
    %%fin:
        mov r8, r14
        inc rsi
    %%exit:
    	xor rdi, rdi
    	mov rax, 60
    	syscall
%endmacro
%macro load_var 0
    ;r15 = variable recuperada
    mov r15, [var_total+r14]
%endmacro 
%macro save_var 0
    ;r14 = ID
    ;r13 = line/start/end/nesting
    and r14, 0xFFFFF
    shl r14, 4
    mov [var_total+r14], r14 ;ID
    add r14, 8
    mov [var_total+r14], r13 ;metadata
%endmacro
