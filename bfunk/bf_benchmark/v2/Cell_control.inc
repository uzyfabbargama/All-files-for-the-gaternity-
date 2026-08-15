; ============================================
; CONTROLADORES DE CELDA
; ============================================
%macro addcontroller 1
    test r10, r10
    jz %%setreset
    jmp %%normal
    %%setreset:
        mov r10, %1
    %%normal:
        mov al, [cell+rbx]
        add al, r10b
        mov [cell+rbx], al
%endmacro

%macro subcontroller 1
    test r10, r10
    jz %%setreset
    jmp %%normal
    %%setreset:
        mov r10, %1
    %%normal:
        mov al, [cell+rbx]
        sub al, r10b
        mov [cell+rbx], al
%endmacro

%macro leftcontroller 1
    test r10, r10
    setnz r9b
    neg r9
    sub r10, %1
    and r10, r9
    shl r10, 3      ; Multiplicar por 8 (tamaño de celda)
    sub rbx, r10
%endmacro

%macro rightcontroller 1
    test r10, r10
    setnz r9b
    neg r9
    add r10, %1
    and r10, r9
    shl r10, 3      ; Multiplicar por 8 (tamaño de celda)
    add rbx, r10
%endmacro
