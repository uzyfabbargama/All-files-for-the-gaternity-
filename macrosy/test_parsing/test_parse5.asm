%macro test 1
	%assign font_code %1
	%if font_code[0, 1, 2] == "let"
		%if font_code[4, 5, 6] == "rax"
			%assign var font_code[4, 5, 6]
			%assign sign font_code[8]
			%if sign == "="
				%assign num font_code[10]
				mov %[var], %[num]
			%endif
		%endif
	%endif
%endmacro

test "let%/ rax%/ =%/ 1"
