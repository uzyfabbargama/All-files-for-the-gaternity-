%macro PARSEAR_LET 1
    %assign font_code %1
    %if font_code[0, 1, 2] == "let"
        %assign var font_code[4, 5, 6]
        %if font_code[8] == "="
            %if font_code[10] >= "0" & font_code[10] <= "9"
                %assign num font_code[10] - 48
                mov %[var], %[num]
            %endif
        %endif
    %endif
%endmacro

PARSEAR_LET "let rax = 0"
