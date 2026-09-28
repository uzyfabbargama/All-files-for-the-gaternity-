#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preprocesador_v8.py
Traduce N-Lang (NeuralScript) a bytecode binario legible.
Soporta: var, proc, decay, growth, conv, norm, drop, logic, ari.
Soporta punteros: var n[puntero], ari var/add/sub/lim.
Soporta comentarios: $ hasta fin de línea.
"""

import sys
import struct

# ============================================================
# GLOBAL
# ============================================================
class GlobalState:
    def __init__(self):
        self.archivo_final = bytearray()
        self.font_code = ""
        self.salida = ""
        self.cantidad_neuronas = 0
        self.cantidad_funciones = 0
        self.cantidad_var_logic = 0
        self.cantidad_args = 0
        self.cantidad_punteros = 0
        self.neuronas = {}       # nombre → ID
        self.funciones = {}      # nombre → ID
        self.var_logic = {}      # nombre → ID
        self.args = {}           # nombre → ID
        self.punteros = {}       # nombre → ID
        self.bucles = []

GLOBAL = GlobalState()

# ============================================================
# HASH XORID (para keywords)
# ============================================================
#def xorid(texto):
#    """Calcula el hash XORID de una palabra."""
#    idx = 0
#    for car in texto:
#        idx = (idx ^ ord(car)) << 1
#        idx &= 0xFFFF
#    return idx

# ============================================================
# ESCRITOR DE BYTECODE LEGIBLE
# ============================================================
def escribir_bytecode_legible(archivo_bin, archivo_txt):
    """Convierte un binario a texto legible (hex + ASCII)."""
    with open(archivo_bin, 'rb') as f:
        data = f.read()
    with open(archivo_txt, 'w') as f:
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hexa = ' '.join(f'{b:02x}' for b in chunk)
            ascii_ = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            f.write(f'{i:08x}  {hexa:<48}  {ascii_}\n')
    print(f"[+] Bytecode legible generado: {archivo_txt}")

# ============================================================
# ESCRITURA DE ENTEROS
# ============================================================
def write_uint8(buf, value):
    buf.append(value & 0xFF)

def write_uint24(buf, value):
    """Escribe un entero de 24 bits (3 bytes) en little-endian."""
    buf.extend(struct.pack('<I', value & 0xFFFFFF)[:3])

def write_uint56(buf, value):
    """Escribe un entero de 56 bits (7 bytes) en little-endian."""
    buf.extend(struct.pack('<Q', value & 0xFFFFFFFFFFFFFF)[:7])

# ============================================================
# UTILIDADES DE TEXTO
# ============================================================
def limpiar_comentarios(texto):
    """
    Elimina los comentarios:
    - $ hasta fin de línea (comentario de línea)
    - $\ ... \$ (comentario multilínea)
    """
    resultado = []
    i = 0
    n = len(texto)
    en_bloque = False
    
    while i < n:
        # Detectar inicio de bloque $\
        if not en_bloque and i + 1 < n and texto[i] == '$' and texto[i+1] == '\\':
            en_bloque = True
            i += 2
            continue
        
        # Detectar fin de bloque \$
        if en_bloque and i + 1 < n and texto[i] == '\\' and texto[i+1] == '$':
            en_bloque = False
            i += 2
            continue
        
        # Si estamos en bloque, saltamos todo
        if en_bloque:
            i += 1
            continue
        
        # Detectar comentario de línea $
        if texto[i] == '$':
            # Saltar hasta fin de línea
            while i < n and texto[i] != '\n':
                i += 1
            continue
        
        # Carácter normal
        resultado.append(texto[i])
        i += 1
    
    return ''.join(resultado)

def siguiente_palabra(texto):
    """Devuelve (palabra, resto) desde el inicio del texto."""
    texto = texto.lstrip()
    if not texto:
        return "", ""
    if ' ' in texto:
        idx = texto.index(' ')
        return texto[:idx], texto[idx+1:]
    if '\n' in texto:
        idx = texto.index('\n')
        return texto[:idx], texto[idx+1:]
    return texto, ""

def es_fin(texto):
    """Devuelve True si el texto está vacío o solo tiene espacios."""
    return not texto or not texto.strip()

# ============================================================
# OBTENER IDs (neuronas, funciones, lógicas, punteros)
# ============================================================
def obtener_id_neuron(nombre):
    if nombre not in GLOBAL.neuronas:
        GLOBAL.neuronas[nombre] = GLOBAL.cantidad_neuronas
        GLOBAL.cantidad_neuronas += 1
    return GLOBAL.neuronas[nombre]

def obtener_id_funcion(nombre):
    if nombre not in GLOBAL.funciones:
        GLOBAL.funciones[nombre] = GLOBAL.cantidad_funciones
        GLOBAL.cantidad_funciones += 1
    return GLOBAL.funciones[nombre]

def obtener_id_var_logic(nombre):
    if nombre not in GLOBAL.var_logic:
        GLOBAL.var_logic[nombre] = GLOBAL.cantidad_var_logic
        GLOBAL.cantidad_var_logic += 1
    return GLOBAL.var_logic[nombre]

def obtener_id_arg(nombre):
    if nombre not in GLOBAL.args:
        GLOBAL.args[nombre] = GLOBAL.cantidad_args
        GLOBAL.cantidad_args += 1
    return GLOBAL.args[nombre]

def obtener_id_puntero(nombre):
    if nombre not in GLOBAL.punteros:
        GLOBAL.punteros[nombre] = GLOBAL.cantidad_punteros
        GLOBAL.cantidad_punteros += 1
    return GLOBAL.punteros[nombre]

# ============================================================
# CONVERSIÓN DE FLOAT A 56 BITS
# ============================================================
def float_a_bit56(valor):
    """Convierte un float (0.0 a 1.999...) a 56 bits (7 bytes)."""
    entero = 1 if valor >= 1.0 else 0
    frac = valor - entero
    frac_bits = int(frac * (2 ** 55))
    return (entero << 55) | (frac_bits & ((1 << 55) - 1))

# ============================================================
# PROCESAR NEURONA + VALOR  (var, decay, growth)
# ============================================================
def procesar_neuron_val():
    """var n1, 0.5 | decay n1, 0.1 | growth n1, 0.2"""
    global GLOBAL
    # Leer keyword (var/decay/growth)
    keyword, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.archivo_final.extend(keyword.encode('ascii'))
    GLOBAL.archivo_final.append(0x20)  # espacio
    GLOBAL.font_code = resto

    # Leer neurona (puede ser n1 o n[puntero])
    neurona, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.font_code = resto

    # ¿Es puntero?
    if '[' in neurona:
        nombre = neurona[:neurona.index('[')]
        puntero = neurona[neurona.index('[')+1:neurona.index(']')]
        id_neuron = obtener_id_neuron(nombre)
        id_puntero = obtener_id_puntero(puntero)
        # Escribir ID de neurona (3 bytes)
        write_uint24(GLOBAL.archivo_final, id_neuron)
        # Escribir '[', ID de puntero, ']'
        GLOBAL.archivo_final.append(ord('['))
        write_uint24(GLOBAL.archivo_final, id_puntero)
        GLOBAL.archivo_final.append(ord(']'))
    else:
        id_neuron = obtener_id_neuron(neurona)
        write_uint24(GLOBAL.archivo_final, id_neuron)

    # Leer valor (float)
    valor_str, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.font_code = resto
    try:
        valor = float(valor_str)
    except ValueError:
        print(f"[-] Error: valor no válido: {valor_str}")
        return

    # Escribir valor como 7 bytes (56 bits)
    bits = float_a_bit56(valor)
    write_uint56(GLOBAL.archivo_final, bits)

# ============================================================
# PROCESAR NEURONA + NEURONA  (proc, norm, drop)
# ============================================================
def procesar_neuron_neuron():
    """proc n1, n2 | norm n1, n2 | drop n1, n2"""
    global GLOBAL
    keyword, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.archivo_final.extend(keyword.encode('ascii'))
    GLOBAL.archivo_final.append(0x20)
    GLOBAL.font_code = resto

    # Leer neurona 1
    n1, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.font_code = resto
    if '[' in n1:
        nombre = n1[:n1.index('[')]
        puntero = n1[n1.index('[')+1:n1.index(']')]
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(nombre))
        GLOBAL.archivo_final.append(ord('['))
        write_uint24(GLOBAL.archivo_final, obtener_id_puntero(puntero))
        GLOBAL.archivo_final.append(ord(']'))
    else:
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n1))
    # Quitar la coma
    if GLOBAL.font_code.startswith(','):
        GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()

    # Leer neurona 2
    n2, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.font_code = resto
    if '[' in n2:
        nombre = n2[:n2.index('[')]
        puntero = n2[n2.index('[')+1:n2.index(']')]
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(nombre))
        GLOBAL.archivo_final.append(ord('['))
        write_uint24(GLOBAL.archivo_final, obtener_id_puntero(puntero))
        GLOBAL.archivo_final.append(ord(']'))
    else:
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n2))

# ============================================================
# PROCESAR NEURONA + NEURONA + BIAS  (conv)
# ============================================================
def procesar_neuron_neuron_bias():
    """conv n1, n2, bias"""
    global GLOBAL
    keyword, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.archivo_final.extend(keyword.encode('ascii'))
    GLOBAL.archivo_final.append(0x20)
    GLOBAL.font_code = resto

    for i in range(3):
        n, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        if i < 2:
            if '[' in n:
                nombre = n[:n.index('[')]
                puntero = n[n.index('[')+1:n.index(']')]
                write_uint24(GLOBAL.archivo_final, obtener_id_neuron(nombre))
                GLOBAL.archivo_final.append(ord('['))
                write_uint24(GLOBAL.archivo_final, obtener_id_puntero(puntero))
                GLOBAL.archivo_final.append(ord(']'))
            else:
                write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n))
        else:
            try:
                bias = float(n)
            except ValueError:
                print(f"[-] Error: bias no válido: {n}")
                return
            write_uint56(GLOBAL.archivo_final, float_a_bit56(bias))

        # Quitar coma
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()

# ============================================================
# PROCESAR LOGIC
# ============================================================
def procesar_logic():
    """logic <subcomando> ..."""
    global GLOBAL
    # Saltar "logic "
    GLOBAL.font_code = GLOBAL.font_code[6:].lstrip()

    subcomando, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.font_code = resto

    # Escribir "logic " + subcomando
    GLOBAL.archivo_final.extend(b"logic ")
    GLOBAL.archivo_final.extend(subcomando.encode('ascii'))
    GLOBAL.archivo_final.append(0x20)

    if subcomando == "cmp":
        # logic cmp var_cond, n1, n2
        var_cond, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_var_logic(var_cond))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        n1, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n1))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        n2, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n2))

    elif subcomando == "cmpv":
        # logic cmpv var_cond, n1, valor
        var_cond, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_var_logic(var_cond))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        n1, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n1))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        valor_str, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        try:
            valor = float(valor_str)
        except ValueError:
            print(f"[-] Error: valor no válido: {valor_str}")
            return
        write_uint56(GLOBAL.archivo_final, float_a_bit56(valor))

    elif subcomando == "cmpn":
        # logic cmpn var_cond, n1
        var_cond, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_var_logic(var_cond))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        n1, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n1))

    elif subcomando == "loop":
        # logic loop var_cond
        var_cond, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_var_logic(var_cond))
        GLOBAL.bucles.append(var_cond)

    elif subcomando == "endloop":
        # logic endloop
        if GLOBAL.bucles:
            GLOBAL.bucles.pop()

    elif subcomando == "def":
        # logic def func_id
        func, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_funcion(func))

    elif subcomando == "endef":
        # logic endef
        pass

    elif subcomando == "yes":
        # logic yes var_cond
        var_cond, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_var_logic(var_cond))

    elif subcomando == "no":
        # logic no var_cond
        var_cond, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_var_logic(var_cond))

    elif subcomando == "endcond":
        # logic endcond
        pass

    elif subcomando == "prom":
        # logic prom n_destino, n1, n2
        n_dest, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n_dest))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        n1, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n1))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        n2, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_neuron(n2))

    elif subcomando == "use":
        # logic use func_id
        func, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_funcion(func))

    else:
        print(f"[-] Subcomando logic desconocido: {subcomando}")

# ============================================================
# PROCESAR ARI (aritmética de punteros)
# ============================================================
def procesar_ari():
    """ari <subcomando> <puntero>, <valor>"""
    global GLOBAL
    # Saltar "ari "
    GLOBAL.font_code = GLOBAL.font_code[4:].lstrip()

    subcomando, resto = siguiente_palabra(GLOBAL.font_code)
    GLOBAL.font_code = resto

    # Escribir "ari " + subcomando
    GLOBAL.archivo_final.extend(b"ari ")
    GLOBAL.archivo_final.extend(subcomando.encode('ascii'))
    GLOBAL.archivo_final.append(0x20)

    if subcomando == "var":
        # ari var puntero, 0
        puntero, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_puntero(puntero))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        valor_str, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        try:
            valor = int(valor_str)
        except ValueError:
            print(f"[-] Error: valor no válido: {valor_str}")
            return
        write_uint24(GLOBAL.archivo_final, valor)

    elif subcomando in ("add", "sub", "lim"):
        # ari add/sub/lim puntero, valor
        puntero, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        write_uint24(GLOBAL.archivo_final, obtener_id_puntero(puntero))
        if GLOBAL.font_code.startswith(','):
            GLOBAL.font_code = GLOBAL.font_code[1:].lstrip()
        valor_str, resto = siguiente_palabra(GLOBAL.font_code)
        GLOBAL.font_code = resto
        try:
            valor = int(valor_str)
        except ValueError:
            print(f"[-] Error: valor no válido: {valor_str}")
            return
        write_uint24(GLOBAL.archivo_final, valor)

    else:
        print(f"[-] Subcomando ari desconocido: {subcomando}")

# ============================================================
# BUCLE PRINCIPAL
# ============================================================
def procesar_texto(font_code, salida):
    """Procesa el código fuente y genera bytecode."""
    global GLOBAL
    GLOBAL.font_code = limpiar_comentarios(font_code)
    GLOBAL.salida = salida
    GLOBAL.archivo_final = bytearray()

    while not es_fin(GLOBAL.font_code):
        palabra, resto = siguiente_palabra(GLOBAL.font_code)
        if palabra == "var" or palabra == "decay" or palabra == "growth":
            procesar_neuron_val()
        elif palabra == "proc" or palabra == "norm" or palabra == "drop":
            procesar_neuron_neuron()
        elif palabra == "conv":
            procesar_neuron_neuron_bias()
        elif palabra == "logic":
            procesar_logic()
        elif palabra == "ari":
            procesar_ari()
        else:
            print(f"[-] Comando desconocido: {palabra}")
            GLOBAL.font_code = resto
            continue
        # Actualizar font_code (cada función lo actualiza)
        # (ya lo hacen las funciones)

    return GLOBAL.archivo_final

# ============================================================
# MAIN
# ============================================================
def main():
    if len(sys.argv) > 2:
        archivo_fuente = sys.argv[1]  # archivo .ns
        archivo_salida = sys.argv[2]  # archivo .bin
        archivo_legible = archivo_salida + ".txt"  # opcional

        with open(archivo_fuente, 'r') as f:
            codigo = f.read()

        procesar_texto(codigo, archivo_salida)

        with open(archivo_salida, 'wb') as f:
            f.write(GLOBAL.archivo_final)

        print(f"[+] Archivo generado: {archivo_salida}")
        print(f"[+] Tamaño: {len(GLOBAL.archivo_final)} bytes")

        # Generar bytecode legible
        escribir_bytecode_legible(archivo_salida, archivo_legible)
    else:
        print("Uso: preprocesador.py <archivo.ns> <salida.bin>")
        sys.exit(1)

if __name__ == "__main__":
    main()
