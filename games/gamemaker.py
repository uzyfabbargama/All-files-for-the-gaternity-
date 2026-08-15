seed = (int(input("Ingresa semilla: ")) + 256) & 0xffffffffff
print(f"semilla: {seed-256}")

bytes_parts = []
bytes_parts.append((seed>>0)&0xff)
bytes_parts.append((seed>>8<<0)&0xff)
bytes_parts.append((seed>>8<<1)&0xff)
bytes_parts.append((seed>>8<<2)&0xff)
bytes_parts.append((seed>>8<<3)&0xff)
bytes_parts.append((seed>>8<<4)&0xff)
bytes_parts.append((seed>>8<<5)&0xff)
bytes_parts.append((seed>>8<<6)&0xff)
#bytes_parts.append((seed>>0x80)&0xff)
for byte_part in bytes_parts:
    print(byte_part)
