def xorid(fragmento):
    id_acumulado = 0
    for caracter in fragmento:
        byte_val = ord(caracter)
        id_acumulado = (id_acumulado ^ byte_val) << 1
    return id_acumulado
