import json
print(""""================
                ==    RECOVERY    ==
                ================
NO ESCRIBA LA EXTENSIÓN .JSON
no es necesario
""")
archivo = input("ingrese el nombre del archivo: ") + ".json"
def migrar_a_xip(archivo_json, archivo_salida):
    with open(archivo_json, 'r') as f:
        datos = json.load(f)
    
    traductor = datos.get("traductor", {})
    
    with open(archivo_salida, 'w') as xip:
        for idx, texto in traductor.items():
            # Convertimos el formato JSON {"1054": "texto"} 
            # al formato XIP: 1054 :: texto ,,
            xip.write(f"{idx} :: {texto} ,,\n")

# Uso
nombre_final = input("¿Cómo quieres llamarla?: ")
migrar_a_xip(archivo, nombre_final) 
