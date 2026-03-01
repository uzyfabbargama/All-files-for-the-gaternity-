import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
import BHL as BHL

# Establecer la versión mínima de Kivy
kivy.require('2.0.0')

class SetupScreen(Screen):
    """Pantalla para definir la personalidad del personaje."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        main_layout.add_widget(Label(text="Define la Personalidad", font_size=24, size_hint_y=0.1))
        
        # Escenario
        main_layout.add_widget(Label(text="Describe el escenario:", size_hint_y=0.05))
        self.scenario_input = TextInput(hint_text="Un mundo post-apocalíptico...", multiline=False, size_hint_y=0.05)
        main_layout.add_widget(self.scenario_input)
        
        # Sliders para las variables de BHL
        main_layout.add_widget(Label(text="Bondad:", size_hint_y=0.05))
        self.bondad_slider = Slider(min=1, max=100, value=50, step=1)
        main_layout.add_widget(self.bondad_slider)
        
        main_layout.add_widget(Label(text="Hostilidad:", size_hint_y=0.05))
        self.hostilidad_slider = Slider(min=1, max=100, value=50, step=1)
        main_layout.add_widget(self.hostilidad_slider)
        
        main_layout.add_widget(Label(text="Lógica:", size_hint_y=0.05))
        self.logica_slider = Slider(min=1, max=100, value=50, step=1)
        main_layout.add_widget(self.logica_slider)
        
        start_button = Button(text="Iniciar Conversación", size_hint_y=0.1, on_press=self.start_chat)
        main_layout.add_widget(start_button)
        
        self.add_widget(main_layout)

    def start_chat(self, instance):
        """Inicializa el juego y cambia a la pantalla de chat."""
        scenario = self.scenario_input.text
        bondad = int(self.bondad_slider.value)
        hostilidad = int(self.hostilidad_slider.value)
        logica = int(self.logica_slider.value)
        
        if not scenario:
            instance.parent.parent.manager.get_screen('popup_screen').show_popup("Error", "Por favor, describe un escenario.")
            return

        BHL.initialize_game(scenario, bondad, hostilidad, logica)
        self.manager.current = 'chat_screen'

class ChatScreen(Screen):
    """Pantalla del chat con el personaje."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Área del chat
        self.chat_history_widget = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.chat_history_widget.bind(minimum_height=self.chat_history_widget.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.chat_history_widget)
        main_layout.add_widget(scroll_view)
        
        # Campo de entrada y botón
        input_layout = BoxLayout(size_hint_y=0.2)
        self.user_input = TextInput(hint_text="Escribe tu mensaje aquí...", multiline=False, size_hint_x=0.8)
        send_button = Button(text="Enviar", size_hint_x=0.2, on_press=self.send_message)
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_button)
        main_layout.add_widget(input_layout)
        
        self.add_widget(main_layout)

    def on_enter(self):
        """Se llama cuando la pantalla se vuelve activa."""
        self.add_message("Personaje", "¡Hola! ¿Cómo te sientes hoy?")

    def add_message(self, sender, message):
        """Añade un mensaje al historial del chat."""
        self.chat_history_widget.add_widget(Label(text=f"{sender}: {message}", size_hint_y=None, height=30))
        
    def send_message(self, instance):
        """Procesa el mensaje del usuario y obtiene la respuesta del personaje."""
        user_message = self.user_input.text
        if not user_message:
            return
        
        self.add_message("Tú", user_message)
        self.user_input.text = ""
        
        try:
            response = BHL.process_user_message(user_message)
            self.add_message("Personaje", response)
        except Exception as e:
            self.add_message("Sistema", f"Error: {e}")

class PopupScreen(Screen):
    def show_popup(self, title, message):
        popup = kivy.uix.popup.Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

class BHLApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name='setup_screen'))
        sm.add_widget(ChatScreen(name='chat_screen'))
        sm.add_widget(PopupScreen(name='popup_screen'))
        return sm

if __name__ == '__main__':
    BHLApp().run()
