; ============================================
; DETECTOR DE PATRONES (8 bytes a la vez)
; ============================================
%macro detectar_plus 0
    xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, "+"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 1
    shr r8, 5
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        addcontroller i
        %assign i i+1
    %endrep
%endmacro

%macro detectar_minus 0
	xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, "-"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 6
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        subcontroller i
        %assign i i+1
    %endrep
%endmacro

%macro detectar_left 0
	xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, "<"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 6
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        leftcontroller i
        %assign i i+1
    %endrep
%endmacro

%macro detectar_right 0
	xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, ">"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 6
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        rightcontroller i
        %assign i i+1
    %endrep
%endmacro
