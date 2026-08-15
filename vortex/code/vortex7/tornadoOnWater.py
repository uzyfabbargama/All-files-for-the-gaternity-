from atomas7 import molecula_a_atomo, modelar_polimero, propiedades_completas

# 1. Simular una molécula de agua (H₂O)
molecula_agua = molecula_a_atomo({
    'H': {'cantidad': 2, 'capas': 1, 'I': 1, 'O': 0},
    'O': {'cantidad': 1, 'capas': 2, 'I': 2, 'O': 4}
})

print("🔬 Propiedades del Agua (H₂O):")
print(propiedades_completas(molecula_agua))

# 2. Simular un polímero de polietileno (C₂H₄)
polietileno = modelar_polimero(molecula_agua, grado_polimerizacion=1000)
print("\n🧪 Propiedades del Polietileno:")
print(polietileno)
