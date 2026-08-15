%macro test 1
	%assign font_code %1
	%if font_code[0, 1, 2] == "let"
		%if font_code[4, 5, 6] == "rax"
			%assign var font_code[5, 6, 7]
			rax
		%endif
	%endif
%endmacro

test "let%/ rax%/ =%/ 1"
