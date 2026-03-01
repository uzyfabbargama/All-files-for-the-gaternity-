; ############################################
; BLOQUE DE INYECCIÓN NUMÉRICA (0-9)
; ############################################
; r12 = Acumulador del valor (ej. 500)
; r9  = Indicador de éxito (0 o 1)

; --- Proceso para el dígito '1' ---
if_num 0, "1", r13   ; ¿Es el carácter '1'?
    sumar_indice      ; Si r9=1, avanzamos el puntero
    mul_10            ; r12 = (r12 * 10) si r9=1
    suma_cond 1       ; r12 = r12 + 1 si r9=1

; --- Proceso para el dígito '2' ---
if_num 0, "2", r13
    sumar_indice
    mul_10
    suma_cond 2

; --- Proceso para el dígito '3' ---
if_num 0, "3", r13
    sumar_indice
    mul_10
    suma_cond 3
    
; --- Proceso para el dígito '3' ---
if_num 0, "4", r13
    sumar_indice
    mul_10
    suma_cond 4
    
; --- Proceso para el dígito '3' ---
if_num 0, "5", r13
    sumar_indice
    mul_10
    suma_cond 5
    
; --- Proceso para el dígito '3' ---
if_num 0, "6", r13
    sumar_indice
    mul_10
    suma_cond 6
    
; --- Proceso para el dígito '3' ---
if_num 0, "7", r13
    sumar_indice
    mul_10
    suma_cond 7
    
; --- Proceso para el dígito '3' ---
if_num 0, "8", r13
    sumar_indice
    mul_10
    suma_cond 8

    ; --- Proceso para el dígito '3' ---
if_num 0, "9", r13
    sumar_indice
    mul_10
    suma_cond 9

; ... (repetir para 4, 5, 6, 7, 8, 9) ...

; --- Proceso para el dígito '0' ---
if_num 0, "0", r13
    sumar_indice
    mul_10
    suma_cond 0       ; Sumar 0 no cambia el valor, pero mul_10 desplaza la cifra anterior
