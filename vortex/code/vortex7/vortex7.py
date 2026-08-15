# vortex7.py
from vortex6 import Vortex6
from materiales import Material

class TornadoConMaterial(Vortex6):
    def __init__(self, material, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.material = material
        self.campo_magnetico = material.magnetismo() * 0.15  # Tesla
        self.conductividad_termica = material.conductividad() * 0.01  # W/(m·K)
    
    def interaccion_con_material(self, dt=0.1):
        # 1. Efecto magnético: desviar partículas cargadas
        if self.campo_magnetico > 0.5:
            # Fuerza de Lorentz
            self.velocity += self.campo_magnetico * dt * 0.001
        
        # 2. Efecto térmico: disipar calor
        if self.conductividad_termica > 0.5:
            self.energy -= self.conductividad_termica * dt * 0.01
        
        # 3. Efecto Hall: generar voltaje
        if self.campo_magnetico > 0.5 and self.conductividad_termica > 0.5:
            voltaje = self.velocity * self.campo_magnetico * 0.01
            print(f"⚡ Voltaje inducido: {voltaje:.2f} V")
        
        return super().update(dt)
