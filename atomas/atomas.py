class Atom:
    def __init__(self, nombre, capas, palitos_I, palitos_O, carga=0):
        self.nombre = nombre
        self.capas = capas
        self.palitos_I = palitos_I  # Electrones d/f (cohesión)
        self.palitos_O = palitos_O  # Electrones s/p (conductividad/reactividad)
        self.carga = carga          # Carga iónica (positiva = catión, negativa = anión)
        self.longitud_palito = 8 - capas  # Fuerza del enlace metálico
        
    def punto_fusion(self):
        # Regla base
        base = self.palitos_I * 100
        base += self.capas * 50
        base -= self.palitos_O * 30
        
        # Los palitos_O en potencias de 2 reducen más
        if self.palitos_O in [1, 2, 4, 8]:
            base -= 50
        
        # Los iones tienen puntos de fusión más altos (fuerzas electrostáticas)
        if self.carga != 0:
            base += abs(self.carga) * 200
        print(f"Punto de fusión: {max(base, -273)}")
        return max(base, -273)
    
    def es_magnetico(self):
        # Si los palitos_I son impares y no hay muchos palitos_O que los apareen
        # Los iones con carga pueden tener espines desapareados
        if self.palitos_I % 2 == 1 and self.palitos_O < 3:
            print(f"Es magnético")
            return True
        # Los iones con electrones desapareados en la capa d
        if self.carga > 0 and self.palitos_I > 5:
            print(f"Es magnético")
            return True
        print(f"No es magnético")
        return False
    
    def conductividad(self):
        # Los palitos_O aumentan la conductividad
        # Los iones tienen mejor conductividad (electrones más móviles)
        base = self.palitos_O * 10
        if self.palitos_I > 5:
            base -= self.palitos_I * 2
        if self.carga != 0:
            base += abs(self.carga) * 15
        print(f"Conductividad: {max(base, 0)}")
        return max(base, 0)
    
    def reactividad(self):
        # Los palitos_O aumentan la reactividad (puertas de entrada)
        # Los cationes son menos reactivos (les faltan electrones)
        base = self.palitos_O * 5
        if self.carga > 0:
            base -= self.carga * 10
        elif self.carga < 0:
            base += abs(self.carga) * 15  # Aniones muy reactivos
        print(f"Reactividad: {max(base, 0)}")
        return max(base, 0)
    def __repr__(self):
        estado = f"{self.nombre}"
        if self.carga > 0:
            estado += f"^{self.carga}+"
            print(f"Estado: {estado}")
        elif self.carga < 0:
            estado += f"^{abs(self.carga)}-"
            print(f"Estado: {estado}")
        return estado

# Átomos neutros
Cu = Atom("Cu", 4, 7, 2)
Fe = Atom("Fe", 4, 8, 0)
Mn = Atom("Mn", 4, 7, 0)
Mg = Atom("Mg", 3, 2, 0)
Zn = Atom("Zn", 4, 6, 3)
Ga = Atom("Ga", 4, 5, 4)

# Iones (según tu idea)
Cu_ion = Atom("Cu", 4, 8, 1, carga=1)   # Cu⁺ (catión cobre)
Cu_ion2 = Atom("Cu", 4, 7, 1, carga=2)  # Cu²⁺ (catión cobre)
Fe_ion = Atom("Fe", 4, 6, 0, carga=3)   # Fe³⁺ (catión hierro)
Mn_ion = Atom("Mn", 4, 5, 0, carga=2)   # Mn²⁺ (catión manganeso)
