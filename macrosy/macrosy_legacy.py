import re
import sys

CONTADOR_SALTOS_GLOBAL = 0

def evaluar_expresion(expr, contexto):
    for var, val in contexto.items():
        expr = expr.replace(var, str(val))
    try:
        if re.match(r'^[\d\s\+\-\*\/\(\)]+$', expr):
            return int(eval(expr))
        else:
            return int(expr)
    except:
        return 0

def expandir_lineas_macros(lineas, macros_registradas, definiciones_texto, contexto_assign):
    global CONTADOR_SALTOS_GLOBAL
    codigo_arm_final = []
    en_rep = False
    bloque_rep = []
    veces_rep = 0
    
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        # 1. CAPTURAMOS LA INDENTACIÓN ORIGINAL (Espacios o tabs al inicio)
        match_indentacion = re.match(r'^([ \t]*)', linea)
        indentacion_original = match_indentacion.group(1) if match_indentacion else ""
        
        linea_limpia = linea.strip()
        
        # Si la línea es un comentario puro de %##, se mantiene o se descarta según prefieras.
        # Para que desaparezca por completo todo %##, lo podamos acá:
        if linea_limpia.startswith('%##'):
            # Si querés que los comentarios puros desaparezcan del todo, poné 'i += 1; continue'
            # Si querés preservarlos como líneas de bitácora puras, descomentá la siguiente línea:
            # codigo_arm_final.append(linea)
            i += 1
            continue
            
        if not linea_limpia:
            codigo_arm_final.append(linea)
            i += 1
            continue

        # --- MANEJO DE %assign ---
        if linea_limpia.startswith('%assign'):
            partes = re.split(r'\s+', linea_limpia, 2)
            if len(partes) >= 3:
                var_name, expr = partes[1], partes[2]
                contexto_assign[var_name] = evaluar_expresion(expr, contexto_assign)
            i += 1
            continue

        # --- MANEJO DE %rep / %endrep ---
        if linea_limpia.startswith('%rep'):
            partes = re.split(r'\s+', linea_limpia, 1)
            veces_rep = evaluar_expresion(partes[1], contexto_assign)
            en_rep = True
            bloque_rep = []
            i += 1
            continue
            
        if linea_limpia.startswith('%endrep'):
            en_rep = False
            for _ in range(veces_rep):
                contexto_temporal = contexto_assign.copy()
                bloque_expandido = expandir_lineas_macros(bloque_rep, macros_registradas, definiciones_texto, contexto_temporal)
                for linea_exp in bloque_expandido.split('\n'):
                    for var, val in contexto_temporal.items():
                        linea_exp = linea_exp.replace(f'%[{var}]', str(val))
                    for nombre, reemplazo in definiciones_texto.items():
                        linea_exp = linea_exp.replace(nombre, reemplazo)
                    codigo_arm_final.append(linea_exp)
            i += 1
            continue
            
        if en_rep:
            bloque_rep.append(linea)
            i += 1
            continue

        # --- DETECCIÓN E INVOCACIÓN DE MACROS ---
        # Poda quirúrgica de comentarios en la línea de la llamada
        linea_sin_comentario_lineal = linea_limpia.split('%##')[0].strip()
        tokens = re.split(r'[\s,]+', linea_sin_comentario_lineal)
        posible_macro = tokens[0]
        
        if posible_macro in macros_registradas:
            cant_args, cuerpo_macro = macros_registradas[posible_macro]
            args_llamada = [t.strip() for t in re.split(r'[\s,]+', linea_sin_comentario_lineal)[1:] if t.strip()]
            
            CONTADOR_SALTOS_GLOBAL += 1
            sufijo_unico = f"_{CONTADOR_SALTOS_GLOBAL}"
            
            cuerpo_reemplazado = []
            for l_cuerpo in cuerpo_macro:
                # Poda absoluta de %## dentro de las líneas del cuerpo de la macro
                if l_cuerpo.strip().startswith('%##'):
                    continue
                
                l_mod = l_cuerpo.split('%##')[0] # Nos quedamos sólo con el código útil
                
                saltar_linea = False
                for idx, arg_val in enumerate(args_llamada):
                    token_arg = f"%{idx+1}"
                    if arg_val == "%_":
                        if token_arg in l_mod:
                            saltar_linea = True
                            break
                    else:
                        l_mod = l_mod.replace(token_arg, arg_val)
                
                if saltar_linea:
                    continue
                
                l_mod = re.sub(r'%%([a-zA-Z0-9_]+)', r'\1' + sufijo_unico, l_mod)
                
                # INYECTAMOS LA INDENTACIÓN ORIGINAL a la línea del cuerpo expandido
                # Evitamos duplicarla si la línea ya venía con espacios heredados internamente
                if l_mod.strip():
                    cuerpo_reemplazado.append(indentacion_original + l_mod.maxsplit if hasattr(l_mod, 'maxsplit') else l_mod)
                else:
                    cuerpo_reemplazado.append(l_mod)
            
            if cuerpo_reemplazado:
                # Pasamos el bloque manteniendo el contexto de indentación heredado
                cuerpo_expandido_final = expandir_lineas_macros(cuerpo_reemplazado, macros_registradas, definiciones_texto, contexto_assign)
                codigo_arm_final.append(cuerpo_expandido_final)
            i += 1
            continue

        # Línea estándar (No macro)
        # Limpiamos cualquier comentario %## al final de líneas comunes
        linea_final = linea.split('%##')[0]
        
        for nombre, reemplazo in definiciones_texto.items():
            linea_final = linea_final.replace(nombre, reemplazo)
            
        for var, val in contexto_assign.items():
            linea_final = linea_final.replace(f'%[{var}]', str(val))
            
        codigo_arm_final.append(linea_final.rstrip())
        i += 1
        
    return '\n'.join(codigo_arm_final)

def transpilar_uzy_a_arm(codigo_nasm):
    # (El resto de la función inicial se mantiene igual, limpiando los %## en la primera lectura)
    lineas = codigo_nasm.split('\n')
    macros_registradas = {}
    definiciones_texto = {}
    contexto_assign = {}
    lineas_filtradas_sin_definiciones = []
    en_macro = False
    macro_actual_nombre = ""
    macro_actual_args = 0
    macro_actual_cuerpo = []
    
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            lineas_filtradas_sin_definiciones.append(linea)
            continue
            
        linea_sin_comentario = linea_limpia.split('%##')[0].strip()
        
        if not linea_sin_comentario:
            # Preservamos la línea vacía o el comentario puro si fuera necesario
            lineas_filtradas_sin_definiciones.append(linea)
            continue

        if linea_sin_comentario.startswith('%define'):
            partes = re.split(r'\s+', linea_sin_comentario, 2)
            if len(partes) >= 3:
                definiciones_texto[partes[1]] = partes[2]
            continue
            
        if linea_sin_comentario.startswith('%macro'):
            partes = re.split(r'\s+', linea_sin_comentario, 2)
            macro_actual_nombre = partes[1]
            macro_actual_args = int(partes[2]) if len(partes) > 2 else 0
            macro_actual_cuerpo = []
            en_macro = True
            continue
            
        if linea_sin_comentario.startswith('%endmacro'):
            macros_registradas[macro_actual_nombre] = (macro_actual_args, macro_actual_cuerpo)
            en_macro = False
            continue
            
        if en_macro:
            macro_actual_cuerpo.append(linea)
            continue
            
        lineas_filtradas_sin_definiciones.append(linea)
        
    return expandir_lineas_macros(lineas_filtradas_sin_definiciones, macros_registradas, definiciones_texto, contexto_assign)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 macrosy6.py <fuente> <renombre>")
        sys.exit(1)
    archivo_a, nombre_salida = sys.argv[1], sys.argv[2]
    try:
        with open(archivo_a, "r") as f_a:
            font_code = transpilar_uzy_a_arm(f_a.read())
        with open(nombre_salida, "w") as f_out:
            f_out.write(font_code)
        print("¡Transpilación exitosa sin residuos!")
    except Exception as e:
        print(f"Error al procesar los archivos: {e}")
