;=========================================
; COMPOSICIÓN VS ANIDACIÓN
;=========================================
; Los dominios son ortogonales y se componen secuencialmente.
; NO se anidan.
;
; Composición secuencial:
;   proc cond, x, y       ; dominio neurona
;   ari lim cond, p, val  ; dominio ari
;   logic cmpn c1, cond   ; dominio logic
;   Coste: O(2K).
;
; Anidación (NO HACER):
;   logic proc cond, x, y
;       logic ari lim cond, p, val
;   Coste: O(3K) o peor.
;   Requiere guardar/restaurar rbx en cada nivel.
;   Rompe la independencia de los opcodes.
;
; La composición secuencial es suficiente porque:
;   - Los dominios son ortogonales.
;   - El estado del sistema (logic_space) es compartido.
;   - Cada opcode es independiente.
;=========================================
