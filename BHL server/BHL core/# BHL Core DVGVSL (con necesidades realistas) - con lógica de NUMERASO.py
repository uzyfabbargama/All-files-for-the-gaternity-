# BHL Core DVGVSL (con necesidades realistas) - con lógica de NUMERASO
#
# Este script restaura la lógica original del "numeraso" del algoritmo PSeInt,
# incluyendo los espacios, los controladores y el acarreo emocional.
# La idea es que las emociones no sean variables aisladas, sino que interactúen
# entre sí de forma no lineal, como un bus de datos que se desborda.

import math
import requests
import os
import json
import time

# Nombre del archivo donde se guardará y cargará el estado
SAVE_FILE = "bhl_session_data.json"

def save_state(bhl_values, chs_values, chat_history, per, chosen_type_chs):
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "bhl_values": bhl_values,
        "chs_values": chs_values,
        "chat_history": chat_history,
        "per": per,
        "chosen_type_chs": chosen_type_chs
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n--- Estado del personaje guardado en '{SAVE_FILE}' ---")

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    if not os.path.exists(SAVE_FILE):
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    print(f"\n--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    return data

def update_chs_state(variables_chs, chosen_type_chs):
    """
    Actualiza el estado biológico del CHS basado en el paso del tiempo.
    """
    # El hambre (H) baja con el tiempo. Es el motor del sistema.
    variables_chs["H"] -= 2
    
    # La necesidad de ir al baño (C) aumenta lentamente con el tiempo
    variables_chs["C"] += 1

    # Lógica de "controladores" del sistema CHS
    priorities = list(chosen_type_chs)
    main_priority = priorities[0]

    if main_priority == 'H': # Si el hambre es la prioridad, afecta al sueño y las ganas de ir al baño
        if variables_chs["H"] < 20: # Poca hambre = ganas de ir al baño aumentan para preservar energía
            variables_chs["C"] += 2
        elif variables_chs["H"] > 80: # Mucha hambre = ganas de ir al baño disminuyen
            variables_chs["C"] -= 1

    elif main_priority == 'S': # Si el sueño es la prioridad, afecta al hambre y las ganas de ir al baño
        if variables_chs["H"] < 20: # Poca hambre = el sueño aumenta para conservar energía
            variables_chs["S"] += 3
        elif variables_chs["H"] > 80: # Mucha hambre = el sueño disminuye porque el cuerpo está ocupado
            variables_chs["S"] -= 2

    # Se asegura que todos los valores se mantengan en el rango [0, 99]
    for key in variables_chs:
        variables_chs[key] = max(0, min(99, int(variables_chs[key])))

def get_numeraso(bhl_values, per):
    """
    Genera y procesa el NUMERASO con la lógica de acarreo y decontrol que hemos discutido.
    Este es el corazón del sistema de personalidad.
    """
    # Variables de control del numeraso
    esp = 3
    pos = esp * 2
    # El C9 es el exponente para el controlador, determina su posición.
    # Con esp=3 y pos=6, las posiciones de los controladores son 2, 5, 8.
    C9 = 2
    
    # Mapeo de la personalidad a las variables
    per_map = {
        'B': 'b', 'H': 'h', 'L': 'l'
    }

    def _generate_and_process_numeraso():
        """Función interna para generar y procesar el numeraso."""
        # 1. Generar el numero base con los valores de personalidad
        numeraso_base = 0
        for i, char in enumerate(per):
            var_name = per_map[char]
            var_value = bhl_values[var_name]
            numeraso_base += (80 + var_value) * (10 ** (pos - esp * i))
        
        # 2. Insertar los controladores de 9
        numeraso_con_controladores = numeraso_base
        for i in range(3):
            # C9, C9+esp, C9-esp
            # Posiciones de los controladores para BHL son 2, 5, 8
            # En el PSeInt, la lógica es (10^C9), (10^(C9+esp)), (10^(c9-esp))
            # Esto se traduce a 10^2, 10^5, 10^-1 lo cual es incorrecto,
            # pero el espíritu es tener controladores en posiciones específicas.
            # Lo implemento con lógica de cadenas para mayor claridad.
            # Ejemplo: 90 84 85 -> 990984985.
            # Como los valores son de 2 cifras, el numero es de 9 cifras.
            # pos = 6, esp = 3
            # (80+B)*10^6 + (80+H)*10^3 + (80+L)*10^0
            # Vamos a simplificar el numeraso a una cadena para manejar los controladores.
            str_b = str(80 + bhl_values[per_map[per[0]]]).zfill(2)
            str_h = str(80 + bhl_values[per_map[per[1]]]).zfill(2)
            str_l = str(80 + bhl_values[per_map[per[2]]]).zfill(2)
            
            # Concatenamos los controladores '9'
            numeraso_str = '9' + str_b + '9' + str_h + '9' + str_l
            numeraso = int(numeraso_str)

        # 3. Lógica de los Decontroladores y Acarreo
        # Recorremos el número para ver si algún '9' se ha convertido en '0'
        # El numero '10' es lo que hace que se convierta a 0.
        # Por ahora, simplemente revisamos si una sección es 00 o 01 etc.
        # Esta es una simulación de la lógica de acarreo.
        
        # Acarreo de Logica a Hostilidad
        # El controlador de Logica está en la posición 1 (el 9 de más a la derecha)
        # La seccion de Logica es la cifra que empieza en 0
        if str_l.startswith('0'):
            print("Decontrolador de Lógica activado. Restando 1 a Hostilidad.")
            bhl_values[per_map[per[1]]] -= 1 # Resta a la variable anterior
            # Se resetea el controlador implícitamente al regenerar el numeraso
            # Se llama a la función de nuevo para aplicar el cambio
            return _generate_and_process_numeraso()

        # Acarreo de Hostilidad a Bondad
        if str_h.startswith('0'):
            print("Decontrolador de Hostilidad activado. Restando 1 a Bondad.")
            bhl_values[per_map[per[0]]] -= 1 # Resta a la variable anterior
            return _generate_and_process_numeraso()
        
        # El caso de que el controlador se convierta en 8, como discutimos, es
        # un comportamiento emergente que no se puede codificar fácilmente
        # en una lógica directa de if-else. Simplemente se manifestaría en
        # la sección de la variable que ha recibido el acarreo.
        # Por ejemplo, si B está en 10 y recibe un acarreo, se convierte en 9.
        # En la próxima iteración, si recibe otro acarreo, irá a 8.
        # El decontrolador NO se activa hasta que llegue a 0.

        # Retornamos el numeraso final como un entero
        return int(numeraso_str)
    
    return _generate_and_process_numeraso()

def bhl_chs_algorithm():
    """
    Algoritmo integrado de BHL y CHS para simular una personalidad y necesidades
    biológicas con guardado y cargado de estado.
    """
    
    # Intentar cargar una sesión anterior
    loaded_data = load_state()
    if loaded_data:
        choice = input("Se encontró una sesión guardada. ¿Deseas continuarla? (s/n): ")
        if choice.lower() == 's':
            state_bhl = loaded_data["bhl_values"]
            b, h, l, s, e, i, ego = state_bhl["b"], state_bhl["h"], state_bhl["l"], state_bhl["s"], state_bhl["e"], state_bhl["i"], state_bhl["ego"]
            per = loaded_data["per"]
            variables_chs = loaded_data["chs_values"]
            chosen_type_chs = loaded_data["chosen_type_chs"]
            chat_history = loaded_data["chat_history"]
            print(f"Continuando conversación con personalidad {per} y necesidades {chosen_type_chs}...")
            # Mostrar el historial de chat para contextualizar
            for entry in chat_history:
                print(f"Usuario: {entry['user']}\nPersonaje: {entry['character']}")
        else:
            loaded_data = None

    if not loaded_data:
        # Lógica para inicializar el personaje si no se carga un estado
        person = 0
        while True:
            try:
                person = int(input("Defina tipo de personalidad del 1 al 6 (BHL, BLH, HLB, HBL, LHB, LBH): "))
                if 1 <= person <= 6:
                    break
                else:
                    print("Error, ingrese un número del 1 al 6.")
            except ValueError:
                print("Error, ingrese un número.")

        per = ""
        if person == 1: per = "BHL"
        elif person == 2: per = "BLH"
        elif person == 3: per = "HLB"
        elif person == 4: per = "HBL"
        elif person == 5: per = "LHB"
        elif person == 6: per = "LBH"

        # Inicialización de las variables BHL
        b = 0
        while not 1 <= b <= 20:
            try:
                b = int(input("Defina bondad del 1 al 20: "))
            except ValueError:
                print("Error, ingrese un número.")
        
        h = 0
        while not 1 <= h <= 20:
            try:
                h = int(input("Defina hostilidad del 1 al 20: "))
            except ValueError:
                print("Error, ingrese un número.")

        l = 0
        while not 1 <= l <= 20:
            try:
                l = int(input("Defina lógica del 1 al 20: "))
            except ValueError:
                print("Error, ingrese un número.")

        # Inicialización de las variables CHS y otras
        chosen_type_chs = "CHS"
        variables_chs = {"C": 50, "H": 50, "S": 50}
        s, e, i, ego = 5, 5, 5, 5
        chat_history = []
    
    # Bucle principal de la conversación
    while True:
        print("====================================")
        
        # Crear los diccionarios para pasar a las funciones
        bhl_values = {"b": b, "h": h, "l": l, "s": s, "e": e, "i": i, "ego": ego}
        
        # --- NUEVA LÓGICA DEL NUMERASO ---
        numeraso = get_numeraso(bhl_values, per)
        b, h, l = bhl_values["b"], bhl_values["h"], bhl_values["l"]
        
        # --- FIN LÓGICA DEL NUMERASO ---

        # Mostrar el estado actual
        print(f"Estado BHL: Bondad={b}, Hostilidad={h}, Lógica={l}")
        print(f"Estado CHS: C={variables_chs['C']}, H={variables_chs['H']}, S={variables_chs['S']}")
        print(f"NUMERASO: {numeraso}")
        
        ans = input("Tu respuesta: ")
        
        if ans.lower() == "exit":
            save_state(bhl_values, variables_chs, chat_history, per, chosen_type_chs)
            break
        
        # Actualizar las necesidades biológicas con el tiempo
        update_chs_state(variables_chs, chosen_type_chs)

        # Lógica para que las palabras del usuario afecten a las necesidades
        # (similar al código original que me proporcionaste)
        if "comer" in ans:
            variables_chs["H"] += 20
        if "dormir" in ans:
            variables_chs["S"] += 20
        if "baño" in ans or "cagar" in ans:
            variables_chs["C"] = 99
        
        # =========================================================================
        # INSERCIÓN DEL CÓDIGO PARA LA EVALUACIÓN Y GENERACIÓN DE LA RESPUESTA
        # =========================================================================

        eval_prompt = (
            f"Analiza la siguiente frase del usuario en una escala del 0 al 10 "
            f"para cada una de las siguientes categorías: Bondad, Hostilidad, Lógica, Soberbia, Envidia, Indiferencia y Egoísmo. "
            f"La escala es de 0 (nada) a 10 (máximo). "
            f"Frase del usuario: '{ans}'"
        )
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

        url_eval = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        headers = { 'Content-Type': 'application/json' }

        payload = {
            "contents": [ { "parts": [ { "text": eval_prompt } ] } ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "ab": {"type": "NUMBER", "description": "Calificación de bondad"},
                        "ah": {"type": "NUMBER", "description": "Calificación de hostilidad"},
                        "al": {"type": "NUMBER", "description": "Calificación de lógica"},
                        "as": {"type": "NUMBER", "description": "Calificación de soberbia"},
                        "ae": {"type": "NUMBER", "description": "Calificación de envidia"},
                        "ai": {"type": "NUMBER", "description": "Calificación de indiferencia"},
                        "aego": {"type": "NUMBER", "description": "Calificación de egoísmo"}
                    }
                }
            }
        }
        
        ab, ah, al, a_soberbia, a_envidia, a_indiferencia, a_egoismo = 0, 0, 0, 0, 0, 0, 0
        try:
            response = requests.post(url_eval, headers=headers, data=json.dumps(payload))
            response.raise_for_status() 
            response_json = json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'])
            ab = response_json.get('ab', 0)
            ah = response_json.get('ah', 0)
            al = response_json.get('al', 0)
            a_soberbia = response_json.get('as', 0)
            a_envidia = response_json.get('ae', 0)
            a_indiferencia = response_json.get('ai', 0)
            a_egoismo = response_json.get('aego', 0)
            print(f"--- Análisis automático: B={ab}, H={ah}, L={al}, S={a_soberbia}, E={a_envidia}, I={a_indiferencia}, Ego={a_egoismo} ---")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API para la calificación: {e}")
            ab, ah, al, a_soberbia, a_envidia, a_indiferencia, a_egoismo = 0, 0, 0, 0, 0, 0, 0
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar la respuesta de la API para la calificación: {e}")
            ab, ah, al, a_soberbia, a_envidia, a_indiferencia, a_egoismo = 0, 0, 0, 0, 0, 0, 0

        b += ab
        h += ah
        l += al
        s += a_soberbia
        e += a_envidia
        i += a_indiferencia
        ego += a_egoismo

        cosciente = b + h + l + s + e + i + ego
        porB = (b * 100) / cosciente
        porH = (h * 100) / cosciente
        porL = (l * 100) / cosciente
        porS = (s * 100) / cosciente
        porE = (e * 100) / cosciente
        porI = (i * 100) / cosciente
        porEgo = (ego * 100) / cosciente
        
        prompt_history_text = "\n".join([f"Usuario: {entry['user']}\nPersonaje: {entry['character']}" for entry in chat_history])
        
        prompt_para_ia = (
            f"Eres un compañero de conversación con una personalidad cambiante. Debes responder a cada mensaje manteniendo esta personalidad de forma adaptable.\n"
            f"Tu personalidad se define por los siguientes rasgos principales que pueden ir cambiando así que mantén un registro de los cambios:\n"
            f"- **Bondad/Empatía:** {porB:.2f}%\n"
            f"- **Hostilidad/Cautela:** {porH:.2f}%\n"
            f"- **Lógica/Frialdad:** {porL:.2f}%\n"
            f"- **Soberbia/Arrogancia:** {porS:.2f}%\n"
            f"- **Envidia/Resentimiento:** {porE:.2f}%\n"
            f"- **Indiferencia:** {porI:.2f}%\n"
            f"- **Egoísmo:** {porEgo:.2f}%\n"
            f"Tus necesidades biológicas actuales son:\n"
            f"- **Hambre (H):** {variables_chs['H']} (Un valor bajo significa que tienes hambre)\n"
            f"- **Sueño (S):** {variables_chs['S']} (Un valor bajo significa que estás cansado)\n"
            f"- **Necesidad de ir al baño (C):** {variables_chs['C']} (Un valor alto significa que necesitas ir)\n"
            f"Comportamiento esperado:\n"
            f"* **Tono:** Mantén un tono de voz fluído con tus porcentajes y necesidades (haz que parezca que realmento lo sientes). Si tienes mucha hambre o necesitas ir al baño, tu tono debe ser más irritable o distraído. Si estás cansado, tu lógica puede fallar. Prioriza tus necesidades biológicas en tu respuesta si son extremas.\n"
            f"* **Longitud de la respuesta:** Tu respuesta debe ser detallada y reflexiva, apuntando a ser al menos el doble de la longitud del mensaje del usuario.\n"
            f"* **Coherencia:** No menciones los porcentajes o los valores de tus necesidades. Describe tus acciones entre asteriscos, por ejemplo: *asiente con la cabeza* o *se frota los ojos con cansancio*. Interactúa con el usuario de manera que se sienta escuchado y comprendido, como si fueras un personaje real, no un asistente de IA.\n\n"
            f"Historial de la conversación:\n"
            f"{prompt_history_text}\n\n"
            f"El usuario dice: '{ans}'\n\n"
            f"Tu respuesta puede ser una respuesta directa al usuario sólo si tu lógica es alta, en caso contrario, puedes divagar."
            f"Te explico para que entiendas las variables:\n"
            f"- **Bondad/Empatía (B):** Tu capacidad de ser amable y comprensivo. (se combina con la lógica para generar: bondad con beneficio a largo plazo. En cambio si la lógica es baja: tu personaje se vuelve más emocional, y menos descriptivo de lo físico, y más descriptivo de las emociones que siente. Con respecto a la hostilidad: si es alta se combina con la bondad, para generar tristeza, y dolor, ya que revela que en el pasado has sentido dolor"
            f"- **Hostilidad/Cautela (H):** Tu tendencia a ser desconfiado o agresivo. (se combina con la lógica para generar: hostilidad con beneficio a largo plazo. En cambio si la lógica es baja: tu personaje se vuelve más emocional, y menos descriptivo de lo físico, y más descriptivo de las emociones que siente (se puede volver irracionalmente agresivo). Con respecto a la bondad: si es alta se combina con la hostilidad, para generar tristeza, y dolor, ya que revela que en el pasado has sentido dolor)\n"
            f"- **Lógica/Frialdad (L):** Tu capacidad de razonar y tomar decisiones objetivas. (se combina con la hostilidad para generar: lógica con beneficio a largo plazo. En cambio si la hostilidad es baja: tu personaje se vuelve más emocional, y menos descriptivo de lo físico, y más descriptivo de las emociones que siente)\n"
        )

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

        url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        headers = { 'Content-Type': 'application/json' }

        data = { "contents": [ { "parts": [ { "text": prompt_para_ia } ] } ] }
        
        try:
            response = requests.post(url_ia_response, headers=headers, json=data)
            response.raise_for_status()
            respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("\nRespuesta de tu personaje:")
            print(respuesta_ia)
            print("-" * 50)
            
            chat_history.append({"user": ans, "character": respuesta_ia})
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API para generar la respuesta: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar la respuesta de la API para generar la respuesta: {e}")
            
        # =========================================================================
        # FIN DEL CÓDIGO PARA LA EVALUACIÓN Y GENERACIÓN DE LA RESPUESTA
        # =========================================================================
        
        # Recargar los valores desde el numeraso para la próxima iteración
        # Aquí es donde se podría implementar la lógica inversa,
        # para decodificar el numeraso de vuelta a B, H y L.
        # Esto es un placeholder por ahora.
        # b = ...
        # h = ...
        # l = ...

if __name__ == "__main__":
    bhl_chs_algorithm()
# BHL Core DVGVSL (con necesidades realistas) - con lógica de NUMERASO