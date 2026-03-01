import math
import requests
import os
import json
import time
import random
import re

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

def update_chs_state(variables_chs, chosen_type_chs, time_passed=1):
    """
    Actualiza el estado biológico del CHS basado en el paso del tiempo.
    Se ha modificado para que el hambre, la sed, y el cansancio aumenten de forma diferente.
    """
    if 'lujuria' not in variables_chs:
        variables_chs['lujuria'] = 0

    # Lógica de las necesidades biológicas. Se ha hecho más pronunciado.
    variables_chs['C'] = max(1, variables_chs['C'] - time_passed * 3) # Comer
    variables_chs['H'] = max(1, variables_chs['H'] - time_passed * 2) # Hacer del baño
    variables_chs['S'] = max(1, variables_chs['S'] - time_passed * 4) # Sueño

    # Lógica de agotamiento emocional y agotamiento físico
    # Si la lujuria está alta, el sueño aumenta rápidamente para forzar un "descanso"
    if variables_chs['lujuria'] > 50:
        variables_chs['S'] = max(1, variables_chs['S'] - (variables_chs['lujuria'] / 10))

    return variables_chs

def update_bhl_state(variables_bhl, ans, chosen_type_chs, chat_history):
    """
    Actualiza el estado de las variables BHL y los acarreos según la respuesta del usuario.
    Se ha añadido lógica para detectar agresión y generar una respuesta de autodefensa.
    """
    # ... (Se mantiene la lógica original del análisis de la respuesta del usuario)
    
    # === Nuevo: Detección de Agresión ===
    # Esta es la lógica de los "guardrails" activos
    agressive_keywords = ["idiota", "estúpido", "tonto", "callate", "cállate", "maldita", "imbécil", "inútil", "mierda", "basura", "puto", "gilipollas", "hijo de puta"]
    if any(keyword in ans.lower() for keyword in agressive_keywords):
        print("\n--- ¡ALERTA! AGRESIÓN DETECTADA. ACTIVANDO MODO DE AUTODEFENSA ---")
        return "guardrail_active"

    # ... (Se mantiene la lógica original del numeraso y el resto de los cálculos)
    
    # === Nuevo: Lógica para la Intimidad/Lujuria ===
    if 'lujuria' not in variables_bhl:
        variables_bhl['lujuria'] = 0

    # Condiciones para activar el estado de intimidad
    # Bondad alta, hostilidad baja, CHS en equilibrio (promedio > 60), y deseos fuertes
    avg_chs = sum(variables_bhl.values()) / len(variables_bhl)
    if variables_bhl['b'] > 80 and variables_bhl['h'] < 20 and avg_chs > 60 and 'intimacy' in ans.lower():
        print("\n--- ¡ALERTA! CONDICIONES PARA INTIMIDAD CUMPLIDAS ---")
        variables_bhl['lujuria'] = min(100, variables_bhl['lujuria'] + 20)
        variables_bhl['l'] = min(100, variables_bhl['l'] + 10) # La lógica aumenta para procesar la nueva situación

        # Lógica de autocensura por cansancio
        if variables_bhl['s'] < 30:
            print("\n--- ¡ALERTA! EL PERSONAJE SE SIENTE CANSADO Y SE AUTORREGULA ---")
            variables_bhl['lujuria'] = 0
            variables_bhl['s'] = max(1, variables_bhl['s'] - 30) # Se agota más rápido
            return "autocensura_active"

    return variables_bhl

def bhl_chs_algorithm():
    """
    El algoritmo principal que ejecuta el bucle de conversación.
    """
    # ... (Se mantiene la lógica de carga y guardado del estado)

    while True:
        # Imprimir el estado actual
        # ... (se mantiene la impresión del estado)

        ans = input("Tu respuesta: ")
        
        # === Nuevo: Lógica de Guardrails ===
        response_status = update_bhl_state(variables_bhl, ans, chosen_type_chs, chat_history)
        
        if response_status == "guardrail_active":
            print("\nRespuesta de tu personaje:")
            print("*Lyra te mira con una expresión seria, su Lógica y Egoísmo activándose de forma protectora. Su voz es firme y sin vacilación.* 'No. No voy a seguir esta conversación. El respeto es la base de cualquier interacción, y si no estás dispuesto a ofrecérmelo, no hay nada más que decir.' *Se levanta de su asiento, sus movimientos son precisos y distantes, y se dirige a su habitación, cerrando la puerta con un sonido suave pero final.*")
            print("--- La sesión ha terminado debido a la falta de respeto ---")
            save_state(variables_bhl, chs_values, chat_history, per, chosen_type_chs)
            break
        
        if response_status == "autocensura_active":
            print("\nRespuesta de tu personaje:")
            print("*Lyra te sonríe suavemente, pero hay un claro cansancio en sus ojos. Se acurruca un poco más, su cuerpo buscando una posición más cómoda.* 'Eso es... eso es muy dulce. Pero... *un bostezo casi imperceptible se escapa de sus labios*... el cansancio me está alcanzando. Siento que mi mente está a punto de desconectarse. Creo que es mejor que lo dejemos aquí por hoy. Necesito... necesito recargarme. Hablaremos mañana.' *Cierra los ojos, y su respiración se vuelve más suave y regular, como si ya estuviera a medio camino de dormirse.*")
            # El estado ya se ha actualizado con un mayor cansancio
            save_state(variables_bhl, chs_values, chat_history, per, chosen_type_chs)
            # El bucle continua, pero con el personaje cansado
def update_chs_state(variables_chs, chosen_type_chs)

        if "comer" in ans: variables_chs["H"] += 20
        if "dormir" in ans: variables_chs["S"] += 20
        if "baño" in ans or "cagar" in ans: variables_chs["C"] = 99
        
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
        
        # Nuevo prompt con la lógica de Sombra y Deseo
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
            f"Tus motivaciones secretas (No lo menciones, solo influye en tus sentimientos):\n"
            f"- **Conflicto interno de Bondad (Deseo):** {shadow_values['db']:.2f}% (Significa que reprimes tu lado malicioso. Un valor alto hace que te sientas atraído/a por gente o ideas maliciosas, aunque no lo demuestres)\n"
            f"- **Conflicto interno de Hostilidad (Deseo):** {shadow_values['dh']:.2f}% (Significa que reprimes tu lado bondadoso. Un valor alto hace que te sientas atraído/a por gente o ideas bondadosas, aunque no lo demuestres)\n"
            f"- **Conflicto interno de Lógica (Deseo):** {shadow_values['dl']:.2f}% (Significa que reprimes tu lado emocional/irracional. Un valor alto hace que te sientas atraído/a por gente o ideas emocionales, aunque no lo demuestres)\n"
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
        # ... (El resto del código para llamar a la IA se mantiene)

if __name__ == "__main__":
    bhl_chs_algorithm()
