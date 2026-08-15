import math
import random

class Vortex5:
    def __init__(self, energy, velocity, pressure, roughness, radius, sign=1):
        self.energy = energy              # Energía total
        self.velocity = velocity          # Velocidad tangencial
        self.pressure = pressure          # Presión central
        self.roughness = roughness        # Rugosidad
        self.radius = radius              # Radio del vórtice
        self.sign = sign                  # +1 = giro horario, -1 = antihorario
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(-10, 10)
        self.time = 0.0
        self.dissipation = 0.01           # Tasa de disipación de energía

    def update(self, dt=0.1):
        # Pérdida de energía exponencial
        self.energy *= math.exp(-self.dissipation * dt)
        
        # Amplitud basada en energía y velocidad
        amplitude = self.energy / (self.velocity * self.roughness)
        
        # El radio crece con la amplitud
        self.radius = amplitude / 2
        
        # Vida útil basada en energía y presión
        if self.pressure > 0:
            life_span = self.energy / (self.pressure * self.roughness)
        else:
            life_span = 0
        
        self.time += dt
        
        return {
            "time": self.time,
            "energy": self.energy,
            "amplitude": amplitude,
            "radius": self.radius,
            "life_span": life_span,
            "active": self.energy > 0 and self.velocity > 0
        }

    def interact(self, other, dt=0.1):
        """
        Interacción optimizada entre dos vórtices.
        - Si giran en signos opuestos: se atraen (v = 0.5 * (v1 + v2) / distancia)
        - Si giran en el mismo signo: se fusionan (el más grande se come al más pequeño)
        - Si se alinean: se repelen (expulsión)
        """
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)
        max_radius = max(self.radius, other.radius)
        
        # Umbral de interacción
        if distance < max_radius * 3.0:
            # 1. Atracción si los signos son opuestos
            if self.sign != other.sign:
                # Los vórtices de signo opuesto se atraen
                attraction_force = 0.5 * (self.velocity + other.velocity) / distance
                self.x -= dx * attraction_force * dt * 0.1
                self.y -= dy * attraction_force * dt * 0.1
                other.x += dx * attraction_force * dt * 0.1
                other.y += dy * attraction_force * dt * 0.1
                
                # Pérdida de energía cuadrática (por fricción del área)
                area_loss = self.radius * other.radius * 0.001
                self.energy -= area_loss * self.velocity**2 * dt
                other.energy -= area_loss * other.velocity**2 * dt
            
            # 2. Fusión si los signos son iguales (mismo giro)
            elif self.sign == other.sign:
                if self.energy > other.energy:
                    # El más grande se come al más pequeño
                    self.energy += other.energy * 0.1
                    other.energy *= 0.9
                    self.radius += other.radius * 0.05
                else:
                    # El otro es más grande
                    other.energy += self.energy * 0.1
                    self.energy *= 0.9
                    other.radius += self.radius * 0.05
            
            # 3. Expulsión si se alinean (los flujos se atraviesan)
            # Si el ángulo relativo es cercano a 180° (se alinean)
            angle_diff = math.atan2(self.y - other.y, self.x - other.x)
            if abs(angle_diff) > math.pi / 2:  # Mayor de 90°
                # Fuerza de repulsión proporcional a la velocidad / radio
                repulsion_force = self.velocity / (other.radius + self.radius)
                self.x += repulsion_force * dt * 0.5
                self.y += repulsion_force * dt * 0.5
                other.x -= repulsion_force * dt * 0.5
                other.y -= repulsion_force * dt * 0.5
            
            # Si un vórtice se queda sin energía, muere
            if self.energy <= 0:
                self.energy = 0
                self.velocity = 0
            if other.energy <= 0:
                other.energy = 0
                other.velocity = 0

    def move(self, pressure_gradient, wind_direction, dt=0.1):
        # Movimiento basado en gradiente de presión (hacia baja presión)
        self.x += pressure_gradient[0] * dt * 0.5
        self.y += pressure_gradient[1] * dt * 0.5
        
        # El viento afecta la trayectoria
        wind_angle = math.atan2(wind_direction[1], wind_direction[0])
        self.x += math.cos(wind_angle) * dt * 0.2
        self.y += math.sin(wind_angle) * dt * 0.2

# ------------------- SIMULACIÓN VORTEX 5.0 -------------------
def simulate_vortex5(steps=100, dt=0.1):
    # Crear dos vórtices con signos opuestos
    v1 = Vortex5(energy=1000.0, velocity=10.0, pressure=0.5, roughness=0.3, radius=10.0, sign=1)
    v2 = Vortex5(energy=800.0, velocity=8.0, pressure=0.4, roughness=0.2, radius=8.0, sign=-1)
    v1.x, v1.y = -5.0, 0.0
    v2.x, v2.y = 5.0, 0.0
    
    pressure_gradient = (-0.1, 0.0)  # Presión baja hacia la izquierda
    wind_direction = (1.0, 0.5)      # Viento hacia la derecha y arriba
    
    for step in range(steps):
        state1 = v1.update(dt)
        state2 = v2.update(dt)
        
        # Interacción entre vórtices
        v1.interact(v2, dt)
        
        # Movimiento
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
simulate_vortex5()
