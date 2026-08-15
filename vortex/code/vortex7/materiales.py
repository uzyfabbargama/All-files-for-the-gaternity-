# materiales.py
from atomas7 import generar_todos_los_atomos, propiedades_completas

class Material:
    def __init__(self, simbolo, capas, I, O, Z=0):
        self.simbolo = simbolo
        self.atomo = {
            'nombre': simbolo,
            'capas': capas,
            'palitos_I': I,
            'palitos_O': O,
            'Z': Z
        }
        self.propiedades = propiedades_completas(self.atomo)
    
    def conductividad(self):
        return self.propiedades['conductividad']
    
    def magnetismo(self):
        return self.propiedades['fuerza_magnetica']
    
    def punto_fusion(self):
        return self.propiedades['punto_fusion']
