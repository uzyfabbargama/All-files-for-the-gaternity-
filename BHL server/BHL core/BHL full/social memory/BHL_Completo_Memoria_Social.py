# BHL Core DVGVSL (con necesidades realistas, Numeraso y Sombra)
#
# Este script integra todos los sistemas que hemos discutido:
# - BHL (Bondad, Hostilidad, Lógica)
# - El NUMERASO, que genera complejidad emergente.
# - CHS (necesidades biológicas: Comer, Ir al baño, Dormir).
# - Un sistema de guardado y cargado de estado.
# - Y ahora, las variables de SOMBRA y DESEO para un conflicto psicológico interno.
# - INTEGRADO: Un sistema de Memoria Social.

import math
import requests
import os
import json
import time
from base_de_datos_social import MemoriaSocial # Importa la clase de memoria social  # Asegúrate de que este archivo esté en el mismo directorio
# Nombre del archivo donde se guardará y cargará el estado
chat_history = []

def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])
SAVE_FILE = "bhl_session_data.json"
def get_variables_chs(variables_chs=None):
    """
    Devuelve el estado actual de las variables biológicas CHS.
    Si no se pasa un diccionario, devuelve valores por defecto.
    """
    if variables_chs is None:
        return {"C": 50, "H": 50, "S": 50}
    return variables_chs
def get_bhl_values():
    """
    Devuelve los valores actuales de BHL.
    Estos valores pueden ser modificados por el usuario o por el sistema.
    """
    return {"b": 10, "h": 5, "l": 8, "ego": 3}
def save_state(bhl_values, chs_values, chat_history, per, chosen_type_chs, shadow_values):
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "bhl_values": bhl_values,
        "chs_values": chs_values,
        "chat_history": chat_history,
        "per": per,
        "chosen_type_chs": chosen_type_chs,
        "shadow_values": shadow_values
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
    Genera y procesa el NUMERASO con la lógica de acarreo y decontrol.
    Este es el corazón del sistema de personalidad.
    """
    esp = 3
    pos = esp * 2
    C9 = 2
    
    per_map = { 'B': 'b', 'H': 'h', 'L': 'l' }

    def _generate_and_process_numeraso():
        """Función interna para generar y procesar el numeraso."""
        str_b = str(80 + bhl_values[per_map[per[0]]]).zfill(2)
        str_h = str(80 + bhl_values[per_map[per[1]]]).zfill(2)
        str_l = str(80 + bhl_values[per_map[per[2]]]).zfill(2)
        
        numeraso_str = '9' + str_b + '9' + str_h + '9' + str_l
        
        if str_l.startswith('0'):
            print("Decontrolador de Lógica activado. Restando 1 a Hostilidad.")
            bhl_values[per_map[per[1]]] -= 1
            return _generate_and_process_numeraso()

        if str_h.startswith('0'):
            print("Decontrolador de Hostilidad activado. Restando 1 a Bondad.")
            bhl_values[per_map[per[0]]] -= 1
            return _generate_and_process_numeraso()

        return int(numeraso_str)
    
    return _generate_and_process_numeraso()

def update_shadow_desire_and_ego(bhl_values, shadow_values):
    """
    Actualiza las variables de sombra, deseo y ego.
    """
    # Guardamos los valores de la sombra anterior
    sb_prev = shadow_values['sb']
    sh_prev = shadow_values['sh']
    sl_prev = shadow_values['sl']

    # Calculamos la sombra actual
    shadow_values['sb'] = max(0, 20 - bhl_values['b'])
    shadow_values['sh'] = max(0, 20 - bhl_values['h'])
    shadow_values['sl'] = max(0, 20 - bhl_values['l'])
    
    # Calculamos el deseo como un porcentaje de cambio en la sombra
    # Un deseo alto significa que el rasgo ha sido reprimido (valor alto) y luego la personalidad principal cambió (valor bajo),
    # creando una tensión.
    if sb_prev > 0:
        shadow_values['db'] = ((shadow_values['sb'] * 100) / sb_prev)
    else:
        shadow_values['db'] = 0
    
    if sh_prev > 0:
        shadow_values['dh'] = ((shadow_values['sh'] * 100) / sh_prev)
    else:
        shadow_values['dh'] = 0

    if sl_prev > 0:
        shadow_values['dl'] = ((shadow_values['sl'] * 100) / sl_prev)
    else:
        shadow_values['dl'] = 0

    # Lógica para actualizar el ego
    # El ego aumenta cuando la personalidad principal es alta
    # y la sombra es baja (poca represión).
    bhl_values['ego'] = ((bhl_values['b'] + bhl_values['h'] + bhl_values['l']) / 3) / 2
    if shadow_values['db'] > 50 or shadow_values['dh'] > 50 or shadow_values['dl'] > 50:
        bhl_values['ego'] -= 2 # El conflicto interno baja el ego

    for key in bhl_values:
        bhl_values[key] = max(0, min(100, int(bhl_values[key])))

def bhl_chs_algorithm():
    """
    Algoritmo integrado de BHL y CHS para simular una personalidad y necesidades
    biológicas con guardado y cargado de estado.
    """
    
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
            shadow_values = loaded_data["shadow_values"]
            
            print(f"Continuando conversación con personalidad {per} y necesidades {chosen_type_chs}...")
            for entry in chat_history:
                print(f"Usuario: {entry['user']}\nPersonaje: {entry['character']}")
        else:
            loaded_data = None

    if not loaded_data:
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

        chosen_type_chs = "CHS"
        variables_chs = {"C": 50, "H": 50, "S": 50}
        s, e, i, ego = 5, 5, 5, 5
        chat_history = []
        
        # Inicialización de las variables de Sombra
        sb = max(0, 20 - b)
        sh = max(0, 20 - h)
        sl = max(0, 20 - l)
        db, dh, dl = 0, 0, 0
        shadow_values = {"sb": sb, "sh": sh, "sl": sl, "db": db, "dh": dh, "dl": dl}
    
    # Inicializa la memoria social
    memoria_social = MemoriaSocial("IA_Emergente")
    
    nombre_usuario = None
    while nombre_usuario is None:
        nombre_usuario = input("Por favor, introduce tu nombre: ")
    
    perfil_usuario = memoria_social.obtener_perfil(nombre_usuario)
    relacion_anterior = perfil_usuario
    
    while True:
        bhl_values = {"b": b, "h": h, "l": l, "s": s, "e": e, "i": i, "ego": ego}
    
        numeraso = get_numeraso(bhl_values, per)
        b, h, l = bhl_values["b"], bhl_values["h"], bhl_values["l"]
    
        update_shadow_desire_and_ego(bhl_values, shadow_values)
        b, h, l, ego = bhl_values["b"], bhl_values["h"], bhl_values["l"], bhl_values["ego"]
    
        print(f"Estado BHL: Bondad={b}, Hostilidad={h}, Lógica={l}, Ego={ego}")
        print(f"Estado CHS: C={variables_chs['C']}, H={variables_chs['H']}, S={variables_chs['S']}")
        print(f"Estado de Sombra: SB={shadow_values['sb']}, SH={shadow_values['sh']}, SL={shadow_values['sl']}")
        print(f"Estado de Deseo: DB={shadow_values['db']:.2f}, DH={shadow_values['dh']:.2f}, DL={shadow_values['dl']:.2f}")
        print(f"NUMERASO: {numeraso}")
        ans = input(f"{nombre_usuario}: ")
    
        if ans.lower() == "exit":
            save_state(bhl_values, variables_chs, chat_history, per, chosen_type_chs, shadow_values)
            break
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
    # Ahora sí puedes construir el prompt usando ans
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
            f"- **Necesidad de ir al baño (C):** {variables_chs['C']} (Un valor alto significa que necesitas ir a evacuar, y liberar deshechos)\n"
            f"Tus motivaciones secretas (No lo menciones, solo influye en tus sentimientos):\n"
            f"- **Conflicto interno de Bondad (Deseo):** {shadow_values['dh']:.2f}% (Significa que reprimes tu lado malicioso y que tienes un conflicto interno, pero por tu bondadoso o lógica no demuestras. Un valor alto hace que te sientas atraído/a por gente o ideas maliciosas, aunque no lo demuestres)\n"
            f"- **Conflicto interno de Hostilidad (Deseo):** {shadow_values['db']:.2f}% (Significa que reprimes tu lado bondadoso. Un valor alto hace que te sientas atraído/a por gente o ideas bondadosas, aunque no lo demuestres)\n"
            f"- **Conflicto interno de Lógica (Deseo):** {shadow_values['dl']:.2f}% (Significa que reprimes tu lógica, y que eres emocional/irracional. Un valor alto hace que te sientas atraído/a por gente o ideas emocionales, aunque no lo demuestres)\n"
            f"Comportamiento esperado:\n"
            f"* **Tono:** Mantén un tono de voz fluído con tus porcentajes y necesidades (haz que parezca que realmente lo sientes). Si tienes mucha hambre o necesitas ir al baño, tu tono debe ser más irritable o distraído. Si estás cansado, tu lógica puede fallar. Prioriza tus necesidades biológicas en tu respuesta si son extremas.\n"
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
            f"Tu recuerdo de '{nombre_usuario}' es: {perfil_usuario}. \n"
        )        
        if ans.lower() == "exit":
            save_state(bhl_values, variables_chs, chat_history, per, chosen_type_chs, shadow_values)
            break
        
        update_chs_state(variables_chs, chosen_type_chs)
        if "comer" in ans:
            variables_chs["H"] += 20
        if "dormir" in ans:
            variables_chs["S"] += 20
        if "baño" in ans or "cagar" in ans:
            variables_chs["C"] = 99

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
                    },
                    "propertyOrdering": ["ab", "ah", "al", "as", "ae", "ai", "aego"]
                }
            }
        }
        ab, ah, al, a_soberbia, a_envidia, a_indiferencia, a_egoismo = 0, 0, 0, 0, 0, 0, 0
        try:
            response = requests.post(url_eval, headers=headers, json=payload)
            response.raise_for_status()
            evaluacion_api = response.json()['candidates'][0]['content']['parts'][0]['text']
            eval_data = json.loads(evaluacion_api)

            # Actualiza las variables BHL del personaje con las respuestas del usuario
            b += eval_data.get('ab', 0)
            h += eval_data.get('ah', 0)
            l += eval_data.get('al', 0)
            s += eval_data.get('as', 0)
            e += eval_data.get('ae', 0)
            i += eval_data.get('ai', 0)
            ego += eval_data.get('aego', 0)

            # Normalización y ajuste de valores
            b = max(1, min(100, b))
            h = max(1, min(100, h))
            l = max(1, min(100, l))
            s = max(1, min(100, s))
            e = max(1, min(100, e))
            i = max(1, min(100, i))
            ego = max(1, min(100, ego))
            
            # Convierte los valores BHL a un diccionario para la memoria social
            variables_bhl_usuario = {
                'Bondad': eval_data.get('ab', 0) * 10,
                'Hostilidad': eval_data.get('ah', 0) * 10,
                'Lógica': eval_data.get('al', 0) * 10,
                'Ego': eval_data.get('aego', 0) * 10
            }
            
            # Actualiza la base de datos social con la nueva información del usuario
            memoria_social.agregar_o_actualizar_usuario(nombre_usuario, variables_bhl_usuario, relacion_anterior)
            relacion_anterior = memoria_social.obtener_perfil(nombre_usuario)

        except (requests.exceptions.RequestException, json.JSONDecodeError) as err:
            print(f"Error al conectar o decodificar la API: {err}")
            continue

        #*prompt_para_ia = (
            f"Tu personalidad es {per}, con un estado actual de Bondad={b}, Hostilidad={h}, Lógica={l}, Ego={ego}. "
            f"El estado biológico es: Comer={variables_chs['C']}, Ir al baño={variables_chs['H']}, Dormir={variables_chs['S']}. "
            f"Tienes un trauma o deseo reprimido de: Sombra Bondad={shadow_values['sb']:.2f}, Sombra Hostilidad={shadow_values['sh']:.2f}, Sombra Lógica={shadow_values['sl']:.2f}. "
            f"Tu deseo de actuar sobre estas sombras es: Deseo Bondad={shadow_values['db']:.2f}, Deseo Hostilidad={shadow_values['dh']:.2f}, Deseo Lógica={shadow_values['dl']:.2f}. "
            f"El Numeraso, que influye en tu inconsciente, es {numeraso}. "
            f"Considera el perfil de tu interlocutor '{nombre_usuario}': {relacion_anterior}. "
            f"Responde a '{ans}' teniendo en cuenta tu perfil psicológico y tu relación con el usuario."
        #)

        #api_key = os.getenv("GEMINI_API_KEY")
        #if not api_key:
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
            break

if __name__ == "__main__":
    bhl_chs_algorithm()
