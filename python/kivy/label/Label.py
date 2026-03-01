from kivy.app import App
from kivy.uix.button import Label

class KivyLabel(App):
    
    def build(self):
        
        return Label (text='[u][color=ff0066][b]Bienvenidos[/b][/color] a [i][color=ff9933] BHLServer[/i] Suscríbete [/color][/u]', markup=True)
    
KivyLabel().run()