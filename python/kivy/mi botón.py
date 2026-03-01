from kivy.app import App
from kivy.uix.button import Button

class mibotón(App):
    
    def build(self):
        
        return Button(text='Entrar', background_color=(0.155,0.45,0.31,0.75))


mibotón().run()