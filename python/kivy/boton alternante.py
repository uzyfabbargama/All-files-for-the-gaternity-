from functools import partial
from kivy.app import App
from kivy.uix.button import Button

class mibotón(App):
    
    def disbale(self, instance, *args):
        instance.disabled = True
    
    def update(self,instance, *args):
        instance.text = "Estoy deshabilitado"
            
    def build(self):
        
        mybtn = Button(Text="Haga click para desactivar")
        mybtn.bind(on_press = partial(self.disable, mybtn))
        mybtn.bind(on_press = partial(self.update, mybtn))
        
        return mybtn


mibotón().run()