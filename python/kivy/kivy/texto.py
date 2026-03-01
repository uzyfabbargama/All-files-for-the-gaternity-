from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label # Opcional: para mostrar el resultado

class MiAppConInput(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # 1. Crear el TextInput
        self.entrada_texto = TextInput(
            text='Escribe algo aquí',
            multiline=False, # Impide que el usuario salte de línea
            size_hint=(1, 0.1), # Ocupa todo el ancho, 10% del alto
            pos_hint={'x': 0, 'y': 0}
        )

        # 2. Crear un botón con colores y tamaño personalizados
        boton_enviar = Button(
            text='Enviar texto',
            background_color=(0.3, 0.8, 0.3, 1), # Verde
            size_hint=(0.1, 0.01), # Ocupa todo el ancho, 15% del alto
            pos_hint={'center_x': 0.9, 'center_y': 0.5}
        )
        
        # 3. Vincular el método al evento 'on_press' del botón
        boton_enviar.bind(on_press=self.obtener_texto)
        
        layout.add_widget(self.entrada_texto)
        layout.add_widget(boton_enviar)
        
        return layout

    def obtener_texto(self, instance):
        # 4. Acceder al texto del TextInput a través de la propiedad `.text`
        texto_ingresado = self.entrada_texto.text
        print(f'Texto recibido: {texto_ingresado}')

if __name__ == '__main__':
    MiAppConInput().run()