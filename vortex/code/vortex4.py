import math
import random

class Vortex4:
    def __init__(self, energy, velocity, pressure, roughness, radius=1.0):
        self.energy = energy
        self.velocity = velocity
        self.pressure = pressure
        self.roughness = roughness
        self.radius = radius
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(-10, 10)
        self.time = 0.0
        self.dissipation_factor = 0.01  # Factor de disipación de energía
    
    def update(self, dt=0.1):
        # 1. Pérdida de energía exponencial
        self.energy *= math.exp(-self.dissipation_factor * dt)
        
        # 2. Vida útil basada en energía y presión
        if self.pressure > 0:
            life_span = self.energy / (self.pressure * self.roughness)
        else:
            life_span = 0
        
        # 3. Amplitud basada en energía y velocidad
        amplitude = self.energy / (self.velocity * self.roughness)
        
        # 4. El radio crece con la energía
        self.radius = amplitude / 2
        
        self.time += dt
        
        return {
            "time": self.time,
            "energy": self.energy,
            "life_span": life_span,
            "amplitude": amplitude,
            "radius": self.radius,
            "active": self.energy > 0 and self.velocity > 0
        }
    
    def move(self, pressure_gradient, wind_direction, dt=0.1):
        # Movimiento basado en gradiente de presión y viento
        # Los tornados se mueven hacia la presión más baja
        self.x += pressure_gradient[0] * dt * 0.5
        self.y += pressure_gradient[1] * dt * 0.5
        
        # El viento afecta la trayectoria (con un ángulo de desviación)
        wind_angle = math.atan2(wind_direction[1], wind_direction[0])
        self.x += math.cos(wind_angle) * dt * 0.2
        self.y += math.sin(wind_angle) * dt * 0.2
    
    def interact(self, other_vortex, dt=0.1):
        # Interacción entre vórtices (atracción y fusión)
        dx = self.x - other_vortex.x
        dy = self.y - other_vortex.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Si están cerca, se atraen (como en la realidad)
        if distance < self.radius + other_vortex.radius:
            # El más grande absorbe al más pequeño
            if self.energy > other_vortex.energy:
                self.energy += other_vortex.energy * 0.1
                other_vortex.energy *= 0.9
            else:
                other_vortex.energy += self.energy * 0.1
                self.energy *= 0.9

# ------------------- SIMULACIÓN VORTEX 4.0 -------------------
def simulate_vortex4(steps=100, dt=0.1):
    # Crear dos vórtices más realistas
    v1 = Vortex4(energy=1000.0, velocity=10.0, pressure=0.5, roughness=0.3, radius=10.0)
    v2 = Vortex4(energy=800.0, velocity=8.0, pressure=0.4, roughness=0.2, radius=8.0)
    v1.x, v1.y = -5.0, 0.0
    v2.x, v2.y = 5.0, 0.0
    
    # Gradiente de presión y viento
    pressure_gradient = (-0.1, 0.0)  # La presión baja hacia la izquierda
    wind_direction = (1.0, 0.5)      # Viento hacia la derecha y arriba
    
    for step in range(steps):
        # Actualizar cada vórtice
        state1 = v1.update(dt)
        state2 = v2.update(dt)
        
        # Interacción entre vórtices (atracción y fusión)
        v1.interact(v2, dt)
        
        # Movimiento basado en presión y viento
        v1.move(pressure_gradient, wind_direction, dt)
        v2.move(pressure_gradient, wind_direction, dt)
        
        # Mostrar estado
        print(f"Paso {step+1}:")
        print(f"  V1: Energía={state1['energy']:.2f}, Amplitud={state1['amplitude']:.2f}m, Radio={state1['radius']:.2f}m")
        print(f"  V2: Energía={state2['energy']:.2f}, Amplitud={state2['amplitude']:.2f}m, Radio={state2['radius']:.2f}m")
        print(f"  Distancia: {math.sqrt((v1.x-v2.x)**2 + (v1.y-v2.y)**2):.2f}")
        print(f"  V1 posición: ({v1.x:.2f}, {v1.y:.2f})")
        print(f"  V2 posición: ({v2.x:.2f}, {v2.y:.2f})")
        print("---")
        
        if not state1['active'] and not state2['active']:
            print("Ambos vórtices se han disipado.")
            break

# Ejecutar
simulate_vortex4()
