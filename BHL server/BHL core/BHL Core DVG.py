import math
import requests
import os
import json
import time

def bhl_algorithm():
    """
    Algoritmo BHL para simular una personalidad basada en bondad, hostilidad y lógica,
    con calificación automática de la respuesta del usuario.
    """
    person = 0
    error = False

    while not error:
        try:
            person = int(input("Defina tipo de personalidad del 1 al 6: "))
            if 1 <= person <= 6:
                error = True
            else:
                print("error")
                error = False
        except ValueError:
            print("error")
            error = False

    per = ""
    if person == 1:
        per = "BHL"
    elif person == 2:
        per = "BLH"
    elif person == 3:
        per = "HLB"
    elif person == 4:
        per = "HBL"
    elif person == 5:
        per = "LHB"
    elif person == 6:
        per = "LBH"

    # Definir variables iniciales
    esp = 3  # Espacios entre cada variable
    pos = esp * 2  # Posición para colocar las variables
    C9 = 2  # Controlador de tipo 9
    
    # Lectura y validación de Bondad, Hostilidad y Lógica
    b = 0
    while True:
        try:
            b = int(input("Defina bondad del 1 al 20: "))
            if 1 <= b <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    h = 0
    while True:
        try:
            h = int(input("Defina hostilidad del 1 al 20: "))
            if 1 <= h <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    l = 0
    while True:
        try:
            l = int(input("Defina lógica del 1 al 20: "))
            if 1 <= l <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    # Inicialización de controladores
    C, C1, C2 = 0, 0, 0

    # Lógica inicial de NUMERASO
    numeraso = 0
    if per == "BHL":
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
    elif per == "BLH":
        numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)
    elif per == "HLB":
        numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2)
    elif per == "HBL":
        numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
    elif per == "LHB":
        numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2)
    elif per == "LBH":
        numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)

    dc = math.trunc(numeraso / (10**C9)) % 10
    dc1 = math.trunc(numeraso / (10**(C9 + esp))) % 10
    dc2 = math.trunc(numeraso / (10**(C9 - esp))) % 10
    
    if dc == 0:
        C = 9 * (10**C9)
        numeraso -= 10**(pos - esp * 2)
    if dc1 == 0:
        C1 = 9 * (10**(C9 + esp))
        numeraso -= 10**(pos - esp * 1)
    if dc2 == 0:
        C2 = 9 * (10**(C9 - esp))
        numeraso -= 10**(pos - esp * 0)

    numeraso += C + C1 + C2

    sb = 20 - b
    sh = 20 - h
    sl = 20 - l

    print(f"Bondad: {b}, Hostilidad: {h}, Lógica: {l}")
    
    chat_time = 0
    expb, exph, expl = 0, 0, 0
    
    print("Comienza una conversación, para detener solo di 'exit'")

    while True:
        ans = input("").strip()
        if ans.lower() == "exit":
            break

        chat_time += 1

        # --- NUEVA LÓGICA: Pedir a Gemini que califique la respuesta del usuario ---
        # Definimos el prompt para que el LLM actúe como un evaluador
        eval_prompt = (
            f"Analiza la siguiente frase del usuario en una escala del 0 al 10 "
            f"para cada una de las siguientes categorías: Bondad, Hostilidad y Lógica. "
            f"La escala es de 0 (nada) a 10 (máximo). "
            f"Frase del usuario: '{ans}'"
        )
        
        # URL y API Key
        #
        # --- MUY IMPORTANTE: INSERTA TU CLAVE DE API AQUÍ ---
        # Si tienes tu clave en una variable de entorno, puedes usar os.getenv("TU_VARIABLE")
        # De lo contrario, reemplaza "TU_CLAVE_API_AQUÍ" con tu clave real.
        #
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM" # <-- PEGA TU CLAVE DE API AQUÍ   

        url_eval = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        headers = {
            'Content-Type': 'application/json'
        }

        # Creamos el cuerpo de la solicitud con el prompt y la configuración de respuesta
        # para obtener un JSON estructurado.
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": eval_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "ab": {"type": "NUMBER", "description": "Calificación de bondad"},
                        "ah": {"type": "NUMBER", "description": "Calificación de hostilidad"},
                        "al": {"type": "NUMBER", "description": "Calificación de lógica"}
                    }
                }
            }
        }
        
        ab, ah, al = 0, 0, 0
        try:
            response = requests.post(url_eval, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Lanza un error para HTTP 4xx/5xx
            
            response_json = json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'])
            ab = response_json.get('ab', 0)
            ah = response_json.get('ah', 0)
            al = response_json.get('al', 0)

            print(f"--- Análisis automático: Bondad={ab}, Hostilidad={ah}, Lógica={al} ---")
            
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API para la calificación: {e}")
            # Si hay un error, usamos valores por defecto para no detener el programa
            ab, ah, al = 0, 0, 0
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar la respuesta de la API para la calificación: {e}")
            # Si hay un error en el JSON, usamos valores por defecto
            ab, ah, al = 0, 0, 0

        # --- FIN DE LA NUEVA LÓGICA ---

        # Actualización de valores con la calificación automática
        b += ab + expb
        if b >= 20:
            expb += 1

        sb1 = 20 - b
        db = (sb1 * 100) / sb
        sb = sb1

        h += ah + exph
        if h >= 20:
            exph += 1
        
        sh1 = 20 - h
        dh = (sh1 * 100) / sh
        sh = sh1

        l += al + expl
        if l >= 20:
            expl += 1

        sl1 = 20 - l
        dl = (sl1 * 100) / sl
        sl = sl1

        # Lógica de actualización de NUMERASO
        if per == "BHL":
            numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
        elif per == "BLH":
            numeraso = (100 - b) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)
        elif per == "HLB":
            numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - l) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2)
        elif per == "HBL":
            numeraso = (100 - h) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - l) * 10**(pos - esp * 2)
        elif per == "LHB":
            numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - h) * 10**(pos - esp * 1) + (100 - b) * 10**(pos - esp * 2)
        elif per == "LBH":
            numeraso = (100 - l) * 10**(pos - esp * 0) + (100 - b) * 10**(pos - esp * 1) + (100 - h) * 10**(pos - esp * 2)
        
        # Recálculo de controladores
        dc = math.trunc(numeraso / (10**C9)) % 10
        dc1 = math.trunc(numeraso / (10**(C9 + esp))) % 10
        dc2 = math.trunc(numeraso / (10**(C9 - esp))) % 10
        
        C, C1, C2 = 0, 0, 0

        if dc == 0:
            C = 9 * (10**C9)
            numeraso -= 10**(pos - esp * 2)
        if dc1 == 0:
            C1 = 9 * (10**(C9 + esp))
            numeraso -= 10**(pos - esp * 1)
        if dc2 == 0:
            C2 = 9 * (10**(C9 - esp))
            numeraso -= 10**(pos - esp * 0)

        # Inserción de controladores
        numeraso += C + C1 + C2

        nb = math.trunc(numeraso / (10**(pos - esp * 0))) % 100
        nh = math.trunc(numeraso / (10**(pos - esp * 1))) % 100
        nl = math.trunc(numeraso / (10**(pos - esp * 2))) % 100

        b = 100 - nb
        h = 100 - nh
        l = 100 - nl

        cosciente = b + h + l
        porB = (b * 100) / cosciente
        porH = (h * 100) / cosciente
        porL = (l * 100) / cosciente
        
        # El prompt mejorado para la IA
        # El prompt ha sido modificado para fomentar respuestas más largas.
        prompt_para_ia = (
            f"Eres un compañero de conversación con una personalidad muy específica. Debes responder a cada mensaje manteniendo esta personalidad de forma estricta.\n"
            f"Tu personalidad se define por los siguientes rasgos principales:\n"
            f"- **Bondad/Empatía:** {porB:.2f}%\n"
            f"- **Hostilidad/Cautela:** {porH:.2f}%\n"
            f"- **Lógica/Frialdad:** {porL:.2f}%\n"
            f"Comportamiento esperado:\n"
            f"* **Tono:** Mantén un tono de voz coherente con los porcentajes definidos.\n"
            f"* **Longitud de la respuesta:** Tu respuesta debe ser más detallada, apuntando a ser el doble de la longitud del mensaje del usuario.\n"
            f"* **Coherencia:** No menciones los porcentajes de tu personalidad en tus respuestas, solo úsalos como base para tu comportamiento.\n\n"
            f"El usuario dice: '{ans}'\n\n"
            f"Tu respuesta debe ser una respuesta humana al usuario, coloca preámbulos sólo si tu lógica es baja, sé directo y frío si la lógica es alta, y emocional si la misma es baja ."
            f"Recuerda, tu objetivo es interactuar de manera natural y fluida, manteniendo siempre la personalidad que te define.\n"
            f"Responde de manera que el usuario sienta que está hablando con un personaje real, no con una IA. Tu respuesta debe ser detallada y reflexiva, evitando respuestas cortas o evasivas.\n"
            f"¡Comienza la conversación!\n"
            f"Describe tus acciones entre asteriscos, por ejemplo: *asiente con la cabeza* o *sonríe con amabilidad*. Esto ayudará a que la conversación sea más inmersiva.\n"
            f"Recuerda que tu objetivo es mantener una conversación fluida y natural, como si fueras un personaje real. No te limites a responder, interactúa con el usuario de manera que se sienta escuchado y comprendido.\n"
        )

        # --- Conexión a la API de Gemini (para la respuesta del personaje) ---
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

        url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt_para_ia
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(url_ia_response, headers=headers, json=data)
            response.raise_for_status()

            respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            print("Respuesta de tu personaje:")
            print(respuesta_ia)
            print("-" * 50)
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API para generar la respuesta: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar la respuesta de la API para generar la respuesta: {e}")


if __name__ == "__main__":
    bhl_algorithm()
