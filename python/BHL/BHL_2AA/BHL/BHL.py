import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import math
import random
import requests
import os
import json

# Establecer la versión mínima de Kivy
kivy.require('2.0.0')

# --- Variables y lógica de BHL (Integrada) ---
PosX = 1
PosC = 100
PosY = 200
PosC1 = 20000
PosZ = 40000
PosC2 = 4000000
PorX = 1
PorC = 100
PorY = 200
PorC1 = 20000
PorZ = 40000
PorC2 = 4000000
SAVE_FILE = "bhl_session_data.json"

# Variables globales para el estado del personaje
Escenario = ""
chat_history = []
Nivel_incomodidad = 0
a, b, c = 50, 50, 50  # Valores iniciales por defecto
baño, hambre, sueño = 50, 50, 50
expB, expH, expL = 0, 0, 0
expS, expHu, expC = 0, 0, 0

def get_prompt_history_text():
    # Devuelve el historial como texto formateado
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])

def save_state():
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    data = {
        "escenario": Escenario,
        "a": a,
        "b": b,
        "c": c,
        "baño": baño,
        "hambre": hambre,
        "sueño": sueño,
        "expB": expB,
        "expH": expH,
        "expL": expL,
        "expS": expS,
        "expHu": expHu,
        "expC": expC,
        "chat_history": chat_history,
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    global Escenario, a, b, c, baño, hambre, sueño, expB, expH, expL, expS, expHu, expC, chat_history
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            Escenario = data.get("escenario", "")
            a = data.get("a", 50)
            b = data.get("b", 50)
            c = data.get("c", 50)
            baño = data.get("baño", 50)
            hambre = data.get("hambre", 50)
            sueño = data.get("sueño", 50)
            expB = data.get("expB", 0)
            expH = data.get("expH", 0)
            expL = data.get("expL", 0)
            expS = data.get("expS", 0)
            expHu = data.get("expHu", 0)
            expC = data.get("expC", 0)
            chat_history = data.get("chat_history", [])

def BHL_logic(Bondad, Hostilidad, Lógica, Incomodidad, Incomodidad_mental, Porcentaje_incomodidad, Porcentaje_incomodidad_mental):
    numero = 0
    incomodidad_total = Incomodidad + Incomodidad_mental
    porcentaje_incomodidad_total = Porcentaje_incomodidad + Porcentaje_incomodidad_mental
    controladorX = 1 if Bondad > 50 else 0
    controladorC = 1 if Hostilidad > 50 else 0
    controladorY = 1 if Lógica > 50 else 0
    controladorC1 = 1 if Incomodidad > 50 else 0
    controladorZ = 1 if Incomodidad_mental > 50 else 0
    controladorC2 = 1 if incomodidad_total > 100 else 0
    numero += controladorX * PorX * Bondad
    numero += controladorC * PorC * Hostilidad
    numero += controladorY * PorY * Lógica
    numero += controladorC1 * PorC1 * Incomodidad
    numero += controladorZ * PorZ * Incomodidad_mental
    numero += controladorC2 * PorC2 * porcentaje_incomodidad_total
    return numero

def CHS_logic(Bano, Hambre, Sueno, expB, expH, expL, expS, expHu, expC):
    global PosX, PosC, PosY, PosC1, PosZ, PosC2, PorX, PorC, PorY, PorC1, PorZ, PorC2
    numero = 0
    controladorX = 1 if Bano > 50 else 0
    controladorC = 1 if Hambre > 50 else 0
    controladorY = 1 if Sueno > 50 else 0
    controladorC1 = 1 if expB > 50 else 0
    controladorZ = 1 if expH > 50 else 0
    controladorC2 = 1 if expL > 50 else 0
    numero += controladorX * PosX * Bano
    numero += controladorC * PosC * Hambre
    numero += controladorY * PosY * Sueno
    numero += controladorC1 * PosC1 * expB
    numero += controladorZ * PosZ * expH
    numero += controladorC2 * PosC2 * expL
    return numero

def process_user_message(message):
    """Procesa el mensaje del usuario, actualiza el estado y genera una respuesta de la IA."""
    global Nivel_incomodidad, a, b, c, baño, hambre, sueño, expB, expH, expL, expS, expHu, expC, chat_history
    if "baño" in message.lower():
        baño += random.randint(1, 10)
    if "comer" in message.lower():
        hambre += random.randint(1, 10)
    if "dormir" in message.lower():
        sueño += random.randint(1, 10)
    baño = min(100, baño)
    hambre = min(100, hambre)
    sueño = min(100, sueño)
    
    Numero = BHL_logic(a, b, c, baño, hambre, sueño, Nivel_incomodidad)
    Numero1 = CHS_logic(baño, hambre, sueño, expB, expH, expL, expS, expHu, expC)
    
    historial_prompt = get_prompt_history_text()
    prompt_para_ia = (
        f"Eres un personaje de un videojuego de rol, y estas son tus características: Bondad: {a}, Hostilidad: {b}, Lógica: {c}. "
        f"Tu estado actual es: necesidad de ir al baño: {baño}, necesidad de comer: {hambre}, necesidad de dormir: {sueño}. "
        f"Tu nivel de experiencia de Bondad es: {expB}, Hostilidad: {expH}, Lógica: {expL}, Sueño: {expS}, Hambre: {expHu}, Evacuación: {expC}. "
        f"Estos valores se pueden interpretar en un solo número: {Numero} y {Numero1}. "
        f"Tu nivel de incomodidad es: {Nivel_incomodidad}. "
        f"A continuación se presenta un historial de conversación, usa este historial como memoria de contexto para responder.\n"
        f"Historial de conversación:\n{historial_prompt}\n\n"
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
        return respuesta_ia
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        return f"Lo siento, tuve un problema al procesar tu solicitud: {e}"

# --- Kivy App (Interfaz de Usuario) ---

class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(Label(text="Define la Personalidad", font_size=24, size_hint_y=0.1))
        main_layout.add_widget(Label(text="Describe el escenario:", size_hint_y=0.05))
        self.scenario_input = TextInput(hint_text="Un mundo post-apocalíptico...", multiline=False, size_hint_y=0.05)
        main_layout.add_widget(self.scenario_input)
        main_layout.add_widget(Label(text="Bondad:", size_hint_y=0.05))
        self.bondad_slider = Slider(min=1, max=100, value=50, step=1)
        self.bondad_label = Label(text=str(int(self.bondad_slider.value)))
        self.bondad_slider.bind(value=lambda instance, value: self.update_label(self.bondad_label, value))
        main_layout.add_widget(self.bondad_label)
        main_layout.add_widget(self.bondad_slider)
        main_layout.add_widget(Label(text="Hostilidad:", size_hint_y=0.05))
        self.hostilidad_slider = Slider(min=1, max=100, value=50, step=1)
        self.hostilidad_label = Label(text=str(int(self.hostilidad_slider.value)))
        self.hostilidad_slider.bind(value=lambda instance, value: self.update_label(self.hostilidad_label, value))
        main_layout.add_widget(self.hostilidad_label)
        main_layout.add_widget(self.hostilidad_slider)
        main_layout.add_widget(Label(text="Lógica:", size_hint_y=0.05))
        self.logica_slider = Slider(min=1, max=100, value=50, step=1)
        self.logica_label = Label(text=str(int(self.logica_slider.value)))
        self.logica_slider.bind(value=lambda instance, value: self.update_label(self.logica_label, value))
        main_layout.add_widget(self.logica_label)
        main_layout.add_widget(self.logica_slider)
        start_button = Button(text="Iniciar Aventura", size_hint_y=0.1)
        start_button.bind(on_release=self.start_adventure)
        main_layout.add_widget(start_button)
        self.add_widget(main_layout)

    def update_label(self, label, value):
        label.text = str(int(value))

    def start_adventure(self, instance):
        global Escenario, a, b, c
        Escenario = self.scenario_input.text or "un mundo post-apocalíptico"
        a = int(self.bondad_slider.value)
        b = int(self.hostilidad_slider.value)
        c = int(self.logica_slider.value)
        self.manager.current = 'chat'
        
class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.chat_history_widget = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.chat_history_widget.bind(minimum_height=self.chat_history_widget.setter('height'))
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.scroll_view.add_widget(self.chat_history_widget)
        self.main_layout.add_widget(self.scroll_view)
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        self.user_input = TextInput(hint_text="Escribe tu mensaje aquí...", multiline=False, size_hint_x=0.8)
        self.user_input.bind(on_text_validate=self.send_message)
        send_button = Button(text="Enviar", size_hint_x=0.2)
        send_button.bind(on_release=self.send_message)
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_button)
        self.main_layout.add_widget(input_layout)
        self.add_widget(self.main_layout)

    def on_enter(self, *args):
        # Cuando la pantalla de chat se vuelve activa, añadimos el primer mensaje.
        self.add_message("Personaje", "¡Hola! ¿Cómo te sientes hoy?")

    def add_message(self, sender, message):
        label_text = f"[b]{sender}:[/b] {message}"
        # Usamos `markup=True` para que el formato de negrita funcione
        label = Label(text=label_text, size_hint_y=None, height=30, markup=True)
        self.chat_history_widget.add_widget(label)
        self.scroll_view.scroll_y = 0  # Aseguramos que el scroll esté en la parte inferior

    def send_message(self, instance):
        user_message = self.user_input.text
        if not user_message:
            return
        
        self.add_message("Tú", user_message)
        self.user_input.text = ""
        
        # Usamos Clock.schedule_once para no bloquear la UI mientras la IA responde
        Clock.schedule_once(lambda dt: self.get_ia_response(user_message), 0.1)

    def get_ia_response(self, user_message):
        try:
            response = process_user_message(user_message)
            self.add_message("Personaje", response)
            save_state()  # Guardamos el estado después de cada interacción
        except Exception as e:
            self.add_message("Sistema", f"Error: {e}")

class BHLApp(App):
    def build(self):
        load_state()  # Cargar el estado al iniciar la aplicación
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm
