# bhl_app.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty

import BHL # This is how you import your script

class StartupScreen(Screen):
    scenario_input = ObjectProperty(None)
    bondad_slider = ObjectProperty(None)
    hostilidad_slider = ObjectProperty(None)
    logica_slider = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(StartupScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        main_layout.add_widget(Label(text="Define el Escenario y la Personalidad", font_size='20sp', size_hint_y=0.1))

        # Escenario Input
        main_layout.add_widget(Label(text="Describe el escenario:", size_hint_y=0.05))
        self.scenario_input = TextInput(multiline=False, size_hint_y=0.1)
        main_layout.add_widget(self.scenario_input)

        # Sliders for BHL values
        main_layout.add_widget(Label(text="Bondad:", size_hint_y=0.05))
        self.bondad_slider = Slider(min=0, max=100, value=50, size_hint_y=0.1)
        self.bondad_label = Label(text=str(int(self.bondad_slider.value)), size_hint_y=0.05)
        self.bondad_slider.bind(value=lambda instance, value: self.bondad_label.setter('text')(instance, str(int(value))))
        main_layout.add_widget(self.bondad_slider)
        main_layout.add_widget(self.bondad_label)

        main_layout.add_widget(Label(text="Hostilidad:", size_hint_y=0.05))
        self.hostilidad_slider = Slider(min=0, max=100, value=50, size_hint_y=0.1)
        self.hostilidad_label = Label(text=str(int(self.hostilidad_slider.value)), size_hint_y=0.05)
        self.hostilidad_slider.bind(value=lambda instance, value: self.hostilidad_label.setter('text')(instance, str(int(value))))
        main_layout.add_widget(self.hostilidad_slider)
        main_layout.add_widget(self.hostilidad_label)
        
        main_layout.add_widget(Label(text="Lógica:", size_hint_y=0.05))
        self.logica_slider = Slider(min=0, max=100, value=50, size_hint_y=0.1)
        self.logica_label = Label(text=str(int(self.logica_slider.value)), size_hint_y=0.05)
        self.logica_slider.bind(value=lambda instance, value: self.logica_label.setter('text')(instance, str(int(value))))
        main_layout.add_widget(self.logica_slider)
        main_layout.add_widget(self.logica_label)

        # Start Button
        start_button = Button(text="Iniciar Conversación", size_hint_y=0.1)
        start_button.bind(on_press=self.start_conversation)
        main_layout.add_widget(start_button)

        self.add_widget(main_layout)

    def start_conversation(self, instance):
        # Pass the values to the chat screen
        self.manager.get_screen('chat').start_game(
            self.scenario_input.text,
            int(self.bondad_slider.value),
            int(self.hostilidad_slider.value),
            int(self.logica_slider.value)
        )
        self.manager.current = 'chat'

class ChatScreen(Screen):
    history_label = ObjectProperty(None)
    user_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Scrollable area for conversation history
        self.history_label = Label(text="", size_hint_y=None, halign='left', valign='top', markup=True)
        self.history_label.bind(texture_size=self.history_label.setter('size'))
        scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)
        scroll_view.add_widget(self.history_label)

        # Input and button layout
        input_layout = BoxLayout(size_hint_y=0.1)
        self.user_input = TextInput(hint_text="Escriba un mensaje...", multiline=False, size_hint_x=0.8)
        self.send_button = Button(text="Enviar", size_hint_x=0.2)
        self.send_button.bind(on_press=self.send_message)
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(self.send_button)
        
        # Save button
        self.save_button = Button(text="Guardar", size_hint_y=0.1)
        self.save_button.bind(on_press=self.save_state)
        
        # Add all widgets to the main layout
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(self.save_button)
        
        self.add_widget(main_layout)

    def start_game(self, scenario, bondad, hostilidad, logica):
        # Here you would initialize the values in your BHL.py script
        # BHL.Escenario = scenario
        # BHL.a = bondad
        # BHL.b = hostilidad
        # BHL.c = logica
        # BHL.initialize_game() # You need to create this function
        
        # For this example, we'll just update the display
        self.history_label.text = f"[b]Escenario:[/b] {scenario}\n[b]Personalidad Inicial:[/b] Bondad={bondad}, Hostilidad={hostilidad}, Lógica={logica}\n\n"
    
    def send_message(self, instance):
        user_message = self.user_input.text
        if user_message:
            # Here you'll call a function in BHL.py to process the message
            # For this example, we'll just simulate a response
            response_from_ai = f"Personaje: Su mensaje '{user_message}' ha sido procesado."
            
            # This is a placeholder for your BHL.py logic
            # response_from_ai = BHL.process_message(user_message)
            
            # Append the new messages to the history
            self.history_label.text += f"[b]Usuario:[/b] {user_message}\n[b]Personaje:[/b] {response_from_ai}\n\n"
            
            self.user_input.text = "" # Clear the input box

    def save_state(self, instance):
        # This will call your save_state function from BHL.py
        # BHL.save_state(...)
        print("Estado guardado.")


class BHLApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartupScreen(name='startup'))
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    BHLApp().run()
