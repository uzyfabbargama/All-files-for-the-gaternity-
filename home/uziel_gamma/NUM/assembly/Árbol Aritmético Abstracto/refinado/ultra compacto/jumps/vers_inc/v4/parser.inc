    mov r14, 0
    xif 784, 3, KW_VAR ; detecta VAR
        do_in r15
        skip KW_VAR, r15
        prev 0, " "
            xorid
            si_nop ;el orden si altera
            
    	si KW_PARENTESIS_OPEN, "("
        	count_in r15
        	skip KW_PARENTESIS_OPEN, r15
        	prev 0, " "
            	xorid
            	si_nop
        si KW_EQUAL, "="
        do_in r15
        skip KW_EQUAL, r15
        prev 0, " "
            xorid
            si_nop
    	
    	si KW_ADD, "+"
        	do_in r15
        	skip KW_ADD, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_SUB, "-"
        	do_in r15
        	skip KW_SUB, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_MUL, "*"
        	do_in r15
        	skip KW_MUL, r15
        	prev 0, " "
        		xorid
            	si_nop
	
    	si KW_DIV, "/"
        	do_in r15
        	skip KW_DIV, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	xif 252, 2, KW_POWER
        	do_in r15
        	skip KW_POWER, r15
        	prev 0, " "
            	xorid
            	si_nop
		
    	si KW_COMMA, ","
        	do_in r15
        	skip KW_COMMA, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_PARENTESIS_CLOSE, ")"
        	do_in r15
        	skip KW_PARENTESIS_CLOSE, r15
        	prev 0, " "
            	xorid
            	si_nop
	

    xif 1856, 4, KW_CTRL
        do_in r15
        skip KW_CTRL, r15
        prev 0, " "
            xorid
            si_nop
		si KW_LLAVES_OPEN, "{"
        	count_in r15
        	skip KW_LLAVES_OPEN, r15
        	prev 0, " "
            	xorid
            	si_nop
    	si KW_PARENTESIS_OPEN, "("
        	count_in r15
        	skip KW_PARENTESIS_OPEN, r15
        	prev 0, " "
            	xorid
            	si_nop
        si KW_EQUAL, "="
        do_in r15
        skip KW_EQUAL, r15
        prev 0, " "
            xorid
            si_nop
    	
    	si KW_ADD, "+"
        	do_in r15
        	skip KW_ADD, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_SUB, "-"
        	do_in r15
        	skip KW_SUB, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_MUL, "*"
        	do_in r15
        	skip KW_MUL, r15
        	prev 0, " "
        		xorid
            	si_nop
	
    	si KW_DIV, "/"
        	do_in r15
        	skip KW_DIV, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	xif 252, 2, KW_POWER
        	do_in r15
        	skip KW_POWER, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_LLAVES_CLOSE, "}"
        	do_in r15
        	skip KW_LLAVES_CLOSE, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    xif 3906, 5, KW_CLASS
        skip KW_CLASS, r15
        do_in r15
        prev 0, " "
            xorid
            si_nop
    	si KW_PARENTESIS_OPEN, "("
        	count_in r15
        	skip KW_PARENTESIS_OPEN, r15
        	prev 0, " "
            	xorid
            	si_nop
        si KW_EQUAL, "="
        do_in r15
        skip KW_EQUAL, r15
        prev 0, " "
            xorid
            si_nop

    	si KW_ADD, "+"
        	do_in r15
        	skip KW_ADD, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_SUB, "-"
        	do_in r15
        	skip KW_SUB, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_MUL, "*"
        	do_in r15
        	skip KW_MUL, r15
        	prev 0, " "
    	si KW_DIV, "/"
        	do_in r15
        	skip KW_DIV, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	xif 252, 2, KW_POWER
        	do_in r15
        	skip KW_POWER, r15
        	prev 0, " "
            	xorid
            	si_nop
		
    	si KW_COMMA, ","
        	do_in r15
        	skip KW_COMMA, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    	si KW_PARENTESIS_CLOSE, ")"
        	do_in r15
        	skip KW_PARENTESIS_CLOSE, r15
        	prev 0, " "
            	xorid
            	si_nop

    

    	si KW_SEMICOLON, ";"
        	do_in r15
        	skip KW_SEMICOLON, r15
        	prev 0, " "
            	xorid
            	si_nop
	
    
    si KW_COMILLAS, '"'
        test r9, r9
        jnz .texto
        
    si KW_CORCHETE_OPEN, "["
        count_in r15
        skip KW_CORCHETE_OPEN, r15
        prev 0, " "
            xorid
            si_nop

    si KW_PUNTO, "."
        do_in r15
        skip KW_PUNTO, r15
        prev 0, " "
            xorid
            si_nop

    
    si KW_COMILLA, "'"
        test r9, r9
        jnz .texto
    si KW_COMMENT, "#"
        skip KW_COMMENT, r15
        test r9, r9
        jnz .comment
            prev 0, " "
                ;skip KW_COMMENT, r15
                xorid
    si KW_DIC, ":"
        do_in r15
        skip KW_DIC, r15
        prev 0, " "
            xorid
            si_nop

    si KW_NOT, "!"
        do_in r15
        skip KW_NOT, r15
        prev 0, " "
            xorid
            si_nop

    si KW_MENOR, "<"
        do_in r15
        skip KW_MENOR, r15
        prev 0, " "
            xorid
            si_nop

    si KW_MAYOR, ">"
        do_in r15
        skip KW_MAYOR, r15
        prev 0, " "
            xorid
            si_nop

    si KW_SPACE, " "
        do_in r15
        skip KW_SPACE, r15
        prev 0, " "
            xorid
            si_nop

    si KW_NEW_LINE, 10
        test r9, r9
        jnz .comment
    si KW_XOR, "^"
        do_in r15
        skip KW_NEW_LINE, r15
        prev 0, " "
            xorid
            si_nop

    
    si KW_AND, "&"
        do_in r15
        skip KW_AND, r15
        prev 0, " "
            xorid
            si_nop

    si KW_OR,"|"
        do_in r15
        skip KW_OR, r15
        prev 0, " "
            xorid
            si_nop

    si KW_1, "1"
        test r9, r9
        jz .numbers
        skip KW_1, r15
        prev 0, " "
            xorid
            si_nop

    si KW_2, "2"
        test r9, r9
        jz .numbers
        skip KW_2, r15
        prev 0, " "
            xorid
            si_nop

    si KW_3, "3"
        test r9, r9
        jz .numbers
        skip KW_3, r15
        prev 0, " "
            xorid
            si_nop

    si KW_4, "4"
        test r9, r9
        jz .numbers
        skip KW_4, r15
        prev 0, " "
            xorid

            si_nop    
    si KW_5, "5"
        test r9, r9
        jz .numbers
        skip KW_5, r15
        prev 0, " "
            xorid
            si_nop

    si KW_6, "6"
        test r9, r9
        jz .numbers
        skip KW_6, r15
        prev 0, " "
            xorid
            si_nop

    si KW_7, "7"
        test r9, r9
        jz .numbers
        skip KW_7, r15
        prev 0, " "
            xorid
            si_nop

    si KW_8, "8"
        test r9, r9
        jz .numbers
        skip KW_8, r15
        prev 0, " "
            xorid
            si_nop

    si KW_9, "9"
        test r9, r9
        jz .numbers
        skip KW_9, r15
        prev 0, " "
            xorid
            si_nop

    si KW_0, "0"
        test r9, r9
        jz .numbers
        skip KW_0, r15
        prev 0, " "
            xorid
            si_nop

        jmp _Parser
