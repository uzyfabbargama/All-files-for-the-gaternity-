import math
import random

# CONSTANTES UNIVERSALES (¡descubiertas por ti!)
PHI = 1.618033988749895      # Proporción áurea
ANGLE_CRITICAL = math.pi / 4  # 45° en radianes
KAPPA = PHI / ANGLE_CRITICAL  # ≈ 2.060144 (¡tu constante!)
ALPHA = 1 / 137.035999084     # Constante de estructura fina

class Vortex3:
    def __init__(self, energy_loss_rate, global_velocity, min_velocity, avg_velocity, roughness, energy=1000.0):
        # Parámetros originales
        self.energy_loss_rate = energy_loss_rate
        self.global_velocity = global_velocity
        self.min_velocity = min_velocity
        self.avg_velocity = avg_velocity
        self.roughness = roughness
        self.energy = energy
        self.time = 0.0
        
        # Posición y radio (para interacciones)
        self.x = random.uniform(-10, 10)
        self.y = random.uniform(-10, 10)
        self.radius = 1.0
        
        # Ángulo de inserción del viento (en radianes)
        self.angle = ANGLE_CRITICAL  # Empieza en el equilibrio (45°)
        
        # Nuevos parámetros basados en KAPPA
        self.kappa_factor = KAPPA  # Factor de estabilidad
        self.alpha_correction = ALPHA  # Corrección electromagnética
        
    def update(self, dt=0.1):
        """Actualiza el vórtice en el tiempo."""
        # 1. Calcular vida útil con factor KAPPA
        if self.global_velocity > self.min_velocity:
            life_span = (self.energy_loss_rate * self.kappa_factor) / (self.global_velocity - self.min_velocity)
        else:
            life_span = 0
        
        # 2. Calcular amplitud con corrección de ángulo
        if self.avg_velocity > 0 and self.roughness > 0:
            amplitude = self.energy / (self.avg_velocity * self.roughness)
            # Ajuste por ángulo: si se desvía de 45°, la amplitud se reduce
            angle_deviation = abs(self.angle - ANGLE_CRITICAL)
            amplitude *= math.cos(angle_deviation)  # Máxima en 45° (cos(0)=1)
        else:
            amplitude = 0
        
        # 3. Actualizar energía y tiempo
        self.time += dt
        self.energy -= self.energy_loss_rate * dt * self.kappa_factor
        
        # 4. Si la energía es baja, colapsa
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
        """Interacción entre dos vórtices (fusión y transferencia de energía)."""
        dx = self.x - other_vortex.x
        dy = self.y - other_vortex.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Umbral de interacción basado en radios
        max_radius = max(self.radius, other_vortex.radius)
        if distance < max_radius * 2.0:
            # El más grande absorbe al más pequeño
            if self.energy > other_vortex.energy:
                # Transferencia de energía con factor KAPPA
                energy_transfer = other_vortex.energy * 0.1 * self.kappa_factor
                self.energy += energy_transfer
                other_vortex.energy -= energy_transfer
                # El radio crece proporcionalmente a la energía absorbida
                self.radius += other_vortex.radius * 0.05
                # La velocidad global aumenta ligeramente
                self.global_velocity += other_vortex.global_velocity * 0.01
                # El ángulo se ajusta hacia el equilibrio (45°)
                self.angle = ANGLE_CRITICAL + (self.angle - ANGLE_CRITICAL) * 0.9
            else:
                # El otro es más grande
                energy_transfer = self.energy * 0.1 * self.kappa_factor
                other_vortex.energy += energy_transfer
                self.energy -= energy_transfer
                other_vortex.radius += self.radius * 0.05
                other_vortex.global_velocity += self.global_velocity * 0.01
                other_vortex.angle = ANGLE_CRITICAL + (other_vortex.angle - ANGLE_CRITICAL) * 0.9
            
            # Si un vórtice se queda sin energía, muere
            if self.energy <= 0:
                self.energy = 0
                self.global_velocity = 0
            if other_vortex.energy <= 0:
                other_vortex.energy = 0
                other_vortex.global_velocity = 0
    
    def move(self, pressure_gradient, wind_direction, dt=0.1):
        """
        Mueve el vórtice basado en el gradiente de presión y la dirección del viento.
        - pressure_gradient: vector (dx, dy) que indica hacia dónde baja la presión.
        - wind_direction: vector (dx, dy) que indica hacia dónde sopla el viento.
        """
        # El vórtice se mueve hacia donde la presión es más baja (gradiente)
        move_x = pressure_gradient[0] * dt * 0.5
        move_y = pressure_gradient[1] * dt * 0.5
        
        # El viento a favor acelera el movimiento, el viento en contra lo frena
        wind_factor = math.cos(self.angle - math.atan2(wind_direction[1], wind_direction[0]))
        move_x += wind_direction[0] * dt * 0.2 * wind_factor
        move_y += wind_direction[1] * dt * 0.2 * wind_factor
        
        # Actualizar posición
        self.x += move_x
        self.y += move_y

# ------------------- SIMULACIÓN CON VORTEX 3.0 -------------------
def simulate_vortex3(steps=100, dt=0.1):
    # Crear dos vórtices con parámetros mejorados
    v1 = Vortex3(
        energy_loss_rate=2.0,
        global_velocity=10.0,
        min_velocity=1.0,
        avg_velocity=5.0,
        roughness=0.3,
        energy=1000.0
    )
    v2 = Vortex3(
        energy_loss_rate=1.5,
        global_velocity=8.0,
        min_velocity=0.5,
        avg_velocity=4.0,
        roughness=0.2,
        energy=800.0
    )
    v1.x, v1.y = -2.0, 0.0
    v2.x, v2.y = 2.0, 0.0
    
    # Simulación de gradiente de presión y viento (ejemplo)
    pressure_gradient = (-0.1, 0.0)  # La presión baja hacia la izquierda
    wind_direction = (1.0, 0.5)      # Viento hacia la derecha y arriba
    
    for step in range(steps):
        # Actualizar cada vórtice
        state1 = v1.update(dt)
        state2 = v2.update(dt)
        
        # Interacción entre vórtices
        v1.interact(v2, dt)
        
        # Movimiento basado en presión y viento
        v1.move(pressure_gradient, wind_direction, dt)
        v2.move(pressure_gradient, wind_direction, dt)
        
        # Mostrar estado
        print(f"Paso {step+1}:")
        print(f"  V1: Energía={state1['energy']:.2f}, Amplitud={state1['amplitude']:.2f}m, Activo={state1['active']}")
        print(f"  V2: Energía={state2['energy']:.2f}, Amplitud={state2['amplitude']:.2f}m, Activo={state2['active']}")
        print(f"  Distancia: {math.sqrt((v1.x-v2.x)**2 + (v1.y-v2.y)**2):.2f}")
        print(f"  V1 posición: ({v1.x:.2f}, {v1.y:.2f})")
        print(f"  V2 posición: ({v2.x:.2f}, {v2.y:.2f})")
        print("---")
        
        if not state1['active'] and not state2['active']:
            print("Ambos vórtices se han disipado.")
            break

# Ejecutar
if __name__ == "__main__":
    print(f"🔬 VORTEX 3.0 - Modelo de vórtices con constante KAPPA = {KAPPA}")
    print(f"📐 Ángulo crítico: {math.degrees(ANGLE_CRITICAL)}°")
    print(f"⚡ Factor de estructura fina: {ALPHA}")
    simulate_vortex3()
