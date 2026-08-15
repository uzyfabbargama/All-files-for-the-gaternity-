# Crear un material (ej. Neodimio)
from materiales import Material
neodimio = Material(simbolo='Nd', capas=6, I=16, O=4, Z=60)

# Crear un tornado sobre Neodimio
from vortex7 import TornadoConMaterial
tornado = TornadoConMaterial(
    material=neodimio,
    energy=1000.0,
    velocity=10.0,
    pressure=0.5,
    roughness=0.3,
    radius=10.0,
    sign=1
)

# Simular 100 pasos
for step in range(100):
    tornado.interaccion_con_material(dt=0.1)
