import re
import sys
import textwrap

CONTADOR_SALTOS_GLOBAL = 0

import ast
import operator

def evaluar_expresion(expr, contexto):
    """
    Evalúa expresiones aritméticas, lógicas, comparativas y slicing de strings.
    Versión SEGURA sin eval() directo.
    """
    
    # --- PASO 1: Preprocesar operadores ---
    # IMPORTANTE: El orden importa (<= antes que <, >= antes que >)
    expr_pre = (expr
        .replace('&&', ' and ')
        .replace('||', ' or ')
        .replace('==', ' == ')
        .replace('!=', ' != ')
        .replace('<=', ' <= ')
        .replace('>=', ' >= ')
        .replace('<', ' < ')
        .replace('>', ' > ')
        .replace('&', ' and ')
        .replace('|', ' or ')
    )
    
    # --- PASO 2: Reemplazo de variables y slicing de strings ---
    for var, val in sorted(contexto.items(), key=lambda x: len(x[0]), reverse=True):
        if isinstance(val, str):
            # Slicing múltiple: var[0,1,2]
            def reemplazar_slice(match):
                indices = [int(i.strip()) for i in match.group(1).split(',')]
                subcadena = "".join([val[i] for i in indices if 0 <= i < len(val)])
                return f'"{subcadena}"' if subcadena else '""'
            
            # Slicing individual: var[10]
            def reemplazar_index(match):
                idx = int(match.group(1).strip())
                if 0 <= idx < len(val):
                    return f'"{val[idx]}"'
                return '""'
            
            expr_pre = re.sub(rf'{var}\[([0-9\s,]+)\]', reemplazar_slice, expr_pre)
            expr_pre = re.sub(rf'{var}\[(\d+)\]', reemplazar_index, expr_pre)
            # Reemplazar variable por su valor literal
            expr_pre = expr_pre.replace(var, f'"{val}"')
        else:
            expr_pre = expr_pre.replace(var, str(val))
    
    # --- PASO 3: Convertir caracteres entre comillas a ASCII si hay operaciones ---
    if re.search(r'["\'].["\']\s*[\-\+\*\/]', expr_pre) or re.search(r'[\-\+\*\/]\s*["\'].["\']', expr_pre):
        expr_pre = re.sub(r'["\'](.)["\']', lambda m: str(ord(m.group(1))), expr_pre)
    
    # --- PASO 4: Evaluación SEGURA con AST ---
    try:
        tree = ast.parse(expr_pre, mode='eval')
        
        # Nodos permitidos (lista blanca)
        NODOS_PERMITIDOS = (
            ast.Expression, ast.Constant, ast.Name, ast.BinOp, ast.UnaryOp,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
            ast.And, ast.Or, ast.Not, ast.Compare,
            ast.Eq, ast.NotEq, ast.Lt, ast.Gt, ast.LtE, ast.GtE,
            ast.Load, ast.BoolOp, ast.USub, ast.UAdd
        )
        
        def eval_node(node):
            if not isinstance(node, NODOS_PERMITIDOS):
                raise ValueError(f"Nodo no permitido: {type(node).__name__} en expresión: {expr_pre}")
            
            if isinstance(node, ast.Constant):
                return node.value
            
            if isinstance(node, ast.Name):
                return contexto.get(node.id, 0)
            
            if isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                ops = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.FloorDiv: operator.floordiv,
                    ast.Mod: operator.mod,
                    ast.And: lambda a, b: 1 if (a and b) else 0,
                    ast.Or: lambda a, b: 1 if (a or b) else 0,
                }
                return ops.get(type(node.op), lambda a, b: 0)(left, right)
            
            if isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                if isinstance(node.op, ast.USub):
                    return -operand
                if isinstance(node.op, ast.UAdd):
                    return +operand
                if isinstance(node.op, ast.Not):
                    return 1 if not operand else 0
                return operand
            
            if isinstance(node, ast.Compare):
                left = eval_node(node.left)
                ops = {
                    ast.Eq: operator.eq,
                    ast.NotEq: operator.ne,
                    ast.Lt: operator.lt,
                    ast.Gt: operator.gt,
                    ast.LtE: operator.le,
                    ast.GtE: operator.ge,
                }
                for op, right in zip(node.ops, node.comparators):
                    right_val = eval_node(right)
                    if not ops.get(type(op), lambda a, b: False)(left, right_val):
                        return 0
                    left = right_val
                return 1
            
            if isinstance(node, ast.BoolOp):
                values = [eval_node(v) for v in node.values]
                if isinstance(node.op, ast.And):
                    return 1 if all(values) else 0
                if isinstance(node.op, ast.Or):
                    return 1 if any(values) else 0
                return 0
            
            return 0
        
        resultado = eval_node(tree.body)
        
        # Convertir bool a int para consistencia
        if isinstance(resultado, bool):
            return 1 if resultado else 0
        
        # Si es string, limpiar comillas
        if isinstance(resultado, str):
            return resultado.strip('"\'')
        
        return int(resultado) if isinstance(resultado, (int, float)) else 0
        
    except Exception as e:
        # Modo DEBUG: descomentar para ver errores
        # print(f"[DEBUG] Error evaluando: {expr_pre} -> {e}")
        return 0

def expandir_lineas_macros(lineas, macros_registradas, definiciones_texto, contexto_assign):
    global CONTADOR_SALTOS_GLOBAL
    codigo_arm_final = []
    
    en_rep = False
    bloque_rep = []
    veces_rep = 0
    
    stack_condicion = []

    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        match_indentacion = re.match(r'^([ \t]*)', linea)
        indentacion_original = match_indentacion.group(1) if match_indentacion else ""
        
        linea_limpia = linea.strip()
        
        if linea_limpia.startswith('%##'):
            i += 1
            continue
            
        if not linea_limpia:
            if all(frame['activo'] for frame in stack_condicion):
                codigo_arm_final.append(linea)
            i += 1
            continue

        # --- MANEJO DE %rep / %endrep ---
        if linea_limpia.startswith('%rep'):
            partes = re.split(r'\s+', linea_limpia, 1)
            veces_rep = int(evaluar_expresion(partes[1], contexto_assign))
            en_rep = True
            bloque_rep = []
            i += 1
            continue
            
        if linea_limpia.startswith('%endrep'):
            en_rep = False
            for _ in range(veces_rep):
                bloque_expandido = expandir_lineas_macros(bloque_rep, macros_registradas, definiciones_texto, contexto_assign)
                if bloque_expandido:
                    codigo_arm_final.append(bloque_expandido)
            i += 1
            continue
            
        if en_rep:
            bloque_rep.append(linea)
            i += 1
            continue

        # Reemplazo de %[var]
        for var, val in contexto_assign.items():
            linea_limpia = linea_limpia.replace(f'%[{var}]', str(val))
            linea = linea.replace(f'%[{var}]', str(val))

        # --- MANEJO DE %str (CAPTURA DE STRING EN VARIABLE) ---
        if linea_limpia.startswith('%str'):
            partes = re.split(r'\s+', linea_limpia, 2)
            if len(partes) >= 3:
                var_name, texto_raw = partes[1], partes[2]
                # Limpiamos comillas envolventes si las tiene
                texto_limpio = texto_raw.strip('"\'')
                contexto_assign[var_name] = texto_limpio
            i += 1
            continue

        # --- BLOQUE CONDICIONAL: %if, %elif, %else, %endif ---
        if linea_limpia.startswith('%if'):
            partes = re.split(r'\s+', linea_limpia, 1)
            condicion_valida = False
            
            padre_activo = all(frame['activo'] for frame in stack_condicion)
            if padre_activo and len(partes) > 1:
                res = evaluar_expresion(partes[1], contexto_assign)
                condicion_valida = bool(res)

            stack_condicion.append({
                'ejecutado': condicion_valida,
                'activo': padre_activo and condicion_valida
            })
            i += 1
            continue

        if linea_limpia.startswith('%elif'):
            if stack_condicion:
                frame = stack_condicion[-1]
                padre_activo = all(f['activo'] for f in stack_condicion[:-1])
                
                if padre_activo and not frame['ejecutado']:
                    partes = re.split(r'\s+', linea_limpia, 1)
                    condicion_valida = bool(evaluar_expresion(partes[1], contexto_assign)) if len(partes) > 1 else False
                    frame['activo'] = condicion_valida
                    if condicion_valida:
                        frame['ejecutado'] = True
                else:
                    frame['activo'] = False
            i += 1
            continue

        if linea_limpia.startswith('%else'):
            if stack_condicion:
                frame = stack_condicion[-1]
                padre_activo = all(f['activo'] for f in stack_condicion[:-1])
                frame['activo'] = padre_activo and (not frame['ejecutado'])
                frame['ejecutado'] = True
            i += 1
            continue

        if linea_limpia.startswith('%endif'):
            if stack_condicion:
                stack_condicion.pop()
            i += 1
            continue

        if not all(frame['activo'] for frame in stack_condicion):
            i += 1
            continue

        # --- MANEJO DE %assign ---
        if linea_limpia.startswith('%assign'):
            partes = re.split(r'\s+', linea_limpia, 2)
            if len(partes) >= 3:
                var_name, expr = partes[1], partes[2]
                res = evaluar_expresion(expr, contexto_assign)
                # Si nos devolvió un string recortado, lo dejamos como string, si no como int
                contexto_assign[var_name] = str(res).strip('"') if isinstance(res, str) else res
            i += 1
            continue

        # --- DETECCIÓN E INVOCACIÓN DE MACROS ---
        linea_sin_comentario_lineal = linea_limpia.split('%##')[0].strip()
        
        # Extraemos el nombre de la macro considerando que los argumentos pueden ser cadenas entre comillas
        match_macro = re.match(r'^([a-zA-Z0-9_]+)\s*(.*)$', linea_sin_comentario_lineal)
        if match_macro:
            posible_macro = match_macro.group(1)
            resto_args = match_macro.group(2).strip()
            
            if posible_macro in macros_registradas:
                cant_args, cuerpo_macro = macros_registradas[posible_macro]
                
                # Respetamos strings completos como un solo argumento
                args_llamada = [a.strip() for a in re.findall(r'".+?"|\'.+?\'|\S+', resto_args)]
                
                CONTADOR_SALTOS_GLOBAL += 1
                sufijo_unico = f"_{CONTADOR_SALTOS_GLOBAL}"
                
                cuerpo_reemplazado = []
                for l_cuerpo in cuerpo_macro:
                    if l_cuerpo.strip().startswith('%##'):
                        continue
                    
                    l_mod = l_cuerpo.split('%##')[0]
                    saltar_linea = False
                    
                    for idx, arg_val in enumerate(args_llamada):
                        token_arg = f"%{idx+1}"
                        if arg_val == "%_":
                            # Este argumento se "come" - no reemplazar nada
                            # Simplemente saltar esta expansión
                            continue
                        else:
                            l_mod = l_mod.replace(token_arg, arg_val)
                    
                    if saltar_linea:
                        continue
                    
                    l_mod = re.sub(r'%%([a-zA-Z0-9_]+)', r'\1' + sufijo_unico, l_mod)
                    
                    if l_mod.strip():
                        cuerpo_reemplazado.append(indentacion_original + l_mod)
                    else:
                        cuerpo_reemplazado.append(l_mod)
                
                if cuerpo_reemplazado:
                    cuerpo_expandido_final = expandir_lineas_macros(cuerpo_reemplazado, macros_registradas, definiciones_texto, contexto_assign)
                    if cuerpo_expandido_final:
                        codigo_arm_final.append(cuerpo_expandido_final)
                i += 1
                continue

        # Línea estándar
        linea_final = linea.split('%##')[0]
        for nombre, reemplazo in definiciones_texto.items():
            linea_final = linea_final.replace(nombre, reemplazo)
            
        codigo_arm_final.append(linea_final.rstrip())
        i += 1
        
    return '\n'.join(codigo_arm_final)

def transpilar_uzy_a_arm(codigo_nasm):
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
            cuerpo_normalizado = textwrap.dedent("\n".join(macro_actual_cuerpo)).split("\n")
            macros_registradas[macro_actual_nombre] = (macro_actual_args, cuerpo_normalizado)
            en_macro = False
            continue
            
        if en_macro:
            macro_actual_cuerpo.append(linea)
            continue
            
        lineas_filtradas_sin_definiciones.append(linea)
        
    return expandir_lineas_macros(lineas_filtradas_sin_definiciones, macros_registradas, definiciones_texto, contexto_assign)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 macrosy9.py <fuente> <renombre>")
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
