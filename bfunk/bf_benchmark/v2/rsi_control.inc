; ============================================
; CONTROLADORES DE RSI (Puntero a código)
; ============================================
%macro rsicontroller 1
    setz r9b
    and r9, 1
    neg r9
    and r9, %1
    add rsi, r9
%endmacro

