# =======================================================
# MOTOR XIP (XorID Pack) - SECCIÓN L / S (Load & Save)
# =======================================================
import os

def xorid(palabra):
    """Genera la frecuencia (ID) única de cada palabra."""
    id_acum = 0
    for char in palabra:
        id_acum = (id_acum ^ ord(char)) << 1
    return id_acum

def setz(diff):
    """Resonancia: 1 si hay sintonía (0 diferencia), 0 si no."""
    return 1 if diff == 0 else 0

def guardar_xip(nombre_archivo, mapa_datos, comentario_cabecera="Archivo de Memoria XIP"):
    """
    S (Save): Guarda los datos en formato legible.
    Recibe: 'datos.xip', {'maria_dinero': 100}, 'Comentario'
    """
    nombre = nombre_archivo if nombre_archivo.endswith(".xip") else nombre_archivo + ".xip"
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(f"// {comentario_cabecera}\n")
        for key, valor in mapa_datos.items():
            f.write(f"{key} :: {valor} ,,\n")
    print(f"[S] Memoria sincronizada en: {nombre}")

# =======================================================
# CLASE MOTOR XIP_Engine
# =======================================================
class XIP_Engine:
    def __init__(self):
        self.memoria = {} # Aquí vive la resonancia aritmética (ID: Valor)
        self.nombres = {} # Opcional: Para saber qué nombre pertenece a qué ID

    def cargar_xip(self, nombre_archivo):
        """
        L (Load): Carga y lexea con xorid ignorando comentarios y espacios.
        """
        nombre = nombre_archivo if nombre_archivo.endswith(".xip") else nombre_archivo + ".xip"
        if not os.path.exists(nombre):
            print(f"[L] Error: {nombre} no existe.")
            return

        with open(nombre, "r", encoding="utf-8") as f:
            for num_linea, linea in enumerate(f, 1):
                # Omitir comentarios (//) y limpiar extremos
                limpia = linea.split("//")[0].strip()
                
                if not limpia or "::" not in limpia:
                    continue

                # Procesar bloques por terminador ',,'
                bloques = limpia.split(",,")
                for bloque in bloques:
                    if "::" not in bloque: continue
                    
                    # Separación de Trama
                    raw_key, raw_val = bloque.split("::")
                    key_str = raw_key.strip()
                    val_str = raw_val.strip()

                    # --- EL CORAZÓN DEL LEXEO ---
                    id_leido = xorid(key_str)
                    
                    # Guardamos por ID (esto es lo que BELLA usaría)
                    self.memoria[id_leido] = val_str
                    self.nombres[id_leido] = key_str # Guardamos el alias original
                    
                    print(f"  [L] Línea {num_linea}: Sintonizado ID {id_leido} ({key_str}) -> {val_str}")

# =======================================================
# PRUEBA DE CAMPO
# =======================================================
if __name__ == "__main__":
    # 1. Imaginamos unos datos en el programa
    datos_uziel = {
        "maria_dinero": 500,
        "bella_conciencia": 1048576,
        "modo_turbo": "activado"
    }

    # 2. Guardamos (S)
    guardar_xip("conciencia_uziel", datos_uziel, "Memoria de Prueba BELLA")

    # 3. Cargamos (L)
    motor = XIP_Engine()
    motor.cargar_xip("conciencia_uziel")

    # 4. Verificación de Resonancia (Comparación tipo Assembler)
    target_id = xorid("maria_dinero")
    if target_id in motor.memoria:
        # Aquí es donde ocurre tu setz(diff)
        print(f"\n[ÉXITO] El valor de 'maria_dinero' es: {motor.memoria[target_id]}")
