# bhl_web_server.py
#
# Este script crea un servidor web local con Flask para interactuar con el sistema BHL-CHS
# desde cualquier navegador en la misma red local. Se ha mejorado la interfaz de usuario
# para que sea más atractiva y muestre el estado del agente de forma más visual.
#
# Para ejecutarlo, necesitas instalar Flask:
# pip install Flask
#
# Luego, ejecuta este archivo desde la terminal:
# python bhl_web_server.py

from flask import Flask, jsonify, render_template_string, request
import math
import requests
import os
import json
import time
import threading
import queue
import random
import time

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

# Cargar el estado si existe al iniciar el servidor
loaded_state = load_state()
if loaded_state:
    agent_state.update(loaded_state)

# -------------------------------------------------------------------
# Lógica de los sistemas (reutilizada y adaptada)
# -------------------------------------------------------------------

def update_chs_state():
    """Actualiza el estado biológico del CHS basado en el paso del tiempo."""
    variables_chs = agent_state["variables_chs"]
    chosen_type_chs = agent_state["chosen_type_chs"]
    
    variables_chs["H"] = max(0, variables_chs["H"] - 2)
    variables_chs["C"] = min(99, variables_chs["C"] + 1)
    variables_chs["S"] = min(99, variables_chs["S"] + 1)

    priorities = list(chosen_type_chs)
    main_priority = priorities[0]
    
    if main_priority == 'H':
        if variables_chs["H"] < 20:
            variables_chs["C"] = min(99, variables_chs["C"] + 2)
        elif variables_chs["H"] > 80:
            variables_chs["C"] = max(0, variables_chs["C"] - 1)
    elif main_priority == 'S':
        if variables_chs["H"] < 20:
            variables_chs["S"] = min(99, variables_chs["S"] + 3)
        elif variables_chs["H"] > 80:
            variables_chs["S"] = max(0, variables_chs["S"] - 2)

    # Asegurarse de que los valores se mantengan en el rango [0, 99]
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
    
    # ----------------------------------------------------------------------
    # IMPORTANTE: Reemplaza "your-gemini-api-key-here" con tu clave de API real.
    # Esta es la causa probable de tu error 400.
    # ----------------------------------------------------------------------
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = "AIzaSyCeJzrNsR3kOxBylpQi-9F8TK4Zo-TtEFw"

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
        
        b_vals["b"] = min(20, b_vals["b"] + response_json.get('ab', 0))
        b_vals["h"] = min(20, b_vals["h"] + response_json.get('ah', 0))
        b_vals["l"] = min(20, b_vals["l"] + response_json.get('al', 0))
        b_vals["s"] = min(20, b_vals["s"] + response_json.get('as', 0))
        b_vals["e"] = min(20, b_vals["e"] + response_json.get('ae', 0))
        b_vals["i"] = min(20, b_vals["i"] + response_json.get('ai', 0))
        b_vals["ego"] = min(20, b_vals["ego"] + response_json.get('aego', 0))
        
        # Actualizar los valores de sombra
        b_vals["sb"] = 20 - b_vals["b"]
        b_vals["sh"] = 20 - b_vals["h"]
        b_vals["sl"] = 20 - b_vals["l"]
        b_vals["ss"] = 20 - b_vals["s"]
        b_vals["se"] = 20 - b_vals["e"]
        b_vals["si"] = 20 - b_vals["i"]
        b_vals["sego"] = 20 - b_vals["ego"]
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API para la calificación: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error al procesar la respuesta de la API para la calificación: {e}")

def call_gemini_api_async(prompt):
    """Llama a la API de Gemini de forma asíncrona para no bloquear el servidor."""
    # ----------------------------------------------------------------------
    # IMPORTANTE: Reemplaza "your-gemini-api-key-here" con tu clave de API real.
    # ----------------------------------------------------------------------
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = "AIzaSyCeJzrNsR3kOxBylpQi-9F8TK4Zo-TtEFw"
    
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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .chat-bubble {
            max-width: 80%;
            border-radius: 1rem;
            padding: 0.75rem 1rem;
            word-wrap: break-word;
        }
        .chat-bubble.user {
            background-color: #3b82f6;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 0.25rem;
        }
        .chat-bubble.character {
            background-color: #e5e7eb;
            color: #1f2937;
            align-self: flex-start;
            border-bottom-left-radius: 0.25rem;
        }
        .progress-bar-container {
            height: 8px;
            background-color: #e5e7eb;
            border-radius: 9999px;
            overflow: hidden;
            margin-top: 4px;
        }
        .progress-bar {
            height: 100%;
            border-radius: 9999px;
            transition: width 0.3s ease-in-out;
        }
    </style>
</head>
<body class="bg-gray-100 flex flex-col items-center justify-start min-h-screen">
    <div class="bg-white rounded-xl shadow-lg p-6 max-w-lg w-full flex flex-col space-y-4 m-4">
        <h1 class="text-3xl font-bold text-center text-gray-800">Agente BHL-CHS</h1>
        
        <div id="state-display" class="bg-gray-200 text-gray-700 p-3 rounded-xl text-sm font-semibold">
            <h2 class="text-lg font-bold text-gray-900 mb-2">Estado del Agente</h2>
            <div id="bhl-state" class="mb-4">
                <p><strong>Personalidad (PER):</strong> <span id="per-type"></span></p>
                <div class="grid grid-cols-2 gap-2 mt-2">
                    <div class="flex items-center space-x-2">
                        <span>Bondad:</span>
                        <div class="flex-grow progress-bar-container"><div id="b-bar" class="progress-bar bg-green-500"></div></div>
                        <span id="b-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Sombra B:</span>
                        <div class="flex-grow progress-bar-container"><div id="sb-bar" class="progress-bar bg-green-300"></div></div>
                        <span id="sb-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Hostilidad:</span>
                        <div class="flex-grow progress-bar-container"><div id="h-bar" class="progress-bar bg-red-500"></div></div>
                        <span id="h-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Sombra H:</span>
                        <div class="flex-grow progress-bar-container"><div id="sh-bar" class="progress-bar bg-red-300"></div></div>
                        <span id="sh-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Lógica:</span>
                        <div class="flex-grow progress-bar-container"><div id="l-bar" class="progress-bar bg-blue-500"></div></div>
                        <span id="l-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Sombra L:</span>
                        <div class="flex-grow progress-bar-container"><div id="sl-bar" class="progress-bar bg-blue-300"></div></div>
                        <span id="sl-val" class="text-xs w-6 text-right"></span>
                    </div>
                </div>
            </div>
            
            <div id="chs-state" class="mt-4 border-t pt-4 border-gray-300">
                <p><strong>Necesidades Biológicas (CHS):</strong> <span id="chs-type"></span></p>
                <div class="grid grid-cols-2 gap-2 mt-2">
                    <div class="flex items-center space-x-2">
                        <span>Hambre:</span>
                        <div class="flex-grow progress-bar-container"><div id="h-chs-bar" class="progress-bar bg-yellow-500"></div></div>
                        <span id="h-chs-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Deseo C:</span>
                        <div class="flex-grow progress-bar-container"><div id="c-chs-bar" class="progress-bar bg-gray-500"></div></div>
                        <span id="c-chs-val" class="text-xs w-6 text-right"></span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span>Sueño:</span>
                        <div class="flex-grow progress-bar-container"><div id="s-chs-bar" class="progress-bar bg-purple-500"></div></div>
                        <span id="s-chs-val" class="text-xs w-6 text-right"></span>
                    </div>
                </div>
            </div>
        </div>

        <div id="chat-box" class="bg-gray-50 h-96 overflow-y-auto p-4 rounded-xl border border-gray-300 flex flex-col space-y-4">
            <div class="text-gray-500 italic text-center">¡Inicia una conversación!</div>
        </div>
        
        <div class="flex space-x-2 mt-4">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje..." class="flex-1 p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500">
            <button id="send-button" class="bg-blue-600 text-white p-3 rounded-xl font-semibold hover:bg-blue-700 transition duration-300">
                Enviar
            </button>
        </div>
        <div id="message-box" class="hidden text-center p-2 rounded-lg mt-2"></div>
    </div>
    
    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        const stateDisplay = document.getElementById('state-display');
        const messageBox = document.getElementById('message-box');
        let isLoading = false;

        function showMessage(message, type = 'info') {
            messageBox.textContent = message;
            messageBox.className = 'text-center p-2 rounded-lg mt-2';
            if (type === 'info') {
                messageBox.classList.add('bg-blue-100', 'text-blue-700', 'block');
            } else if (type === 'error') {
                messageBox.classList.add('bg-red-100', 'text-red-700', 'block');
            }
            setTimeout(() => {
                messageBox.classList.remove('block');
                messageBox.classList.add('hidden');
            }, 3000);
        }

        function createChatBubble(text, sender) {
            const bubble = document.createElement('div');
            bubble.classList.add('chat-bubble', sender === 'user' ? 'user' : 'character');
            bubble.textContent = text;
            chatBox.appendChild(bubble);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function updateStateUI(state) {
            const bhl = state.variables_bhl;
            const chs = state.variables_chs;

            document.getElementById('per-type').textContent = state.per;
            document.getElementById('chs-type').textContent = state.chosen_type_chs;
            
            // BHL
            document.getElementById('b-val').textContent = bhl.b;
            document.getElementById('b-bar').style.width = `${(bhl.b / 20) * 100}%`;
            document.getElementById('sb-val').textContent = bhl.sb;
            document.getElementById('sb-bar').style.width = `${(bhl.sb / 20) * 100}%`;
            document.getElementById('h-val').textContent = bhl.h;
            document.getElementById('h-bar').style.width = `${(bhl.h / 20) * 100}%`;
            document.getElementById('sh-val').textContent = bhl.sh;
            document.getElementById('sh-bar').style.width = `${(bhl.sh / 20) * 100}%`;
            document.getElementById('l-val').textContent = bhl.l;
            document.getElementById('l-bar').style.width = `${(bhl.l / 20) * 100}%`;
            document.getElementById('sl-val').textContent = bhl.sl;
            document.getElementById('sl-bar').style.width = `${(bhl.sl / 20) * 100}%`;

            // CHS
            document.getElementById('h-chs-val').textContent = chs.H;
            document.getElementById('h-chs-bar').style.width = `${(chs.H / 99) * 100}%`;
            document.getElementById('c-chs-val').textContent = chs.C;
            document.getElementById('c-chs-bar').style.width = `${(chs.C / 99) * 100}%`;
            document.getElementById('s-chs-val').textContent = chs.S;
            document.getElementById('s-chs-bar').style.width = `${(chs.S / 99) * 100}%`;
        }

        async function fetchState() {
            try {
                const response = await fetch('/get_state');
                const data = await response.json();
                updateStateUI(data.state);
                // Clear chatbox and rebuild history
                chatBox.innerHTML = '';
                if (data.state.chat_history.length === 0) {
                     chatBox.innerHTML = '<div class="text-gray-500 italic text-center">¡Inicia una conversación!</div>';
                } else {
                    data.state.chat_history.forEach(item => {
                        createChatBubble(item.user, 'user');
                        createChatBubble(item.character, 'character');
                    });
                }
            } catch (error) {
                console.error('Error fetching state:', error);
                showMessage('Error al cargar el estado.', 'error');
            }
        }

        sendButton.addEventListener('click', () => {
            if (isLoading) return;
            const message = userInput.value.trim();
            if (message) {
                isLoading = true;
                sendButton.textContent = 'Enviando...';
                sendButton.disabled = true;
                
                createChatBubble(message, 'user');
                userInput.value = '';

                fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        createChatBubble(data.response, 'character');
                        updateStateUI(data.state);
                    } else {
                        showMessage(data.error, 'error');
                        createChatBubble("Error: No pude obtener una respuesta.", 'character');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Error de conexión con el servidor.', 'error');
                    createChatBubble("Error de conexión.", 'character');
                })
                .finally(() => {
                    isLoading = false;
                    sendButton.textContent = 'Enviar';
                    sendButton.disabled = false;
                });
            }
        });

        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendButton.click();
            }
        });

        // Cargar estado inicial y iniciar el temporizador
        fetchState();
        setInterval(() => {
            # update_chs_state() se llama en cada petición, pero podríamos hacer
            # un polling periódico para actualizar la UI sin interacción del usuario.
            # Para esta demo, lo mantendremos simple.
        }, 15000); // 15 segundos

    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get_state")
def get_state():
    return jsonify({"state": agent_state})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"success": False, "error": "Mensaje vacío"}), 400

    # 1. Actualizar el estado del CHS basado en el tiempo
    update_chs_state()
    
    # 2. Actualizar el estado del BHL basado en el input del usuario
    update_bhl_state(user_message)
    
    # 3. Construir el prompt para la respuesta del personaje
    bhl_vals = agent_state["variables_bhl"]
    chs_vals = agent_state["variables_chs"]
    per_type = agent_state["per"]

    prompt_para_ia = (
        f"Eres un personaje cuya personalidad es del tipo '{per_type}'.\n"
        f"Tus valores BHL (Bondad, Hostilidad, Lógica) son: "
        f"Bondad={bhl_vals['b']}, Hostilidad={bhl_vals['h']}, Lógica={bhl_vals['l']}.\n"
        f"Tus valores de Sombra (Bondad, Hostilidad, Lógica) son: "
        f"Bondad={bhl_vals['sb']}, Hostilidad={bhl_vals['sh']}, Lógica={bhl_vals['sl']}.\n"
        f"Tus valores de CHS (Cagar, Hambre, Sueño) son: "
        f"Hambre={chs_vals['H']}, Cagar={chs_vals['C']}, Sueño={chs_vals['S']}.\n"
        f"Tu tipo de necesidades CHS es: {agent_state['chosen_type_chs']}.\n"
        f"Tu historial de conversación: {agent_state['chat_history']}.\n"
        f"Considerando todos estos factores (valores BHL, CHS, tu historial y la prioridad de tus necesidades), "
        f"responde al siguiente mensaje del usuario. Sé breve, coherente y muestra una personalidad "
        f"con las motivaciones que tus valores implican.\n"
        f"Mensaje del usuario: {user_message}"
    )

    # 4. Llamar a la API de Gemini de forma asíncrona
    api_thread = threading.Thread(target=call_gemini_api_async, args=(prompt_para_ia,))
    api_thread.start()

    # 5. Esperar la respuesta
    api_thread.join(timeout=30) # Espera un máximo de 30 segundos

    try:
        response_data = response_queue.get(timeout=1) # Intenta obtener la respuesta
        if response_data["success"]:
            respuesta_ia = response_data["text"]
            # Guardar la interacción en el historial
            agent_state["chat_history"].append({"user": user_message, "character": respuesta_ia})
            save_state()
            return jsonify({"success": True, "response": respuesta_ia, "state": agent_state})
        else:
            return jsonify({"success": False, "error": response_data["error"]}), 500
    except queue.Empty:
        return jsonify({"success": False, "error": "La IA tardó demasiado en responder."}), 504

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

