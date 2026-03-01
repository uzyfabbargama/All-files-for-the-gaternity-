# BHL_Flet.py

import math
import random
import requests
import os
import json
import time

# Variables globales para el estado del personaje
Escenario = ""
chat_history = []
Nivel_incomodidad = 0
SAVE_FILE = "bhl_session_data.json"
a, b, c = 50, 50, 50  # Valores iniciales por defecto
baño, hambre, sueño = 50, 50, 50

# Variables de experiencia (serán actualizadas)
expB, expH, expL = 0, 0, 0
expS, expHu, expC = 0, 0, 0

# --- Lógica de Inicialización ---
def initialize_game(escenario_inicial, bondad, hostilidad, logica):
    """Inicializa el estado del personaje con los valores de la UI."""
    global Escenario, a, b, c
    Escenario = escenario_inicial
    a = max(1, bondad)
    b = max(1, hostilidad)
    c = max(1, logica)
    print(f"Juego inicializado. Escenario: {Escenario}, B: {a}, H: {b}, L: {c}")

# --- Funciones de Lógica del Personaje (las mismas que tenías) ---
def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])

def save_state():
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "bhl_values": Numeraso(a, b, c),
        "Exp_B": expB,
        "Exp_H": expH,
        "Exp_L": expL,
        "chs_values": Numeraso2(baño, hambre, sueño),
        "Exp_S": expS,
        "Exp_Hu": expHu,
        "Exp_C": expC,
        "chat_history": chat_history,
        "escenario": Escenario,
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n--- Estado del personaje guardado en '{SAVE_FILE}' ---")

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    global a, b, c, baño, hambre, sueño, expB, expH, expL, expS, expHu, expC, chat_history, Escenario
    if not os.path.exists(SAVE_FILE):
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    print(f"\n--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    
    # Restaura los valores de la personalidad
    Numero_cargado = data["bhl_values"]
    a = (Numero_cargado // 10**(3*2)) % 100
    b = (Numero_cargado // 10**3) % 100
    c = Numero_cargado % 100

    # Restaura las necesidades
    Numero1_cargado = data["chs_values"]
    baño = (Numero1_cargado // 10**(3*2)) % 100
    hambre = (Numero1_cargado // 10**3) % 100
    sueño = Numero1_cargado % 100
    
    expB = data["Exp_B"]
    expH = data["Exp_H"]
    expL = data["Exp_L"]
    expS = data["Exp_S"]
    expHu = data["Exp_Hu"]
    expC = data["Exp_C"]
    chat_history = data["chat_history"]
    Escenario = data["escenario"]
    return data

def Numeraso(a, b, c): #lógica del Numeraso, acarreo, y controladores, sin if 
    Bondad = a
    Hostilidad = b
    Lógica = c
    Numero_generado = Bondad*(10**(3*2)) + Hostilidad*(10**3) + Lógica + 9*10**8 + 9*10**5 + 9*10**2
    return Numero_generado

def Numeraso_update():
    global expB, expH, expL
    Numero_generado = Numeraso(a, b, c)
    C1 = (Numero_generado // 10**8) % 10
    C2 = (Numero_generado // 10**5) % 10
    C3 = (Numero_generado // 10**2) % 10
    caso = C1 + C2 + C3
    expL = 0
    expB = 0
    expH = 0
    while caso != 27:
        D1 = 9 - C1
        D2 = 9 - C2
        D3 = 9 - C3
        expB += D1 % 2
        expH += D2 % 2
        expL += D3 % 2
        Numero_generado += D1 * 10**8 + D2 * 10**5 + D3 * 10**2
        Numero_generado += D1 % 2
        Numero_generado -= (D1 % 2) * (10**3)
        Numero_generado -= D2 % 2
        Numero_generado -= (D3 % 2) * (10**(3*2))
        C1 = (Numero_generado // 10**8) % 10
        C2 = (Numero_generado // 10**5) % 10
        C3 = (Numero_generado // 10**2) % 10
        caso = C1 + C2 + C3
    return Numero_generado % 10**9, expB, expH, expL

def Numeraso2(baño, hambre, sueño): #definir el numeraso de las necesidades
    C = baño
    H = hambre
    S = sueño
    Numero_de_necesidad = C * 10**(3*2) + H * 10**(3) + S
    Numero_de_necesidad += 9*10**8 + 9*10**5 + 9*10**2
    return Numero_de_necesidad

def Numeraso2_update():
    global expS, expHu, expC
    Numero_de_necesidad = Numeraso2(baño, hambre, sueño)
    C4 = (Numero_de_necesidad // 10**8) % 10
    C5 = (Numero_de_necesidad // 10**5) % 10
    C6 = (Numero_de_necesidad // 10**2) % 10
    caso = C4 + C5 + C6
    expS = 0
    expHu = 0
    expC = 0
    while caso != 27:
        D4 =  9 - C4
        D5 =  9 - C5
        D6 = 9 - C6
        expS += D4 % 2
        expHu += D5 % 2
        expC += D6 % 2
        Numero_de_necesidad += (D4 % 2)
        Numero_de_necesidad -= (D4 % 2) * (10**3)
        Numero_de_necesidad -= (D5 % 2)
        Numero_de_necesidad -= (D6 % 2) * (10**(3*2))
        C4 = (Numero_de_necesidad // 10**8) % 10
        C5 = (Numero_de_necesidad // 10**5) % 10
        C6 = (Numero_de_necesidad // 10**2) % 10
        caso = C4 + C5 + C6
        Numero_de_necesidad += 1*10**3
    return Numero_de_necesidad, expS, expHu, expC

# --- Función Principal para procesar el mensaje del usuario ---
def process_user_message(message):
    global Escenario, Nivel_incomodidad, a, b, c, baño, hambre, sueño, expB, expH, expL, expS, expHu, expC

    # Actualiza las necesidades biológicas pasivamente
    baño += 1
    hambre += 1
    sueño += 1

    # Analiza la frase del usuario con la API de Gemini
    eval_prompt = (
        f"Analiza la siguiente frase del usuario en una escala del 0 al 20 "
        f"para cada una de las siguientes categorías: Bondad, Hostilidad y Lógica. "
        f"La escala es de 0 (nada) a 20 (máximo). "
        f"También debes analizar el nivel de satisfacción biológica en las categorías: Hambre, Ir al baño, y dormir"
        f"Esas necesidades, se analizan a diferencia de las emociones, del 0 al 100"
        f"Frase del usuario: '{message}'"
        f"También debes analizar la incomodidad que te puede generar la interacción con el usuario y aumentar la calificación de la incomodidad"
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
                    "ac": {"type": "NUMBER", "description": "Calificación de satisfacción con la eliminación de residuos"},
                    "ahu": {"type": "NUMBER", "description": "Calificación de satisfacción con la alimentación"},
                    "As": {"type": "NUMBER", "description": "Calificación de satisfacción con la calidad del sueño"},
                    "ai": {"type": "NUMBER", "description": "Calificación de incomodidad"}
                },
                "propertyOrdering": ["ab", "ah", "al", "ac", "ahu", "As", "ai"]
            }
        }
    }
    
    try:
        response = requests.post(url_eval, headers=headers, json=payload)
        response.raise_for_status()
        evaluacion_api = response.json()['candidates'][0]['content']['parts'][0]['text']
        eval_data = json.loads(evaluacion_api)

        # Actualiza las variables BHL del personaje con las respuestas del usuario
        a += eval_data.get('ab', 0) + expB
        b += eval_data.get('ah', 0) + expH
        c += eval_data.get('al', 0) + expL
        baño += eval_data.get('ac', 0) - expC
        hambre += eval_data.get('ahu', 0) - expHu
        sueño += eval_data.get('As', 0) - expS
        Nivel_incomodidad = eval_data.get('ai', 0)
    except (requests.exceptions.RequestException, json.JSONDecodeError) as err:
        print(f"Error al conectar o decodificar la API: {err}")
        return "Error: No se pudo procesar tu mensaje. Intenta de nuevo más tarde."

    # Efecto de las necesidades en la personalidad
    a -= (baño // 10) + (hambre // 10) + (sueño // 10)
    b += (baño // 10) + (hambre // 10) + (sueño // 10)
    c -= ((baño // 10)*2) + ((hambre // 10)*2) + ((sueño // 10)*2)

    # Lógica para actualizar el escenario
    prompt_para_escenario = (
        f"Eres un narrador. Basado en el siguiente mensaje del usuario y el escenario actual, "
        f"describe el nuevo escenario en una sola frase concisa. "
        f"No añadas diálogos ni descripciones del personaje. Simplemente actualiza el escenario. "
        f"Si el mensaje del usuario no cambia el escenario, repite el escenario actual. "
        f"Escenario actual: '{Escenario}'\n"
        f"Mensaje del usuario: '{message}'\n"
        f"Nuevo escenario:"
    )
    url_escenario = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }
    data_escenario = { "contents": [ { "parts": [ { "text": prompt_para_escenario } ] } ] }
    try:
        response_escenario = requests.post(url_escenario, headers=headers, json=data_escenario)
        response_escenario.raise_for_status()
        Escenario_nuevo = response_escenario.json()['candidates'][0]['content']['parts'][0]['text']
        Escenario = Escenario_nuevo.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar el escenario: {e}")
        
    # Lógica para generar la respuesta del personaje
    Bondad_actual = max(1, a)
    Hostilidad_actual = max(1, b)
    Lógica_actual = max(1, c)
    Cagar_actual = max(1, baño)
    Hambre_actual = max(1, hambre)
    Sueño_actual = max(1, sueño)
    
    cosiente = Bondad_actual + Hostilidad_actual + Lógica_actual
    porB = (Bondad_actual * 100) / cosiente
    porH = (Hostilidad_actual * 100) / cosiente
    porL = (Lógica_actual * 100) / cosiente
    
    Sombra_B = 100 - Bondad_actual
    Sombra_H = 100 - Hostilidad_actual
    Sombra_L = 100 - Lógica_actual
    Deseo_H = Sombra_H / Hostilidad_actual if Hostilidad_actual > 0 else 0
    Deseo_B = Sombra_B / Bondad_actual if Bondad_actual > 0 else 0
    Deseo_L = Sombra_L / Lógica_actual if Lógica_actual > 0 else 0

    prompt_para_ia = (
        f"Eres un personaje con la siguiente personalidad y necesidades:\n"
        f"Personalidad: Bondad={porB:.2f}%, Hostilidad={porH:.2f}%, Lógica={porL:.2f}%\n"
        f"Motivaciones secretas (no las menciones): "
        f"Reprimiendo Bondad (Deseo={Deseo_B}%), Reprimiendo Hostilidad (Deseo={Deseo_H}%), Reprimiendo Lógica (Deseo={Deseo_L}%).\n"
        f"Necesidades físicas: Hambre={Hambre_actual}, Sueño={Sueño_actual}, Evacuación={Cagar_actual}\n"
        f"Sientes una incomodidad general de {Nivel_incomodidad} y estás procesando las experiencias de Bondad={expB}, Hostilidad={expH} y Lógica={expL}.\n"
        f"Tono y comportamiento: Tu tono es fluido con tus porcentajes y necesidades. Actúa con incomodidad si es alta. Responde de forma detallada y reflexiva.\n\n"
        f"Historial de la conversación:\n"
        f"{get_prompt_history_text()}\n"
        f"Usuario: '{message}'\n\n"
        f"Tu respuesta es la de tu personaje."
        f"Para empezar, toma de punto de partida la descripción de este escenario {Escenario}"
        f"Si tienes un valor de experiencia de evacuación: {expC}, experiencia de sueño {expS}, y Experiencia de hambre {expHu} altas (mayor o cercano a 100) tendrás patologías crónicas"
        f"Experiencia de sueño: problemas para dormir"
        f"Experiencia de evacuación: problemas gastrointestinales, problemas para ir al baño"
        f"Experiencia de hambre: Problemas de obesidad, relacionados con el apetito, como que la comida no te satisface"
    )

    url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }
    data = { "contents": [ { "parts": [ { "text": prompt_para_ia } ] } ] }
    
    try:
        response = requests.post(url_ia_response, headers=headers, json=data)
        response.raise_for_status()
        respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
        chat_history.append({"user": message, "character": respuesta_ia})
        
        # Devuelve la respuesta generada por la IA
        return respuesta_ia
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"Error al procesar la respuesta de la API: {e}")
        return "Error: No se pudo generar una respuesta."
