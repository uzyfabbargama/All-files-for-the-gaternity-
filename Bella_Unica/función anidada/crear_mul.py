def crear_multiplicador(factor):
    """Crea una función que multiplica por un factor fijo."""
    def multiplicar(x):
        return x * factor
    return multiplicar

# Uso:
duplicar = crear_multiplicador(2)
triplicar = crear_multiplicador(3)

print(duplicar(5))  # 10
print(triplicar(5))  # 15
