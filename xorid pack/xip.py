# xip.py - La biblioteca oficial de XorID Pack
import os

def _xorid(palabra):
    id_acum = 0
    for char in palabra:
        id_acum = (id_acum ^ ord(char)) << 1
    return id_acum

def load(ruta):
    """Carga un archivo .xip y devuelve un diccionario de IDs."""
    memoria = {}
    if not os.path.exists(ruta): return memoria
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            limpia = linea.split("//")[0].strip()
            if not limpia or "::" not in limpia: continue
            bloques = limpia.split(",,")
            for b in bloques:
                if "::" not in b: continue
                k, v = b.split("::")
                # El corazón del estándar: El ID es la llave
                memoria[_xorid(k.strip())] = v.strip()
    return memoria

def dump(datos, ruta, comentario="XIP Standard"):
    """Guarda un diccionario en formato .xip."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"// {comentario}\n")
        for k, v in datos.items():
            f.write(f"{k} :: {v} ,,\n")
