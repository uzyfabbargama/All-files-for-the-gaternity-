import math

# Definir la función de activación (sigmoide)
def sigmoide(x):
    return 1 / (1 + math.exp(-x))

# Entradas, pesos y sesgo
entradas = [0.5, 0.7]  # Por ejemplo, edad y puntuación en un test
pesos = [0.9, 0.4]     # Pesos iniciales
sesgo = -0.3

# Calcular la suma ponderada
suma_ponderada = 0
for i in range(len(entradas)):
    suma_ponderada += entradas[i] * pesos[i]

# Sumar el sesgo
suma_con_sesgo = suma_ponderada + sesgo

# Aplicar la función de activación para obtener la salida
salida_neurona = sigmoide(suma_con_sesgo)

print(f"La suma ponderada es: {suma_ponderada}")
print(f"La suma con sesgo es: {suma_con_sesgo}")
print(f"La salida final de la neurona es: {salida_neurona}")