%macro PARSEAR_LET 1
    %if %1[0, 1, 2] == "let"
        %assign var %1[4, 5, 6]
        %if %1[8] == "="
            %if %1[10] >= "0" & %1[10] <= "9"
                %assign num %1[10] - 48
                mov %[var], %[num]
            %endif
        %endif
    %endif
%endmacro

PARSEAR_LET "let rax = 0"
