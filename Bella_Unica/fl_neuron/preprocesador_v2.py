import struct

def parse_and_serialize(source_code):
    # Tablas de símbolos (mapean nombres a offsets de memoria)
    neuron_map = {}
    logic_var_map = {}
    function_map = {}  # <- Definida dentro de la función contenedora
    
    next_neuron_offset = 0x01
    next_logic_offset = 0x01
    next_func_offset = 0x01   # <- Binding correcto para nonlocal

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
            function_map[name] = next_func_offset
            next_func_offset += 1
        return function_map[name]

    # ============================================================
    # NUEVA FUNCIÓN: Convertir decimal a formato de 55 bits
    # ============================================================
    def float_to_custom56(val):
        """Convierte un float (0.0 a 1.999...) al formato entero de 56 bits."""
        if isinstance(val, int):
            # Si es entero, convertirlo a formato de 56 bits
            entero = val
            return entero << 8  # Simple desplazamiento para enteros
        elif isinstance(val, float):
            entero = 1 if val >= 1.0 else 0
            frac = val - entero
            frac_bits = int(frac * (2 ** 55))
            return (entero << 55) | (frac_bits & ((1 << 55) - 1))
        elif isinstance(val, str):
            # Si es string, intentar convertir
            if val.startswith('0x') or val.startswith('0X'):
                return int(val, 16)
            else:
                return int(float(val) * (1 << 55))
        return 0

    serialized_bytes = bytearray()
    lines = source_code.splitlines()

    for line in lines:
        line = line.split('$')[0].strip()
        if not line:
            continue

        line = line.replace(',', ' ')
        tokens = line.split()
        if not tokens:
            continue

        cmd = tokens[0].lower()

        if cmd == 'var':
            var_name = tokens[1]
            val_str = tokens[2]
            
            # ============================================================
            # NUEVO: Parsear valor (decimal, hex, float)
            # ============================================================
            try:
                if val_str.startswith('0x') or val_str.startswith('0X'):
                    val = int(val_str, 16)
                elif '.' in val_str:
                    # Es un float decimal
                    val_float = float(val_str)
                    val = float_to_custom56(val_float)
                else:
                    val = int(val_str, 0)
            except ValueError:
                # Si falla, intentar como float
                val_float = float(val_str)
                val = float_to_custom56(val_float)
            
            var_id = get_neuron_id(var_name)
            
            serialized_bytes.extend(b'var ')
            serialized_bytes.append(var_id)
            serialized_bytes.extend(b'\x00\x00\x00')
            serialized_bytes.extend(val.to_bytes(7, byteorder='little'))

        elif cmd == 'proc':
            n1_id = get_neuron_id(tokens[1])
            n2_id = get_neuron_id(tokens[2])
            
            serialized_bytes.extend(b'proc')
            serialized_bytes.append(n1_id)
            serialized_bytes.extend(b'\x00\x00\x00')
            serialized_bytes.append(n2_id)

        elif cmd == 'decay':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            
            # Decay usa valores pequeños (enteros)
            if val_str.startswith('0x') or val_str.startswith('0X'):
                val = int(val_str, 16)
            elif '.' in val_str:
                val = int(float(val_str))
            else:
                val = int(val_str, 0)
            
            serialized_bytes.extend(b'decay ')
            serialized_bytes.append(n_id)
            serialized_bytes.extend(b'\x00\x00\x00')
            serialized_bytes.append(val & 0xFF)

        elif cmd == 'growth':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            
            # Growth usa valores pequeños (enteros)
            if val_str.startswith('0x') or val_str.startswith('0X'):
                val = int(val_str, 16)
            elif '.' in val_str:
                val = int(float(val_str))
            else:
                val = int(val_str, 0)
            
            serialized_bytes.extend(b'growth ')
            serialized_bytes.append(n_id)
            serialized_bytes.extend(b'\x00\x00\x00')
            serialized_bytes.append(val & 0xFF)

        elif cmd == 'logic':
            subcmd = tokens[1].lower()
            
            if subcmd == 'cmp':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                n2_id = get_neuron_id(tokens[4])
                
                serialized_bytes.extend(b'logic cmp ')
                serialized_bytes.append(cond_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                serialized_bytes.append(n1_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                serialized_bytes.append(n2_id)
                serialized_bytes.extend(b'\x00\x00\x00')

            elif subcmd == 'cmpv':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                val_str = tokens[4]
                
                # Comparar con valor constante
                if val_str.startswith('0x') or val_str.startswith('0X'):
                    val = int(val_str, 16)
                elif '.' in val_str:
                    val = float_to_custom56(float(val_str))
                else:
                    val = int(val_str, 0)
                
                serialized_bytes.extend(b'logic cmpv ')
                serialized_bytes.append(cond_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                serialized_bytes.append(n1_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                serialized_bytes.extend(val.to_bytes(8, byteorder='little'))

            elif subcmd == 'cmpn':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                
                serialized_bytes.extend(b'logic cmpn ')
                serialized_bytes.append(cond_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                serialized_bytes.append(n1_id)
                serialized_bytes.extend(b'\x00\x00\x00')

            elif subcmd == 'loop':
                cond_id = get_logic_id(tokens[2])
                
                serialized_bytes.extend(b'logic loop ')
                serialized_bytes.append(cond_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                
            elif subcmd == 'endloop':
                serialized_bytes.extend(b'logic endloop ')

            elif subcmd == 'def':
                func_name = tokens[2].split('(')[0]
                func_id = get_func_id(func_name)
                
                serialized_bytes.extend(b'logic def ')
                serialized_bytes.append(func_id)
                serialized_bytes.extend(b'\x00\x00\x00')
                
                raw_args = line.split('(')[1].rstrip(')').strip() if '(' in line else ''
                pairs = [p.strip() for p in raw_args.split(',')] if raw_args else []
                
                serialized_bytes.append(len(pairs))
                for pair in pairs:
                    pos_str, var_name = pair.split('=')
                    serialized_bytes.append(int(pos_str.strip()))
                    serialized_bytes.append(get_logic_id(var_name.strip()))

            elif subcmd == 'yes':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic yes ')
                serialized_bytes.append(cond_id)
                serialized_bytes.extend(b'\x00' * 8) 

            elif subcmd == 'no':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic no  ')
                serialized_bytes.append(cond_id)
                serialized_bytes.extend(b'\x00' * 8)

            elif subcmd == 'endef':
                serialized_bytes.extend(b'logic endef ')

    serialized_bytes.append(0x00)
    return serialized_bytes, neuron_map, logic_var_map, function_map

def generate_nasm_data_section(binary_data):
    # Convierte el bytearray a un formato db 0xXX, 0xYY para NASM
    formatted_bytes = ", ".join(f"0x{b:02x}" for b in binary_data)
    return f'section .data\n    font_code db {formatted_bytes}'

if __name__ == "__main__":
    source = """
$ Inicializamos neuronas
var n1, 0x123456789ABC
var n2, 0x001122334455

$ Procesamos y ajustamos
proc n1, n2
decay n1, 10
growth n2, 15

$ Comparación lógica
logic cmp cond1, n1, n2
"""

    data, n_map, l_map, f_map = parse_and_serialize(source)

    nasm_code = generate_nasm_data_section(data)

    print(nasm_code)
    print("\nMapeo de neuronas:", n_map)
    print("Mapeo de vars lógicas:", l_map)
    print("Mapeo de funciones:", f_map)
