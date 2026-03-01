import kivy
from kivy.app import App
from kivy.uix.label import Label


class saludo(App):

    def build(self):
        
        return Label(text="Hola mundo")
    

saludo().run()