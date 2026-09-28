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
    function_map = {}

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

    serialized_bytes = bytearray()
    lines = source_code.splitlines()

    for line in lines:
        line = line.split('$')[0].strip()
        if not line:
            continue

        line_clean = line.replace(',', ' ')
        tokens = line_clean.split()
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
                    val = float_to_custom56(float(val_str))
                else:
                    val = int(val_str, 0)
            except ValueError:
                val = float_to_custom56(float(val_str))

            var_id = get_neuron_id(var_name)
            
            # Formato híbrido: texto "var " + ID 32 bits + Valor 56 bits (7 bytes)
            serialized_bytes.extend(b'var ')
            write_uint32(serialized_bytes, var_id)
            serialized_bytes.extend(val.to_bytes(7, byteorder='little'))

        elif cmd == 'proc':
            n1_id = get_neuron_id(tokens[1])
            n2_id = get_neuron_id(tokens[2])
            
            # Formato híbrido: texto "proc" + ID1 32 bits + ID2 32 bits
            serialized_bytes.extend(b'proc')
            write_uint32(serialized_bytes, n1_id)
            write_uint32(serialized_bytes, n2_id)

        elif cmd == 'decay':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            val = int(float(val_str)) if '.' in val_str else int(val_str, 0)

            serialized_bytes.extend(b'decay ')
            write_uint32(serialized_bytes, n_id)
            write_uint8(serialized_bytes, val & 0xFF)

        elif cmd == 'growth':
            n_id = get_neuron_id(tokens[1])
            val_str = tokens[2]
            val = int(float(val_str)) if '.' in val_str else int(val_str, 0)

            serialized_bytes.extend(b'growth ')
            write_uint32(serialized_bytes, n_id)
            write_uint8(serialized_bytes, val & 0xFF)

        elif cmd == 'prom':
            # Opcode personalizada: prom dest n1 n2
            dest_id = get_neuron_id(tokens[1])
            n1_id = get_neuron_id(tokens[2])
            n2_id = get_neuron_id(tokens[3])

            serialized_bytes.extend(b'prom')
            write_uint32(serialized_bytes, dest_id)
            write_uint32(serialized_bytes, n1_id)
            write_uint32(serialized_bytes, n2_id)

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

            elif subcmd == 'loop':
                cond_id = get_logic_id(tokens[2])
                serialized_bytes.extend(b'logic loop ')
                write_uint32(serialized_bytes, cond_id)

            elif subcmd == 'endloop':
                serialized_bytes.extend(b'logic endloop ')

    # Fin del stream de código
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
