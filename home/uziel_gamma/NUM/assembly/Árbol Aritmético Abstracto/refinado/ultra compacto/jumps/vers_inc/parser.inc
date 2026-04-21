    mov r14, 0
    xif 784, 3, KW_VAR ; detecta VAR
        do_in r15
        skip
        prev 0, " "
            xorid
            skip ;el orden si altera
    xif 1856, 4, KW_CTRL
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    xif 3906, 5, P_CLASS
        skip
        do_in r15
        prev 0, " "
            skip
            xorid
    si KW_PARENTESIS_OPEN, "("
        count_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_COMMA, ","
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_PARENTESIS_CLOSE, ")"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_LLAVES_OPEN, "{"
        count_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_LLAVES_CLOSE, ")"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_ADD, "+"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_SUB, "-"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_MUL, "*"
        do_in r15
        skip
        prev 0, " "
    si KW_DIV, "/"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    xif 252, 2, KW_POWER
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_SEMICOLON, ";"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_EQUAL, "="
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_COMILLAS, '"'
        test r9, r9
        jnz .texto
        
    si KW_CORCHETE_OPEN, "["
        count_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_PUNTO, "."
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    
    si KW_COMILLA, "'"
        test r9, r9
        jnz .texto
    si KW_COMMENT, "#"
        skip
        test r9, r9
        jnz .comment
            prev 0, " "
                skip
                xorid
    si KW_DIC, ":"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_NOT, "!"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_MENOR, "<"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_MAYOR, ">"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_SPACE, " "
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_NEW_LINE, 10
        test r9, r9
        jnz .comment
    si KW_XOR, "^"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    
    si KW_AND, "&"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_OR,"|"
        do_in r15
        skip
        prev 0, " "
            skip
            xorid
    si KW_1, "1"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_2, "2"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_3, "3"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_4, "4"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid    
    si KW_5, "5"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_6, "6"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_7, "7"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_8, "8"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_9, "9"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
    si KW_0, "0"
        test r9, r9
        jz .numbers
        skip
        prev 0, " "
            skip
            xorid
        jmp _Parser