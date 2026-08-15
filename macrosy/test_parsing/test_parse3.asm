%macro test 1
	%assign font_code %1
	%if font_code[0, 1, 2] == "let"
		%if font_code[4, 5, 6] == "rax"
			%assign var font_code[5, 6, 7]
			 ; 8
			%assign a font_code[8]
			%[a]
			 ; 9
			%assign b font_code[9]
			%[b]
			 ; 10
			%assign c font_code[10]
			%[c]
		%endif
	%endif
%endmacro

test "let%/ rax%/ =%/ 1"
