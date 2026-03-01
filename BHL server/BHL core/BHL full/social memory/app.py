# app.py
# Este archivo contiene la aplicación completa: servidor web y lógica de chat.
# Asegúrate de que los archivos 'BHL Completo Memoria Social.py' y 'base_de_datos_social.py'
# se encuentren en el mismo directorio.

from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import requests
import os
import json

# Importamos las clases y funciones de tus módulos existentes.
from base_de_datos_social import MemoriaSocial
from BHL_Completo_Memoria_Social import (
    load_state,
    save_state,
    update_chs_state,
    get_numeraso,
    update_shadow_desire_and_ego,
    get_prompt_history_text,
    get_bhl_values,
    get_variables_chs,
)
# Importamos el nuevo módulo social_parser
from social_parser import update_social_memory
# Inicializamos la aplicación Flask
app = Flask(__name__)
CORS(app)

# La API key para Gemini.
API_KEY = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# Inicializamos el estado del personaje y la memoria social de manera global.
state = {
    "bhl_values": {"b": 15, "h": 5, "l": 10, "ego": 5},
    "shadow_values": {"sb": 5, "sh": 15, "sl": 10, "db": 0, "dh": 0, "dl": 0},
    "per": "BHL",
    "numeraso": 0,
    "memoria_social": MemoriaSocial("IA_Emergente")
}

HTML_TEMPLATE = """
<!-- index.html -->
<!-- Este archivo contiene la interfaz de usuario. Usa HTML, CSS y JavaScript. -->

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BHL: Tu compañero de IA</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }

        .chat-container {
            width: 100%;
            max-width: 600px;
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            height: 80vh;
            overflow: hidden;
        }

        .messages {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 80%;
            padding: 12px 18px;
            border-radius: 20px;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .user-message {
            background-color: #2a2a2a;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }

        .ai-message {
            background-color: #0d47a1;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }

        .input-area {
            display: flex;
            padding: 15px;
            border-top: 1px solid #333;
        }

        .input-area input {
            flex-grow: 1;
            padding: 10px 15px;
            border-radius: 25px;
            border: none;
            background-color: #333;
            color: #fff;
            outline: none;
            font-size: 16px;
        }

        .input-area button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 25px;
            margin-left: 10px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .input-area button:hover {
            background-color: #45a049;
        }

        .bhl-bars {
            width: 100%;
            max-width: 600px;
            margin-top: 20px;
            display: flex;
            gap: 10px;
            height: 30px;
            border-radius: 10px;
            overflow: hidden;
            border: 2px solid #333;
        }

        .bar {
            height: 100%;
            transition: width 0.5s ease-in-out;
            position: relative;
        }

        .bar-label {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
            font-size: 14px;
        }

        #bondad { background-color: #4CAF50; }
        #hostilidad { background-color: #f44336; }
        #logica { background-color: #2196F3; }
    </style>
</head>
<body>

    <div class="chat-container">
        <div class="messages" id="messages-container">
            <!-- Los mensajes del chat se añadirán aquí dinámicamente -->
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Escribe un mensaje...">
            <button id="send-button">Enviar</button>
        </div>
    </div>

    <div class="bhl-bars">
        <div class="bar" id="bondad" style="width: 33%;">
            <span class="bar-label">Bondad</span>
        </div>
        <div class="bar" id="hostilidad" style="width: 33%;">
            <span class="bar-label">Hostilidad</span>
        </div>
        <div class="bar" id="logica" style="width: 33%;">
            <span class="bar-label">Lógica</span>
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('messages-container');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        // Referencias a las barras BHL
        const bondadBar = document.getElementById('bondad');
        const hostilidadBar = document.getElementById('hostilidad');
        const logicaBar = document.getElementById('logica');

        function appendMessage(message, type) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.classList.add(type === 'user' ? 'user-message' : 'ai-message');
            messageElement.textContent = message;
            chatContainer.appendChild(messageElement);
            chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll
        }

        function updateBHLBars(bhl_values) {
            const b = bhl_values.b;
            const h = bhl_values.h;
            const l = bhl_values.l;
            
            const total = b + h + l;
            
            // Calculamos los porcentajes
            const bPercent = (b / total) * 100;
            const hPercent = (h / total) * 100;
            const lPercent = (l / total) * 100;

            // Actualizamos el ancho de las barras
            bondadBar.style.width = `${bPercent}%`;
            hostilidadBar.style.width = `${hPercent}%`;
            logicaBar.style.width = `${lPercent}%`;
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;

            // Mostramos el mensaje del usuario
            appendMessage(message, 'user');
            userInput.value = '';

            try {
                // Realizamos la petición al servidor Flask
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                // Mostramos la respuesta de la IA
                appendMessage(data.response, 'ai');
                
                // Actualizamos las barras BHL con los nuevos valores del servidor
                updateBHLBars(data.bhl_values);

            } catch (error) {
                console.error('Error:', error);
                appendMessage('Lo siento, no pude comunicarme con la IA.', 'ai');
            }
        }

        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""
@app.route('/', methods=['GET'])
def index():
    """
    Ruta principal que sirve la interfaz de usuario.
    """
    return render_template_string(HTML_TEMPLATE)
def calcular_porcentajes(bhl):
    total = sum([bhl.get(k, 0) for k in ['b', 'h', 'l', 'ego', 's', 'e', 'i']])
    if total == 0:
        return {k: 0 for k in ['B', 'H', 'L', 'S', 'E', 'I', 'Ego']}
    return {
        'B': (bhl.get('b', 0) * 100) / total,
        'H': (bhl.get('h', 0) * 100) / total,
        'L': (bhl.get('l', 0) * 100) / total,
        'S': (bhl.get('s', 0) * 100) / total,
        'E': (bhl.get('e', 0) * 100) / total,
        'I': (bhl.get('i', 0) * 100) / total,
        'Ego': (bhl.get('ego', 0) * 100) / total,
    }

@app.route('/chat', methods=['POST'])
def chat():
    """
    Ruta que maneja las peticiones de chat y actualiza la personalidad.
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        nombre_usuario = data.get('user', 'Usuario')

        if not user_message:
            return jsonify({"error": "No se recibió ningún mensaje"}), 400

        # Paso 1: Obtener el estado actual del personaje
        bhl_values = state["bhl_values"]
        shadow_values = state["shadow_values"]
        per = state["per"]
        memoria_social = state["memoria_social"]
        # Si usas variables_chs, prompt_history_text, ans, perfil_usuario, defínelos aquí:
        variables_chs = get_variables_chs() if 'get_variables_chs' in globals() else {"H": 90, "S": 97, "C":80}
        prompt_history_text = get_prompt_history_text() if 'get_prompt_history_text' in globals() else ""
        ans = user_message
        perfil_usuario = memoria_social.obtener_perfil(nombre_usuario)
        # Paso 2: Actualizar las variables BHL y de sombra basándose en la interacción
        # Aquí puedes implementar una lógica para modificar los valores BHL,
        # por ejemplo, basándote en el contenido del mensaje del usuario.
        # Por ahora, simularemos un cambio.
        bhl_values['b'] += 1
        bhl_values['h'] -= 1
        bhl_values['l'] += 0.5

        # Aseguramos que los valores se mantengan dentro de un rango
        for key in bhl_values:
            if isinstance(bhl_values[key], (int, float)):
                bhl_values[key] = max(0, min(20, bhl_values[key]))
        
        # Actualizamos las variables de sombra, deseo y ego
        update_shadow_desire_and_ego(bhl_values, shadow_values)
        
        # Calculamos el Numeraso
        numeraso = get_numeraso(bhl_values, per)
        
        # Paso 3: Actualizar la memoria social
        memoria_social.agregar_o_actualizar_usuario(nombre_usuario, bhl_values)  
        # Calcula los porcentajes aquí
        porcentajes = calcular_porcentajes(bhl_values)
        porB = porcentajes['B']
        porH = porcentajes['H']
        porL = porcentajes['L']
        porS = porcentajes['S']
        porE = porcentajes['E']
        porI = porcentajes['I']
        porEgo = porcentajes['Ego']      
        # Paso 4: Construir el prompt para Gemini
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
            f"Tu recuerdo de '{nombre_usuario}' es: {perfil_usuario}. \n"
        )


        # Paso 5: Llamar a la API de Gemini
        payload = {"contents": [{"parts": [{"text": prompt_para_ia}]}]}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()

        gemini_response = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No se pudo obtener una respuesta.')

        # Paso 6: Devolver la respuesta y los nuevos valores BHL
        return jsonify({
            "response": gemini_response,
            "bhl_values": bhl_values
        })

    except requests.exceptions.RequestException as e:
        print(f"Error al llamar a la API de Gemini: {e}")
        return jsonify({"error": "Error al comunicarse con el servicio de IA."}), 500
    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": "Ha ocurrido un error inesperado."}), 500

if __name__ == '__main__':
    # Este comando ejecutará el servidor Flask.
    # El servidor automáticamente sirve el HTML y responde a las peticiones del chat.
    app.run(host="0.0.0.0", port=5000)
    # Ejecutamos la función de cifrado/decodificación
    #from Critographnium import critographium