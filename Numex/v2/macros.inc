%macro num 2
    mov r9, 0
    mov r9, %1
    shr r9, 63
    and r9, 1 ;cambié xor por and
    add %2, r9 ;estaba al revés
    shl r9, 63
    xor %1, r9
    ;add r9, %1
%endmacro
