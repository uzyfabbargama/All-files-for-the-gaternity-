from kivy.app import App

from kivy.uix.button import Button

class miButton(App):
    
    def build(self):
        
        return Button(text = 'Bienvenido', pos = (300, 100), size_hint = (.20, .20))
    
miButton().run()