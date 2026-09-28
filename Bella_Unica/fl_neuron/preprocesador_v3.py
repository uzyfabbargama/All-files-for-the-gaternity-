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
    # FUNCIÓN PARA ESCRIBIR IDs DE 32 BITS EN BYTECODE
    # ============================================================
    def write_uint32(buf, value):
        """Escribe un entero de 32 bits en little-endian"""
        buf.extend(struct.pack('<I', value))

    def write_uint64(buf, value):
        """Escribe un entero de 64 bits en little-endian"""
        buf.extend(struct.pack('<Q', value))

    def write_uint8(buf, value):
        """Escribe un entero de 8 bits"""
        buf.append(value & 0xFF)

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
            
            try:
                if val_str.startswith('0x') or val_str.startswith('0X'):
                    val = int(val_str, 16)
                elif '.' in val_str:
                    val_float = float(val_str)
                    val = float_to_custom56(val_float)
                else:
                    val = int(val_str, 0)
            except ValueError:
                val_float = float(val_str)
                val = float_to_custom56(val_float)
            
            var_id = get_neuron_id(var_name)
            
            # Escribir: "var " + ID(4 bytes) + valor(7 bytes)
            serialized_bytes.extend(b'var ')
            write_uint32(serialized_bytes, var_id)
            # Valor de 56 bits = 7 bytes
            serialized_bytes.extend(val.to_bytes(7, byteorder='little'))

        elif cmd == 'proc':
            n1_id = get_neuron_id(tokens[1])
            n2_id = get_neuron_id(tokens[2])
            
            # Escribir: "proc" + ID1(4 bytes) + ID2(4 bytes)
            serialized_bytes.extend(b'proc')
            write_uint32(serialized_bytes, n1_id)
            write_uint32(serialized_bytes, n2_id)

        elif cmd == 'decay':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            
            if val_str.startswith('0x') or val_str.startswith('0X'):
                val = int(val_str, 16)
            elif '.' in val_str:
                val = int(float(val_str))
            else:
                val = int(val_str, 0)
            
            serialized_bytes.extend(b'decay ')
            write_uint32(serialized_bytes, n_id)
            write_uint8(serialized_bytes, val & 0xFF)

        elif cmd == 'growth':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            
            if val_str.startswith('0x') or val_str.startswith('0X'):
                val = int(val_str, 16)
            elif '.' in val_str:
                val = int(float(val_str))
            else:
                val = int(val_str, 0)
            
            serialized_bytes.extend(b'growth ')
            write_uint32(serialized_bytes, n_id)
            write_uint8(serialized_bytes, val & 0xFF)

        elif cmd == 'logic':
            subcmd = tokens[1].lower()
            
            if subcmd == 'cmp':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                n2_id = get_neuron_id(tokens[4])
                
                serialized_bytes.extend(b'logic cmp ')
                write_uint32(serialized_bytes, cond_id)
                write_uint32(serialized_bytes, n1_id)
                write_uint32(serialized_bytes, n2_id)

            elif subcmd == 'cmpv':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                val_str = tokens[4]
                
                if val_str.startswith('0x') or val_str.startswith('0X'):
                    val = int(val_str, 16)
                elif '.' in val_str:
                    val = float_to_custom56(float(val_str))
                else:
                    val = int(val_str, 0)
                
                serialized_bytes.extend(b'logic cmpv ')
                write_uint32(serialized_bytes, cond_id)
                write_uint32(serialized_bytes, n1_id)
                write_uint64(serialized_bytes, val)

            elif subcmd == 'cmpn':
                cond_id = get_logic_id(tokens[2])
                n1_id = get_neuron_id(tokens[3])
                
                serialized_bytes.extend(b'logic cmpn ')
                write_uint32(serialized_bytes, cond_id)
                write_uint32(serialized_bytes, n1_id)

            elif subcmd == 'loop':
                cond_id = get_logic_id(tokens[2])
                
                serialized_bytes.extend(b'logic loop ')
                write_uint32(serialized_bytes, cond_id)

            elif subcmd == 'endloop':
                serialized_bytes.extend(b'logic endloop ')

            elif subcmd == 'def':
                func_name = tokens[2].split('(')[0]
                func_id = get_func_id(func_name)
                
                serialized_bytes.extend(b'logic def ')
                write_uint32(serialized_bytes, func_id)
                
                raw_args = line.split('(')[1].rstrip(')').strip() if '(' in line else ''
                pairs = [p.strip() for p in raw_args.split(',')] if raw_args else []
                
                write_uint8(serialized_bytes, len(pairs))
                for pair in pairs:
                    pos_str, var_name = pair.split('=')
                    write_uint8(serialized_bytes, int(pos_str.strip()))
                    write_uint32(serialized_bytes, get_logic_id(var_name.strip()))

            elif subcmd == 'yes':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic yes ')
                write_uint32(serialized_bytes, cond_id)
                serialized_bytes.extend(b'\x00' * 8)

            elif subcmd == 'no':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic no  ')
                write_uint32(serialized_bytes, cond_id)
                serialized_bytes.extend(b'\x00' * 8)

            elif subcmd == 'endef':
                serialized_bytes.extend(b'logic endef ')

    serialized_bytes.append(0x00)
    return serialized_bytes, neuron_map, logic_var_map, function_map

def generate_nasm_data_section(binary_data):
    formatted_bytes = ", ".join(f"0x{b:02x}" for b in binary_data)
    return f'section .data\n    font_code db {formatted_bytes}'
    
