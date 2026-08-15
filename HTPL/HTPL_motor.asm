ok, a hacerlo (versión 2)
section .data
font_code db: """respuesta_olfativa = {                                         
    percepcion_usuario = "alcohol_huele_a_podrido"             
    if (percepcion_usuario == true) {                          
        texto_brutal = ["Tienes razón. Es podrido.             
                        Pero los humanos son masoquistas       
                        evolutivos."]                          
        ofrecer_alternativa = ["¿Pruebas un agua con gas y limó\ 
n?                               Eso sí huele a limpio."]      
    } else {                                                   
        texto_default = ["La cerveza es rica, bro."]           
    }                                                          
}                                                              """
section .bss
var_total resb 0x100000
section .text
global _start
_start:
    %define KW_if 360
    %define KW_else 1078
    %define KW_open_bracket 246
    %define KW_close_bracket 250
    %define KW_equal 122
    %define KW_double_quote 68
    %define KW_simple_quote 78
    %define KW_let 540
    %define KW_isvar 2240
    xor rsi, rsi ; puntero
    xor rdx, rdx ; línea
    xor rcx, rcx ;contador
    xor r8, r8 ; temporal
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
            jmp %xorid
        %%next:
            inc rsi
            inc rcx
            cmp cl, 32
            je %%next_line
            jmp %%xorid
        %%next_line:
            inc rdx
            xor cl, cl
        %%fin:
            mov r8, r14
            inc rsi
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
    %macro take_line 0
        ;r10 = start/end/nesting
        mov r10, r13
        mov r9, 0xFFFFFFFF
        shl r9, 4
        or r9, 0xFFFF
        and r10, r9
        shr r13, 48
        and r13, 0xFFFF
    %endmacro
    %macro compare_text 0
        
        xor r13, rdx
        xor rdx, r13
        xor r13, rdx
        %%pretext:
            mov r9, r10 ;start
            shr r9, 32
            and r9, 0xFFFF
            mov r8, r10 ;end
            shr r8, 16
            and r8, 0xFFFF
            mov r11, r10 ;nesting
            and r11, 0xFFFF
            mov rax, rdx
            shl rax, 6
            add rax, r9
            mov cx, r9w
            mov rsi, rax
            xor r9, r9
        %%text:
            mov al, [rsi+font_code]
            movzx rax, al
            xor r9, al
            shl r9, 1
            inc cx
            cmp cx, r8
            je %%exit
            jmp %%text
        %%exit:
            xor cx, cx
    %endmacro
parseo:
    id_variable
    cmp r14, KW_if
    je condition_if
    cmp r14, KW_else
    je condition_else
    cmp r14, KW_let
    je variable
    cmp r14, KW_open_bracket
    je bracket_context
    cmp r14, KW_double_quote
    je text
    cmp r14, KW_simple_quote
    je text1
    jmp parseo
;condition if
condition_if:
    id_variable
    %define KW_open_parenthesis 80
    %define KW_close_parenthesis 82
    %define KW_conditional_equal 142
    id_variable
    cmp r14, KW_isvar
    jne nothing
    load_var
    
    cmp r14, KW_close_bracket
