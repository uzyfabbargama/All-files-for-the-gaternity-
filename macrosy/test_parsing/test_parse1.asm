%macro test 1
	%assign font_code %1
	%if font_code[0, 1, 2] == "let"
		%1
	%endif
%endmacro

test "let rax = 1"
