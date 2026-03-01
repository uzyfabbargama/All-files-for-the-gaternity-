# main.py
import math
import random
import requests
import os
import json
import time
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.clock import mainthread

# Clave de API, se recomienda usar variables de entorno
API_KEY = "AIzaSyBa6T3dKbfNA_SxI_dj5Ymk7fB6gk8i3zM"

# Nombre del archivo donde se guardará y cargará el estado
SAVE_FILE = "bhl_session_data.json"

# Variables globales para el estado del personaje
Numero = 0
expB, expH, expL = 0, 0, 0
Numero1 = 0
expS, expHu, expC = 0, 0, 0
chat_history = []
Nivel_incomodidad = 0
Escenario = "Un espacio en blanco."

def save_state():
    """Guarda el estado actual del personaje y la conversación en un archivo JSON."""
    global Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history
    data = {
        "bhl_values": Numero,
        "Exp_B": expB,
        "Exp_H": expH,
        "Exp_L": expL,
        "chs_values": Numero1,
        "Exp_S": expS,
        "Exp_Hu": expHu,
        "Exp_C": expC,
        "chat_history": chat_history,
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n--- Estado del personaje guardado en '{SAVE_FILE}' ---")

def load_state():
    """Carga el estado del personaje y la conversación desde un archivo JSON."""
    global Numero, expB, expH, expL, Numero1, expS, expHu, expC, chat_history
    if not os.path.exists(SAVE_FILE):
        return None
    
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    print(f"\n--- Estado del personaje cargado desde '{SAVE_FILE}' ---")
    
    Numero = data["bhl_values"]
    expB = data["Exp_B"]
    expH = data["Exp_H"]
    expL = data["Exp_L"]
    Numero1 = data["chs_values"]
    expS = data["Exp_S"]
    expHu = data["Exp_Hu"]
    expC = data["Exp_C"]
    chat_history = data["chat_history"]

    return data

# Lógica del Numeraso (mismo código que proporcionaste)
def Numeraso(a, b, c): 
    Bondad = a 
    Hostilidad = b 
    Lógica = c 
    Numero_generado = Bondad*(10**(3*2)) + Hostilidad*(10**3) + Lógica + 9*10**8 + 9*10**5 + 9*10**2 
    return Numero_generado

def Numeraso_update(a, b, c):        
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

def Numeraso2(a, b, c):
    C = a
    H = b
    S = c
    Numero_de_necesidad = C * 10**(3 * 2) + H * 10**3 + S
    Numero_de_necesidad += 9 * 10**8 + 9 * 10**5 + 9 * 10**2
    return Numero_de_necesidad

def Numeraso2_update(a, b, c):
    Numero_de_necesidad = Numeraso2(a, b, c)
    C4 = (Numero_de_necesidad // 10**8) % 10
    C5 = (Numero_de_necesidad // 10**5) % 10
    C6 = (Numero_de_necesidad // 10**2) % 10
    caso = C4 + C5 + C6
    expS = 0
    expHu = 0
    expC = 0
    while caso != 27:
        D4 = 9 - C4
        D5 = 9 - C5
        D6 = 9 - C6
        expS += D4 % 2 
        expHu += D5 % 2
        expC += D6 % 2
        Numero_de_necesidad += (D4 % 2)
        Numero_de_necesidad -= (D4 % 2) * (10**3)
        Numero_de_necesidad -= (D5 % 2)
        Numero_de_necesidad -= (D6 % 2) * (10**(3 * 2))
        C4 = (Numero_de_necesidad // 10**8) % 10
        C5 = (Numero_de_necesidad // 10**5) % 10
        C6 = (Numero_de_necesidad // 10**2) % 10
        caso = C4 + C5 + C6
        Numero_de_necesidad += 1 * 10**3
    return Numero_de_necesidad, expS, expHu, expC

def get_prompt_history_text():
    return "\n".join([f"Usuario: {msg['user']}\nIA: {msg['character']}" for msg in chat_history])

class BHLApp(App):
    def build(self):
        # Cargar la interfaz desde el archivo KV
        return Builder.load_file('chat_interface.kv')

    def on_start(self):
        # Cargar el estado al iniciar la app
        self.load_initial_state()

    def load_initial_state(self):
        # Lógica para cargar el estado inicial
        global Numero, expB, expH, expL, Numero1, expS, expHu, expC, Escenario
        data = load_state()
        if data:
            self.root.ids.chat_history.add_widget(Label(text="--- Estado de la sesión cargado ---", size_hint_y=None, height=40, markup=True))
        else:
            self.root.ids.chat_history.add_widget(Label(text="--- Sesión nueva ---", size_hint_y=None, height=40, markup=True))
            # Valores iniciales si no hay estado guardado
            try:
                a_init = 50
                b_init = 50
                c_init = 50
                baño_init = 50
                hambre_init = 50
                sueño_init = 50
                Numero, expB, expH, expL = Numeraso_update(a_init, b_init, c_init)
                Numero1, expS, expHu, expC = Numeraso2_update(baño_init, hambre_init, sueño_init)
                self.root.ids.chat_history.add_widget(Label(text="Define el escenario:", size_hint_y=None, height=40, halign='left', text_size=(self.root.ids.chat_history.width, None)))
                self.root.ids.user_input.hint_text = "Describe el escenario..."
                self.root.ids.send_button.on_press = self.set_scenario
            except Exception as e:
                print(f"Error en la carga inicial: {e}")
                self.root.ids.chat_history.add_widget(Label(text=f"Error al iniciar: {e}", size_hint_y=None, height=40, markup=True))

    def set_scenario(self):
        global Escenario
        input_text = self.root.ids.user_input.text.strip()
        if input_text:
            Escenario = input_text
            self.root.ids.chat_history.add_widget(Label(text=f"[b]Tu[/b]: {input_text}", size_hint_y=None, height=40, halign='right', text_size=(self.root.ids.chat_history.width, None), markup=True))
            self.root.ids.chat_history.add_widget(Label(text=f"[b]Narrador[/b]: El escenario ha sido establecido como: '{Escenario}'. ¡Puedes iniciar la conversación!", size_hint_y=None, height=40, halign='left', text_size=(self.root.ids.chat_history.width, None), markup=True))
            self.root.ids.user_input.text = ""
            self.root.ids.user_input.hint_text = "Escribe un mensaje..."
            self.root.ids.send_button.on_press = self.send_message
            self.root.ids.chat_history.add_widget(Label(text="--- La conversación ha iniciado ---", size_hint_y=None, height=40, markup=True))

    def send_message(self):
        user_message = self.root.ids.user_input.text.strip()
        if not user_message:
            return

        self.root.ids.user_input.text = ""
        self.root.ids.chat_history.add_widget(Label(text=f"[b]Tú[/b]: {user_message}", size_hint_y=None, height=40, halign='left', text_size=(self.root.ids.chat_history.width, None), markup=True))

        # Deshabilitar el botón de envío y el campo de texto
        self.root.ids.send_button.disabled = True
        self.root.ids.user_input.disabled = True
        self.root.ids.user_input.hint_text = "Generando respuesta..."

        # Ejecutar la lógica de la IA en un hilo separado para no congelar la UI
        threading.Thread(target=self.generate_response_in_thread, args=(user_message,)).start()
    
    @mainthread
    def update_ui_after_response(self, character_response):
        # Habilitar el botón de envío y el campo de texto
        self.root.ids.send_button.disabled = False
        self.root.ids.user_input.disabled = False
        self.root.ids.user_input.hint_text = "Escribe un mensaje..."
        
        # Añadir la respuesta del personaje al chat
        self.root.ids.chat_history.add_widget(Label(text=f"[b]Personaje[/b]: {character_response}", size_hint_y=None, height=40, halign='right', text_size=(self.root.ids.chat_history.width, None), markup=True))
        
        # Scroll al final del historial
        self.root.ids.chat_scroll.scroll_to(self.root.ids.chat_history.children[0])


    def generate_response_in_thread(self, user_message):
        global Numero, expB, expH, expL, Numero1, expS, expHu, expC, Nivel_incomodidad, Escenario, chat_history
        
        # Lógica de evaluación del usuario
        try:
            url_eval = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
            headers = { 'Content-Type': 'application/json' }
            eval_prompt = (
                f"Analiza la siguiente frase del usuario: '{user_message}' "
                f"Devuelve un JSON con calificaciones del 0 al 20 para: bondad, hostilidad y lógica. "
                f"Y del 0 al 100 para: hambre, ir_al_baño, sueño e incomodidad."
            )
            payload = {
                "contents": [ { "parts": [ { "text": eval_prompt } ] } ],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "responseSchema": {
                        "type": "OBJECT",
                        "properties": {
                            "bondad": {"type": "NUMBER"},
                            "hostilidad": {"type": "NUMBER"},
                            "logica": {"type": "NUMBER"},
                            "hambre": {"type": "NUMBER"},
                            "ir_al_baño": {"type": "NUMBER"},
                            "sueño": {"type": "NUMBER"},
                            "incomodidad": {"type": "NUMBER"}
                        }
                    }
                }
            }
            response = requests.post(url_eval, headers=headers, json=payload)
            response.raise_for_status()
            eval_data = json.loads(response.json()['candidates'][0]['content']['parts'][0]['text'])
            
            # Actualiza las variables con los datos de la IA
            Numero += eval_data.get('bondad', 0) * (10**(3*2)) + expB
            Numero += eval_data.get('hostilidad', 0) * (10**3) + expH
            Numero += eval_data.get('logica', 0) + expL
            
            Numero1 += eval_data.get('ir_al_baño', 0) * (10**(3*2)) - expC
            Numero1 += eval_data.get('hambre', 0) * (10**3) - expHu
            Numero1 += eval_data.get('sueño', 0) - expS
            
            Necesidad_C = (Numero1 // 10**(3*2)%100)
            Necesidad_H = (Numero1 // 10**3) % 100 
            Necesidad_S = Numero1 % 100
            
            Numero -= (Necesidad_C // 10)*10**(3*2)%100 + (Necesidad_H // 10)*10**(3*2)%100 + (Necesidad_S // 10)*10**(3*2)%100 
            Numero += (Necesidad_C // 10)*10**(3)%100 + (Necesidad_H // 10)*10**(3)%100 + (Necesidad_S // 10)*10**(3)%100
            Numero -= ((Necesidad_C // 10)%100)*2 + ((Necesidad_H // 10)%100)*2 + ((Necesidad_S // 10)%100)*2
            Nivel_incomodidad = eval_data.get('incomodidad', 0)
        
        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
            print(f"Error en la evaluación de la API: {e}")
            return # Salir del hilo si hay un error
            
        # Lógica de actualización de escenario
        try:
            url_escenario = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
            data_escenario = { "contents": [ { "parts": [ { "text": f"Eres un narrador. Describe el nuevo escenario en una sola frase concisa. Escenario actual: '{Escenario}' Mensaje: '{user_message}'" } ] } ] }
            response_escenario = requests.post(url_escenario, headers=headers, json=data_escenario)
            response_escenario.raise_for_status()
            Escenario = response_escenario.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            # Actualizar la UI del escenario
            self.root.ids.scenario_label.text = f"Escenario: {Escenario}"
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar el escenario: {e}")
            
        # Generar respuesta del personaje
        try:
            Bondad_actual = max(1, Numero // (10**(3*2)) %100)
            Hostilidad_actual = max(1,Numero // (10**3) % 100)
            Lógica_actual = max(1,Numero % (100))
            Cagar_actual = max(1,Numero1 // 10**(3*2)) %100
            Hambre_actual = max(1,Numero1 // 10**3 % 100)
            Sueño_actual = max(1,Numero1 % 10)
            
            cosiente = Bondad_actual + Hostilidad_actual + Lógica_actual
            porB = (Bondad_actual * 100) / cosiente
            porH = (Hostilidad_actual * 100) / cosiente
            porL = (Lógica_actual * 100) / cosiente
            Sombra_B = 100 - Bondad_actual
            Sombra_H = 100 - Hostilidad_actual
            Sombra_L = 100 - Lógica_actual
            Deseo_H = Sombra_H / Hostilidad_actual
            Deseo_B = Sombra_B / Bondad_actual
            Deseo_L = Sombra_L / Lógica_actual
            
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
                f"Usuario: '{user_message}'\n\n"
                f"Tu respuesta es la de tu personaje."
                f"Para empezar, toma de punto de partida la descripción de este escenario {Escenario}"
                f"Si tienes un valor de experiencia de evacuación: {expC}, experiencia de sueño {expS}, y Experiencia de hambre {expHu} altas (mayor o cercano a 100) tendrás patologías crónicas"
                f"Experiencia de sueño: problemas para dormir"
                f"Experiencia de evacuación: problemas gastrointestinales, problemas para ir al baño"
                f"Experiencia de hambre: Problemas de obesidad, relacionados con el apetito, como que la comida no te satisface"
            )
            
            url_ia_response = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
            data = { "contents": [ { "parts": [ { "text": prompt_para_ia } ] } ] }
            response = requests.post(url_ia_response, headers=headers, json=data)
            response.raise_for_status()
            respuesta_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
            
            chat_history.append({"user": user_message, "character": respuesta_ia})
            
            self.update_ui_after_response(respuesta_ia)
            
        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
            self.update_ui_after_response(f"Error al generar la respuesta: {e}")

if __name__ == '__main__':
    BHLApp().run()
