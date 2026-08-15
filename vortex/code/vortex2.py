import math
import random

class Vortex:
    def __init__(self, energy_loss_rate, global_velocity, min_velocity, avg_velocity, roughness, energy=1000.0):
        self.energy_loss_rate = energy_loss_rate
        self.global_velocity = global_velocity
        self.min_velocity = min_velocity
        self.avg_velocity = avg_velocity
        self.roughness = roughness
        self.energy = energy
        self.time = 0.0
        # Posición en el espacio 2D (para interacciones)
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(-10, 10)
        self.radius = 1.0  # Radio inicial del vórtice

    def update(self, dt=0.1):
        # Calcular vida útil y amplitud (como antes)
        if self.global_velocity > self.min_velocity:
            life_span = self.energy_loss_rate / (self.global_velocity - self.min_velocity)
        else:
            life_span = 0

        if self.avg_velocity > 0 and self.roughness > 0:
            amplitude = self.energy / (self.avg_velocity * self.roughness)
        else:
            amplitude = 0

        self.time += dt
        self.energy -= self.energy_loss_rate * dt

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

    def interact(self, other_vortex, dt=0.1):
        """
        Interacción entre dos vórtices.
        - Si están cerca, intercambian energía.
        - El más grande "se come" al más pequeño.
        """
        # Distancia entre vórtices
        dx = self.x - other_vortex.x
        dy = self.y - other_vortex.y
        distance = math.sqrt(dx**2 + dy**2)

        # Si están lo suficientemente cerca (dentro del radio del más grande)
        max_radius = max(self.radius, other_vortex.radius)
        if distance < max_radius * 2.0:  # Umbral de interacción
            # El más grande absorbe energía del más pequeño
            if self.energy > other_vortex.energy:
                # El grande (self) se come al pequeño (other)
                energy_transfer = other_vortex.energy * 0.1  # 10% de la energía del pequeño
                self.energy += energy_transfer
                other_vortex.energy -= energy_transfer
                # El radio del grande crece
                self.radius += other_vortex.radius * 0.05
                # La velocidad global del grande aumenta ligeramente
                self.global_velocity += other_vortex.global_velocity * 0.01
            else:
                # El otro es más grande
                energy_transfer = self.energy * 0.1
                other_vortex.energy += energy_transfer
                self.energy -= energy_transfer
                other_vortex.radius += self.radius * 0.05
                other_vortex.global_velocity += self.global_velocity * 0.01

            # Si un vórtice se queda sin energía, muere
            if self.energy <= 0:
                self.energy = 0
                self.global_velocity = 0
            if other_vortex.energy <= 0:
                other_vortex.energy = 0
                other_vortex.global_velocity = 0

# ------------------- SIMULACIÓN CON DOS VÓRTICES -------------------
def simulate_two_vortices(steps=100, dt=0.1):
    # Crear dos vórtices
    v1 = Vortex(
        energy_loss_rate=2.0,
        global_velocity=10.0,
        min_velocity=1.0,
        avg_velocity=5.0,
        roughness=0.3,
        energy=1000.0
    )
    v2 = Vortex(
        energy_loss_rate=1.5,
        global_velocity=8.0,
        min_velocity=0.5,
        avg_velocity=4.0,
        roughness=0.2,
        energy=800.0
    )
    # Colocarlos cerca para que interactúen
    v1.x, v1.y = -2.0, 0.0
    v2.x, v2.y = 2.0, 0.0

    for step in range(steps):
        # Actualizar cada vórtice
        state1 = v1.update(dt)
        state2 = v2.update(dt)

        # Interacción entre vórtices
        v1.interact(v2, dt)

        # Mostrar estado
        print(f"Paso {step+1}:")
        print(f"  V1: Energía={state1['energy']:.2f}, Amplitud={state1['amplitude']:.2f}m, Activo={state1['active']}")
        print(f"  V2: Energía={state2['energy']:.2f}, Amplitud={state2['amplitude']:.2f}m, Activo={state2['active']}")
        print(f"  Distancia: {math.sqrt((v1.x-v2.x)**2 + (v1.y-v2.y)**2):.2f}")
        print("---")

        if not state1['active'] and not state2['active']:
            print("Ambos vórtices se han disipado.")
            break

# Ejecutar
simulate_two_vortices()
