import math
import random

class Vortex:
    def __init__(self, energy_loss_rate, global_velocity, min_velocity, avg_velocity, roughness):
        """
        Inicializa un vórtice con los parámetros de tu modelo.
        """
        self.energy_loss_rate = energy_loss_rate  # 1. Pérdida de energía en el tiempo
        self.global_velocity = global_velocity    # 2. Velocidad global
        self.min_velocity = min_velocity          # 3. Velocidad mínima (lentitud máxima)
        self.avg_velocity = avg_velocity          # 4. Promedio de velocidades
        self.roughness = roughness                # 5. Nivel de lisidad (0 = liso, 1 = muy rugoso)
        self.energy = 1000.0                      # Energía inicial (se puede ajustar)
        self.time = 0.0                           # Tiempo de vida del vórtice
        
    def update(self, dt=0.1):
        """
        Actualiza el vórtice en el tiempo.
        """
        # 6. Calcular la vida útil del vórtice
        if self.global_velocity > self.min_velocity:
            life_span = self.energy_loss_rate / (self.global_velocity - self.min_velocity)
        else:
            life_span = 0  # El vórtice se disipa
        
        # Calcular la amplitud del vórtice
        if self.avg_velocity > 0 and self.roughness > 0:
            amplitude = self.energy / (self.avg_velocity * self.roughness)
        else:
            amplitude = 0
        
        # Actualizar el tiempo y la energía
        self.time += dt
        self.energy -= self.energy_loss_rate * dt  # La energía se pierde con el tiempo
        
        # Si la energía es demasiado baja, el vórtice colapsa
        if self.energy <= 0:
            self.energy = 0
            self.global_velocity = 0
            amplitude = 0
            life_span = 0
        
        return {
            "time": self.time,
            "energy": self.energy,
            "life_span": life_span,
            "amplitude": amplitude,
            "active": self.energy > 0 and self.global_velocity > self.min_velocity
        }

# ------------------- SIMULACIÓN -------------------
def simulate_vortex(steps=100, dt=0.1):
    # Crear un vórtice con parámetros arbitrarios
    vortex = Vortex(
        energy_loss_rate=2.0,    # Pérdida de energía por segundo
        global_velocity=10.0,    # Velocidad global (m/s)
        min_velocity=1.0,        # Velocidad mínima
        avg_velocity=5.0,        # Velocidad promedio
        roughness=0.3            # Superficie moderadamente lisa
    )
    
    # Simular
    for _ in range(steps):
        state = vortex.update(dt)
        print(f"Tiempo: {state['time']:.2f}s | "
              f"Energía: {state['energy']:.2f} | "
              f"Vida útil: {state['life_span']:.2f}s | "
              f"Amplitud: {state['amplitude']:.2f}m | "
              f"Activo: {state['active']}")
        
        if not state['active']:
            print("El vórtice se ha disipado.")
            break

# Ejecutar
simulate_vortex()
