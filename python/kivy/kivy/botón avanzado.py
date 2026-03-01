from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MiApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        
        # Botón con color y tamaño personalizados
        mi_boton = Button(
            text='Botón Personalizado',
            size_hint=(0.5, 0.3),  # 50% de ancho, 30% de alto
            background_color=(0.2, 0.7, 0.9, 1), # Azul claro
            pos_hint={'center_x': 0.5}  # Centrado horizontalmente
        )
        
        layout.add_widget(mi_boton)
        
        return layout

if __name__ == '__main__':
    MiApp().run()