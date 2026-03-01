# bhl_web_server.py
#
# Este script crea un servidor web local con Flask para interactuar con el sistema BHL-CHS
# desde cualquier navegador en la misma red local (como tu celular).
#
# Para ejecutarlo, necesitas instalar Flask:
# pip install Flask
#
# Luego, ejecuta este archivo desde la terminal:
# python bhl_web_server.py
#
# Para acceder desde tu celular, usa la dirección IP de tu computadora (ej: 192.168.1.5:5000)

from flask import Flask, jsonify, render_template_string, request
import math
import requests
import os
import json
import time
import threading
import queue
import random

app = Flask(__name__)

# Nombre del archivo donde se guardará y cargará el estado
SAVE_FILE = "bhl_session_data.json"

# -------------------------------------------------------------------
# Variables de estado del Agente Principal
# Usamos un diccionario global para mantener el estado del personaje
# -------------------------------------------------------------------
agent_state = {
    "variables_bhl": {
        "b": random.randint(1, 20),  # Bondad
        "h": random.randint(1, 20),  # Hostilidad
        "l": random.randint(1, 20),  # Lógica
        "s": random.randint(1, 20),  # Soberbia
        "e": random.randint(1, 20),  # Envidia
        "i": random.randint(1, 20),  # Indiferencia
        "ego": random.randint(1, 20), # Egoísmo
        "sb": 0, # Sombra Bondad
        "sh": 0, # Sombra Hostilidad
        "sl": 0, # Sombra Lógica
        "ss": 0, # Sombra Soberbia
        "se": 0, # Sombra Envidia
        "si": 0, # Sombra Indiferencia
        "sego": 0 # Sombra Egoísmo
    },
    "variables_chs": {
        "C": random.randint(0, 99),  # Cagar (alto valor = necesidad)
        "H": random.randint(0, 99),  # Hambre (alto valor = satisfecho)
        "S": random.randint(0, 99),  # Sueño (alto valor = despierto)
    },
    "per": random.choice(["BHL", "BLH", "HLB", "HBL", "LHB", "LBH"]),
    "chosen_type_chs": random.choice(["CHS", "CSH", "HCS", "HSC", "SCH", "SHC"]),
    "chat_history": []
}

# Calcular los valores "super" en base a los iniciales
agent_state["variables_bhl"]["sb"] = 20 - agent_state["variables_bhl"]["b"]
agent_state["variables_bhl"]["sh"] = 20 - agent_state["variables_bhl"]["h"]
agent_state["variables_bhl"]["sl"] = 20 - agent_state["variables_bhl"]["l"]
agent_state["variables_bhl"]["ss"] = 20 - agent_state["variables_bhl"]["s"]
agent_state["variables_bhl"]["se"] = 20 - agent_state["variables_bhl"]["e"]
agent_state["variables_bhl"]["si"] = 20 - agent_state["variables_bhl"]["i"]
agent_state["variables_bhl"]["sego"] = 20 - agent_state["variables_bhl"]["ego"]

# Cola para manejar la comunicación entre hilos (para la IA)
response_queue = queue.Queue()

# -------------------------------------------------------------------
# Lógica de guardado/cargado de estado
# -------------------------------------------------------------------
def save_state():
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "variables_bhl": agent_state["variables_bhl"],
        "variables_chs": agent_state["variables_chs"],
        "per": agent_state["per"],
        "chosen_type_chs": agent_state["chosen_type_chs"],
        "chat_history": agent_state["chat_history"]
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    if not os.path.exists(SAVE_FILE):
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    return data

# -------------------------------------------------------------------
# Lógica de los sistemas (reutilizada y adaptada)
# -------------------------------------------------------------------

def update_chs_state():
    """Actualiza el estado biológico del CHS basado en el paso del tiempo."""
    variables_chs = agent_state["variables_chs"]
    chosen_type_chs = agent_state["chosen_type_chs"]
    
    variables_chs["H"] -= 2
    variables_chs["C"] += 1

    priorities = list(chosen_type_chs)
    main_priority = priorities[0]

    if main_priority == 'H':
        if variables_chs["H"] < 20:
            variables_chs["C"] += 2
        elif variables_chs["H"] > 80:
            variables_chs["C"] -= 1
    elif main_priority == 'S':
        if variables_chs["H"] < 20:
            variables_chs["S"] += 3
        elif variables_chs["H"] > 80:
            variables_chs["S"] -= 2
    
    for key in variables_chs:
        variables_chs[key] = max(0, min(99, int(variables_chs[key])))

def update_bhl_state(user_input):
    """Califica el input del usuario y actualiza los valores BHL."""
    eval_prompt = (
        f"Analiza la siguiente frase del usuario en una escala del 0 al 10 "
        f"para cada una de las siguientes categorías: Bondad, Hostilidad, Lógica, Soberbia, Envidia, Indiferencia y Egoísmo. "
        f"La escala es de 0 (nada) a 10 (máximo). "
        f"Frase del usuario: '{user_input}'"
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
    
    b_vals = agent_state["variables_bhl"]
    
    try:
        response = requests.post(url_eval, headers=headers, data=json.dumps(payload))
        response.raise_for_status() 
        response_json = json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'])
        
        b_vals["b"] += response_json.get('ab', 0)
        b_vals["h"] += response_json.get('ah', 0)
        b_vals["l"] += response_json.get('al', 0)
        b_vals["s"] += response_json.get('as', 0)
        b_vals["e"] += response_json.get('ae', 0)
        b_vals["i"] += response_json.get('ai', 0)
        b_vals["ego"] += response_json.get('aego', 0)
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API para la calificación: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al procesar la respuesta de la API para la calificación: {e}")

def call_gemini_api_async(prompt):
    """Llama a la API de Gemini de forma asíncrona para no bloquear el servidor."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zMn"
    
    url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    headers = { 'Content-Type': 'application/json' }
    data = { "contents": [ { "parts": [ { "text": prompt } ] } ] }
    
    try:
        response = requests.post(url_ia_response, headers=headers, json=data)
        response.raise_for_status()
        respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
        response_queue.put({"success": True, "text": respuesta_ia})
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        response_queue.put({"success": False, "error": str(e)})
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al procesar la respuesta de la API: {e}")
        response_queue.put({"success": False, "error": str(e)})


# -------------------------------------------------------------------
# Rutas del servidor Flask
# -------------------------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat BHL-CHS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-100 flex flex-col items-center justify-start min-h-screen">
    <div class="bg-white rounded-xl shadow-lg p-6 max-w-lg w-full flex flex-col space-y-4 m-4">
        <h1 class="text-3xl font-bold text-center text-gray-800">Agente BHL-CHS</h1>
        <div id="state-display" class="bg-gray-200 text-gray-700 p-3 rounded-lg text-sm font-mono">
            Cargando estado...
        </div>
        <div id="chat-box" class="bg-gray-50 h-96 overflow-y-auto p-4 rounded-lg border border-gray-300 flex flex-col space-y-4">
            <div class="text-gray-500 italic text-center">¡Inicia una conversación!</div>
        </div>
        <div class="flex space-x-2 mt-4">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje..." class="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            <button id="send-button" class="bg-blue-600 text-white p-3 rounded-lg font-semibold hover:bg-blue-700 transition duration-300">
                Enviar
            </button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const stateDisplay = document.getElementById('state-display');

        async function fetchState() {
            try {
                const response = await fetch('/get_state');
                const data = await response.json();
                updateUI(data);
            } catch (error) {
                console.error('Error fetching state:', error);
                stateDisplay.textContent = 'Error al cargar el estado.';
            }
        }

        function updateUI(data) {
            // Actualizar el estado del agente
            const bhl = data.state.variables_bhl;
            const chs = data.state.variables_chs;
            const per = data.state.per;
            const chs_type = data.state.chosen_type_chs;

            const bhl_display = `B:${bhl.b}, H:${bhl.h}, L:${bhl.l}, S:${bhl.s}, E:${bhl.e}, I:${bhl.i}, Ego:${bhl.ego} (Tipo: ${per})`;
            const chs_display = `C:${chs.C}, H:${chs.H}, S:${chs.S} (Tipo: ${chs_type})`;
            stateDisplay.innerHTML = `<strong>Estado BHL:</strong> ${bhl_display}<br><strong>Estado CHS:</strong> ${chs_display}`;

            // Reconstruir el historial de chat
            chatBox.innerHTML = '';
            if (data.state.chat_history.length === 0) {
                chatBox.innerHTML = '<div class="text-gray-500 italic text-center">¡Inicia una conversación!</div>';
            } else {
                data.state.chat_history.forEach(entry => {
                    const userMsg = document.createElement('div');
                    userMsg.className = 'text-right text-gray-800';
                    userMsg.textContent = `Tú: ${entry.user}`;
                    chatBox.appendChild(userMsg);

                    const agentMsg = document.createElement('div');
                    agentMsg.className = 'text-left text-blue-600 font-semibold';
                    agentMsg.textContent = `Personaje: ${entry.character}`;
                    chatBox.appendChild(agentMsg);
                });
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;

            userInput.value = '';
            sendButton.disabled = true;
            sendButton.textContent = 'Pensando...';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_input: message }),
                });
                const data = await response.json();
                if (data.success) {
                    updateUI(data);
                } else {
                    console.error('API Error:', data.error);
                    alert('Hubo un error con la respuesta de la IA. Intenta de nuevo.');
                }
            } catch (error) {
                console.error('Network Error:', error);
                alert('Error de conexión con el servidor. Intenta de nuevo.');
            } finally {
                sendButton.disabled = false;
                sendButton.textContent = 'Enviar';
            }
        }

        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Cargar el estado inicial al cargar la página
        fetchState();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    """Ruta principal que sirve el HTML del chat."""
    return render_template_string(HTML_TEMPLATE)

@app.route("/get_state")
def get_state():
    """Ruta para que el frontend obtenga el estado actual del agente."""
    save_state()
    return jsonify(state=agent_state)

@app.route("/chat", methods=["POST"])
def chat():
    """Ruta para manejar la conversación y actualizar el estado."""
    user_input = request.json.get("user_input")
    if not user_input:
        return jsonify({"success": False, "error": "No se recibió un mensaje de usuario."}), 400

    # Lógica de actualización del estado del agente
    update_chs_state()
    
    user_input_lower = user_input.lower()
    if "comer" in user_input_lower or "comida" in user_input_lower:
        agent_state["variables_chs"]["H"] += 50
    elif "descansar" in user_input_lower or "dormir" in user_input_lower:
        agent_state["variables_chs"]["S"] += 50
    elif "baño" in user_input_lower or "necesito ir" in user_input_lower:
        agent_state["variables_chs"]["C"] -= 50

    for key in agent_state["variables_chs"]:
        agent_state["variables_chs"][key] = max(0, min(99, int(agent_state["variables_chs"][key])))

    update_bhl_state(user_input)

    # Calcular porcentajes BHL
    bhl_vals = agent_state["variables_bhl"]
    cosciente = sum(bhl_vals[key] for key in ["b", "h", "l", "s", "e", "i", "ego"])
    if cosciente == 0:
        cosciente = 1
    porB = (bhl_vals["b"] * 100) / cosciente
    porH = (bhl_vals["h"] * 100) / cosciente
    porL = (bhl_vals["l"] * 100) / cosciente
    porS = (bhl_vals["s"] * 100) / cosciente
    porE = (bhl_vals["e"] * 100) / cosciente
    porI = (bhl_vals["i"] * 100) / cosciente
    porEgo = (bhl_vals["ego"] * 100) / cosciente

    prompt_history_text = "\n".join([f"Usuario: {entry['user']}\nPersonaje: {entry['character']}" for entry in agent_state["chat_history"]])

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
        f"Tus necesidades biológicas actuales son:\n"
        f"- **Hambre (H):** {agent_state['variables_chs']['H']} (Un valor bajo significa que tienes hambre)\n"
        f"- **Sueño (S):** {agent_state['variables_chs']['S']} (Un valor bajo significa que estás cansado)\n"
        f"- **Necesidad de ir al baño (C):** {agent_state['variables_chs']['C']} (Un valor alto significa que necesitas ir)\n"
        f"Comportamiento esperado:\n"
        f"* **Tono:** Mantén un tono de voz coherente con tus porcentajes y necesidades. Si tienes mucha hambre o necesitas ir al baño, tu tono debe ser más irritable o distraído. Si estás cansado, tu lógica puede fallar. Prioriza tus necesidades biológicas en tu respuesta si son extremas.\n"
        f"* **Longitud de la respuesta:** Tu respuesta debe ser detallada y reflexiva, apuntando a ser al menos el doble de la longitud del mensaje del usuario.\n"
        f"* **Coherencia:** No menciones los porcentajes o los valores de tus necesidades. Describe tus acciones entre asteriscos, por ejemplo: *asiente con la cabeza* o *se frota los ojos con cansancio*. Interactúa con el usuario de manera que se sienta escuchado y comprendido, como si fueras un personaje real, no un asistente de IA.\n\n"
        f"Historial de la conversación:\n"
        f"{prompt_history_text}\n\n"
        f"El usuario dice: '{user_input}'\n\n"
        f"Tu respuesta debe ser una respuesta directa al usuario."
    )
    
    # Iniciar la llamada a la API en un hilo separado
    threading.Thread(target=call_gemini_api_async, args=(prompt_para_ia,)).start()
    
    try:
        # Esperar la respuesta de la API (con un timeout)
        response_data = response_queue.get(timeout=30)
        
        if response_data["success"]:
            respuesta_ia = response_data["text"]
            agent_state["chat_history"].append({"user": user_input, "character": respuesta_ia})
            save_state()
            return jsonify(success=True, response=respuesta_ia, state=agent_state)
        else:
            return jsonify({"success": False, "error": response_data["error"]}), 500
    except queue.Empty:
        return jsonify({"success": False, "error": "La IA tardó demasiado en responder."}), 500

def initialize_state_and_run_server():
    """Inicializa el estado del agente y ejecuta el servidor."""
    global agent_state
    
    # Cargar estado si existe
    loaded_data = load_state()
    if loaded_data:
        choice = input("Se encontró una sesión guardada. ¿Deseas continuarla? (s/n): ")
        if choice.lower() == 's':
            agent_state["variables_bhl"] = loaded_data["variables_bhl"]
            agent_state["variables_chs"] = loaded_data["variables_chs"]
            agent_state["per"] = loaded_data["per"]
            agent_state["chosen_type_chs"] = loaded_data["chosen_type_chs"]
            agent_state["chat_history"] = loaded_data["chat_history"]
            print("\n--- Estado del personaje cargado y listo para el servidor ---")
    else:
        # Lógica para definir la personalidad inicial BHL si no se cargó una sesión
        person = 0
        while True:
            try:
                person = int(input("Defina tipo de personalidad del 1 al 6: "))
                if 1 <= person <= 6:
                    break
                else:
                    print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        
        if person == 1: agent_state["per"] = "BHL"
        elif person == 2: agent_state["per"] = "BLH"
        elif person == 3: agent_state["per"] = "HLB"
        elif person == 4: agent_state["per"] = "HBL"
        elif person == 5: agent_state["per"] = "LHB"
        elif person == 6: agent_state["per"] = "LBH"

        # Definir variables iniciales BHL
        bhl_vals = agent_state["variables_bhl"]
        while True:
            try:
                bhl_vals["b"] = int(input("Defina bondad del 1 al 20: "))
                if 1 <= bhl_vals["b"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        while True:
            try:
                bhl_vals["h"] = int(input("Defina hostilidad del 1 al 20: "))
                if 1 <= bhl_vals["h"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        while True:
            try:
                bhl_vals["l"] = int(input("Defina lógica del 1 al 20: "))
                if 1 <= bhl_vals["l"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        while True:
            try:
                bhl_vals["s"] = int(input("Defina soberbia del 1 al 20: "))
                if 1 <= bhl_vals["s"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        while True:
            try:
                bhl_vals["e"] = int(input("Defina envidia del 1 al 20: "))
                if 1 <= bhl_vals["e"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        while True:
            try:
                bhl_vals["i"] = int(input("Defina indiferencia del 1 al 20: "))
                if 1 <= bhl_vals["i"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        while True:
            try:
                bhl_vals["ego"] = int(input("Defina egoísmo del 1 al 20: "))
                if 1 <= bhl_vals["ego"] <= 20: break
                else: print("Error, ingrese nuevamente")
            except ValueError:
                print("Error, ingrese nuevamente")
        
        bhl_vals["sb"] = 20 - bhl_vals["b"]
        bhl_vals["sh"] = 20 - bhl_vals["h"]
        bhl_vals["sl"] = 20 - bhl_vals["l"]
        bhl_vals["ss"] = 20 - bhl_vals["s"]
        bhl_vals["se"] = 20 - bhl_vals["e"]
        bhl_vals["si"] = 20 - bhl_vals["i"]
        bhl_vals["sego"] = 20 - bhl_vals["ego"]

        # Lógica para definir las necesidades biológicas iniciales CHS
        permutations_chs = ["CHS", "CSH", "HCS", "HSC", "SCH", "SHC"]
        chosen_type_chs = ""
        while True:
            print("Elige el tipo de necesidades biológicas (CHS, CSH, HCS, HSC, SCH, SHC):")
            chosen_type_chs = input("> ").upper()
            if chosen_type_chs in permutations_chs:
                agent_state["chosen_type_chs"] = chosen_type_chs
                break
            print("Opción inválida. Intenta de nuevo.")

    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    initialize_state_and_run_server()
# -------------------------------------------------------------------
# Inicia el servidor Flask y carga el estado del agente.