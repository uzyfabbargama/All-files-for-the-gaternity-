from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MiApp(App):
    def build(self):
        # Crear un layout para organizar los widgets
        layout = BoxLayout(orientation='vertical')
        
        # Crear una instancia del botón
        mi_boton = Button(text='Haz clic')
        
        # Añadir el botón al layout
        layout.add_widget(mi_boton)
        
        return layout

if __name__ == '__main__':
    MiApp().run()