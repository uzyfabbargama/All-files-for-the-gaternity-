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
MEMORIA_EMOCIONAL_FILE = "bhl_emocional_data.txt"
MEMORIA_CONVERSACION = 50 # Número de conversaciones a recordar en el prompt
conversacion_count = 0

a, b, c = 50, 50, 50  # Valores iniciales por defecto
baño, hambre, sueño = 50, 50, 50

# Variables de experiencia (serán actualizadas)
expB, expH, expL = 0, 0, 0
expS, expHu, expC = 0, 0, 0

# --- Lógica de Inicialización ---
def initialize_game(escenario_inicial, bondad, hostilidad, logica):
    """Inicializa el estado del personaje con los valores de la UI."""
    global Escenario, a, b, c, conversacion_count, chat_history
    Escenario = escenario_inicial
    a = max(1, bondad)
    b = max(1, hostilidad)
    c = max(1, logica)
    chat_history = []
    conversacion_count = 0
    print(f"Juego inicializado. Escenario: {Escenario}, B: {a}, H: {b}, L: {c}")

def get_prompt_history_text():
    # Devuelve el historial como texto formateado, limitado al número de conversaciones
    history_to_send = chat_history[-MEMORIA_CONVERSACION:]
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in history_to_send])

def save_state():
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "a_b_c_values": [a, b, c],
        "exp_values": [expB, expH, expL],
        "chs_values": [baño, hambre, sueño],
        "exp_chs": [expS, expHu, expC],
        "chat_history": chat_history,
        "conversacion_count": conversacion_count,
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n--- Estado del personaje guardado en '{SAVE_FILE}' ---")

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    global a, b, c, expB, expH, expL, baño, hambre, sueño, expS, expHu, expC, chat_history, conversacion_count
    if not os.path.exists(SAVE_FILE):
        print(f"--- Archivo de guardado '{SAVE_FILE}' no encontrado. Se iniciará un nuevo juego. ---")
        return False
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    
    a, b, c = data["a_b_c_values"]
    expB, expH, expL = data["exp_values"]
    baño, hambre, sueño = data["chs_values"]
    expS, expHu, expC = data["exp_chs"]
    chat_history = data["chat_history"]
    conversacion_count = data["conversacion_count"]
    
    print(f"--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    return True

def save_emocional_data():
    """Guarda la 'memoria emocional' en un archivo de texto."""
    global conversacion_count
    # Genera un "numerazo" basado en el estado actual del personaje
    numerazo = (a * 10000000) + (b * 100000) + (c * 1000) + (expS * 10) + (expHu) + (expC)
    
    with open(MEMORIA_EMOCIONAL_FILE, 'a') as f:
        f.write(f"Conversación {conversacion_count}: {numerazo}\n")

def get_emocional_data():
    """Lee la 'memoria emocional' del archivo de texto."""
    if not os.path.exists(MEMORIA_EMOCIONAL_FILE):
        return "El personaje no tiene recuerdos emocionales."
        
    with open(MEMORIA_EMOCIONAL_FILE, 'r') as f:
        return f.read()

def process_user_message(message):
    """Procesa el mensaje del usuario y obtiene una respuesta de la IA."""
    global a, b, c, baño, hambre, sueño, expS, expHu, expC, chat_history, conversacion_count

    if message.lower() == "exit":
        save_state()
        return "Hasta luego."
        
    # Lógica para la progresión de la incomodidad
    incomodidad_base = a / 20 + b / 20 + c / 20
    baño = baño + random.randint(1, 10)
    hambre = hambre + random.randint(1, 10)
    sueño = sueño + random.randint(1, 10)

    # Actualiza variables de experiencia (como antes)
    if sueño >= 100:
        expS += (sueno / 100)
    if hambre >= 100:
        expHu += (hambre / 100)
    if baño >= 100:
        expC += (baño / 100)

    # Lógica de la IA (ahora con la memoria emocional)
    emocional_data = get_emocional_data()
    prompt_history = get_prompt_history_text()
    
    prompt_para_ia = (
        f"Eres un personaje en un mundo de juego de rol. Tienes las siguientes estadísticas:\n"
        f"Bondad (a): {a}, Hostilidad (b): {b}, Lógica (c): {c}\n"
        f"Necesidades físicas: Baño: {baño}, Hambre: {hambre}, Sueño: {sueño}\n"
        f"Experiencia emocional del pasado: {emocional_data}\n"
        f"Historial de conversación reciente:\n{prompt_history}\n"
        f"Usuario: '{message}'\n\n"
        f"Tu respuesta es la de tu personaje."
        f"Para empezar, toma de punto de partida la descripción de este escenario {Escenario}"
        f"Si tienes un valor de experiencia de evacuación: {expC}, experiencia de sueño {expS}, y Experiencia de hambre {expHu} altas (mayor o cercano a 100) tendrás patologías crónicas"
        f"Experiencia de sueño: problemas para dormir"
        f"Experiencia de evacuación: problemas gastrointestinales, problemas para ir al baño"
        f"Experiencia de hambre: Problemas de obesidad, relacionados con el apetito, como que la comida no te satisface"
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
        
        chat_history.append({"user": message, "character": respuesta_ia})
        
        # Incrementa el contador y guarda la memoria emocional
        conversacion_count += 1
        save_emocional_data()
        
        # Devuelve la respuesta generada por la IA
        return respuesta_ia
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        return f"Ocurrió un error al conectar con la IA: {e}"
