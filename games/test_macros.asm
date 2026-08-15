%macro conmutar 2
    %## Alterna los bits del registro %1 usando la máscara %2
    eor %1, %1, %2
%endmacro

%macro cargar_y_conmutar 2
    %assign i 0
    %rep 3
        %if i == 0
            mov %1, #0
        %elif i == 1
            conmutar %1, %2
        %else
            conmutar %1, %2
        %endif
        %assign i i + 1
    %endrep
%endmacro

_start:
    cargar_y_conmutar r0, #0xFF
