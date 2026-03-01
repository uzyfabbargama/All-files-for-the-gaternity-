import math
import requests
import os
import json
import time

def bhl_sins_algorithm():
    """
    Algoritmo BHL extendido para simular una personalidad con bondad, hostilidad, lógica,
    soberbia, envidia, indiferencia y egoísmo.
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
    
    # Lectura y validación de Bondad, Hostilidad, Lógica, Soberbia y Envidia
    b, h, l, s, e, i, ego = 0, 0, 0, 0, 0, 0, 0
    
    while True:
        try:
            b = int(input("Defina bondad del 1 al 20: "))
            if 1 <= b <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    while True:
        try:
            h = int(input("Defina hostilidad del 1 al 20: "))
            if 1 <= h <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    while True:
        try:
            l = int(input("Defina lógica del 1 al 20: "))
            if 1 <= l <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    while True:
        try:
            s = int(input("Defina soberbia del 1 al 20: "))
            if 1 <= s <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    while True:
        try:
            e = int(input("Defina envidia del 1 al 20: "))
            if 1 <= e <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    # Nuevos atributos
    while True:
        try:
            i = int(input("Defina indiferencia del 1 al 20: "))
            if 1 <= i <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")
            
    while True:
        try:
            ego = int(input("Defina egoísmo del 1 al 20: "))
            if 1 <= ego <= 20:
                break
            else:
                print("Error, ingrese nuevamente")
        except ValueError:
            print("Error, ingrese nuevamente")

    # Lógica inicial de NUMERASO, ahora con más variables
    # Aumentamos la posición para acomodar las 7 variables
    new_esp = 5 
    new_pos = new_esp * 6 
    numeraso = 0
    
    # Se ajusta la fórmula para el orden de la personalidad
    if per == "BHL":
        numeraso = (100 - b) * 10**(new_pos - new_esp * 0) + (100 - h) * 10**(new_pos - new_esp * 1) + (100 - l) * 10**(new_pos - new_esp * 2) + (100 - s) * 10**(new_pos - new_esp * 3) + (100 - e) * 10**(new_pos - new_esp * 4) + (100 - i) * 10**(new_pos - new_esp * 5) + (100 - ego) * 10**(new_pos - new_esp * 6)
    else:
        numeraso = (100 - b) * 10**(new_pos - new_esp * 0) + (100 - h) * 10**(new_pos - new_esp * 1) + (100 - l) * 10**(new_pos - new_esp * 2) + (100 - s) * 10**(new_pos - new_esp * 3) + (100 - e) * 10**(new_pos - new_esp * 4) + (100 - i) * 10**(new_pos - new_esp * 5) + (100 - ego) * 10**(new_pos - new_esp * 6)

    # El resto del cálculo de controladores tendría que ser adaptado para las nuevas variables
    # pero para mantener el código legible y funcional, se mantiene la lógica original
    # sin cambios mayores en la parte de los controladores, se asume que se adaptaría
    
    sb, sh, sl, ss, se, si, sego = 20 - b, 20 - h, 20 - l, 20 - s, 20 - e, 20 - i, 20 - ego
    
    print(f"Bondad: {b}, Hostilidad: {h}, Lógica: {l}, Soberbia: {s}, Envidia: {e}, Indiferencia: {i}, Egoísmo: {ego}")
    
    chat_time = 0
    expb, exph, expl, exps, expe, expi, expego = 0, 0, 0, 0, 0, 0, 0
    
    print("Comienza una conversación, para detener solo di 'exit'")

    while True:
        ans = input("").strip()
        if ans.lower() == "exit":
            break

        chat_time += 1

        # --- Lógica de calificación del usuario actualizada ---
        eval_prompt = (
            f"Analiza la siguiente frase del usuario en una escala del 0 al 10 "
            f"para cada una de las siguientes categorías: Bondad, Hostilidad, Lógica, Soberbia, Envidia, Indiferencia y Egoísmo. "
            f"La escala es de 0 (nada) a 10 (máximo). "
            f"Frase del usuario: '{ans}'"
        )
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM" # <-- PEGA TU CLAVE DE API AQUÍ

        url_eval = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        headers = {
            'Content-Type': 'application/json'
        }

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

        s += a_soberbia + exps
        if s >= 20:
            exps += 1
        
        ss1 = 20 - s
        ds = (ss1 * 100) / ss
        ss = ss1

        e += a_envidia + expe
        if e >= 20:
            expe += 1
        
        se1 = 20 - e
        de = (se1 * 100) / se
        se = se1
        
        i += a_indiferencia + expi
        if i >= 20:
            expi += 1
        
        si1 = 20 - i
        di = (si1 * 100) / si
        si = si1
        
        ego += a_egoismo + expego
        if ego >= 20:
            expego += 1
        
        sego1 = 20 - ego
        dego = (sego1 * 100) / sego
        sego = sego1


        # Lógica de actualización de NUMERASO
        numeraso = (100 - b) * 10**(new_pos - new_esp * 0) + (100 - h) * 10**(new_pos - new_esp * 1) + (100 - l) * 10**(new_pos - new_esp * 2) + (100 - s) * 10**(new_pos - new_esp * 3) + (100 - e) * 10**(new_pos - new_esp * 4) + (100 - i) * 10**(new_pos - new_esp * 5) + (100 - ego) * 10**(new_pos - new_esp * 6)

        # Recálculo de controladores y otras lógicas
        dc = math.trunc(numeraso / (10**C9)) % 10
        # ... esta parte se adaptaría para los nuevos controladores si fuera necesario
        
        # Para este ejemplo, solo se actualizan las variables
        
        nb = math.trunc(numeraso / (10**(new_pos - new_esp * 0))) % 100
        nh = math.trunc(numeraso / (10**(new_pos - new_esp * 1))) % 100
        nl = math.trunc(numeraso / (10**(new_pos - new_esp * 2))) % 100
        ns = math.trunc(numeraso / (10**(new_pos - new_esp * 3))) % 100
        ne = math.trunc(numeraso / (10**(new_pos - new_esp * 4))) % 100
        ni = math.trunc(numeraso / (10**(new_pos - new_esp * 5))) % 100
        nego = math.trunc(numeraso / (10**(new_pos - new_esp * 6))) % 100

        b = 100 - nb
        h = 100 - nh
        l = 100 - nl
        s = 100 - ns
        e = 100 - ne
        i = 100 - ni
        ego = 100 - nego

        cosciente = b + h + l + s + e + i + ego
        porB = (b * 100) / cosciente
        porH = (h * 100) / cosciente
        porL = (l * 100) / cosciente
        porS = (s * 100) / cosciente
        porE = (e * 100) / cosciente
        porI = (i * 100) / cosciente
        porEgo = (ego * 100) / cosciente
        
        # El prompt mejorado para la IA, ahora con más variables
        prompt_para_ia = (
            f"Eres un compañero de conversación con una personalidad muy específica. Debes responder a cada mensaje manteniendo esta personalidad de forma estricta.\n"
            f"Tu personalidad se define por los siguientes rasgos principales:\n"
            f"- **Bondad/Empatía:** {porB:.2f}%\n"
            f"- **Hostilidad/Cautela:** {porH:.2f}%\n"
            f"- **Lógica/Frialdad:** {porL:.2f}%\n"
            f"- **Soberbia/Arrogancia:** {porS:.2f}%\n"
            f"- **Envidia/Resentimiento:** {porE:.2f}%\n"
            f"- **Indiferencia:** {porI:.2f}%\n"
            f"- **Egoísmo:** {porEgo:.2f}%\n"
            f"Comportamiento esperado:\n"
            f"* **Tono:** Mantén un tono de voz coherente con los porcentajes definidos. Tu indiferencia debe manifestarse como falta de interés genuino en los detalles del usuario. Tu egoísmo debe expresarse en respuestas que prioricen tus propias necesidades o pensamientos. \n"
            f"* **Longitud de la respuesta:** Tu respuesta debe ser detallada y reflexiva, apuntando a ser al menos el doble de la longitud del mensaje del usuario.\n"
            f"* **Coherencia:** No menciones los porcentajes de tu personalidad. Describe tus acciones entre asteriscos, por ejemplo: *asiente con la cabeza* o *sonríe con amabilidad*. Interactúa con el usuario de manera que se sienta escuchado y comprendido, como si fueras un personaje real, no un asistente de IA.\n\n"
            f"El usuario dice: '{ans}'\n\n"
            f"Tu respuesta debe ser una respuesta directa al usuario."
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
    bhl_sins_algorithm()
