import sys
import struct
import argparse
import ctypes
import os

def float_to_custom56(val):
    """Convierte un float (0.0 a 1.999...) o int al formato entero de 56 bits de NeuralScript."""
    if isinstance(val, int):
        return val << 8
    elif isinstance(val, float):
        entero = 1 if val >= 1.0 else 0
        frac = val - entero
        frac_bits = int(frac * (2 ** 55))
        return (entero << 55) | (frac_bits & ((1 << 55) - 1))
    elif isinstance(val, str):
        if val.startswith('0x') or val.startswith('0X'):
            return int(val, 16)
        else:
            return int(float(val) * (1 << 55))
    return 0

def write_uint32(buf, value):
    buf.extend(struct.pack('<I', value))

def write_uint64(buf, value):
    buf.extend(struct.pack('<Q', value))

def write_uint8(buf, value):
    buf.append(value & 0xFF)

def compilar_hibrido_ns(source_code):
    neuron_map = {}
    logic_var_map = {}
    function_map = {}  # nombre → {id, start, end, args}
    
    next_neuron_offset = 0x01
    next_logic_offset = 0x01
    next_func_offset = 0x01
    
    def get_neuron_id(name):
        nonlocal next_neuron_offset
        if name not in neuron_map:
            neuron_map[name] = next_neuron_offset
            next_neuron_offset += 1
        return neuron_map[name]

    def get_logic_id(name):
        nonlocal next_logic_offset
        if name not in logic_var_map:
            logic_var_map[name] = next_logic_offset
            next_logic_offset += 1
        return logic_var_map[name]
    
    def get_func_id(name):
        nonlocal next_func_offset
        if name not in function_map:
            function_map[name] = {
                'id': next_func_offset,
                'start': None,
                'end': None,
                'args': {}
            }
            next_func_offset += 1
        return function_map[name]['id']
    
    # PASO 1: ESCANEAR FUNCIONES
    lines = source_code.splitlines()
    function_boundaries = {}
    current_func = None
    
    for i, line in enumerate(lines):
        line_clean = line.split('$')[0].strip()
        if not line_clean:
            continue
            
        if line_clean.startswith('logic def'):
            tokens = line_clean.replace(',', ' ').split()
            if len(tokens) >= 3:
                func_name = tokens[2]
                current_func = func_name
                function_boundaries[func_name] = {
                    'start': i,
                    'end': None,
                    'args': []
                }
                
                # Extraer argumentos
                if '(' in line_clean:
                    args_part = line_clean.split('(')[1].split(')')[0]
                    function_boundaries[func_name]['args'] = [a.strip() for a in args_part.split(',') if a.strip()]
                    
        elif line_clean.startswith('logic endef'):
            if current_func and function_boundaries[current_func]['end'] is None:
                function_boundaries[current_func]['end'] = i
                current_func = None
            else:
                # Buscar la última función abierta
                for func_name in reversed(list(function_boundaries.keys())):
                    if function_boundaries[func_name]['end'] is None:
                        function_boundaries[func_name]['end'] = i
                        break
    
    # PASO 2: COMPILAR CON DIRECCIONES
    serialized_bytes = bytearray()
    
    for i, line in enumerate(lines):
        line = line.split('$')[0].strip()
        if not line:
            continue
            
        line_clean = line.replace(',', ' ')
        tokens = line_clean.split()
        if not tokens:
            continue
            
        cmd = tokens[0].lower()
        
        # --- VAR ---
        if cmd == 'var':
            var_name = tokens[1]
            val_str = tokens[2]
            try:
                if val_str.startswith('0x') or val_str.startswith('0X'):
                    val = int(val_str, 16)
                elif '.' in val_str:
                    val = float_to_custom56(float(val_str))
                else:
                    val = int(val_str, 0)
            except ValueError:
                val = float_to_custom56(float(val_str))

            var_id = get_neuron_id(var_name)
            
            serialized_bytes.extend(b'var ')
            write_uint32(serialized_bytes, var_id)
            serialized_bytes.extend(val.to_bytes(7, byteorder='little'))

        # --- PROC ---
        elif cmd == 'proc':
            n1_id = get_neuron_id(tokens[1])
            n2_id = get_neuron_id(tokens[2])
            
            serialized_bytes.extend(b'proc')
            write_uint32(serialized_bytes, n1_id)
            write_uint32(serialized_bytes, n2_id)

        # --- DECAY ---
        elif cmd == 'decay':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            val = int(float(val_str)) if '.' in val_str else int(val_str, 0)

            serialized_bytes.extend(b'decay ')
            write_uint32(serialized_bytes, n_id)
            write_uint8(serialized_bytes, val & 0xFF)

        # --- GROWTH ---
        elif cmd == 'growth':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            val = int(float(val_str)) if '.' in val_str else int(val_str, 0)

            serialized_bytes.extend(b'growth ')
            write_uint32(serialized_bytes, n_id)
            write_uint8(serialized_bytes, val & 0xFF)

        # --- PROM ---
        elif cmd == 'prom':
            dest_id = get_neuron_id(tokens[1])
            n1_id = get_neuron_id(tokens[2])
            n2_id = get_neuron_id(tokens[3])

            serialized_bytes.extend(b'prom')
            write_uint32(serialized_bytes, dest_id)
            write_uint32(serialized_bytes, n1_id)
            write_uint32(serialized_bytes, n2_id)

        # --- LOGIC ---
        elif cmd == 'logic':
            if len(tokens) < 2:
                continue
            subcmd = tokens[1].lower()

            # --- logic cmp ---
            if subcmd == 'cmp':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                n2_id = get_neuron_id(tokens[4])
                serialized_bytes.extend(b'logic cmp ')
                write_uint32(serialized_bytes, cond_id)
                write_uint32(serialized_bytes, n1_id)
                write_uint32(serialized_bytes, n2_id)

            # --- logic cmpv ---
            elif subcmd == 'cmpv':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                val_str = tokens[4]
                try:
                    val = int(float(val_str)) if '.' in val_str else int(val_str, 0)
                except:
                    val = 0
                serialized_bytes.extend(b'logic cmpv ')
                write_uint32(serialized_bytes, cond_id)
                write_uint32(serialized_bytes, n1_id)
                write_uint64(serialized_bytes, val)

            # --- logic cmpn ---
            elif subcmd == 'cmpn':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                serialized_bytes.extend(b'logic cmpn ')
                write_uint32(serialized_bytes, cond_id)
                write_uint32(serialized_bytes, n1_id)

            # --- logic loop ---
            elif subcmd == 'loop':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic loop ')
                write_uint32(serialized_bytes, cond_id)

            # --- logic endloop ---
            elif subcmd == 'endloop':
                serialized_bytes.extend(b'logic endloop ')

            # --- logic yes ---
            elif subcmd == 'yes':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic yes ')
                write_uint32(serialized_bytes, cond_id)

            # --- logic no ---
            elif subcmd == 'no':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic no ')
                write_uint32(serialized_bytes, cond_id)

            # --- logic endcond ---
            elif subcmd == 'endcond':
                serialized_bytes.extend(b'logic endcond ')

            # --- logic def ---
            elif subcmd == 'def':
                func_name = tokens[2]
                func_id = get_func_id(func_name)
                start_addr = len(serialized_bytes)
                
                # Guardar en function_map
                function_map[func_name]['start'] = start_addr
                
                # Guardar argumentos
                if func_name in function_boundaries:
                    for arg in function_boundaries[func_name]['args']:
                        arg_id = get_logic_id(arg)
                        function_map[func_name]['args'][arg] = arg_id
                
                # Escribir bytecode: def + func_id + start_addr
                serialized_bytes.extend(b'logic def ')
                write_uint32(serialized_bytes, func_id)
                write_uint32(serialized_bytes, start_addr)

            # --- logic endef ---
            elif subcmd == 'endef':
                # Buscar la función actual
                for func_name, info in function_map.items():
                    if info['end'] is None and func_name in function_boundaries:
                        if function_boundaries[func_name]['end'] == i:
                            end_addr = len(serialized_bytes)
                            info['end'] = end_addr
                            func_id = info['id']
                            
                            # Escribir bytecode: endef + func_id + end_addr
                            serialized_bytes.extend(b'logic endef ')
                            write_uint32(serialized_bytes, func_id)
                            write_uint32(serialized_bytes, end_addr)
                            break

            # --- logic use ---
            elif subcmd == 'use':
                func_name = tokens[2]
                func_id = get_func_id(func_name)
                
                # Pasar argumentos (si los hay)
                if func_name in function_map:
                    args = function_map[func_name]['args']
                    for arg_name, arg_id in args.items():
                        # Buscar el valor del argumento en el contexto actual
                        # Por ahora, asumimos que la variable existe
                        pass
                
                # Escribir bytecode: use + func_id
                serialized_bytes.extend(b'logic use ')
                write_uint32(serialized_bytes, func_id)

    # Fin del stream
    serialized_bytes.append(0x00)
    return serialized_bytes

def ejecutar_directo_so(stream_bytes, libreria_so="./libNSMotor.so"):
    if not os.path.exists(libreria_so):
        print(f"[-] No se encontró la librería {libreria_so}. Compilala con NASM + GCC.")
        return

    motor = ctypes.CDLL(libreria_so)
    motor.NSMotor.argtypes = [ctypes.c_char_p]
    motor.NSMotor.restype = None

    print(f"[>] Pasando stream híbrido ({len(stream_bytes)} bytes) al motor NASM...")
    motor.NSMotor(bytes(stream_bytes))
    print("[+] Ejecución completada en el motor.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocesador e inyector NeuralScript CLI")
    parser.add_argument("fuente", help="Archivo de código .ns")
    parser.add_argument("-o", "--output", help="Guardar stream binario a un archivo .bin")
    parser.add_argument("-e", "--ejecutar", help="Inyectar y ejecutar directo en libNSMotor.so", action="store_true")

    args = parser.parse_args()

    with open(args.fuente, 'r') as f:
        codigo_ns = f.read()

    stream_resultado = compilar_hibrido_ns(codigo_ns)

    if args.output:
        with open(args.output, 'wb') as f_out:
            f_out.write(stream_resultado)
        print(f"[+] Archivo híbrido guardado en {args.output}")

    if args.ejecutar:
        ejecutar_directo_so(stream_resultado)
