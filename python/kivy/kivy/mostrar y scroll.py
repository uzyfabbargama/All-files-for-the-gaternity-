from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.core.window import Window

class DisplayApp(App):
    def build(self):
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        self.text_input = TextInput(
            hint_text='Introduce tu texto aquí',
            size_hint_y=None,
            height=30,
            multiline=False
        )
        
        update_button = Button(
            text='Mostrar texto',
            size_hint_y=None,
            height=40,
        )
        update_button.bind(on_press=self.update_display)
        
        self.scroll_view = ScrollView()
        
        self.text_label = Label(
            text='',
            size_hint_y=None,
            padding=[10, 10],
            valign='top'
        )

        # 1. SOLUCIÓN: Usar una función lambda para enlazar solo el alto.
        #    La función lambda 'instance, value' recibe el widget y la tupla de tamaño.
        #    Luego, actualiza la altura con el segundo elemento de la tupla (el alto).
        self.text_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        self.scroll_view.add_widget(self.text_label)
        
        root_layout.add_widget(self.text_input)
        root_layout.add_widget(update_button)
        root_layout.add_widget(self.scroll_view)

        return root_layout

    def update_display(self, instance):
        entered_text = self.text_input.text
        self.text_label.text = entered_text
        self.text_input.text = ''

if __name__ == '__main__':
    DisplayApp().run()