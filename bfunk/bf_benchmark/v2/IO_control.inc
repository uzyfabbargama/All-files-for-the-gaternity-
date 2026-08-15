; ============================================
; ENTRADA / SALIDA
; ============================================
%macro output_char 0
    cmp byte [font_code+rsi], '.'
    jne %%exit
    
    push rsi
    push rbx
    push rax
    
    movzx rdi, byte [cell+rbx]
    mov rax, 1
    sub rsp, 8          ; Alinear a 16 bytes
    mov [rsp], dil
    mov rsi, rsp
    mov rdx, 1
    syscall
    add rsp, 8
    
    pop rax
    pop rbx
    pop rsi
%%exit:
%endmacro

%macro input_char 0
    cmp byte [font_code+rsi], ','
    jne %%exit
    push rsi
    push rbx
    
    mov rax, 0
    mov rdi, 0
    sub rsp, 8          ; Alinear stack
    mov rsi, rsp
    mov rdx, 1
    syscall
    movzx rcx, byte [rsp]  ; Usar RCX como temporal
    add rsp, 8
    
    mov [cell+rbx], cl     ; Guardar en la celda actual (RBX sigue intacto)
    
    pop rbx
    pop rsi
%%exit:
%endmacro
